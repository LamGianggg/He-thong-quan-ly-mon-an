import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.switch_callback = switch_callback
        
        # Configure grid for proper expansion
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Main container frame
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Title frame
        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.grid(row=0, column=0, pady=(0, 20))
        
        title = ctk.CTkLabel(
            title_frame, 
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG", 
            font=("Arial", 24, "bold")
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            title_frame, 
            text="Chọn chế độ sử dụng", 
            font=("Arial", 16)
        )
        subtitle.pack(pady=(5, 0))
        
        # Options frame
        options_frame = ctk.CTkFrame(container, fg_color="transparent")
        options_frame.grid(row=1, column=0, sticky="nsew")
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        options_frame.grid_rowconfigure(0, weight=1)
        
        # Customer option
        customer_frame = ctk.CTkFrame(
            options_frame,
            width=300,
            height=300,
            border_width=2,
            border_color="#4CAF50",
            corner_radius=10
        )
        customer_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        
        customer_emoji = ctk.CTkLabel(
            customer_frame,
            text="👤",
            font=("Arial", 72),
            justify="center"
        )
        customer_emoji.pack(pady=(30, 10))
        
        customer_title = ctk.CTkLabel(
            customer_frame,
            text="KHÁCH HÀNG",
            font=("Arial", 18, "bold")
        )
        customer_title.pack(pady=(0, 20))
        
        customer_button = ctk.CTkButton(
            customer_frame,
            text="Bắt đầu mua sắm",
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=lambda: switch_callback("CustomerScreen")
        )
        customer_button.pack(pady=(0, 20), padx=20, fill="x")
        
        # Manager option
        manager_frame = ctk.CTkFrame(
            options_frame,
            width=300,
            height=300,
            border_width=2,
            border_color="#f44336",
            corner_radius=10
        )
        manager_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        
        manager_emoji = ctk.CTkLabel(
            manager_frame,
            text="👔",
            font=("Arial", 72),
            justify="center"
        )
        manager_emoji.pack(pady=(30, 10))
        
        manager_title = ctk.CTkLabel(
            manager_frame,
            text="QUẢN LÝ",
            font=("Arial", 18, "bold")
        )
        manager_title.pack(pady=(0, 20))
        
        manager_button = ctk.CTkButton(
            manager_frame,
            text="Đăng nhập",
            fg_color="#f44336",
            hover_color="#d32f2f",
            command=lambda: switch_callback("LoginScreen")
        )
        manager_button.pack(pady=(0, 20), padx=20, fill="x")
