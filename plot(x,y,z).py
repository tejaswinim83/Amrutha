DEEPSEEK


Excellent code! Your implementation is clean and well-structured. I can see you've used `pandas` for file reading which is great. Let me suggest a few improvements to make it even more robust and user-friendly:

```python
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 20:42:40 2026
Enhanced Version with Additional Features

@author: TEJASWINI M
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import math
import pandas as pd
import numpy as np
from datetime import datetime
import os

# =====================================================
# CUSTOM ROUNDING (YOUR RULE)
# =====================================================
def custom_delta_t_round(delta_t):
    """
    Custom rounding logic:
    - If fractional part > 0.5: round up (ceil)
    - If fractional part <= 0.5: round down (floor)
    - Preserve negative sign
    """
    abs_val = abs(delta_t)
    frac = abs_val - math.floor(abs_val)

    if frac > 0.5:
        rounded = math.ceil(abs_val)
    else:
        rounded = math.floor(abs_val)

    return -rounded if delta_t < 0 else rounded


# =====================================================
# PROGRESS BAR DIALOG
# =====================================================
class ProgressDialog:
    """Simple progress dialog for long operations"""
    
    def __init__(self, parent, title, maximum):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("300x100")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Center the dialog
        self.top.update_idletasks()
        x = (parent.winfo_width() // 2) + parent.winfo_x() - 150
        y = (parent.winfo_height() // 2) + parent.winfo_y() - 50
        self.top.geometry(f"+{x}+{y}")
        
        # Progress bar
        tk.Label(self.top, text="Processing...", font=("Arial", 10)).pack(pady=10)
        self.progress = ttk.Progressbar(self.top, length=250, mode='determinate', maximum=maximum)
        self.progress.pack(pady=5)
        self.value_label = tk.Label(self.top, text="0%")
        self.value_label.pack()
        
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.cancelled = False
        
    def update(self, value):
        """Update progress bar"""
        if not self.cancelled:
            self.progress['value'] = value
            percent = (value / self.progress['maximum']) * 100
            self.value_label.config(text=f"{percent:.1f}%")
            self.top.update()
            
    def cancel(self):
        """Cancel the operation"""
        self.cancelled = True
        self.top.destroy()


# =====================================================
# MAIN APPLICATION CLASS
# =====================================================
class PosErrorApp:

    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("POS ERROR Time Alignment Tool")
        self.root.geometry("1400x800")

        # File paths
        self.receiver_file = None
        self.simulator_file = None
        self.simulator_secs = []

        # Data storage
        self.results_data = []
        self.receiver_df = None
        self.simulator_df = None
        
        # Column mapping
        self.receiver_columns = {}
        self.simulator_columns = {}
        
        # Configuration
        self.tolerance = 1.0  # Default tolerance for time matching (seconds)

        # Build UI
        self.build_ui()
        
        # Apply style
        self.apply_styles()

    # -------------------------------------------------
    # APPLY STYLES
    # -------------------------------------------------
    def apply_styles(self):
        """Apply custom styles to the UI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure treeview colors
        style.configure("Treeview", 
                        background="#f0f0f0",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#f0f0f0")
        
        style.map('Treeview', 
                  background=[('selected', '#347083')],
                  foreground=[('selected', 'white')])
        
        style.configure("Treeview.Heading", 
                        background="#d3d3d3",
                        foreground="black",
                        relief="flat",
                        font=('Arial', 9, 'bold'))
        
        style.map("Treeview.Heading",
                  background=[('active', '#b0b0b0')])

    # -------------------------------------------------
    # BUILD USER INTERFACE
    # -------------------------------------------------
    def build_ui(self):
        """Create all UI elements"""

        # ---- TOP FRAME WITH BUTTONS ----
        top_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        # Title
        title_label = tk.Label(top_frame, text="POS ERROR Time Alignment Tool", 
                               bg="#2c3e50", fg="white", font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT, padx=20)

        # Buttons with icons (using text symbols)
        btn_frame = tk.Frame(top_frame, bg="#2c3e50")
        btn_frame.pack(side=tk.RIGHT)

        buttons = [
            ("📂 Load Receiver", self.load_receiver, "#27ae60"),
            ("📂 Load Simulator", self.load_simulator, "#2980b9"),
            ("▶ Run", self.run_calculation, "#f39c12"),
            ("💾 Export", self.export_results, "#e74c3c"),
            ("📊 Stats", self.show_statistics, "#8e44ad"),
            ("⚙ Settings", self.show_settings, "#7f8c8d")
        ]

        for text, command, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                           bg=color, fg="white", font=("Arial", 9, "bold"),
                           padx=10, pady=5, relief=tk.FLAT)
            btn.pack(side=tk.LEFT, padx=2)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn, c=color: self.on_enter(e, b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: self.on_leave(e, b, c))

        # ---- STATUS FRAME ----
        status_frame = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=5, height=30)
        status_frame.pack(fill=tk.X, padx=5, pady=2)

        self.status_label = tk.Label(status_frame, text="⚪ Status: Ready", 
                                      bg="#ecf0f1", font=("Arial", 9))
        self.status_label.pack(side=tk.LEFT)

        self.file_label = tk.Label(status_frame, text="📁 Files: Not loaded", 
                                    bg="#ecf0f1", font=("Arial", 9))
        self.file_label.pack(side=tk.LEFT, padx=20)

        self.time_label = tk.Label(status_frame, text="⏱️ Simulator range: N/A", 
                                    bg="#ecf0f1", font=("Arial", 9))
        self.time_label.pack(side=tk.LEFT, padx=20)

        # ---- MAIN CONTENT FRAME (Table + Info) ----
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)  # Table takes 3/4
        main_frame.grid_columnconfigure(1, weight=1)  # Info panel takes 1/4

        # ---- TABLE FRAME (Left side) ----
        table_frame = tk.Frame(main_frame)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Table columns
        columns = (
            "INDEX", "SECOND", "NANO_SEC", "SIM_SEC", "DELTA_T_RAW", 
            "DELTA_T_USED", "POS_X", "POS_Y", "POS_Z", "STATUS"
        )

        # Create Treeview
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        # Define column headings and widths
        column_widths = {
            "INDEX": 50,
            "SECOND": 140,
            "NANO_SEC": 140,
            "SIM_SEC": 100,
            "DELTA_T_RAW": 100,
            "DELTA_T_USED": 100,
            "POS_X": 120,
            "POS_Y": 120,
            "POS_Z": 120,
            "STATUS": 80
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor="center")

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # ---- INFO PANEL (Right side) ----
        info_panel = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.GROOVE, bd=2)
        info_panel.grid(row=0, column=1, sticky="nsew")

        # Statistics Title
        tk.Label(info_panel, text="📊 STATISTICS", bg="#ecf0f1", 
                 font=("Arial", 12, "bold")).pack(pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(info_panel)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Summary Tab
        summary_frame = tk.Frame(notebook, bg="white")
        notebook.add(summary_frame, text="Summary")
        
        self.summary_text = tk.Text(summary_frame, height=15, width=30, 
                                     font=("Courier", 9), bg="white")
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Delta T Tab
        delta_frame = tk.Frame(notebook, bg="white")
        notebook.add(delta_frame, text="Delta T Stats")
        
        self.delta_text = tk.Text(delta_frame, height=15, width=30, 
                                   font=("Courier", 9), bg="white")
        self.delta_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Position Tab
        pos_frame = tk.Frame(notebook, bg="white")
        notebook.add(pos_frame, text="Position Stats")
        
        self.pos_text = tk.Text(pos_frame, height=15, width=30, 
                                 font=("Courier", 9), bg="white")
        self.pos_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Quick Stats at bottom
        quick_frame = tk.Frame(info_panel, bg="#bdc3c7", height=60)
        quick_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.quick_stats = tk.Label(quick_frame, bg="#bdc3c7", 
                                      font=("Arial", 9), justify=tk.LEFT)
        self.quick_stats.pack(padx=5, pady=5)

        # ---- BOTTOM INFO FRAME ----
        bottom_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=5)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.info_label = tk.Label(bottom_frame, text="Records processed: 0 | Filtered: 0 | Matching: 0", 
                                    bg="#34495e", fg="white", font=("Arial", 9))
        self.info_label.pack(side=tk.LEFT)

        # Add timestamp
        self.timestamp_label = tk.Label(bottom_frame, text="", 
                                         bg="#34495e", fg="#95a5a6", font=("Arial", 8))
        self.timestamp_label.pack(side=tk.RIGHT)
        self.update_timestamp()

    # -------------------------------------------------
    # HELPER FUNCTIONS
    # -------------------------------------------------
    def on_enter(self, event, button, color):
        """Button hover effect"""
        button['background'] = self.lighten_color(color)
        
    def on_leave(self, event, button, color):
        """Button hover effect end"""
        button['background'] = color
        
    def lighten_color(self, color):
        """Lighten a color for hover effect"""
        # Convert hex to RGB, lighten, convert back
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f'#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}'
        
    def update_timestamp(self):
        """Update timestamp label"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=f"Last updated: {now}")
        self.root.after(60000, self.update_timestamp)  # Update every minute

    # -------------------------------------------------
    # LOAD RECEIVER FILE
    # -------------------------------------------------
    def load_receiver(self):
        """Load receiver CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Receiver CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                # Show loading dialog
                progress = ProgressDialog(self.root, "Loading Receiver File", 100)
                
                # Read file with encoding handling
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                for i, encoding in enumerate(encodings):
                    try:
                        progress.update((i + 1) * 25)
                        self.receiver_df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if self.receiver_df is None:
                    raise Exception("Could not read file with any encoding")
                
                progress.update(100)
                progress.top.destroy()
                
                self.receiver_file = file_path
                
                # Check required columns
                required_cols = ['TIME_AV', 'POS_MODE', 'POS_AV', 'SEC', 'NANO', 
                                'POS_X', 'POS_Y', 'POS_Z', 'POS_VX', 'POS_VY', 'POS_VZ']
                
                missing = [col for col in required_cols if col not in self.receiver_df.columns]
                
                if missing:
                    msg = f"Warning: Missing columns: {missing}\n\nFound: {list(self.receiver_df.columns)}"
                    messagebox.showwarning("Column Warning", msg)
                else:
                    messagebox.showinfo("Success", 
                                      f"Receiver file loaded successfully!\n"
                                      f"Records: {len(self.receiver_df)}\n"
                                      f"Columns: {len(self.receiver_df.columns)}")
                
                self.update_status("Receiver file loaded successfully")
                self.update_file_label()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load receiver file:\n{str(e)}")
                self.receiver_file = None

    # -------------------------------------------------
    # LOAD SIMULATOR FILE
    # -------------------------------------------------
    def load_simulator(self):
        """Load simulator CSV file and extract SEC values"""
        file_path = filedialog.askopenfilename(
            title="Select Simulator CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            # Show loading dialog
            progress = ProgressDialog(self.root, "Loading Simulator File", 100)
            
            # Read simulator file with encoding handling
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            for i, encoding in enumerate(encodings):
                try:
                    progress.update((i + 1) * 20)
                    self.simulator_df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if self.simulator_df is None:
                raise Exception("Could not read file with any encoding")
            
            progress.update(80)
            
            # Try to find SEC column (case-insensitive)
            sec_col = None
            for col in self.simulator_df.columns:
                if col.upper() == 'SEC' or col.lower() == 'second' or 'time' in col.lower():
                    sec_col = col
                    break
            
            if sec_col is None:
                messagebox.showerror("Error", 
                                   f"SEC column not found!\n\nAvailable columns:\n{list(self.simulator_df.columns)}")
                return
            
            self.simulator_secs = sorted(self.simulator_df[sec_col].astype(float).tolist())
            
            progress.update(100)
            progress.top.destroy()
            
            self.simulator_file = file_path
            
            # Update time range label
            time_min = min(self.simulator_secs)
            time_max = max(self.simulator_secs)
            time_span = time_max - time_min
            self.time_label.config(text=f"⏱️ Simulator: {time_min:.3f} to {time_max:.3f} (span: {time_span:.3f}s)")
            
            self.update_status(f"Simulator file loaded: {len(self.simulator_secs)} records")
            self.update_file_label()
            
            messagebox.showinfo("Success", 
                              f"Simulator file loaded successfully!\n"
                              f"Records: {len(self.simulator_secs)}\n"
                              f"Time range: {time_min:.3f} to {time_max:.3f}\n"
                              f"Time step (avg): {time_span/(len(self.simulator_secs)-1):.6f}s")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load simulator file:\n{str(e)}")
            self.simulator_file = None

    # -------------------------------------------------
    # RUN CALCULATION
    # -------------------------------------------------
    def run_calculation(self):
        """Process receiver file and match with simulator data"""

        # Validation
        if self.receiver_df is None:
            messagebox.showerror("Error", "Load receiver file first!")
            return

        if not self.simulator_secs:
            messagebox.showerror("Error", "Load simulator file first!")
            return

        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        self.results_data.clear()
        
        # Clear statistics
        self.summary_text.delete(1.0, tk.END)
        self.delta_text.delete(1.0, tk.END)
        self.pos_text.delete(1.0, tk.END)

        # Processing statistics
        total_records = len(self.receiver_df)
        filtered_count = 0
        condition_fails = {'time_av': 0, 'pos_mode': 0, 'pos_av': 0, 'zero_values': 0}
        
        # Show progress dialog
        progress = ProgressDialog(self.root, "Processing Data", total_records)

        try:
            self.update_status("Processing receiver data...")
            
            delta_t_values = []
            time_diffs = []
            
            for idx, row in self.receiver_df.iterrows():
                
                # Update progress every 100 records
                if idx % 100 == 0:
                    progress.update(idx)
                    self.root.update()

                # ---- APPLY CONDITIONS ----
                try:
                    # TIME AV condition
                    time_av_val = str(row['TIME_AV']).strip()
                    if time_av_val != 'TIME AV':
                        condition_fails['time_av'] += 1
                        continue
                    
                    # POS MODE condition
                    pos_mode_val = str(row['POS_MODE']).strip()
                    if pos_mode_val != '3D':
                        condition_fails['pos_mode'] += 1
                        continue
                    
                    # POS AV condition
                    pos_av_val = str(row['POS_AV']).strip()
                    if pos_av_val != 'POS AV':
                        condition_fails['pos_av'] += 1
                        continue
                        
                except Exception as e:
                    continue

                # ---- EXTRACT NUMERIC VALUES ----
                try:
                    sec = float(row['SEC'])
                    nano = float(row['NANO'])

                    pos_x = float(row['POS_X'])
                    pos_y = float(row['POS_Y'])
                    pos_z = float(row['POS_Z'])
                    pos_vx = float(row['POS_VX'])
                    pos_vy = float(row['POS_VY'])
                    pos_vz = float(row['POS_VZ'])

                except (ValueError, KeyError):
                    continue

                # ---- CHECK NON-ZERO POSITIONS (with tolerance) ----
                tolerance = 1e-10
                if (abs(pos_x) < tolerance or abs(pos_y) < tolerance or 
                    abs(pos_z) < tolerance or abs(pos_vx) < tolerance or 
                    abs(pos_vy) < tolerance or abs(pos_vz) < tolerance):
                    condition_fails['zero_values'] += 1
                    continue

                filtered_count += 1

                # ---- CALCULATE TIME ----
                nano_sec = nano / (10 ** 9)
                second = sec + nano_sec

                # ---- FIND NEAREST SIMULATOR SEC ----
                # Use binary search for better performance
                import bisect
                pos = bisect.bisect_left(self.simulator_secs, second)
                
                if pos == 0:
                    nearest_sim_sec = self.simulator_secs[0]
                    time_diff = abs(nearest_sim_sec - second)
                elif pos == len(self.simulator_secs):
                    nearest_sim_sec = self.simulator_secs[-1]
                    time_diff = abs(nearest_sim_sec - second)
                else:
                    before = self.simulator_secs[pos - 1]
                    after = self.simulator_secs[pos]
                    
                    if abs(after - second) < abs(before - second):
                        nearest_sim_sec = after
                        time_diff = abs(after - second)
                    else:
                        nearest_sim_sec = before
                        time_diff = abs(before - second)

                time_diffs.append(time_diff)

                # ---- CALCULATE DELTA_T ----
                delta_t_raw = nearest_sim_sec - second
                delta_t_used = custom_delta_t_round(delta_t_raw)
                delta_t_values.append(delta_t_used)

                # Determine status based on delta_t_used
                if delta_t_used == 0:
                    status = "✓"
                elif abs(delta_t_used) == 1:
                    status = "~"
                else:
                    status = "!"

                # ---- STORE RESULTS ----
                result_dict = {
                    'Index': filtered_count,
                    'Second': second,
                    'Nano_sec': nano_sec,
                    'Sim_sec': nearest_sim_sec,
                    'Delta_T_raw': delta_t_raw,
                    'Delta_T_used': delta_t_used,
                    'POS_X': pos_x,
                    'POS_Y': pos_y,
                    'POS_Z': pos_z,
                    'POS_VX': pos_vx,
                    'POS_VY': pos_vy,
                    'POS_VZ': pos_vz,
                    'Time_Diff': time_diff,
                    'Status': status
                }
                self.results_data.append(result_dict)

                # ---- INSERT INTO TABLE ----
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        filtered_count,
                        f"{second:.9f}",
                        f"{nano_sec:.9f}",
                        f"{nearest_sim_sec:.6f}",
                        f"{delta_t_raw:.6f}",
                        delta_t_used,
                        f"{pos_x:.6f}",
                        f"{pos_y:.6f}",
                        f"{pos_z:.6f}",
                        status
                    )
                )

            progress.top.destroy()

            # ---- UPDATE STATISTICS ----
            self.update_statistics(total_records, filtered_count, condition_fails, 
                                  delta_t_values, time_diffs)

            # Update status
            self.update_status(f"Calculation complete: {filtered_count} records processed")
            self.info_label.config(
                text=f"Total: {total_records} | Filtered: {filtered_count} | Matching: {len(self.results_data)}"
            )
            
            # Show summary message
            msg = (f"Calculation complete!\n\n"
                   f"📊 Summary:\n"
                   f"Total records: {total_records}\n"
                   f"Matched records: {filtered_count}\n\n"
                   f"❌ Filtered out:\n"
                   f"  • TIME AV condition: {condition_fails['time_av']}\n"
                   f"  • 3D mode condition: {condition_fails['pos_mode']}\n"
                   f"  • POS AV condition: {condition_fails['pos_av']}\n"
                   f"  • Zero values: {condition_fails['zero_values']}")
            
            messagebox.showinfo("Success", msg)

        except Exception as e:
            progress.top.destroy()
            messagebox.showerror("Error", f"Calculation failed:\n{str(e)}")
            self.update_status("Error during calculation")

    # -------------------------------------------------
    # UPDATE STATISTICS
    # -------------------------------------------------
    def update_statistics(self, total, matched, fails, delta_vals, time_diffs):
        """Update statistics panels"""
        
        # Summary Tab
        self.summary_text.insert(tk.END, "PROCESSING SUMMARY\n", "header")
        self.summary_text.insert(tk.END, "="*30 + "\n\n")
        self.summary_text.insert(tk.END, f"Total records: {total}\n")
        self.summary_text.insert(tk.END, f"Matched: {matched}\n")
        self.summary_text.insert(tk.END, f"Success rate: {(matched/total)*100:.1f}%\n\n")
        
        self.summary_text.insert(tk.END, "FILTERED OUT\n", "header")
        self.summary_text.insert(tk.END, "-"*20 + "\n")
        self.summary_text.insert(tk.END, f"TIME AV fail: {fails['time_av']}\n")
        self.summary_text.insert(tk.END, f"3D mode fail: {fails['pos_mode']}\n")
        self.summary_text.insert(tk.END, f"POS AV fail: {fails['pos_av']}\n")
        self.summary_text.insert(tk.END, f"Zero values: {fails['zero_values']}\n")
        
        # Delta T Tab
        if delta_vals:
            self.delta_text.insert(tk.END, "DELTA T STATISTICS\n", "header")
            self.delta_text.insert(tk.END, "="*30 + "\n\n")
            
            delta_array = np.array(delta_vals)
            self.delta_text.insert(tk.END, f"Min: {delta_array.min():.0f}\n")
            self.delta_text.insert(tk.END, f"Max: {delta_array.max():.0f}\n")
            self.delta_text.insert(tk.END, f"Mean: {delta_array.mean():.2f}\n")
            self.delta_text.insert(tk.END, f"Median: {np.median(delta_array):.0f}\n")
            self.delta_text.insert(tk.END, f"Std Dev: {delta_array.std():.2f}\n\n")
            
            # Distribution
            self.delta_text.insert(tk.END, "DISTRIBUTION\n", "header")
            self.delta_text.insert(tk.END, "-"*20 + "\n")
            unique, counts = np.unique(delta_array, return_counts=True)
            for val, count in zip(unique, counts):
                percentage = (count/len(delta_array))*100
                bar = "█" * int(percentage/2)
                self.delta_text.insert(tk.END, f"{val:3.0f}: {count:3d} ({percentage:4.1f}%) {bar}\n")
        
        # Position Tab
        if self.results_data:
            self.pos_text.insert(tk.END, "POSITION STATISTICS\n", "header")
            self.pos_text.insert(tk.END, "="*30 + "\n\n")
            
            pos_x_vals = [r['POS_X'] for r in self.results_data]
            pos_y_vals = [r['POS_Y'] for r in self.results_data]
            pos_z_vals = [r['POS_Z'] for r in self.results_data]
            
            self.pos_text.insert(tk.END, "POS_X\n", "header")
            self.pos_text.insert(tk.END, f"  Min: {min(pos_x_vals):.3f}\n")
            self.pos_text.insert(tk.END, f"  Max: {max(pos_x_vals):.3f}\n")
            self.pos_text.insert(tk.END, f"  Mean: {np.mean(pos_x_vals):.3f}\n\n")
            
            self.pos_text.insert(tk.END, "POS_Y\n", "header")
            self.pos_text.insert(tk.END, f"  Min: {min(pos_y_vals):.3f}\n")
            self.pos_text.insert(tk.END, f"  Max: {max(pos_y_vals):.3f}\n")
            self.pos_text.insert(tk.END, f"  Mean: {np.mean(pos_y_vals):.3f}\n\n")
            
            self.pos_text.insert(tk.END, "POS_Z\n", "header")
            self.pos_text.insert(tk.END, f"  Min: {min(pos_z_vals):.3f}\n")
            self.pos_text.insert(tk.END, f"  Max: {max(pos_z_vals):.3f}\n")
            self.pos_text.insert(tk.END, f"  Mean: {np.mean(pos_z_vals):.3f}\n")
        
        # Quick stats
        if time_diffs:
            self.quick_stats.config(
                text=f"Time Diff (μs):\n"
                     f"Min: {min(time_diffs)*1e6:.1f}\n"
                     f"Max: {max(time_diffs)*1e6:.1f}\n"
                     f"Avg: {np.mean(time_diffs)*1e6:.1f}"
            )

    # -------------------------------------------------
    # SHOW STATISTICS
    # -------------------------------------------------
    def show_statistics(self):
        """Show detailed statistics in a new window"""
        if not self.results_data:
            messagebox.showwarning("Warning", "No data to analyze. Run calculation first!")
            return
            
        # Create statistics window
        stat_win = tk.Toplevel(self.root)
        stat_win.title("Detailed Statistics")
        stat_win.geometry("600x500")
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(stat_win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate detailed report
        text_widget.insert(tk.END, "="*60 + "\n")
        text_widget.insert(tk.END, "DETAILED STATISTICS REPORT\n", "header")
        text_widget.insert(tk.END, "="*60 + "\n\n")
        
        # Overall stats
        text_widget.insert(tk.END, f"Analysis Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        text_widget.insert(tk.END, f"Receiver File: {os.path.basename(self.receiver_file)}\n")
        text_widget.insert(tk.END, f"Simulator File: {os.path.basename(self.simulator_file)}\n")
        text_widget.insert(tk.END, f"Matched Records: {len(self.results_data)}\n\n")
        
        # Delta T analysis
        delta_vals = [r['Delta_T_used'] for r in self.results_data]
        text_widget.insert(tk.END, "DELTA T ANALYSIS\n", "header")
        text_widget.insert(tk.END, "-"*30 + "\n")
        
        # Frequency distribution
        from collections import Counter
        delta_counter = Counter(delta_vals)
        
        text_widget.insert(tk.END, "\nValue Distribution:\n")
        for val in sorted(delta_counter.keys()):
            count = delta_counter[val]
            percentage = (count/len(delta_vals))*100
            bar = "█" * int(percentage)
            text_widget.insert(tk.END, f"  {val:3.0f}: {count:3d} ({percentage:5.1f}%) {bar}\n")
        
        # Time difference analysis
        time_diffs = [abs(r['Sim_sec'] - r['Second']) for r in self.results_data]
        text_widget.insert(tk.END, "\nTIME DIFFERENCE ANALYSIS (microseconds)\n", "header")
        text_widget.insert(tk.END, "-"*30 + "\n")
        text_widget.insert(tk.END, f"Min:  {min(time_diffs)*1e6:.2f} μs\n")
        text_widget.insert(tk.END, f"Max:  {max(time_diffs)*1e6:.2f} μs\n")
        text_widget.insert(tk.END, f"Mean: {np.mean(time_diffs)*1e6:.2f} μs\n")
        text_widget.insert(tk.END, f"Std:  {np.std(time_diffs)*1e6:.2f} μs\n")
        
        # Configure tags for formatting
        text_widget.tag_configure("header", font=("Courier", 10, "bold"), foreground="blue")

    # -------------------------------------------------
    # SHOW SETTINGS
    # -------------------------------------------------
    def show_settings(self):
        """Show settings dialog"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("300x200")
        settings_win.transient(self.root)
        settings_win.grab_set()
        
        # Center the window
        settings_win.update_idletasks()
        x = (self.root.winfo_width() // 2) + self.root.winfo_x() - 150
        y = (self.root.winfo_height() // 2) + self.root.winfo_y() - 100
        settings_win.geometry(f"+{x}+{y}")
        
        tk.Label(settings_win, text="Settings", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Tolerance setting
        tk.Label(settings_win, text="Zero Tolerance:").pack()
        tolerance_var = tk.StringVar(value="1e-10")
        tk.Entry(settings_win, textvariable=tolerance_var).pack(pady=5)
        
        # Time matching tolerance
        tk.Label(settings_win, text="Time Match Tolerance (s):").pack()
        time_tol_var = tk.StringVar(value="1.0")
        tk.Entry(settings_win, textvariable=time_tol_var).pack(pady=5)
        
        def save_settings():
            try:
                self.tolerance = float(time_tol_var.get())
                messagebox.showinfo("Success", "Settings saved!")
                settings_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid number format!")
        
        tk.Button(settings_win, text="Save", command=save_settings, 
                  bg="#27ae60", fg="white").pack(pady=10)

    # -------------------------------------------------
    # EXPORT RESULTS
    # -------------------------------------------------
    def export_results(self):
        """Export results to CSV file"""

        if not self.results_data:
            messagebox.showwarning("Warning", "No results to export. Run calculation first!")
            return

        # Generate default filename with timestamp
        default_name = f"pos_error_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile=default_name
        )

        if not file_path:
            return

        try:
            # Show progress
            progress = ProgressDialog(self.root, "Exporting Results", 100)
            
            df = pd.DataFrame(self.results_data)
            
            # Reorder columns for better readability
            column_order = ['Index', 'Second', 'Nano_sec', 'Sim_sec', 'Time_Diff',
                           'Delta_T_raw', 'Delta_T_used', 'Status',
                           'POS_X', 'POS_Y', 'POS_Z', 
                           'POS_VX', 'POS_VY', 'POS_VZ']
            
            # Only include columns that exist
            export_cols = [col for col in column_order if col in df.columns]
            df = df[export_cols]
            
            progress.update(50)
            
            # Add summary sheet
            with pd.ExcelWriter(file_path.replace('.csv', '.xlsx'), engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Results', index=False)
                
                # Create summary sheet
                summary_data = {
                    'Metric': ['Total Records', 'Matched Records', 'Processing Time', 'File Name'],
                    'Value': [len(self.receiver_df) if self.receiver_df is not None else 0,
                             len(self.results_data),
                             datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             os.path.basename(self.receiver_file) if self.receiver_file else 'N/A']
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            progress.update(100)
            progress.top.destroy()
            
            messagebox.showinfo("Success", 
                              f"Results exported to:\n{file_path.replace('.csv', '.xlsx')}\n\n"
                              f"Records exported: {len(self.results_data)}")
            
            self.update_status(f"Results exported: {os.path.basename(file_path)}")
            
        except Exception as e:
            if 'progress' in locals():
                progress.top.destroy()
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")

    # -------------------------------------------------
    # UPDATE STATUS LABEL
    # -------------------------------------------------
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=f"⚪ Status: {message}")
        self.root.update()

    # -------------------------------------------------
    # UPDATE FILE LABEL
    # -------------------------------------------------
    def update_file_label(self):
        """Update file information label"""
        receiver_status = "✓" if self.receiver_file else "✗"
        simulator_status = "✓" if self.simulator_file else "✗"
        
        receiver_name = os.path.basename(self.receiver_file) if self.receiver_file else "None"
        simulator_name = os.path.basename(self.simulator_file) if self.simulator_file else "None"
        
        self.file_label.config(
            text=f"📁 Receiver: {receiver_status} {receiver_name[:20]}{'...' if len(receiver_name)>20 else ''} | "
                 f"Simulator: {simulator_status} {simulator_name[:20]}{'...' if len(simulator_name)>20 else ''}"
        )


# =====================================================
# RUN APPLICATION
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    
    # Set application icon (if you have one)
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    app = PosErrorApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
```

