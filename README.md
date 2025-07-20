# CyberPH Encryptor/Decryptor

A secure, professional-grade document encryption and decryption tool with a modern GUI interface.

## Features

- 🔒 **Strong Encryption**: Uses AES-256 encryption with PBKDF2 key derivation
- 📄 **Multiple Formats**: Supports TXT, DOC, DOCX, PDF, Excel, PowerPoint, images, and more
- 🖥️ **Modern GUI**: Intuitive interface with real-time status logging
- 🔐 **Password Protection**: Secure password-based encryption
- 📦 **Standalone EXE**: No installation required, runs anywhere
- 🛡️ **Secure Storage**: Encrypted files contain metadata and use .cyberph extension

## Supported File Types

- **Documents**: TXT, DOC, DOCX, PDF
- **Spreadsheets**: XLS, XLSX
- **Presentations**: PPT, PPTX
- **Images**: JPG, PNG, BMP, GIF
- **Archives**: ZIP, RAR, 7Z
- **Any File Type**: The application can encrypt any binary file

## Quick Start

### Option 1: Run from Source
1. Install Python 3.8+ on your system
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Option 2: Build EXE
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Build the EXE:
   ```bash
   python build_exe.py
   ```
3. Run the generated EXE:
   ```bash
   dist/CyberPH-Encryptor.exe
   ```

## How to Use

### Encrypting Files
1. **Launch** the CyberPH Encryptor application
2. **Select File** using the "Select File" button
3. **Click "🔒 Encrypt File"**
4. **Enter Password** when prompted (remember this password!)
5. **Confirm Password** to ensure accuracy
6. The encrypted file will be saved with `.cyberph` extension

### Decrypting Files
1. **Launch** the CyberPH Encryptor application
2. **Select** the `.cyberph` encrypted file
3. **Click "🔓 Decrypt File"**
4. **Enter Password** used during encryption
5. The original file will be restored with `decrypted_` prefix

## Security Features

- **AES-256 Encryption**: Military-grade encryption standard
- **PBKDF2 Key Derivation**: 100,000 iterations with random salt
- **Metadata Protection**: File information is securely stored
- **No Password Storage**: Passwords are never saved or logged
- **Secure Memory**: Sensitive data is cleared from memory

## File Structure

```
CyberPH-Encyptor-Decryptor/
├── main.py              # Main application source code
├── requirements.txt     # Python dependencies
├── build_exe.py        # EXE build script
├── README.md           # This file
└── dist/               # Generated EXE files (after build)
    └── CyberPH-Encryptor.exe
```

## Requirements

- **Python**: 3.8+ (for source code)
- **Dependencies**: cryptography, pyinstaller
- **OS**: Windows (EXE), Linux/Mac (Python)
- **Memory**: Minimum 100MB RAM
- **Storage**: 50MB free space

## Troubleshooting

### Common Issues

1. **"File not found" error**
   - Ensure the selected file exists and is accessible
   - Check file permissions

2. **"Wrong password" error**
   - Verify you're using the correct password
   - Password is case-sensitive

3. **EXE build fails**
   - Ensure PyInstaller is installed: `pip install pyinstaller`
   - Run build script with administrator privileges

4. **GUI doesn't appear**
   - Check if tkinter is installed: `python -m tkinter`
   - Try running from command line to see error messages

### Performance Notes

- Large files (>100MB) may take longer to encrypt/decrypt
- Progress bar shows activity during processing
- Status log provides real-time feedback

## Security Recommendations

1. **Use Strong Passwords**: Minimum 12 characters with mixed case, numbers, symbols
2. **Store Passwords Safely**: Use a password manager
3. **Backup Important Files**: Keep encrypted backups
4. **Verify Decryption**: Always test decryption after encryption
5. **Secure Deletion**: Securely delete original files if needed

## Development

### Building from Source
```bash
git clone https://github.com/TadashiJei/CyberPH-Chef
cd CyberPH-Encyptor-Decryptor
pip install -r requirements.txt
python main.py
```

### Creating Distribution
```bash
python build_exe.py
```

## License

© 2024 CyberPH - All Rights Reserved

## Support

For technical support or questions, please contact the CyberPH development team.

---

**⚠️ Important Security Notice**: Always remember your encryption passwords. Lost passwords cannot be recovered, and encrypted files will be permanently inaccessible without them.
