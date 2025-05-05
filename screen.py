import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class InitialLoginScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.switch_callback = switch_callback
        
        # Main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        
        # App logo/title
        ctk.CTkLabel(
            main_frame, 
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG",
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 40))
        
        # Login form
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack()
        
        # Username field
        ctk.CTkLabel(
            form_frame, 
            text="Tên đăng nhập:",
            font=("Arial", 14)
        ).grid(row=0, column=0, pady=5, sticky="w")
        
        self.username_entry = ctk.CTkEntry(
            form_frame, 
            width=300,
            placeholder_text="Nhập tên đăng nhập"
        )
        self.username_entry.grid(row=1, column=0, pady=5)
        
        # Password field
        ctk.CTkLabel(
            form_frame, 
            text="Mật khẩu:",
            font=("Arial", 14)
        ).grid(row=2, column=0, pady=5, sticky="w")
        
        self.password_entry = ctk.CTkEntry(
            form_frame, 
            width=300,
            show="*",
            placeholder_text="Nhập mật khẩu"
        )
        self.password_entry.grid(row=3, column=0, pady=5)
        
        # Login button
        login_button = ctk.CTkButton(
            form_frame,
            text="Đăng nhập",
            width=300,
            height=40,
            command=self.attempt_login
        )
        login_button.grid(row=4, column=0, pady=20)
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            form_frame,
            text="",
            text_color="#f44336",
            font=("Arial", 12)
        )
        self.error_label.grid(row=5, column=0)
    
    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Simple validation - in a real app, you'd check against a database
        if username == "" and password == "":
            self.switch_callback("WelcomeScreen")
        else:
            self.error_label.configure(text="Tên đăng nhập hoặc mật khẩu không đúng")
