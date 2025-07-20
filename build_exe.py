#!/usr/bin/env python3
"""
Build script for CyberPH Encryptor/Decryptor
Creates a standalone EXE file using PyInstaller
"""

import os
import subprocess
import sys
from pathlib import Path

def build_exe():
    """Build the application as a standalone EXE"""
    print("Building CyberPH Encryptor/Decryptor EXE...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single EXE file
        "--windowed",                   # Hide console window (GUI app)
        "--name", "CyberPH-Encryptor",  # Output EXE name
        "--add-data", "requirements.txt;.",  # Include requirements file
        "--hidden-import", "tkinter",   # Ensure tkinter is included
        "--hidden-import", "cryptography",  # Ensure cryptography is included
        "--distpath", "dist",           # Output directory
        "--workpath", "build",          # Work directory
        "--clean",                      # Clean before build
        "main.py"                       # Main script
    ]
    
    # Add icon if available
    if os.path.exists("icon.ico"):
        cmd.insert(-1, "--icon")
        cmd.insert(-1, "icon.ico")
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild completed successfully!")
        print("EXE file location: dist/CyberPH-Encryptor.exe")
        print("\nYou can now distribute the EXE file!")
        
        # Check if EXE was created
        exe_path = Path("dist/CyberPH-Encryptor.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"EXE size: {size_mb:.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()
