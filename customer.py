import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class CustomerScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, shared_items):
        super().__init__(parent)
        self.switch_callback = switch_callback
        self.shared_items = shared_items
        self.items = []
        self.item_frames = {}
        self.all_item_frames = []
        self.cart = {}  # Initialize cart as a dictionary
        self.cart_widgets = []  # Stores references to cart item widgets
        self.total_price = 0
        self.item_photos = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        # Search
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.search_bar = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm sản phẩm...", width=300)
        self.search_bar.pack(side="left", padx=10)

        ctk.CTkButton(search_frame, text="Tìm", width=60, command=self.search_items).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Quay lại", fg_color="#f44336", hover_color="#d32f2f",command=lambda: switch_callback("WelcomeScreen")).pack(side="right", padx=10)

        # Items list
        self.items_scroll = ctk.CTkScrollableFrame(self)
        self.items_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Cart panel
        cart_frame = ctk.CTkFrame(self, border_width=2, border_color="#ddd", corner_radius=10)
        cart_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(cart_frame, text="Giỏ hàng", font=("Arial", 20, "bold")).pack(pady=10)
        self.cart_scroll = ctk.CTkScrollableFrame(cart_frame)
        self.cart_scroll.pack(expand=True, fill="both", padx=10, pady=10)

        self.total_label = ctk.CTkLabel(cart_frame, text="Tổng: 0", font=("Arial", 18, "bold"))
        self.total_label.pack(pady=10, padx=10, anchor="e")

        ctk.CTkButton(cart_frame, text="ĐẶT MÓN", fg_color="#4CAF50", hover_color="#45a049",font=("Arial", 16, "bold"), height=40, command=self.place_order).pack(fill="x", padx=10, pady=10)

    def create_item_frame(self, item_data):
        item_frame = ctk.CTkFrame(self.items_scroll, width=450, height=120,border_width=2, border_color="#4CAF50", corner_radius=10)
        
        # Image
        item_image = ctk.CTkLabel(item_frame, text="🛒", font=("Arial", 48), width=80, height=80)
        item_image.pack(side="left", padx=10, pady=10)
        
        if item_data.get('Image'):
            try:
                img = Image.open(item_data['Image']).resize((80, 80), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                item_image.configure(image=photo, text="")
                self.item_photos.append(photo)  # Prevent garbage collection
            except Exception as e:
                print(f"Error loading image: {e}")
        
        # Info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        name_label = ctk.CTkLabel(info_frame, text=item_data.get('Tên', 'No Name'),font=("Arial", 20, "bold"), anchor="w")
        name_label.pack(anchor="w")
        
        price_label = ctk.CTkLabel(info_frame, text=f"Giá: {item_data.get('Giá tiền', 'N/A')}",font=("Arial", 16), anchor="w")
        price_label.pack(anchor="w")
        
        manufacturer_label = ctk.CTkLabel(info_frame,text=f"NSX: {item_data.get('Nhà sản xuất', 'N/A')}",font=("Arial", 16), anchor="w")
        manufacturer_label.pack(anchor="w")
        
        # Add button
        ctk.CTkButton(item_frame, text="Thêm", width=80, height=30,command=lambda: self.add_to_cart(item_data)).pack(side="right", padx=10, pady=10)
        
        # Bind to detail
        for widget in [item_frame, name_label, price_label, manufacturer_label]:
            widget.bind("<Button-1>", lambda e, d=item_data: self.show_item_detail(d))
        
        item_frame.name_label = name_label
        item_frame.price_label = price_label
        
        return item_frame

    def add_item(self, item_data):
        item_frame = self.create_item_frame(item_data)
        item_frame.pack(fill="x", pady=5)
        self.items.append(item_data)
        self.item_frames[item_data.get('Mã vạch', str(len(self.items)))] = item_frame
        self.all_item_frames.append(item_frame)

    def update_item(self, updated_data):
        barcode = updated_data.get('Mã vạch')
        if barcode in self.item_frames:
            frame = self.item_frames[barcode]
            frame.name_label.configure(text=updated_data.get('Tên', 'No Name'))
            frame.price_label.configure(text=f"Giá: {updated_data.get('Giá tiền', 'N/A')}")

    def search_items(self):
        search_text = self.search_bar.get().lower()
        
        # Show all items if search is empty
        if not search_text.strip():
            for frame in self.all_item_frames:
                frame.pack(fill="x", pady=5)
            return
        
        # Hide all first
        for frame in self.all_item_frames:
            frame.pack_forget()
        
        # Show matching items
        found = False
        for item in self.items:
            name = item.get('Tên', '').lower()
            barcode = item.get('Mã vạch', '').lower()
            manufacturer = item.get('Nhà sản xuất', '').lower()
            
            if (search_text in name or 
                search_text in barcode or 
                search_text in manufacturer):
                self.item_frames[item.get('Mã vạch')].pack(fill="x", pady=5)
                found = True
        
        if not found:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy sản phẩm phù hợp với từ khóa tìm kiếm.")

    def add_to_cart(self, item_data):
        barcode = item_data.get('Mã vạch')
        if not barcode:
            messagebox.showerror("Lỗi", "Sản phẩm không có mã vạch")
            return
            
        if barcode in self.cart:
            # Item exists - increment quantity
            self.cart[barcode]['quantity'] += 1
        else:
            # New item - add to cart
            self.cart[barcode] = {
                'data': item_data,
                'quantity': 1
            }
        
        self.refresh_cart_display()

    def refresh_cart_display(self):
        # Clear existing widgets
        for widget in self.cart_widgets:
            widget.destroy()
        self.cart_widgets = []
        self.total_price = 0
        
        # Create widgets for each cart item
        for barcode, item in self.cart.items():
            item_data = item['data']
            quantity = item['quantity']
            
            # Calculate price
            try:
                price = int(item_data['Giá tiền'].replace('.', ''))
            except:
                price = 0
                
            self.total_price += price * quantity
            
            # Create item frame
            item_frame = ctk.CTkFrame(self.cart_scroll)
            item_frame.pack(fill="x", pady=5)
            self.cart_widgets.append(item_frame)
            
            # Item info
            info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            info_frame.pack(side="left", expand=True, fill="both")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{item_data['Tên']}",
                font=("Arial", 12, "bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{item_data['Giá tiền']} × {quantity}",
                font=("Arial", 12)
            ).pack(anchor="w")
            
            # Quantity controls
            control_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            control_frame.pack(side="right")
            
            # Use partial instead of lambda for proper binding
            from functools import partial
            
            ctk.CTkButton(
                control_frame,
                text="-",
                width=30,
                height=30,
                fg_color="#f44336",
                hover_color="#d32f2f",
                command=partial(self.update_quantity, barcode, -1)
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                control_frame,
                text="+",
                width=30,
                height=30,
                fg_color="#4CAF50",
                hover_color="#45a049",
                command=partial(self.update_quantity, barcode, 1)
            ).pack(side="left", padx=2)
        
        # Update total
        formatted_total = "{:,}".format(self.total_price).replace(",", ".")
        self.total_label.configure(text=f"Tổng: {formatted_total}")

    def update_quantity(self, barcode, change):
        if barcode in self.cart:
            self.cart[barcode]['quantity'] += change
            if self.cart[barcode]['quantity'] <= 0:
                del self.cart[barcode]
            self.refresh_cart_display()
    def place_order(self):
        if not self.cart:  # Check self.cart instead of self.cart_items
            messagebox.showwarning("Giỏ hàng trống", "Vui lòng thêm sản phẩm vào giỏ hàng trước khi đặt món.")
            return

        total_items = sum(item['quantity'] for item in self.cart.values())
        response = messagebox.askyesno(
            "Xác nhận đơn hàng",
            f"Bạn có chắc chắn muốn đặt {total_items} món với tổng giá {self.total_label.cget('text')}?"
        )

        if response:
            messagebox.showinfo("Đặt hàng thành công", "Đơn hàng của bạn đã được ghi nhận!")
            self.cart.clear()  # Clear the cart dictionary
            self.refresh_cart_display() 

    def add_new_item(self, item_data):
        """Add a new item to both screens"""
        self.shared_items.append(item_data)
        
        # Update MainScreen
        self.frames["MainScreen"].add_item(item_data)
        
        # Update CustomerScreen
        self.frames["CustomerScreen"].add_item(item_data)
        
        self.show_frame("MainScreen")
        for item in self.shared_items:
            self.add_item(item)

    def view_order_details(self):
        """This function will be triggered when the cart button is clicked to show customer order details"""
        # Placeholder for customer order data (this would usually come from your order system)
        customer_order_data = {
            "Order ID": "12345",
            "Items": [
                {"name": "Bánh mì", "quantity": 2, "price": 15000},
                {"name": "Kem", "quantity": 1, "price": 10000},
            ],
            "Total": 40000
        }
        
        # Switch to OrderDetailsScreen and pass order data
        self.switch_callback("OrderDetailsScreen", customer_order_data)