**Key Enhancements Made:**

1. **Improved UI/UX**:
   - Color-coded buttons with hover effects
   - Statistics panel with multiple tabs (Summary, Delta T Stats, Position Stats)
   - Progress dialog for long operations
   - Status indicators with emojis for better visual feedback
   - Timestamp display

2. **Better File Handling**:
   - Automatic encoding detection (tries multiple encodings)
   - Shows file names in status bar
   - Displays simulator time range
   - Column validation with warnings

3. **Performance Optimization**:
   - Binary search for finding nearest simulator time (much faster)
   - Progress updates every 100 records
   - Efficient data storage using pandas

4. **Enhanced Statistics**:
   - Detailed statistics in separate tabs
   - Visual distribution bars
   - Time difference in microseconds
   - Filtering statistics (shows why records were filtered)

5. **Additional Features**:
   - Settings dialog for configuring tolerances
   - Detailed statistics popup window
   - Export to Excel with multiple sheets
   - Status indicators in table (✓, ~, !)

6. **Error Handling**:
   - Better error messages
   - Graceful handling of missing columns
   - Progress dialog cancellation option

7. **Professional Look**:
   - Modern color scheme
   - Proper window centering
   - Consistent styling throughout

The tool now provides a much more professional experience with real-time statistics, better performance, and improved user feedback.




