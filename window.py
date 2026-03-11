"""
Visualization windows for Page Replacement Visualizer
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from typing import List, Dict

from constants import COLORS, FONT_FAMILY, AnimationSpeed
from models import PageFaultResult
from controllers import AnimationController


class VisualizationWindow:
    """Window for visualizing algorithm execution"""
    
    def __init__(self, parent, result: PageFaultResult, pages: List[int], 
                 num_frames: int, controller: AnimationController):
        """Initialize visualization window"""
        self.parent = parent
        self.result = result
        self.pages = pages
        self.num_frames = num_frames
        self.controller = controller
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Visualization: {result.algorithm_name}")
        self.window.geometry("1200x750+0+0")
        self.window.configure(bg=COLORS['background'])
        
        # Create UI components
        self._create_header()
        self._create_animation_area()
        self._create_controls()
        self._create_metrics_panel()
        
        # Start animation
        self.window.after(100, self._animate)
    
    def _create_header(self):
        """Create header with algorithm name"""
        header = tk.Frame(self.window, bg=COLORS['primary'], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=f"🔍 {self.result.algorithm_name} Visualization",
            font=(FONT_FAMILY, 20, 'bold'),
            bg=COLORS['primary'],
            fg='white',
            pady=15
        ).pack()
    
    def _create_animation_area(self):
        """Create scrollable area for animation frames"""
        # Container
        container = tk.Frame(self.window, bg=COLORS['background'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas with scrollbar
        canvas = tk.Canvas(container, bg=COLORS['background'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, 
                                 command=canvas.xview)
        
        self.animation_frame = tk.Frame(canvas, bg=COLORS['background'])
        
        self.animation_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.animation_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas = canvas
        
        # Headers
        self._create_animation_headers()
    
    def _create_animation_headers(self):
        """Create headers for animation grid"""
        # Headers directly in animation_frame to align with columns
        tk.Label(
            self.animation_frame,
            text="Page",
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['secondary'],
            fg='white',
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=1
        ).grid(row=0, column=0, padx=2, pady=2, sticky='ew')
        
        for i in range(self.num_frames):
            tk.Label(
                self.animation_frame,
                text=f"Frame {i+1}",
                font=(FONT_FAMILY, 12, 'bold'),
                bg=COLORS['background'],
                width=12,
                relief=tk.FLAT
            ).grid(row=i+1, column=0, padx=2, pady=2, sticky='ew')
        
        tk.Label(
            self.animation_frame,
            text="Status",
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['secondary'],
            fg='white',
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=1
        ).grid(row=self.num_frames+1, column=0, padx=2, pady=2, sticky='ew')
    
    def _create_controls(self):
        """Create animation control buttons"""
        control_frame = tk.Frame(self.window, bg=COLORS['background'])
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Speed selection
        tk.Label(
            control_frame,
            text="Speed:",
            font=(FONT_FAMILY, 11),
            bg=COLORS['background']
        ).pack(side=tk.LEFT, padx=5)
        
        speed_var = tk.StringVar(value="Medium")
        speed_menu = ttk.Combobox(
            control_frame,
            textvariable=speed_var,
            values=["Slow", "Medium", "Fast", "Instant"],
            state="readonly",
            width=10
        )
        speed_menu.pack(side=tk.LEFT, padx=5)
        speed_menu.bind("<<ComboboxSelected>>", 
                       lambda e: self._change_speed(speed_var.get()))
        
        # Store button reference for updating text
        self.pause_button = ttk.Button(
            control_frame,
            text="⏸ Pause",
            command=self._toggle_pause
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="⏹ Stop",
            command=self._stop_animation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="🔄 Restart",
            command=self._restart_animation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="✖ Close",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _create_metrics_panel(self):
        """Create panel showing performance metrics"""
        metrics_frame = tk.LabelFrame(
            self.window,
            text="📊 Performance Metrics",
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['card'],
            padx=10,
            pady=10
        )
        metrics_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        metrics = [
            ("Total Faults:", self.result.total_faults, COLORS['fault']),
            ("Total Hits:", self.result.total_hits, COLORS['hit']),
            ("Fault Ratio:", f"{self.result.fault_ratio:.4f}", COLORS['fault']),
            ("Hit Ratio:", f"{self.result.hit_ratio:.4f}", COLORS['hit']),
            ("Execution Time:", f"{self.result.execution_time:.2f} ms", COLORS['text']),
        ]
        
        for label, value, color in metrics:
            container = tk.Frame(metrics_frame, bg=COLORS['card'])
            container.pack(side=tk.LEFT, padx=15)
            
            tk.Label(
                container,
                text=label,
                font=(FONT_FAMILY, 10),
                bg=COLORS['card']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                container,
                text=str(value),
                font=(FONT_FAMILY, 10, 'bold'),
                fg=color,
                bg=COLORS['card']
            ).pack(side=tk.LEFT, padx=5)
    
    def _animate(self):
        """Animate the algorithm execution step by step"""
        if self.controller.is_stopped:
            return
        
        # Handle restart
        if self.controller.is_restarting:
            self._clear_animation()
            self.controller.is_restarting = False
            self.controller.current_step = 0
        
        if self.controller.is_paused:
            self.window.after(100, self._animate)
            return
        
        step = self.controller.current_step
        
        if step >= len(self.pages):
            return  # Animation complete
        
        # Create column for current step
        col = step + 1
        
        # Page number
        page = self.pages[step]
        tk.Label(
            self.animation_frame,
            text=str(page),
            font=(FONT_FAMILY, 11, 'bold'),
            bg=COLORS['secondary'],
            fg='white',
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=2
        ).grid(row=0, column=col, padx=2, pady=2, sticky='ew')
        
        # Frame states
        frames = self.result.frame_states[step]
        for i in range(self.num_frames):
            value = frames[i] if i < len(frames) else ""
            tk.Label(
                self.animation_frame,
                text=str(value),
                font=(FONT_FAMILY, 11),
                bg='white',
                width=12,
                height=2,
                relief=tk.SOLID,
                bd=1
            ).grid(row=i+1, column=col, padx=2, pady=2, sticky='ew')
        
        # Status (Hit/Fault)
        is_fault = self.result.fault_indicators[step]
        status_text = "FAULT" if is_fault else "HIT"
        status_color = COLORS['fault'] if is_fault else COLORS['hit']
        
        tk.Label(
            self.animation_frame,
            text=status_text,
            font=(FONT_FAMILY, 10, 'bold'),
            fg=status_color,
            bg=COLORS['background'],
            width=12,
            height=2
        ).grid(row=self.num_frames+1, column=col, padx=2, pady=2, sticky='ew')
        
        # Scroll to show current step
        self.window.update()
        self.canvas.xview_moveto(step / len(self.pages))
        
        # Next step
        self.controller.current_step += 1
        self.controller.wait()
        self.window.after(50, self._animate)
    
    def _toggle_pause(self):
        """Toggle pause/resume"""
        if self.controller.is_paused:
            self.controller.resume()
            self.pause_button.config(text="⏸ Pause")
        else:
            self.controller.pause()
            self.pause_button.config(text="▶ Resume")
    
    def _stop_animation(self):
        """Stop animation"""
        self.controller.stop()
    
    def _restart_animation(self):
        """Restart animation from beginning"""
        self.controller.restart()
        self.pause_button.config(text="⏸ Pause")
        self.window.after(50, self._animate)
    
    def _clear_animation(self):
        """Clear all animation columns except headers"""
        # Remove all widgets except column 0 (headers)
        for widget in self.animation_frame.winfo_children():
            info = widget.grid_info()
            if info and info.get('column', 0) > 0:
                widget.destroy()
    
    def _change_speed(self, speed_str: str):
        """Change animation speed"""
        speed_map = {
            "Slow": AnimationSpeed.SLOW,
            "Medium": AnimationSpeed.MEDIUM,
            "Fast": AnimationSpeed.FAST,
            "Instant": AnimationSpeed.INSTANT
        }
        self.controller.set_speed(speed_map[speed_str])


class ComparisonWindow:
    """Window for comparing multiple algorithms"""
    
    def __init__(self, parent, results: Dict[str, PageFaultResult], 
                 pages: List[int], num_frames: int):
        """Initialize comparison window"""
        self.parent = parent
        self.results = results
        self.pages = pages
        self.num_frames = num_frames
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Algorithm Comparison")
        self.window.geometry("900x600")
        self.window.configure(bg=COLORS['background'])
        
        self._create_ui()
    
    def _create_ui(self):
        """Create comparison UI"""
        # Header
        header = tk.Frame(self.window, bg=COLORS['primary'], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📊 Algorithm Comparison",
            font=(FONT_FAMILY, 20, 'bold'),
            bg=COLORS['primary'],
            fg='white',
            pady=15
        ).pack()
        
        # Input info
        info_frame = tk.Frame(self.window, bg=COLORS['background'])
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Page Reference String: {' '.join(map(str, self.pages))}",
            font=(FONT_FAMILY, 10),
            bg=COLORS['background']
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Number of Frames: {self.num_frames}",
            font=(FONT_FAMILY, 10),
            bg=COLORS['background']
        ).pack(anchor='w')
        
        # Comparison table
        self._create_comparison_table()
        
        # Visual comparison (bar chart simulation)
        self._create_visual_comparison()
        
        # Export and close buttons
        button_frame = tk.Frame(self.window, bg=COLORS['background'])
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="💾 Export to CSV",
            font=(FONT_FAMILY, 11),
            bg=COLORS['success'],
            fg='white',
            command=self._export_results,
            pady=5,
            padx=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="✖ Close",
            font=(FONT_FAMILY, 11),
            bg=COLORS['accent'],
            fg='white',
            command=self.window.destroy,
            pady=5,
            padx=15
        ).pack(side=tk.RIGHT, padx=5)
    
    def _create_comparison_table(self):
        """Create table comparing algorithm metrics"""
        table_frame = tk.LabelFrame(
            self.window,
            text="Performance Metrics",
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['card'],
            padx=10,
            pady=10
        )
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Headers
        headers = ["Algorithm", "Faults", "Hits", "Fault Ratio", "Hit Ratio", "Time (ms)"]
        for col, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=(FONT_FAMILY, 11, 'bold'),
                bg=COLORS['secondary'],
                fg='white',
                relief=tk.RAISED,
                bd=1,
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky='ew', padx=1, pady=1)
        
        # Data rows
        for row, (algo_name, result) in enumerate(self.results.items(), start=1):
            data = [
                algo_name,
                result.total_faults,
                result.total_hits,
                f"{result.fault_ratio:.4f}",
                f"{result.hit_ratio:.4f}",
                f"{result.execution_time:.2f}"
            ]
            
            for col, value in enumerate(data):
                bg_color = 'white' if row % 2 == 0 else '#f8f9fa'
                tk.Label(
                    table_frame,
                    text=str(value),
                    font=(FONT_FAMILY, 10),
                    bg=bg_color,
                    relief=tk.SOLID,
                    bd=1,
                    padx=10,
                    pady=8
                ).grid(row=row, column=col, sticky='ew', padx=1, pady=1)
        
        # Configure column weights
        for col in range(len(headers)):
            table_frame.columnconfigure(col, weight=1)
    
    def _create_visual_comparison(self):
        """Create visual bar chart comparison"""
        chart_frame = tk.LabelFrame(
            self.window,
            text="Visual Comparison - Fault Ratio",
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['card'],
            padx=10,
            pady=10
        )
        chart_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        max_ratio = max(r.fault_ratio for r in self.results.values()) if self.results else 1
        
        for algo_name, result in self.results.items():
            row_frame = tk.Frame(chart_frame, bg=COLORS['card'])
            row_frame.pack(fill=tk.X, pady=5)
            
            # Algorithm name
            tk.Label(
                row_frame,
                text=f"{algo_name}:",
                font=(FONT_FAMILY, 10),
                bg=COLORS['card'],
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            # Bar
            bar_width = int((result.fault_ratio / max_ratio) * 400) if max_ratio > 0 else 0
            canvas = tk.Canvas(row_frame, width=450, height=25, 
                             bg=COLORS['card'], highlightthickness=0)
            canvas.pack(side=tk.LEFT)
            
            # Determine color based on performance
            bar_color = COLORS['success']
            if result.fault_ratio > 0.6:
                bar_color = COLORS['fault']
            elif result.fault_ratio > 0.4:
                bar_color = COLORS['warning']
            
            canvas.create_rectangle(0, 5, bar_width, 20, fill=bar_color, outline='')
            canvas.create_text(bar_width + 10, 12, 
                             text=f"{result.fault_ratio:.4f}", 
                             anchor='w', font=(FONT_FAMILY, 9))
    
    def _export_results(self):
        """Export comparison results to CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Comparison Results"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["Page Replacement Algorithm Comparison"])
                writer.writerow([f"Page Reference String: {' '.join(map(str, self.pages))}"])
                writer.writerow([f"Number of Frames: {self.num_frames}"])
                writer.writerow([])
                
                # Write metrics
                writer.writerow(["Algorithm", "Total Faults", "Total Hits", 
                               "Fault Ratio", "Hit Ratio", "Execution Time (ms)"])
                
                for algo_name, result in self.results.items():
                    writer.writerow([
                        algo_name,
                        result.total_faults,
                        result.total_hits,
                        f"{result.fault_ratio:.6f}",
                        f"{result.hit_ratio:.6f}",
                        f"{result.execution_time:.4f}"
                    ])
            
            messagebox.showinfo("Success", f"Results exported to:\n{file_path}")
        
        except (IOError, OSError) as e:
            messagebox.showerror("Error", f"Failed to export results:\n{str(e)}")
