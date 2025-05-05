import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_callback, shared_items):
        super().__init__(parent)
        self.switch_callback = switch_callback
        self.shared_items = shared_items
        self.items = []
        self.item_frames = {}
        self.all_item_frames = []

        # Configure layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top bar
        top_bar = ctk.CTkFrame(self, height=50)
        top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        top_bar.grid_columnconfigure(1, weight=1)

        # Title
        title = ctk.CTkLabel(top_bar, text="Quản lý sản phẩm", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, padx=10)

        # Search bar
        search_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        search_frame.grid(row=0, column=1, sticky="e", padx=10)

        self.search_bar = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm sản phẩm...", width=300)
        self.search_bar.pack(side="left", padx=5)

        search_button = ctk.CTkButton(search_frame, text="Tìm", width=60, command=self.search_items)
        search_button.pack(side="left", padx=5)

        # Add item button
        add_button = ctk.CTkButton(top_bar, text="+ Thêm sản phẩm", fg_color="#4CAF50",hover_color="#45a049", command=lambda: switch_callback("AddItemScreen"))
        add_button.grid(row=0, column=2, padx=10)

        # Logout button
        logout_button = ctk.CTkButton(top_bar, text="Đăng xuất", fg_color="#f44336",
                                    hover_color="#d32f2f", command=lambda: switch_callback("WelcomeScreen"))
        logout_button.grid(row=0, column=3, padx=10)

        # Scrollable area for items
        self.items_scroll = ctk.CTkScrollableFrame(self)
        self.items_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.items_scroll.grid_columnconfigure(0, weight=1)

        # Floating "View Orders" button
        self.view_orders_button = ctk.CTkButton(
            self,
            text="📋",  # Using a clipboard emoji as icon
            width=50,
            height=50,
            corner_radius=25,  # Makes it perfectly round
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=("Arial", 20),
            command=self.view_order_details
        )
        # Place in bottom right corner with some padding
        self.view_orders_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

        # Load items
        self.load_sample_items()

    def load_sample_items(self):
        """Load items from file with proper error handling"""
        try:
            with open(r"C:\Users\Pham Ngan\Documents\csm\food_data.txt", "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        item_data = json.loads(line.strip())
                        # Validate required fields
                        if not all(key in item_data for key in ['Tên', 'Giá tiền', 'Số lượng']):
                            continue
                        self.add_item(item_data)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file dữ liệu sản phẩm")

    def create_item_frame(self, item_data):
        """Create a properly formatted item frame"""
        item_frame = ctk.CTkFrame(self.items_scroll, height=100, border_width=2,
                                border_color="#ddd", corner_radius=10)
        item_frame.grid_columnconfigure(1, weight=1)

        # Image placeholder
        item_image = ctk.CTkLabel(item_frame, text="📦", font=("Arial", 36), width=60, height=60)
        item_image.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Info section
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Name
        name_label = ctk.CTkLabel(info_frame, text=item_data.get('Tên', 'N/A'),
                                font=("Arial", 16, "bold"), anchor="w")
        name_label.pack(anchor="w")

        # Details
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(anchor="w")

        # Price (with proper fallback)
        price = item_data.get('Giá tiền', 'N/A')
        price_label = ctk.CTkLabel(details_frame, text=f"Giá: {price}",
                                 font=("Arial", 14), anchor="w")
        price_label.pack(side="left", padx=5)

        # Quantity (with proper fallback)
        quantity = item_data.get('Số lượng', 'N/A')
        quantity_label = ctk.CTkLabel(details_frame, text=f"Số lượng: {quantity}",
                                    font=("Arial", 14), anchor="w")
        quantity_label.pack(side="left", padx=5)

        # Action buttons
        button_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        button_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

        edit_button = ctk.CTkButton(button_frame, text="Sửa", width=60,
                                  command=lambda: self.switch_callback("ItemDetailScreen", item_data, self.update_item))
        edit_button.pack(pady=5)

        delete_button = ctk.CTkButton(button_frame, text="Xóa", width=60,
                                    fg_color="#f44336", hover_color="#d32f2f",
                                    command=lambda: self.delete_item(item_data))
        delete_button.pack(pady=5)

        # Store references for updates
        item_frame.name_label = name_label
        item_frame.price_label = price_label
        item_frame.quantity_label = quantity_label

        return item_frame

    def add_item(self, item_data):
        """Add item to display, checking for duplicates"""
        if item_data.get('Mã vạch') in self.item_frames:
            return  # Skip if already exists
            
        item_frame = self.create_item_frame(item_data)
        item_frame.grid(row=len(self.items), column=0, sticky="ew", pady=5)
        
        self.items.append(item_data)
        self.item_frames[item_data.get('Mã vạch', str(len(self.items)))] = item_frame
        self.all_item_frames.append(item_frame)

    def create_item_frame(self, item_data):
        item_frame = ctk.CTkFrame(self.items_scroll, height=100, border_width=2,border_color="#ddd", corner_radius=10)
        item_frame.grid_columnconfigure(1, weight=1)

        # Image
        item_image = ctk.CTkLabel(item_frame, text="📦", font=("Arial", 36), width=60, height=60)
        item_image.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        if item_data.get('Image'):
            try:
                img = Image.open(item_data['Image'])
                img = img.resize((60, 60), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                item_image.configure(image=photo, text="")
                item_image.image = photo  # prevent garbage collection
            except Exception as e:
                print(f"Lỗi khi tải ảnh: {e}")

        # Info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        name_label = ctk.CTkLabel(info_frame, text=item_data.get('Tên', 'No Name'),
                                  font=("Arial", 16, "bold"), anchor="w")
        name_label.pack(anchor="w")

        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(anchor="w")

        price_label = ctk.CTkLabel(details_frame, text=f"Giá: {item_data.get('Giá tiền', 'N/A')}",
                                   font=("Arial", 14), anchor="w")
        price_label.pack(side="left", padx=5)

        quantity_label = ctk.CTkLabel(details_frame, text=f"Số lượng: {item_data.get('Số lượng', 'N/A')}",
                                      font=("Arial", 14), anchor="w")
        quantity_label.pack(side="left", padx=5)

        # Buttons
        button_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        button_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

        edit_button = ctk.CTkButton(button_frame, text="Sửa", width=60,
                                    command=lambda: self.switch_callback("ItemDetailScreen", item_data, self.update_item))
        edit_button.pack(pady=5)

        delete_button = ctk.CTkButton(button_frame, text="Xóa", width=60,
                                      fg_color="#f44336", hover_color="#d32f2f",
                                      command=lambda: self.delete_item(item_data))
        delete_button.pack(pady=5)
        
        # Bind click
        def show_detail(event):
            self.switch_callback("ItemDetailScreen", item_data, self.update_item)

        item_frame.bind("<Button-1>", show_detail)
        name_label.bind("<Button-1>", show_detail)
        price_label.bind("<Button-1>", show_detail)
        quantity_label.bind("<Button-1>", show_detail)

        # Store for updates
        item_frame.name_label = name_label
        item_frame.price_label = price_label
        item_frame.quantity_label = quantity_label

        return item_frame

    def add_item(self, item_data):
        item_frame = self.create_item_frame(item_data)
        item_frame.grid(row=len(self.items), column=0, sticky="ew", pady=5)

        self.items.append(item_data)
        self.item_frames[item_data.get('Mã vạch', str(len(self.items)))] = item_frame
        self.all_item_frames.append(item_frame)

    def update_item(self, updated_data):
        barcode = updated_data.get('Mã vạch')
        if barcode in self.item_frames:
            item_frame = self.item_frames[barcode]
            item_frame.name_label.configure(text=updated_data.get('Tên', 'No Name'))
            item_frame.price_label.configure(text=f"Giá: {updated_data.get('Giá tiền', 'N/A')}")
            item_frame.quantity_label.configure(text=f"Số lượng: {updated_data.get('Số lượng', 'N/A')}")

    def delete_item(self, item_data):
        response = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa sản phẩm {item_data.get('Tên', '')}?"
        )
        
        if response:
            barcode = item_data.get('Mã vạch')

            # Remove from shared_items
            self.shared_items[:] = [item for item in self.shared_items if item.get('Mã vạch') != barcode]

            # Remove frame from UI
            frame = self.item_frames.get(barcode)
            if frame:
                frame.destroy()
                self.all_item_frames.remove(frame)
                del self.item_frames[barcode]

            # Remove from items list
            self.items = [item for item in self.items if item.get('Mã vạch') != barcode]

            # Update data file
        self.save_items_to_file()


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
    def add_new_item(self, item_data):
        """Add a new item to both screens and save to a JSON file"""
        self.shared_items.append(item_data)
        self.add_item(item_data)  # Add to MainScreen
        
        # Also add to CustomerScreen if it exists
        if "CustomerScreen" in self.master.frames:
            self.master.frames["CustomerScreen"].add_item(item_data)
        
        self.save_items_to_file()

    def save_items_to_file(self):
        """Save shared items to a JSON file"""
        file_path = 'items.json'  # Specify your desired file path here
        with open(file_path, 'w') as json_file:
            json.dump(self.shared_items, json_file, indent=4)
    def view_order_details(self):
        """This function will be triggered when the button is clicked to show customer order details"""
        
        # Create sample order data (in a real app, this would come from your database)
        sample_order_data = {
            "Order ID": "ORD12345",
            "Customer": "Nguyễn Văn A",
            "Items": [
                {"name": "Bánh mì", "quantity": 2, "price": "15.000"},
                {"name": "Kem", "quantity": 1, "price": "10.000"}
            ],
            "Total": "40.000",
            "Date": "2023-05-15",
            "Status": "Đã hoàn thành"
        }
        
        # Format the order details for display
        formatted_order_details = f"""
        Order ID: {sample_order_data['Order ID']}
        Customer: {sample_order_data['Customer']}
        Date: {sample_order_data['Date']}
        Status: {sample_order_data['Status']}
        
        Items:
        """
        
        for item in sample_order_data['Items']:
            formatted_order_details += f"    - {item['name']} x {item['quantity']} @ {item['price']}\n"
        
        formatted_order_details += f"""
        Total: {sample_order_data['Total']}
        """
        
        # Print the formatted order details (you can use this for logging or debugging)
        print(formatted_order_details)

        # Switch to the order detail screen, passing the formatted order data
        self.switch_callback("OrderDetailsScreen", formatted_order_details)
