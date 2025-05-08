import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re
from cfg_parser import CFGParser
from custom_scrolled_text import CustomScrolledText
from tree_visualizer import TreeVisualizer

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CFG Parser Application(DATE FORMAT)")
        # Center the spawn of the GUI 
        self.window_width = 1600
        self.window_height = 1000  
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.center_x = int((self.screen_width / 2) - (self.window_width / 2))
        self.center_y = int((self.screen_height / 2) - (self.window_height / 2))
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}")
        # Declare the parser in app
        self.parser = CFGParser()
        
        # Configure the grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)  
        
        # Grammar display__________________________________________________________________________________
        grammar_frame = ctk.CTkFrame(main_frame)
        grammar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        grammar_frame.grid_columnconfigure(0,weight=1)
        
        grammar_label = ctk.CTkLabel(grammar_frame, text="Grammar Definition", font=ctk.CTkFont(size=14, weight="bold"))
        grammar_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)
        # Updated CFG
        grammar_text = """S -> M/D/Y | M-D-Y | M.D.Y
M -> 0X | 1V
D -> 0X | 1N | 2N | 3Z
Y -> NNNN
N -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
X -> 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
V -> 0 | 1 | 2
Z -> 0 | 1"""
        grammar_display = ctk.CTkTextbox(grammar_frame, wrap="word", width=500, height=200, font=ctk.CTkFont(size=16))
        grammar_display.configure(font=ctk.CTkFont(size=16))
        grammar_display.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        grammar_display.insert(tk.END, grammar_text)
        grammar_display.configure(state='disabled')
        # ___________________________________________________________________________________________________________________   
        # Input frame
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.grid(row=1, column=0, sticky="n", padx=10, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Description label
        description = ctk.CTkLabel(input_frame, text="Enter a string that conforms to the grammar (e.g., '05/12/2023'):",
                                font=ctk.CTkFont(size=14))
        description.grid(row=0, column=0, sticky="n", padx=5, pady=5)
        
        # Input field
        self.input_var = tk.StringVar()
        input_entry = ctk.CTkEntry(input_frame, textvariable=self.input_var, width=300)
        input_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # Process button
        process_button = ctk.CTkButton(input_frame, text="Process Input", command=self.process_input)
        process_button.grid(row=2, column=0, padx=5, pady=5)
        
        # Results frame with tabs
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        results_label = ctk.CTkLabel(results_frame, text="Parsing Results", font=ctk.CTkFont(size=14, weight="bold"))
        results_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)
        
        # Tabview for results
        self.tab_view = ctk.CTkTabview(results_frame)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.tab_view.grid_columnconfigure(0, weight=1)
        self.tab_view.grid_rowconfigure(0, weight=1)
        
        # Create tabs
        self.validation_tab = self.tab_view.add("Validation")
        self.leftmost_tab = self.tab_view.add("Leftmost Derivation")
        self.rightmost_tab = self.tab_view.add("Rightmost Derivation")
        self.trees_tab = self.tab_view.add("Parse Trees")
        
        # Configure tabs grid            
        self.validation_tab.grid_columnconfigure(0, weight=1)
        self.leftmost_tab.grid_columnconfigure(0, weight=1)
        self.rightmost_tab.grid_columnconfigure(0, weight=1)
        
        # Special configuration for trees tab
        self.trees_tab.grid_columnconfigure(0, weight=1)
        self.trees_tab.grid_rowconfigure(0, weight=1)
        self.trees_tab.grid_rowconfigure(1, weight=1)
        
        # Text widgets for each tab
        self.validation_result = CustomScrolledText(self.validation_tab, wrap=tk.WORD, font=("Courier", 14))
        self.validation_result.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.leftmost_result = CustomScrolledText(self.leftmost_tab, wrap=tk.WORD, font=("Courier", 14))
        self.leftmost_result.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.rightmost_result = CustomScrolledText(self.rightmost_tab, wrap=tk.WORD, font=("Courier", 14))
        self.rightmost_result.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create frames for parse trees
        self.leftmost_tree_frame = ctk.CTkFrame(self.trees_tab)
        self.leftmost_tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.leftmost_tree_frame.grid_columnconfigure(0, weight=1)
        self.leftmost_tree_frame.grid_rowconfigure(1, weight=1)
        
        self.rightmost_tree_frame = ctk.CTkFrame(self.trees_tab)
        self.rightmost_tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.rightmost_tree_frame.grid_columnconfigure(0, weight=1)
        self.rightmost_tree_frame.grid_rowconfigure(1, weight=1)
        
        # Labels for tree frames
        ctk.CTkLabel(self.leftmost_tree_frame, text="Leftmost Derivation Parse Tree:", 
                font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        
        ctk.CTkLabel(self.rightmost_tree_frame, text="Rightmost Derivation Parse Tree:", 
                font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        
        # Create tree visualization canvases
        self.leftmost_tree_canvas_frame = ctk.CTkFrame(self.leftmost_tree_frame)
        self.leftmost_tree_canvas_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.leftmost_tree_canvas_frame.grid_columnconfigure(0, weight=1)
        self.leftmost_tree_canvas_frame.grid_rowconfigure(0, weight=1)
        
        self.rightmost_tree_canvas_frame = ctk.CTkFrame(self.rightmost_tree_frame)
        self.rightmost_tree_canvas_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.rightmost_tree_canvas_frame.grid_columnconfigure(0, weight=1)
        self.rightmost_tree_canvas_frame.grid_rowconfigure(0, weight=1)
        
        # Create scrollable canvas containers
        self.leftmost_tree_scroll_x = ctk.CTkScrollbar(self.leftmost_tree_canvas_frame, orientation="horizontal")
        self.leftmost_tree_scroll_x.grid(row=1, column=0, sticky="ew")
        
        self.leftmost_tree_scroll_y = ctk.CTkScrollbar(self.leftmost_tree_canvas_frame, orientation="vertical")
        self.leftmost_tree_scroll_y.grid(row=0, column=1, sticky="ns")
        
        self.rightmost_tree_scroll_x = ctk.CTkScrollbar(self.rightmost_tree_canvas_frame, orientation="horizontal")
        self.rightmost_tree_scroll_x.grid(row=1, column=0, sticky="ew")
        
        self.rightmost_tree_scroll_y = ctk.CTkScrollbar(self.rightmost_tree_canvas_frame, orientation="vertical")
        self.rightmost_tree_scroll_y.grid(row=0, column=1, sticky="ns")
        
        # Create tree visualizers
        self.leftmost_tree_canvas = TreeVisualizer(
            self.leftmost_tree_canvas_frame, 
            bg="#f0f0f0", 
            highlightthickness=0,
            xscrollcommand=self.leftmost_tree_scroll_x.set,
            yscrollcommand=self.leftmost_tree_scroll_y.set
        )
        self.leftmost_tree_canvas.grid(row=0, column=0, sticky="nsew")
        
        self.rightmost_tree_canvas = TreeVisualizer(
            self.rightmost_tree_canvas_frame, 
            bg="#f0f0f0", 
            highlightthickness=0,
            xscrollcommand=self.rightmost_tree_scroll_x.set,
            yscrollcommand=self.rightmost_tree_scroll_y.set
        )
        self.rightmost_tree_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Configure scrollbars
        self.leftmost_tree_scroll_x.configure(command=self.leftmost_tree_canvas.xview)
        self.leftmost_tree_scroll_y.configure(command=self.leftmost_tree_canvas.yview)
        self.rightmost_tree_scroll_x.configure(command=self.rightmost_tree_canvas.xview)
        self.rightmost_tree_scroll_y.configure(command=self.rightmost_tree_canvas.yview)
    
    def process_input(self):
        input_string = self.input_var.get().strip()
        
        if not input_string:
            messagebox.showerror("Error", "Please enter an input string")
            return
        
        # Validate input
        is_valid = self.parser.validate_input(input_string)
        
        # Clear previous results
        self.validation_result.configure(state='normal')
        self.validation_result.delete(1.0, tk.END)
        self.leftmost_result.configure(state='normal')
        self.leftmost_result.delete(1.0, tk.END)
        self.rightmost_result.configure(state='normal')
        self.rightmost_result.delete(1.0, tk.END)
        
        # Show validation result
        if is_valid:
            self.validation_result.insert(tk.END, f"✓ The input '{input_string}' is valid according to the grammar.\n\n")
            self.validation_result.insert(tk.END, "Explanation:\n")
            
            # Determine separator type
            separator = None
            if '/' in input_string:
                separator = '/'
                self.validation_result.insert(tk.END, f"S -> M/D/Y (using '/' separator)\n")
            elif '-' in input_string:
                separator = '-'
                self.validation_result.insert(tk.END, f"S -> M-D-Y (using '-' separator)\n")
            else:  # '.' in input_string
                separator = '.'
                self.validation_result.insert(tk.END, f"S -> M.D.Y (using '.' separator)\n")
            
            # individually check the input and separate via the separator
            parts = re.split(r'[-/.]', input_string)
            month, day, year = parts
            
            self.validation_result.insert(tk.END, f"Month part ({month}):\n")
            if month[0] == '0':
                self.validation_result.insert(tk.END, f"  M -> 0X where X = {month[1]}\n")
            else:
                self.validation_result.insert(tk.END, f"  M -> 1V where V = {month[1]}\n")
            
            self.validation_result.insert(tk.END, f"Day part ({day}):\n")
            if day[0] == '0':
                self.validation_result.insert(tk.END, f"  D -> 0X where X = {day[1]}\n")
            elif day[0] in '12':
                self.validation_result.insert(tk.END, f"  D -> {day[0]}N where N = {day[1]}\n")
            else:
                self.validation_result.insert(tk.END, f"  D -> 3Z where Z = {day[1]}\n")
            
            self.validation_result.insert(tk.END, f"Year part ({year}):\n")
            self.validation_result.insert(tk.END, f"  Y -> NNNN where N = {year[0]}, {year[1]}, {year[2]}, {year[3]}\n")
            
            # Generate derivations and trees
            leftmost_steps, leftmost_tree = self.parser.leftmost_derivation(input_string)
            rightmost_steps, rightmost_tree = self.parser.rightmost_derivation(input_string)
            
            # Display