#!/usr/bin/env python3
"""
CyberPH Encryptor/Decryptor
A secure document encryption and decryption tool supporting TXT, DOC, PDF, and other formats.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
from pathlib import Path
import secrets
from datetime import datetime

class CyberPHEncryptor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CyberPH Encryptor/Decryptor v1.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Set application icon and styling
        self.setup_styles()
        self.create_gui()
        
    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Heading.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 12, 'bold'))
        
        style.configure('Custom.TButton',
                       background='#3498db',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        
        style.map('Custom.TButton',
                 background=[('active', '#2980b9')])
        
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="CyberPH Encryptor/Decryptor", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Secure Document Encryption & Decryption", style='Heading.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # File selection frame
        file_frame = tk.Frame(main_frame, bg='#2c3e50')
        file_frame.pack(fill='x', pady=(0, 20))
        
        self.file_label = ttk.Label(file_frame, text="No file selected", background='#34495e', foreground='#ecf0f1', padding=10)
        self.file_label.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        select_btn = ttk.Button(file_frame, text="Select File", command=self.select_file, style='Custom.TButton')
        select_btn.pack(side='right')
        
        # Encryption method selection
        method_frame = tk.Frame(main_frame, bg='#2c3e50')
        method_frame.pack(fill='x', pady=10)
        
        method_label = ttk.Label(method_frame, text="Encryption Method:", style='Heading.TLabel')
        method_label.pack(side='left')
        
        self.encryption_method = tk.StringVar(value="password")
        password_rb = tk.Radiobutton(method_frame, text="Password", variable=self.encryption_method, 
                                   value="password", bg='#2c3e50', fg='#ecf0f1', 
                                   selectcolor='#34495e', activebackground='#34495e')
        password_rb.pack(side='left', padx=(20, 10))
        
        key_rb = tk.Radiobutton(method_frame, text="Encryption Key", variable=self.encryption_method, 
                              value="key", bg='#2c3e50', fg='#ecf0f1', 
                              selectcolor='#34495e', activebackground='#34495e')
        key_rb.pack(side='left', padx=(10, 20))
        
        # Key management frame
        key_frame = tk.Frame(main_frame, bg='#2c3e50')
        key_frame.pack(fill='x', pady=10)
        
        generate_key_btn = ttk.Button(key_frame, text="Generate Key", 
                                    command=self.generate_key, style='Custom.TButton')
        generate_key_btn.pack(side='left', padx=(0, 5))
        
        import_key_btn = ttk.Button(key_frame, text="Import Key", 
                                  command=self.import_key, style='Custom.TButton')
        import_key_btn.pack(side='left', padx=(5, 5))
        
        export_key_btn = ttk.Button(key_frame, text="Export Key", 
                                  command=self.export_key, style='Custom.TButton')
        export_key_btn.pack(side='left', padx=(5, 0))
        
        # Current key display
        self.key_display = ttk.Label(key_frame, text="No key loaded", 
                                   background='#34495e', foreground='#ecf0f1', 
                                   font=('Consolas', 8), padding=5)
        self.key_display.pack(side='right', fill='x', expand=True, padx=(20, 0))
        
        # Operation buttons frame
        operation_frame = tk.Frame(main_frame, bg='#2c3e50')
        operation_frame.pack(fill='x', pady=20)
    
        encrypt_btn = ttk.Button(operation_frame, text="Encrypt File", 
                               command=self.encrypt_file, style='Custom.TButton')
        encrypt_btn.pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        decrypt_btn = ttk.Button(operation_frame, text="Decrypt File", 
                               command=self.decrypt_file, style='Custom.TButton')
        decrypt_btn.pack(side='right', padx=(10, 0), fill='x', expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=20)
        
        # Status text area
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        status_label = ttk.Label(status_frame, text="Status Log:", style='Heading.TLabel')
        status_label.pack(anchor='w')
        
        self.status_text = tk.Text(status_frame, bg='#34495e', fg='#ecf0f1', 
                                  font=('Consolas', 10), height=15, wrap='word')
        self.status_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Scrollbar for status text
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side='right', fill='y')
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        # Footer
        footer_label = ttk.Label(main_frame, text="© 2024 CyberPH - Secure Document Protection", 
                               background='#2c3e50', foreground='#95a5a6', font=('Arial', 8))
        footer_label.pack(pady=(20, 0))
        
        self.selected_file = None
        self.current_key = None
        self.log_message("CyberPH Encryptor/Decryptor initialized successfully.")
        self.log_message("Supported formats: TXT, DOC, DOCX, PDF, and more...")
        self.log_message("Choose between Password or Encryption Key methods.")
        
    def log_message(self, message):
        """Add a message to the status log"""
        self.status_text.insert(tk.END, f"[{self.get_timestamp()}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def select_file(self):
        """Open file dialog to select a file"""
        file_types = [
            ("All Supported", "*.txt;*.doc;*.docx;*.pdf;*.xlsx;*.pptx;*.jpg;*.png;*.zip"),
            ("Text files", "*.txt"),
            ("Word documents", "*.doc;*.docx"),
            ("PDF files", "*.pdf"),
            ("Excel files", "*.xlsx"),
            ("PowerPoint files", "*.pptx"),
            ("Images", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"),
            ("Archives", "*.zip;*.rar;*.7z"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select file to encrypt/decrypt",
            filetypes=file_types
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(text=f"Selected: {os.path.basename(filename)}")
            self.log_message(f"File selected: {filename}")
            
    def generate_key_from_password(self, password, salt=None):
        """Generate encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
        
    def generate_key(self):
        """Generate a new random encryption key"""
        try:
            # Generate a new Fernet key
            new_key = Fernet.generate_key()
            self.current_key = new_key
            
            # Display key preview (first 16 chars + ...)
            key_preview = new_key.decode()[:16] + "..."
            self.key_display.config(text=f"Key: {key_preview}")
            
            self.log_message("New encryption key generated successfully!")
            self.log_message("Remember to export and save your key securely.")
            
            # Ask if user wants to save the key
            if messagebox.askyesno("Save Key", "Would you like to save this key to a file?"):
                self.export_key()
                
        except Exception as e:
            self.log_message(f"Key generation failed: {str(e)}")
            messagebox.showerror("Error", f"Key generation failed: {str(e)}")
            
    def import_key(self):
        """Import an encryption key from file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Import Encryption Key",
                filetypes=[("Key files", "*.key"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            with open(file_path, 'rb') as f:
                key_data = f.read().strip()
                
            # Validate the key
            try:
                # Try to create a Fernet instance to validate
                test_fernet = Fernet(key_data)
                self.current_key = key_data
                
                # Display key preview
                key_preview = key_data.decode()[:16] + "..."
                self.key_display.config(text=f"Key: {key_preview}")
                
                self.log_message(f"Encryption key imported from: {os.path.basename(file_path)}")
                
            except Exception:
                raise ValueError("Invalid key format")
                
        except Exception as e:
            self.log_message(f"Key import failed: {str(e)}")
            messagebox.showerror("Error", f"Key import failed: {str(e)}")
            
    def export_key(self):
        """Export the current encryption key to file"""
        if not self.current_key:
            messagebox.showerror("Error", "No key to export! Generate a key first.")
            return
            
        try:
            # Get save location
            file_path = filedialog.asksaveasfilename(
                title="Export Encryption Key",
                defaultextension=".key",
                filetypes=[("Key files", "*.key"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            # Save key with metadata
            key_data = {
                'key': self.current_key.decode(),
                'generated': datetime.now().isoformat(),
                'version': '1.0',
                'application': 'CyberPH Encryptor'
            }
            
            with open(file_path, 'w') as f:
                json.dump(key_data, f, indent=2)
                
            # Also save just the raw key
            raw_key_path = file_path.replace('.key', '_raw.key')
            with open(raw_key_path, 'wb') as f:
                f.write(self.current_key)
                
            self.log_message(f"Key exported to: {os.path.basename(file_path)}")
            self.log_message(f"Raw key saved to: {os.path.basename(raw_key_path)}")
            messagebox.showinfo("Success", f"Key exported successfully!\n\nKey file: {os.path.basename(file_path)}\nRaw key: {os.path.basename(raw_key_path)}")
            
        except Exception as e:
            self.log_message(f"Key export failed: {str(e)}")
            messagebox.showerror("Error", f"Key export failed: {str(e)}")
        
    def encrypt_file(self):
        """Encrypt the selected file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
            
        if not os.path.exists(self.selected_file):
            messagebox.showerror("Error", "Selected file does not exist!")
            return
            
        # Determine encryption method
        method = self.encryption_method.get()
        
        if method == "password":
            # Get password from user
            password = simpledialog.askstring("Password", "Enter encryption password:", show='*')
            if not password:
                return
                
            # Confirm password
            confirm_password = simpledialog.askstring("Confirm Password", "Confirm encryption password:", show='*')
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return
        else:
            # Use encryption key
            if not self.current_key:
                messagebox.showerror("Error", "No encryption key available! Generate or import a key first.")
                return
            password = None
            
        try:
            self.progress.start()
            self.log_message("Starting encryption process...")
            
            # Generate or use encryption key
            if method == "password":
                key, salt = self.generate_key_from_password(password)
                fernet = Fernet(key)
                encryption_method = "password"
            else:
                fernet = Fernet(self.current_key)
                salt = None
                encryption_method = "key"
            
            # Read file content
            self.log_message("Reading file content...")
            with open(self.selected_file, 'rb') as file:
                file_data = file.read()
                
            # Encrypt the data
            self.log_message("Encrypting file data...")
            encrypted_data = fernet.encrypt(file_data)
            
            # Create metadata
            metadata = {
                'original_filename': os.path.basename(self.selected_file),
                'file_size': len(file_data),
                'encryption_timestamp': self.get_timestamp(),
                'encryption_method': encryption_method,
                'version': '1.0'
            }
            
            if salt is not None:
                metadata['salt'] = base64.b64encode(salt).decode()
            
            # Save encrypted file
            output_file = self.selected_file + '.cyberph'
            self.log_message(f"Saving encrypted file as: {output_file}")
            
            with open(output_file, 'wb') as file:
                # Write metadata
                metadata_json = json.dumps(metadata).encode()
                file.write(len(metadata_json).to_bytes(4, 'big'))
                file.write(metadata_json)
                # Write encrypted data
                file.write(encrypted_data)
                
            self.progress.stop()
            self.log_message("File encrypted successfully!")
            messagebox.showinfo("Success", f"File encrypted successfully!\nSaved as: {os.path.basename(output_file)}")
            
        except Exception as e:
            self.progress.stop()
            self.log_message(f"Encryption failed: {str(e)}")
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            
    def decrypt_file(self):
        """Decrypt the selected file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
            
        if not os.path.exists(self.selected_file):
            messagebox.showerror("Error", "Selected file does not exist!")
            return
            
        if not self.selected_file.endswith('.cyberph'):
            messagebox.showerror("Error", "Please select a .cyberph encrypted file!")
            return
            
        try:
            self.progress.start()
            self.log_message("Starting decryption process...")
            
            # Read encrypted file
            self.log_message("Reading encrypted file...")
            with open(self.selected_file, 'rb') as file:
                # Read metadata
                metadata_length = int.from_bytes(file.read(4), 'big')
                metadata_json = file.read(metadata_length)
                metadata = json.loads(metadata_json.decode())
                
                # Read encrypted data
                encrypted_data = file.read()
                
            # Determine decryption method and get key
            encryption_method = metadata.get('encryption_method', 'password')
            
            if encryption_method == "password":
                # Get password from user
                password = simpledialog.askstring("Password", "Enter decryption password:", show='*')
                if not password:
                    return
                    
                # Extract salt and generate key
                salt = base64.b64decode(metadata['salt'])
                key, _ = self.generate_key_from_password(password, salt)
                fernet = Fernet(key)
            else:
                # Use encryption key
                if not self.current_key:
                    messagebox.showerror("Error", "No encryption key available! Import the correct key first.")
                    return
                fernet = Fernet(self.current_key)
            
            # Decrypt the data
            self.log_message("Decrypting file data...")
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Save decrypted file
            original_filename = metadata['original_filename']
            output_file = os.path.join(os.path.dirname(self.selected_file), f"decrypted_{original_filename}")
            
            self.log_message(f"Saving decrypted file as: {output_file}")
            with open(output_file, 'wb') as file:
                file.write(decrypted_data)
                
            self.progress.stop()
            self.log_message("File decrypted successfully!")
            self.log_message(f"Original filename: {original_filename}")
            self.log_message(f"Original size: {metadata['file_size']} bytes")
            messagebox.showinfo("Success", f"File decrypted successfully!\nSaved as: {os.path.basename(output_file)}")
            
        except Exception as e:
            self.progress.stop()
            self.log_message(f"Decryption failed: {str(e)}")
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CyberPHEncryptor()
    app.run()