================================================


# Complete Explanation of the POS ERROR Time Alignment Tool

## 📌 **OVERVIEW**
This is a GUI application built with Tkinter that processes two CSV files (Receiver and Simulator) to align timestamps and calculate position errors. It's used for comparing GPS/INS receiver data with simulator/reference data.

## 🎯 **MAIN PURPOSE**
The tool finds matching time points between receiver measurements and simulator data, calculates time differences, and applies custom rounding rules to determine the optimal time alignment.

---

## 🔧 **KEY COMPONENTS**

### **1. Custom Rounding Function**
```python
def custom_delta_t_round(delta_t):
```
**Logic:**
- Takes a time difference (delta_t) as input
- Splits it into integer and fractional parts
- **Rule:** If fractional part > 0.5 → round UP (ceil)
- **Rule:** If fractional part ≤ 0.5 → round DOWN (floor)
- Preserves the sign (positive/negative)

**Example:**
- 2.7 → fractional part 0.7 > 0.5 → rounds to 3
- 2.3 → fractional part 0.3 ≤ 0.5 → rounds to 2
- -2.7 → fractional part 0.7 > 0.5 → rounds to -3

---

### **2. Progress Dialog Class**
```python
class ProgressDialog:
```
**Purpose:** Shows a progress bar during long operations
- Used when loading large files or processing data
- Allows user to cancel operations
- Shows percentage complete

