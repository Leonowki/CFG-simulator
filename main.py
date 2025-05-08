import customtkinter as ctk
from cfg_parser import CFGParser
from custom_scrolled_text import CustomScrolledText
from App import App


def main():
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
    
main()