import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class AddItemScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, add_item_callback):
        super().__init__(parent)
        self.switch_callback = switch_callback
        self.add_item_callback = add_item_callback
        self.image_path = None
        
        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(self, text="Thêm sản phẩm", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Content frame
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Left column - image
        image_frame = ctk.CTkFrame(content_frame, width=250, height=250)
        image_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.image_label = ctk.CTkLabel(
            image_frame, 
            text="Click để chọn ảnh", 
            fg_color="#f9f9f9", 
            corner_radius=10
        )
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)
        self.image_label.bind("<Button-1>", self.select_image)
        
        # Right column - form
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.inputs = {}
        fields = [
            "Tên:", "Đơn vị:", "Nhà sản xuất:", 
            "Mã vạch:", "Giá tiền:", "Số lượng:"
        ]
        
        for i, field in enumerate(fields):
            label = ctk.CTkLabel(form_frame, text=field)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            entry = ctk.CTkEntry(form_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.inputs[field.strip(':')] = entry
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        add_button = ctk.CTkButton(
            button_frame, 
            text="Thêm sản phẩm", 
            fg_color="#4CAF50", 
            hover_color="#45a049",
            command=self.add_item
        )
        add_button.pack(side="left", padx=10)
        
        back_button = ctk.CTkButton(
            button_frame, 
            text="Quay lại", 
            fg_color="#f44336", 
            hover_color="#d32f2f",
            command=lambda: switch_callback("MainScreen")
        )
        back_button.pack(side="right", padx=10)
    
    def select_image(self, event):
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image Files", "*.png *.jpg *.bmp *.jpeg")]
        )
        
        if file_path:
            self.image_path = file_path
            try:
                img = Image.open(file_path)
                img = img.resize((230, 230), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.image_label.configure(image=self.photo, text="")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")
    
    def add_item(self):
        item_data = {key: entry.get() for key, entry in self.inputs.items()}
        item_data['Image'] = self.image_path
        
        # Validate required fields
        if not item_data['Tên'] or not item_data['Giá tiền']:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên và giá sản phẩm")
            return
        
        self.add_item_callback(item_data)
        self.switch_callback("MainScreen")