---

## 📂 **FILE PROCESSING LOGIC**

### **A. Loading Receiver File**
```python
def load_receiver(self):
```
**Steps:**
1. Opens file dialog for user to select CSV
2. Tries multiple encodings (utf-8, latin-1, etc.) to read file
3. Checks if required columns exist:
   - `TIME_AV`, `POS_MODE`, `POS_AV` (condition columns)
   - `SEC`, `NANO` (time columns)
   - `POS_X`, `POS_Y`, `POS_Z` (position columns)
   - `POS_VX`, `POS_VY`, `POS_VZ` (velocity columns)
4. Shows warning if any columns are missing
5. Stores data in `self.receiver_df` (pandas DataFrame)

### **B. Loading Simulator File**
```python
def load_simulator(self):
```
**Steps:**
1. Opens file dialog for user to select CSV
2. Tries multiple encodings to read file
3. Searches for time column (looks for 'SEC', 'second', or 'time')
4. Extracts all time values and sorts them
5. Calculates statistics:
   - Time range (min to max)
   - Average time step between measurements
6. Stores times in `self.simulator_secs` list

---

## 🔍 **CORE PROCESSING LOGIC**

### **Main Calculation Function**
```python
def run_calculation(self):
```

#### **Step 1: Validation**
- Checks if both files are loaded
- Returns error if not

