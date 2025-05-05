import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class OrderDetailsScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, order_data):
        super().__init__(parent)
        self.switch_callback = switch_callback
        self.order_data = order_data
        
        # Main layout for the order details screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Title for the order details screen
        title_label = ctk.CTkLabel(
            self, 
            text="Chi tiết đơn hàng của khách", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Order details display (just a placeholder for now)
        order_details_label = ctk.CTkLabel(
            self, 
            text=str(self.order_data), 
            font=("Arial", 16)
        )
        order_details_label.grid(row=1, column=0, padx=20, pady=10)
        
        # Add a back button to return to the main screen
        back_button = ctk.CTkButton(
            self, 
            text="Quay lại", 
            width=200, 
            height=40,
            fg_color="#f44336", 
            hover_color="#d32f2f",
            command=lambda: self.switch_callback("MainScreen")
        )
        back_button.grid(row=2, column=0, padx=20, pady=20)
    def show_frame(self, page_name, *args):
        """Show a frame for the given page name"""
        if page_name in ["ItemDetailScreen", "OrderDetailsScreen"]:
            # Destroy old instance if exists
            if self.frames[page_name]:
                self.frames[page_name].destroy()
            
            # Create new instance
            if page_name == "ItemDetailScreen":
                item_data, callback = args
                new_frame = ItemDetailScreen(self.container, self.show_frame, item_data, callback)
            else:  # OrderDetailsScreen
                order_data = args[0] if args else None
                new_frame = OrderDetailsScreen(self.container, self.show_frame, order_data)
            
            new_frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = new_frame
            frame = new_frame
        else:
            frame = self.frames.get(page_name)
            if frame is None:
                raise ValueError(f"Không tìm thấy trang: {page_name}")
            
        frame.tkraise()

class EditItemDialog(ctk.CTkToplevel):
    def __init__(self, parent, item_data):
        super().__init__(parent)
        self.title("Chỉnh sửa thông tin")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.fields = {}
        
        # Create form fields
        fields_info = [
            ("Tên:", item_data.get('Tên', '')),
            ("Mã vạch:", item_data.get('Mã vạch', '')),
            ("Đơn vị:", item_data.get('Đơn vị', '')),
            ("Nhà sản xuất:", item_data.get('Nhà sản xuất', '')),
            ("Số lượng:", item_data.get('Số lượng', '')),
            ("Giá tiền:", item_data.get('Giá tiền', ''))
        ]
        
        for i, (label_text, value) in enumerate(fields_info):
            label = ctk.CTkLabel(self, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            entry = ctk.CTkEntry(self)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.fields[label_text.strip(':')] = entry
        
        # Add buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(fields_info), column=0, columnspan=2, pady=10)
        
        ok_button = ctk.CTkButton(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side="right", padx=10)
        
        self.updated_data = None
    
    def on_ok(self):
        self.updated_data = {key: entry.get() for key, entry in self.fields.items()}
        self.destroy()
    
    def on_cancel(self):
        self.updated_data = None
        self.destroy()
    
    def get_updated_data(self):
        return self.updated_data

class ItemDetailScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, item_data, update_main_callback):
        super().__init__(parent)
        self.switch_callback = switch_callback
        self.item_data = item_data
        self.update_main_callback = update_main_callback
        
        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(self, text="Chi tiết sản phẩm", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")
        
        # Back button
        back_button = ctk.CTkButton(
            self, 
            text="Quay lại", 
            fg_color="#f44336", 
            hover_color="#d32f2f",
            command=lambda: switch_callback("MainScreen")
        )
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        # Content frame
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Image section
        image_frame = ctk.CTkFrame(content_frame, width=300, height=300, corner_radius=10)
        image_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.image_label = ctk.CTkLabel(image_frame, text="No Image", fg_color="transparent")
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)
        
        if item_data.get('Image'):
            try:
                img = Image.open(item_data['Image'])
                img = img.resize((280, 280), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.image_label.configure(image=self.photo, text="")
                # Keep reference to prevent garbage collection
                self.image_label.image = self.photo
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_label.configure(text="Image not available")
        
        # Info section
        info_frame = ctk.CTkFrame(content_frame)
        info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Name with edit button
        name_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=5)
        
        self.name_label = ctk.CTkLabel(
            name_frame, 
            text=f"Tên: {item_data.get('Tên', 'N/A')}", 
            font=("Arial", 20, "bold")
        )
        self.name_label.pack(side="left")
        
        # Fixed edit button - removed problematic image reference
        edit_button = ctk.CTkButton(
            name_frame, 
            text="✏️", 
            width=24, 
            height=24,
            fg_color="transparent",
            hover_color="#e0e0e0",
            command=self.edit_item_info
        )
        edit_button.pack(side="right", padx=5)
        
        # Other info labels
        self.price_label = ctk.CTkLabel(
            info_frame, 
            text=f"Giá: {item_data.get('Giá tiền', 'N/A')}", 
            font=("Arial", 18)
        )
        self.price_label.pack(anchor="w", pady=5)
        
        self.unit_label = ctk.CTkLabel(
            info_frame, 
            text=f"Đơn vị: {item_data.get('Đơn vị', 'N/A')}"
        )
        self.unit_label.pack(anchor="w", pady=5)
        
        self.manufacturer_label = ctk.CTkLabel(
            info_frame, 
            text=f"Nhà sản xuất: {item_data.get('Nhà sản xuất', 'N/A')}"
        )
        self.manufacturer_label.pack(anchor="w", pady=5)
        
        self.barcode_label = ctk.CTkLabel(
            info_frame, 
            text=f"Mã vạch: {item_data.get('Mã vạch', 'N/A')}"
        )
        self.barcode_label.pack(anchor="w", pady=5)
        
        self.quantity_label = ctk.CTkLabel(
            info_frame, 
            text=f"Số lượng: {item_data.get('Số lượng', 'N/A')}"
        )
        self.quantity_label.pack(anchor="w", pady=5)
        
        # Ratings section
        ratings_label = ctk.CTkLabel(
            info_frame, 
            text="Đánh giá:", 
            font=("Arial", 16, "bold")
        )
        ratings_label.pack(anchor="w", pady=(15, 5))
        
        # Sample ratings
        sample_ratings = [
            "Husji kole amkie dakjoe kole <3  5/5",
            "Kosdi anfei okji das dka :((   4/5)"
        ]
        
        for rating in sample_ratings:
            rating_label = ctk.CTkLabel(info_frame, text=rating, text_color="#555")
            rating_label.pack(anchor="w")
        
        # Action buttons
        button_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        edit_price_button = ctk.CTkButton(
            button_frame, 
            text="Sửa giá", 
            command=self.edit_price
        )
        edit_price_button.pack(side="left", padx=5)
        
        restock_button = ctk.CTkButton(
            button_frame, 
            text="Nhập hàng", 
            fg_color="#4CAF50", 
            hover_color="#45a049"
        )
        restock_button.pack(side="left", padx=5)
        
        delete_button = ctk.CTkButton(
            button_frame, 
            text="Xóa", 
            fg_color="#f44336", 
            hover_color="#d32f2f"
        )
        delete_button.pack(side="left", padx=5)
    
    def edit_item_info(self):
        dialog = EditItemDialog(self, self.item_data)
        self.wait_window(dialog)
        
        updated_data = dialog.get_updated_data()
        if updated_data:
            # Update our local data
            for key, value in updated_data.items():
                self.item_data[key] = value
            
            # Update the displayed information
            self.name_label.configure(text=f"Tên: {updated_data.get('Tên', 'N/A')}")
            self.unit_label.configure(text=f"Đơn vị: {updated_data.get('Đơn vị', 'N/A')}")
            self.manufacturer_label.configure(text=f"Nhà sản xuất: {updated_data.get('Nhà sản xuất', 'N/A')}")
            self.barcode_label.configure(text=f"Mã vạch: {updated_data.get('Mã vạch', 'N/A')}")
            self.quantity_label.configure(text=f"Số lượng: {updated_data.get('Số lượng', 'N/A')}")
            self.price_label.configure(text=f"Giá: {updated_data.get('Giá tiền', 'N/A')}")
            
            # Update main screen
            self.update_main_callback(self.item_data)
    
    def edit_price(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Sửa giá")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        
        price_frame = ctk.CTkFrame(dialog)
        price_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        price_label = ctk.CTkLabel(price_frame, text="Giá mới:")
        price_label.pack()
        
        self.price_input = ctk.CTkEntry(price_frame)
        self.price_input.insert(0, self.item_data.get('Giá tiền', ''))
        self.price_input.pack(pady=10)
        
        button_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        button_frame.pack()
        
        ok_button = ctk.CTkButton(
            button_frame, 
            text="OK", 
            command=lambda: self.update_price(dialog)
        )
        ok_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy
        )
        cancel_button.pack(side="right", padx=10)
    
    def update_price(self, dialog):
        new_price = self.price_input.get()
        self.item_data['Giá tiền'] = new_price
        self.price_label.configure(text=f"Giá: {new_price}")
        self.update_main_callback(self.item_data)
        dialog.destroy()
    def show_frame(self, page_name, *args):
        """Show a frame for the given page name"""
        if page_name in ["ItemDetailScreen", "OrderDetailsScreen"]:
            # Destroy old instance if exists
            if self.frames[page_name]:
                self.frames[page_name].destroy()
            
            # Create new instance
            if page_name == "ItemDetailScreen":
                item_data, callback = args
                new_frame = ItemDetailScreen(self.container, self.show_frame, item_data, callback)
            else:  # OrderDetailsScreen
                order_data = args[0] if args else None
                new_frame = OrderDetailsScreen(self.container, self.show_frame, order_data)
            
            new_frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = new_frame
            frame = new_frame
        else:
            frame = self.frames.get(page_name)
            if frame is None:
                raise ValueError(f"Không tìm thấy trang: {page_name}")
            
        frame.tkraise()
