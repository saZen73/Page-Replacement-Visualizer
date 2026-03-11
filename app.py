"""
Main application class for Page Replacement Visualizer
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple, List

from constants import COLORS, FONT_FAMILY, MAX_FRAMES, MAX_PAGES
from controllers import AnimationController
from algorithms import FIFOAlgorithm, LRUAlgorithm, OptimalAlgorithm
from window import VisualizationWindow, ComparisonWindow


class PageReplacementApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.title("Page Replacement Algorithm Visualizer")
        self.root.geometry("800x750+0+0")
        self.root.configure(bg=COLORS['background'])
        self.root.resizable(True, True)
        
        # Animation controller
        self.controller = AnimationController()
        
        # Recent inputs
        self.recent_inputs = []
        
        # UI components (initialized in _create_ui)
        self.algo_var = None
        self.frames_entry = None
        self.pages_entry = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Create main application UI"""
        # Header
        header = tk.Frame(self.root, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=" Page Replacement Algorithm Visualizer ",
            font=(FONT_FAMILY, 22, 'bold'),
            bg=COLORS['primary'],
            fg='white',
            pady=20
        ).pack()
        
        # Main content area
        content = tk.Frame(self.root, bg=COLORS['background'])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Input section
        self._create_input_section(content)
        
        # Action buttons
        self._create_action_buttons(content)
        
        # Preset section
        self._create_preset_section(content)
        
        # Footer
        self._create_footer()
    
    def _create_input_section(self, parent):
        """Create input fields section"""
        input_frame = tk.LabelFrame(
            parent,
            text="Configuration",
            font=(FONT_FAMILY, 14, 'bold'),
            bg=COLORS['card'],
            padx=20,
            pady=15
        )
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Algorithm selection
        algo_frame = tk.Frame(input_frame, bg=COLORS['card'])
        algo_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            algo_frame,
            text="🧠 Algorithm:",
            font=(FONT_FAMILY, 12),
            bg=COLORS['card'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.algo_var = tk.StringVar(value="FIFO")
        algo_menu = ttk.Combobox(
            algo_frame,
            textvariable=self.algo_var,
            values=["FIFO", "LRU", "Optimal"],
            state="readonly",
            font=(FONT_FAMILY, 11),
            width=30
        )
        algo_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Number of frames
        frames_frame = tk.Frame(input_frame, bg=COLORS['card'])
        frames_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            frames_frame,
            text="📦 Number of Frames:",
            font=(FONT_FAMILY, 12),
            bg=COLORS['card'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.frames_entry = tk.Entry(
            frames_frame,
            font=(FONT_FAMILY, 11),
            relief=tk.SOLID,
            bd=1
        )
        self.frames_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.frames_entry.insert(0, "3")
        
        # Page reference string
        pages_frame = tk.Frame(input_frame, bg=COLORS['card'])
        pages_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            pages_frame,
            text="📃 Page References:",
            font=(FONT_FAMILY, 12),
            bg=COLORS['card'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10), anchor='n')
        
        pages_container = tk.Frame(pages_frame, bg=COLORS['card'])
        pages_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.pages_entry = tk.Text(
            pages_container,
            font=(FONT_FAMILY, 11),
            height=3,
            relief=tk.SOLID,
            bd=1,
            wrap=tk.WORD
        )
        self.pages_entry.pack(fill=tk.BOTH, expand=True)
        self.pages_entry.insert("1.0", "7 0 1 2 0 3 0 4 2 3 0 3 2")
        
        tk.Label(
            pages_container,
            text="(Space-separated integers)",
            font=(FONT_FAMILY, 9, 'italic'),
            bg=COLORS['card'],
            fg=COLORS['secondary']
        ).pack(anchor='w', pady=(2, 0))
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg=COLORS['background'])
        button_frame.pack(fill=tk.X, pady=10)
        
        # Visualize single algorithm
        tk.Button(
            button_frame,
            text="🔍 Visualize",
            font=(FONT_FAMILY, 13, 'bold'),
            bg=COLORS['primary'],
            fg='white',
            activebackground=COLORS['secondary'],
            activeforeground='white',
            command=self._visualize_single,
            pady=12,
            cursor='hand2'
        ).pack(fill=tk.X, pady=5)
        
        # Compare all algorithms
        tk.Button(
            button_frame,
            text="📊 Compare All Algorithms",
            font=(FONT_FAMILY, 13, 'bold'),
            bg=COLORS['success'],
            fg='white',
            activebackground='#058a68',
            activeforeground='white',
            command=self._compare_all,
            pady=12,
            cursor='hand2'
        ).pack(fill=tk.X, pady=5)
        
        # Clear inputs
        tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=(FONT_FAMILY, 11),
            bg=COLORS['warning'],
            fg='white',
            activebackground='#d66d00',
            activeforeground='white',
            command=self._clear_inputs,
            pady=8,
            cursor='hand2'
        ).pack(fill=tk.X, pady=5)
    
    def _create_preset_section(self, parent):
        """Create preset examples section"""
        preset_frame = tk.LabelFrame(
            parent,
            text="Quick Start - Example Scenarios",
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['card'],
            padx=15,
            pady=10
        )
        preset_frame.pack(fill=tk.X, pady=(10, 0))
        
        presets = [
            ("📘 Example 1", "3", "7 0 1 2 0 3 0 4 2 3 0 3 2"),
            ("📗 Example 2", "4", "1 2 3 4 1 2 5 1 2 3 4 5"),
            ("📙 Example 3", "3", "2 3 2 1 5 2 4 5 3 2 5 2"),
        ]
        
        for name, frames, pages in presets:
            tk.Button(
                preset_frame,
                text=name,
                font=(FONT_FAMILY, 10),
                bg='white',
                fg=COLORS['text'],
                relief=tk.RAISED,
                bd=1,
                command=lambda f=frames, p=pages: self._load_preset(f, p),
                cursor='hand2',
                pady=5
            ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def _create_footer(self):
        """Create footer with exit button"""
        footer = tk.Frame(self.root, bg=COLORS['background'])
        footer.pack(fill=tk.X, padx=40, pady=(10, 20))
        
        tk.Button(
            footer,
            text="❌ Exit Application",
            font=(FONT_FAMILY, 11, 'bold'),
            bg=COLORS['accent'],
            fg='white',
            activebackground='#d62839',
            activeforeground='white',
            command=self.root.destroy,
            pady=8,
            cursor='hand2'
        ).pack()
    
    def _validate_inputs(self) -> Optional[Tuple[int, List[int]]]:
        """
        Validate user inputs.
        
        Returns:
            Tuple of (num_frames, pages) if valid, None otherwise
        """
        # Validate number of frames
        try:
            num_frames = int(self.frames_entry.get().strip())
            if num_frames <= 0:
                messagebox.showerror("Invalid Input", 
                                   "Number of frames must be positive.")
                return None
            if num_frames > MAX_FRAMES:
                messagebox.showerror("Invalid Input", 
                                   f"Number of frames cannot exceed {MAX_FRAMES}.")
                return None
        except ValueError:
            messagebox.showerror("Invalid Input", 
                               "Number of frames must be a valid integer.")
            return None
        
        # Validate page reference string
        try:
            pages_text = self.pages_entry.get("1.0", tk.END).strip()
            pages = list(map(int, pages_text.split()))
            
            if not pages:
                messagebox.showerror("Invalid Input", 
                                   "Page reference string cannot be empty.")
                return None
            
            if len(pages) > MAX_PAGES:
                messagebox.showwarning("Warning", 
                                     f"Page reference string exceeds {MAX_PAGES} pages. "
                                     "Animation may be slow.")
            
            if any(p < 0 for p in pages):
                messagebox.showerror("Invalid Input", 
                                   "Page numbers must be non-negative.")
                return None
                
        except ValueError:
            messagebox.showerror("Invalid Input", 
                               "Page reference string must contain space-separated integers.")
            return None
        
        # Warn if frames > unique pages
        unique_pages = len(set(pages))
        if num_frames >= unique_pages:
            response = messagebox.askyesno(
                "Warning",
                f"Number of frames ({num_frames}) is >= unique pages ({unique_pages}).\n"
                "This may result in very few or no page faults.\n\n"
                "Continue anyway?"
            )
            if not response:
                return None
        
        return num_frames, pages
    
    def _visualize_single(self):
        """Visualize selected algorithm"""
        # Validate inputs
        validation = self._validate_inputs()
        if not validation:
            return
        
        num_frames, pages = validation
        algorithm = self.algo_var.get()
        
        # Reset controller
        self.controller.reset()
        
        # Execute algorithm
        try:
            algo_class = {
                'FIFO': FIFOAlgorithm,
                'LRU': LRUAlgorithm,
                'Optimal': OptimalAlgorithm
            }[algorithm]
            
            algo = algo_class(pages, num_frames)
            result = algo.execute()
            
            # Show visualization
            VisualizationWindow(self.root, result, pages, num_frames, self.controller)
            
        except (ValueError, KeyError, AttributeError) as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def _compare_all(self):
        """Compare all algorithms"""
        # Validate inputs
        validation = self._validate_inputs()
        if not validation:
            return
        
        num_frames, pages = validation
        
        # Execute all algorithms
        try:
            results = {}
            
            for name, algo_class in [('FIFO', FIFOAlgorithm), 
                                     ('LRU', LRUAlgorithm), 
                                     ('Optimal', OptimalAlgorithm)]:
                algo = algo_class(pages, num_frames)
                results[name] = algo.execute()
            
            # Show comparison window
            ComparisonWindow(self.root, results, pages, num_frames)
            
        except (ValueError, KeyError, AttributeError) as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def _clear_inputs(self):
        """Clear all input fields"""
        self.frames_entry.delete(0, tk.END)
        self.pages_entry.delete("1.0", tk.END)
        self.algo_var.set("FIFO")
    
    def _load_preset(self, frames: str, pages: str):
        """Load a preset configuration"""
        self.frames_entry.delete(0, tk.END)
        self.frames_entry.insert(0, frames)
        
        self.pages_entry.delete("1.0", tk.END)
        self.pages_entry.insert("1.0", pages)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
