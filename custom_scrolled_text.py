import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk

class CustomScrolledText(tk.Frame):
    def __init__(self, master=None, **kwargs):
        # Get the current appearance mode index (0 for Light, 1 for Dark)
        mode_index = 1 if ctk.get_appearance_mode() == "Dark" else 0
        
        # Get colors from the theme manager
        bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][mode_index]
        text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"][mode_index]
        select_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"][mode_index]
        
        super().__init__(master, bg=bg_color)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create a standard Scrolled Text
        self.text = scrolledtext.ScrolledText(self, **kwargs)
        self.text.grid(row=0, column=0, sticky="nsew")
        
        # Custom styling
        self.text.configure(
            bg=bg_color,
            fg=text_color,
            insertbackground=text_color,
            selectbackground=select_color,
            relief="flat",
            borderwidth=0
        )
    
    def insert(self, index, text):
        self.text.insert(index, text)
    
    def delete(self, start, end):
        self.text.delete(start, end)
    
    def configure(self, **kwargs):
        self.text.configure(**kwargs)
    
    def get(self, start, end=None):
        return self.text.get(start, end)