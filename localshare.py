import os, socket, qrcode, shutil, uvicorn, webbrowser, sys, time
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, Response
from io import BytesIO
from typing import List
from threading import Timer

PORT = 8080 
UPLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "LocalDrop_Shared")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# --- NEW: CLEANUP FUNCTION ---
def clear_old_files():
    """Deletes the shared folder and recreates it to ensure a fresh start"""
    if os.path.exists(UPLOAD_DIR):
        try:
            shutil.rmtree(UPLOAD_DIR)
            print(f"🧹 Cleaned up old files in {UPLOAD_DIR}")
        except Exception as e:
            print(f"⚠️ Could not clear directory: {e}")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

# Call it immediately when the script runs
clear_old_files()

app = FastAPI()

def get_local_ip():
    """ Improved IP detection that works offline and across different OS behaviors """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This doesn't need a real connection, just a route to exists
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        try:
            # Fallback for some Linux/Mac environments
            IP = socket.gethostbyname(socket.gethostname())
        except:
            IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def resource_path(relative_path):
    """ Correctly locate index.html whether running as script or bundled binary """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

@app.get("/", response_class=HTMLResponse)
async def index():
    path = resource_path("index.html")
    if not os.path.exists(path):
        return HTMLResponse(content=f"<h1>Error</h1><p>index.html not found at {path}</p>", status_code=404)
    return FileResponse(path)

@app.get("/config")
async def get_config():
    ip = get_local_ip()
    return {"ip": ip, "url": f"http://{ip}:{PORT}"}

@app.get("/qr")
async def get_qr():
    url = f"http://{get_local_ip()}:{PORT}"
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/files")
async def list_files():
    return JSONResponse(os.listdir(UPLOAD_DIR))

@app.post("/upload")
async def handle_upload(files: List[UploadFile] = File(...)):
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"status": "ok"}

@app.get("/download/{filename}")
async def handle_download(filename: str):
    return FileResponse(path=os.path.join(UPLOAD_DIR, filename), filename=filename)

@app.delete("/delete/{filename}")
async def handle_delete(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
    return {"status": "deleted"}

def open_browser():
    """ Wait a split second for the server to bind before opening browser """
    time.sleep(1.5)
    webbrowser.open(f"http://{get_local_ip()}:{PORT}")

if __name__ == "__main__":
    # Start browser in a separate thread so it doesn't block the server startup
    Timer(1, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")