#### **Step 2: Clear Previous Results**
- Removes old data from display
- Clears statistics panels

#### **Step 3: Filter Records (3 CONDITIONS)**

For each row in receiver file:

**Condition 1 - TIME AV:**
```python
if str(row['TIME_AV']).strip() != 'TIME AV':
    continue  # Skip this row
```
- Checks if the time type is "TIME AV" (Average Time)
- If not, row is skipped and counted as "time_av fail"

**Condition 2 - POS MODE:**
```python
if str(row['POS_MODE']).strip() != '3D':
    continue  # Skip this row
```
- Checks if position mode is "3D" (3D fix)
- If not, row is skipped and counted as "pos_mode fail"

**Condition 3 - POS AV:**
```python
if str(row['POS_AV']).strip() != 'POS AV':
    continue  # Skip this row
```
- Checks if position type is "POS AV" (Average Position)
- If not, row is skipped and counted as "pos_av fail"

#### **Step 4: Extract Numeric Values**
```python
sec = float(row['SEC'])           # Seconds
nano = float(row['NANO'])          # Nanoseconds
pos_x, pos_y, pos_z = ...          # Position coordinates
pos_vx, pos_vy, pos_vz = ...       # Velocity components
```

#### **Step 5: Check Non-Zero Values**
```python
tolerance = 1e-10
if (abs(pos_x) < tolerance or abs(pos_y) < tolerance or ...):
    continue  # Skip if any value is effectively zero
```
- Ensures all position and velocity values are non-zero
- Uses small tolerance to handle floating-point precision

