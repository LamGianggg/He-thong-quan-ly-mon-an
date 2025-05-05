import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.switch_callback = switch_callback
        
        # Main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Image frame
        # Manager emoji directly without a surrounding frame
        manager_image = ctk.CTkLabel(
            main_frame,
            text="👔",  # Manager emoji
            font=("Arial", 72)
        )
        manager_image.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        
        # Form frame
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        welcome_label = ctk.CTkLabel(
            form_frame, 
            text='Xin chào: "Tên người dùng"', 
            font=("Arial", 24, "bold")
        )
        welcome_label.pack(pady=20)
        
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=10)
        
        password_label = ctk.CTkLabel(
            password_frame, 
            text="Mật khẩu:", 
            font=("Arial", 16, "bold")
        )
        password_label.pack(side="left", padx=10)
        
        self.password_input = ctk.CTkEntry(
            password_frame, 
            width=200, 
            show="*"
        )
        self.password_input.pack(side="left")
        
        login_button = ctk.CTkButton(
            form_frame, 
            text="Đăng nhập", 
            width=200, 
            height=40,
            command=lambda: switch_callback("MainScreen")
        )
        login_button.pack(pady=10)
        
        change_account = ctk.CTkButton(
            form_frame, 
            text="Đổi tài khoản", 
            fg_color="transparent",
            text_color="blue",
            hover=False,
            command=lambda: print("Change account clicked")
        )
        change_account.pack(pady=5)
        
        create_account = ctk.CTkButton(
            form_frame, 
            text="Tạo tài khoản", 
            fg_color="transparent",
            text_color="blue",
            font=("Arial", 12, "bold"),
            hover=False,
            command=lambda: print("Create account clicked")
        )
        create_account.pack(pady=5)
        
        back_button = ctk.CTkButton(
            form_frame, 
            text="Quay lại", 
            width=200, 
            height=40,
            fg_color="#f44336", 
            hover_color="#d32f2f",
            command=lambda: switch_callback("WelcomeScreen")
        )
        back_button.pack(pady=20)
