import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from add import AddItemScreen
from customer import CustomerScreen
from item import ItemDetailScreen , OrderDetailsScreen
from login import LoginScreen
from mana import MainScreen
from screen import InitialLoginScreen
from welcome import WelcomeScreen
import json

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống quản lý cửa hàng")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Configure main window grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Container to hold all frames
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Shared items list
        self.shared_items = self.load_initial_items()
        
        # Initialize screens
        self.frames = {
            "InitialLoginScreen": InitialLoginScreen(self.container, self.show_frame),
            "WelcomeScreen": WelcomeScreen(self.container, self.show_frame),
            "LoginScreen": LoginScreen(self.container, self.show_frame),
            "MainScreen": MainScreen(self.container, self.show_frame, self.shared_items),
            "CustomerScreen": CustomerScreen(self.container, self.show_frame, self.shared_items),
            "AddItemScreen": AddItemScreen(self.container, self.show_frame, self.add_new_item),
            "ItemDetailScreen": None,
            "OrderDetailsScreen": None
        }

        # Grid all screens except dynamic ones
        for name, frame in self.frames.items():
            if frame is not None:
                frame.grid(row=0, column=0, sticky="nsew")

        # Show initial login screen on launch
        self.show_frame("InitialLoginScreen")
        self.load_items_to_screens()
    def load_initial_items(self):
        """Load initial items from file or create sample data"""
        try:
            with open("food_data.txt", "r", encoding="utf-8") as f:
                return [json.loads(line.strip()) for line in f if line.strip()]
        except (FileNotFoundError, json.JSONDecodeError):
            # Return sample data if file doesn't exist or is invalid
            return [
                {
                    'Tên': 'Kem',
                    'Đơn vị': 'Cái',
                    'Nhà sản xuất': 'Unknown',
                    'Mã vạch': '03693490142904',
                    'Giá tiền': '10.000',
                    'Số lượng': '36',
                    'Image': None
                },
                {
                    'Tên': 'Bánh mì',
                    'Đơn vị': 'Ổ',
                    'Nhà sản xuất': 'ABC Bakery',
                    'Mã vạch': '123456789012',
                    'Giá tiền': '15.000',
                    'Số lượng': '20',
                    'Image': None
                }
            ]
    def load_items_to_screens(self):
        """Load items into both MainScreen and CustomerScreen"""
        for item in self.shared_items:
            self.frames["MainScreen"].add_item(item)
            self.frames["CustomerScreen"].add_item(item)
    def add_new_item(self, item_data):
        """Add a new item to the shared list and both screens"""
        # Add to shared list
        self.shared_items.append(item_data)
        
        # Save to file
        with open("food_data.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(item_data, ensure_ascii=False) + "\n")
        
        # Update both screens
        self.frames["MainScreen"].add_item(item_data)
        self.frames["CustomerScreen"].add_item(item_data)
        
        # Return to main screen
        self.show_frame("MainScreen")

    def show_frame(self, page_name, *args):
        if page_name == "ItemDetailScreen":
            item_data, callback = args
            # Create ItemDetailScreen dynamically when needed
            detail_screen = ItemDetailScreen(self.container, self.show_frame, item_data, callback)
            detail_screen.grid(row=0, column=0, sticky="nsew")
            self.frames["ItemDetailScreen"] = detail_screen
            frame = detail_screen
        elif page_name == "OrderDetailsScreen":
            order_data = args[0]  # Get the customer order data
            # Create OrderDetailsScreen dynamically when needed
            order_details_screen = OrderDetailsScreen(self.container, self.show_frame, order_data)
            order_details_screen.grid(row=0, column=0, sticky="nsew")
            self.frames["OrderDetailsScreen"] = order_details_screen
            frame = order_details_screen
        else:
            frame = self.frames.get(page_name)
            if frame is None:
                raise ValueError(f"Không tìm thấy trang: {page_name}")
            
            # Make sure the frame is visible and fully expanded
            frame.grid(row=0, column=0, sticky="nsew")

        frame.tkraise()