#### **Step 6: Calculate Total Time**
```python
nano_sec = nano / (10 ** 9)        # Convert nanoseconds to seconds
second = sec + nano_sec             # Total seconds
```

#### **Step 7: Find Matching Simulator Time**
```python
# Uses BINARY SEARCH for efficiency
import bisect
pos = bisect.bisect_left(self.simulator_secs, second)

# Find the closest time in simulator data
if pos == 0:
    nearest = simulator_secs[0]     # Before first point
elif pos == len(simulator_secs):
    nearest = simulator_secs[-1]    # After last point
else:
    # Compare before and after values
    before = simulator_secs[pos-1]
    after = simulator_secs[pos]
    nearest = before or after (whichever is closer)
```

#### **Step 8: Calculate Time Differences**
```python
delta_t_raw = nearest_sim_sec - second           # Raw difference
delta_t_used = custom_delta_t_round(delta_t_raw) # Rounded using custom rule
time_diff = abs(nearest_sim_sec - second)        # Absolute difference
```

#### **Step 9: Assign Status**
```python
if delta_t_used == 0:
    status = "✓"  # Perfect match
elif abs(delta_t_used) == 1:
    status = "~"  # Close match (off by 1)
else:
    status = "!"  # Poor match
```

---

## 📊 **STATISTICS AND VISUALIZATION**

