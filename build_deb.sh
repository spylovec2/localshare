#!/bin/bash

# --- 0. Configuration ---
TARGET_PORT="8080"

# --- 1. Cleanup & Directory Structure ---
rm -rf build dist pkg LocalShare.deb
mkdir -p pkg/usr/bin
mkdir -p pkg/usr/share/applications
mkdir -p pkg/usr/share/pixmaps
mkdir -p pkg/DEBIAN

# --- 2. Build Binary (EXCLUSIONS ADDED HERE) ---
echo "📦 Building standalone binary and resolving Qt conflicts..."

python3 -m PyInstaller --onefile --clean \
    --add-data "index.html:." \
    --exclude-module PyQt5 \
    --exclude-module PyQt6 \
    --exclude-module matplotlib \
    --exclude-module numpy \
    --exclude-module tkinter \
    --exclude-module IPython \
    --exclude-module PySide2 \
    --exclude-module PySide6 \
    --name LocalShare localshare.py

if [ -f "dist/LocalShare" ]; then
    cp dist/LocalShare pkg/usr/bin/
else
    echo "❌ Build failed! Check the errors above."
    exit 1
fi

# --- 3. Process & Copy Icon ---
if [ -f "icon.png" ]; then
    python3 <<EOT
from PIL import Image
try:
    img = Image.open('icon.png').resize((512, 512))
    img.save('pkg/usr/share/pixmaps/LocalShare.png')
except: pass
EOT
else
    touch pkg/usr/share/pixmaps/LocalShare.png 
fi

# --- 4. Create the .desktop file ---
cat <<EOT > pkg/usr/share/applications/LocalShare.desktop
[Desktop Entry]
Type=Application
Terminal=true
# Use 'sh -c' to launch, which helps some window managers handle focus better
Exec=sh -c "/usr/bin/LocalShare"
Name=LocalShare
Comment=LocalShare Server (Close terminal to stop)
Icon=LocalShare
Categories=Utility;Network;
StartupNotify=true
EOT

# --- 5. Control File ---
cat <<EOT > pkg/DEBIAN/control
Package: LocalShare
Version: 3.3
Section: utils
Priority: optional
Architecture: amd64
Maintainer: spy <spy@local>
Description: LocalShare with fixed build dependencies.
EOT

# --- 6. Post-Install Script ---
cat <<EOT > pkg/DEBIAN/postinst
#!/bin/bash
chmod 755 /usr/bin/LocalShare
update-desktop-database /usr/share/applications
EOT
chmod 755 pkg/DEBIAN/postinst

# --- 7. Build Package ---
dpkg-deb --build pkg LocalShare.deb
echo "🚀 Success! Build complete without Qt conflicts."
echo "Install it with: sudo dpkg -i LocalShare.deb"