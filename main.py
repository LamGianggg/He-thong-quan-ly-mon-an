import customtkinter as ctk
from app import App
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# ... [Keep all your other class definitions the same until App class]
# In the App class, modify the __init__ method to include shared items:

if __name__ == "__main__":
    app = App()
    app.mainloop()