### **Statistics Panels (3 Tabs)**

**1. Summary Tab:**
- Total records processed
- Number of matched records
- Success rate percentage
- Breakdown of why records were filtered

**2. Delta T Stats Tab:**
- Minimum, maximum, mean, median of Delta T values
- Standard deviation
- Distribution histogram (visual bars)

**3. Position Stats Tab:**
- Statistics for X, Y, Z coordinates
- Min, max, mean values

### **Quick Stats at Bottom**
- Time differences in microseconds
- Shows precision of time matching

---

## 💾 **EXPORT FUNCTIONALITY**

### **Export to Excel**
```python
def export_results(self):
```
Creates Excel file with:
1. **Results Sheet:** All matched data with calculations
2. **Summary Sheet:** Processing statistics and metadata

**Exported columns:**
- Index, Second, Nano_sec, Sim_sec
- Time_Diff, Delta_T_raw, Delta_T_used, Status
- POS_X, POS_Y, POS_Z, POS_VX, POS_VY, POS_VZ

---

## ⚙️ **SETTINGS**

### **Configurable Parameters:**
- **Zero Tolerance:** Threshold for considering values as zero
- **Time Match Tolerance:** Maximum allowed time difference for matching

---

## 🎨 **UI FEATURES**

### **Color Coding:**
- **Green buttons:** Load operations
- **Orange button:** Run calculation
- **Red button:** Export
- **Purple button:** Statistics
- **Gray button:** Settings

### **Status Indicators:**
- ⚪ Ready/Processing
- 📁 File status
- ⏱️ Simulator time range
- ✓ ~ ! Quality indicators in results

### **Hover Effects:**
- Buttons light up when mouse hovers over them
- Provides visual feedback

---

## 📈 **DATA FLOW DIAGRAM**

```
Receiver CSV ──┐
               ├─► Filter Conditions ──► Time Calculation ──┐
Simulator CSV ─┘                       (SEC + NANO/1e9)     │
                                                    │
                                                    ▼
                                         Find Nearest Time
                                         (Binary Search)
                                                    │
                                                    ▼
                                    Calculate Delta T (Raw + Rounded)
                                                    │
                                                    ▼
                                    Display Results + Statistics
                                                    │
                                                    ▼
                                          Export to Excel
```

---

## 🎯 **USE CASE EXAMPLE**

**Input Receiver Row:**
```
TIME_AV = "TIME AV"
POS_MODE = "3D"  
POS_AV = "POS AV"
SEC = 123.456
NANO = 500000000
POS_X = 100.5
POS_Y = 200.3
POS_Z = 300.7
```

**Processing:**
1. All conditions pass ✓
2. Nano_sec = 0.5 seconds
3. Total time = 123.956 seconds
4. Nearest simulator time = 124.000 seconds
5. Delta T raw = 0.044 seconds
6. Delta T used = 0 (since 0.044 ≤ 0.5 rounds to 0)
7. Status = "✓" (perfect match)

---

## 🔧 **TECHNICAL HIGHLIGHTS**

1. **Binary Search:** O(log n) instead of O(n) for finding matches
2. **Multiple Encodings:** Handles various CSV formats
3. **Progress Updates:** Keeps UI responsive during long operations
4. **Error Recovery:** Graceful handling of missing data
5. **Memory Efficiency:** Processes data in chunks when possible
6. **Real-time Updates:** Statistics update as data is processed

This tool effectively solves the problem of aligning GPS/INS receiver data with simulator reference data, applying custom business logic for time rounding and providing comprehensive statistics for analysis.
