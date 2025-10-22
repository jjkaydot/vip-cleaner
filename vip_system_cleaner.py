import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import tempfile
import ctypes
import sys
from pathlib import Path
import threading
import subprocess

class VIPSystemCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("VIP System Cleaner")
        self.root.geometry("500x750")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(False, False)
        
        # Statistics
        self.files_cleaned = 0
        self.space_freed = 0
        self.locations_count = 0
        self.is_cleaning = False
        
        # Cleaning locations with paths and selection state
        self.cleaning_locations = {
            'Temporary Files': {
                'path': tempfile.gettempdir(),
                'selected': tk.BooleanVar(value=True),
                'description': 'User temp files'
            },
            'Windows Cache': {
                'path': os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
                'selected': tk.BooleanVar(value=True),
                'description': 'System cache'
            },
            'Prefetch Files': {
                'path': os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch'),
                'selected': tk.BooleanVar(value=True),
                'description': 'Prefetch data'
            },
            'Browser Cache': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
                'selected': tk.BooleanVar(value=True),
                'description': 'Browser cache'
            },
            'Recycle Bin': {
                'path': 'shell:RecycleBinFolder',
                'selected': tk.BooleanVar(value=True),
                'description': 'Deleted items'
            },
            'Windows Update Cache': {
                'path': os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SoftwareDistribution', 'Download'),
                'selected': tk.BooleanVar(value=True),
                'description': 'Update files'
            },
            'System Log Files': {
                'path': os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Logs'),
                'selected': tk.BooleanVar(value=True),
                'description': 'System logs'
            }
        }
        
        # Remove default window decorations
        self.root.overrideredirect(True)
        
        # Center window on screen
        self.center_window()
        
        # Create UI
        self.create_ui()
        
        # Bind dragging
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def create_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Custom title bar
        self.title_bar = tk.Frame(main_frame, bg='#0a0a0a', height=60)
        self.title_bar.pack(fill='x', padx=10, pady=(10, 0))
        
        # macOS style buttons
        button_frame = tk.Frame(self.title_bar, bg='#0a0a0a')
        button_frame.pack(side='left', pady=10)
        
        self.create_mac_button(button_frame, '#ff5f57', self.close_window).pack(side='left', padx=2)
        self.create_mac_button(button_frame, '#ffbd2e', self.minimize_window).pack(side='left', padx=2)
        self.create_mac_button(button_frame, '#28c840', lambda: None).pack(side='left', padx=2)
        
        # Title
        title_label = tk.Label(self.title_bar, text="VIP System Cleaner", 
                              font=('Segoe UI', 14, 'bold'), 
                              fg='#FFD700', bg='#0a0a0a')
        title_label.pack(side='left', padx=130)
        
        # Icon and Title Section
        icon_frame = tk.Frame(main_frame, bg='#0a0a0a')
        icon_frame.pack(pady=(20, 10))
        
        # Golden diamond icon
        icon_canvas = tk.Canvas(icon_frame, width=60, height=60, 
                               bg='#0a0a0a', highlightthickness=0)
        icon_canvas.pack()
        
        # Draw rounded square with golden gradient background
        self.draw_rounded_rectangle(icon_canvas, 5, 5, 55, 55, radius=12, fill='#FFD700')
        
        # Draw diamond icon
        icon_canvas.create_polygon(30, 20, 40, 30, 30, 40, 20, 30, 
                                   fill='white', outline='')
        
        # Title
        title = tk.Label(main_frame, text="VIP System Cleaner", 
                        font=('Segoe UI', 26, 'bold'), 
                        fg='#FFD700', bg='#0a0a0a')
        title.pack(pady=(10, 0))
        
        # Subtitle
        subtitle = tk.Label(main_frame, text="💎 Premium Edition - Golden Theme 💎", 
                           font=('Segoe UI', 10), 
                           fg='#DAA520', bg='#0a0a0a')
        subtitle.pack(pady=(0, 20))
        
        # System Status Panel
        status_panel = tk.Frame(main_frame, bg='#1a1a1a', 
                               highlightbackground='#FFD700', 
                               highlightthickness=2)
        status_panel.pack(padx=20, pady=10, fill='x')
        
        # Status header
        status_header = tk.Frame(status_panel, bg='#1a1a1a')
        status_header.pack(fill='x', padx=15, pady=(10, 5))
        
        # Golden diamond indicator
        status_dot = tk.Canvas(status_header, width=12, height=12, 
                              bg='#1a1a1a', highlightthickness=0)
        status_dot.pack(side='left')
        status_dot.create_polygon(6, 2, 10, 6, 6, 10, 2, 6, fill='#FFD700', outline='')
        
        status_label = tk.Label(status_header, text="System Status", 
                               font=('Segoe UI', 11, 'bold'), 
                               fg='#FFD700', bg='#1a1a1a')
        status_label.pack(side='left', padx=5)
        
        self.status_text = tk.Label(status_header, text="Ready to clean...", 
                                    font=('Segoe UI', 9), 
                                    fg='#DAA520', bg='#1a1a1a')
        self.status_text.pack(side='right')
        
        # Statistics
        stats_frame = tk.Frame(status_panel, bg='#1a1a1a')
        stats_frame.pack(fill='x', padx=15, pady=(10, 15))
        
        # Files Cleaned
        self.files_label = self.create_stat_box(stats_frame, "0", "Files Cleaned", '#FFD700')
        self.files_label.pack(side='left', expand=True, padx=5)
        
        # Space Freed
        self.space_label = self.create_stat_box(stats_frame, "0 MB", "Space Freed", '#FFA500')
        self.space_label.pack(side='left', expand=True, padx=5)
        
        # Locations
        self.locations_label = self.create_stat_box(stats_frame, "0", "Selected", '#FF8C00')
        self.locations_label.pack(side='left', expand=True, padx=5)
        
        # Cleaning Locations Panel
        locations_panel = tk.Frame(main_frame, bg='#1a1a1a', 
                                  highlightbackground='#FFD700', 
                                  highlightthickness=2)
        locations_panel.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Locations header
        locations_header = tk.Frame(locations_panel, bg='#1a1a1a')
        locations_header.pack(fill='x', padx=15, pady=(10, 5))
        
        # Golden diamond indicator
        loc_dot = tk.Canvas(locations_header, width=12, height=12, 
                           bg='#1a1a1a', highlightthickness=0)
        loc_dot.pack(side='left')
        loc_dot.create_polygon(6, 2, 10, 6, 6, 10, 2, 6, fill='#FFD700', outline='')
        
        loc_label = tk.Label(locations_header, text="Cleaning Locations", 
                            font=('Segoe UI', 11, 'bold'), 
                            fg='#FFD700', bg='#1a1a1a')
        loc_label.pack(side='left', padx=5)
        
        # Select All / Deselect All buttons
        select_frame = tk.Frame(locations_header, bg='#1a1a1a')
        select_frame.pack(side='right')
        
        select_all_btn = tk.Button(select_frame, text="Select All", 
                                   font=('Segoe UI', 8),
                                   fg='#FFD700', bg='#2a2a2a',
                                   activebackground='#3a3a3a',
                                   activeforeground='#FFD700',
                                   relief='flat', cursor='hand2',
                                   command=self.select_all)
        select_all_btn.pack(side='left', padx=2)
        
        deselect_all_btn = tk.Button(select_frame, text="Clear All", 
                                     font=('Segoe UI', 8),
                                     fg='#FFD700', bg='#2a2a2a',
                                     activebackground='#3a3a3a',
                                     activeforeground='#FFD700',
                                     relief='flat', cursor='hand2',
                                     command=self.deselect_all)
        deselect_all_btn.pack(side='left', padx=2)
        
        # Locations list with checkboxes
        locations_list = tk.Frame(locations_panel, bg='#1a1a1a')
        locations_list.pack(fill='both', expand=True, padx=15, pady=(10, 15))
        
        for location_name, location_data in self.cleaning_locations.items():
            self.create_location_item(locations_list, location_name, location_data)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#0a0a0a')
        button_frame.pack(padx=20, pady=5, fill='x')
        
        # Start Cleaning Button
        self.clean_btn = tk.Button(button_frame, text="💎  Start VIP Cleaning", 
                                   font=('Segoe UI', 11, 'bold'),
                                   fg='#0a0a0a', bg='#FFD700', 
                                   activebackground='#FFA500',
                                   activeforeground='#0a0a0a',
                                   relief='flat', cursor='hand2',
                                   command=self.start_cleaning)
        self.clean_btn.pack(side='left', fill='x', expand=True, ipady=10)
        
        # Exit Button
        exit_btn = tk.Button(button_frame, text="✕  Exit", 
                            font=('Segoe UI', 11, 'bold'),
                            fg='#FFD700', bg='#2a2a2a', 
                            activebackground='#3a3a3a',
                            activeforeground='#FFD700',
                            relief='flat', cursor='hand2',
                            command=self.close_window,
                            highlightbackground='#FFD700',
                            highlightthickness=1)
        exit_btn.pack(side='right', padx=(10, 0), ipadx=20, ipady=10)
        
        # Footer
        footer = tk.Frame(main_frame, bg='#0a0a0a')
        footer.pack(pady=(5, 10))
        
        footer_text = tk.Label(footer, text="💎 VIP System Cleaner - Premium Edition 💎", 
                               font=('Segoe UI', 9, 'bold'), 
                               fg='#FFD700', bg='#0a0a0a')
        footer_text.pack()
        
    def create_location_item(self, parent, name, data):
        item_frame = tk.Frame(parent, bg='#1a1a1a')
        item_frame.pack(fill='x', pady=3)
        
        # Checkbox
        checkbox = tk.Checkbutton(item_frame, 
                                 variable=data['selected'],
                                 bg='#1a1a1a',
                                 activebackground='#1a1a1a',
                                 selectcolor='#2a2a2a',
                                 fg='#FFD700',
                                 activeforeground='#FFD700',
                                 cursor='hand2',
                                 command=self.update_selected_count)
        checkbox.pack(side='left', padx=(0, 5))
        
        # Location name (clickable)
        name_label = tk.Label(item_frame, text=name, 
                             font=('Segoe UI', 10, 'bold'), 
                             fg='#FFD700', bg='#1a1a1a', 
                             cursor='hand2',
                             anchor='w')
        name_label.pack(side='left', fill='x', expand=True)
        name_label.bind('<Button-1>', lambda e: self.open_location(data['path']))
        
        # Folder icon button
        folder_btn = tk.Label(item_frame, text="📁", 
                             font=('Segoe UI', 10), 
                             bg='#1a1a1a',
                             cursor='hand2')
        folder_btn.pack(side='right', padx=5)
        folder_btn.bind('<Button-1>', lambda e: self.open_location(data['path']))
        
        # Description
        desc_label = tk.Label(item_frame, text=f"  {data['description']}", 
                             font=('Segoe UI', 8), 
                             fg='#888888', bg='#1a1a1a', 
                             anchor='w')
        desc_label.pack(side='left', padx=(30, 0))
        
    def open_location(self, path):
        """Open the location in Windows Explorer"""
        try:
            if path == 'shell:RecycleBinFolder':
                # Open Recycle Bin
                subprocess.Popen(['explorer', 'shell:RecycleBinFolder'])
            elif os.path.exists(path):
                # Open folder in Explorer
                subprocess.Popen(['explorer', path])
            else:
                messagebox.showwarning("Location Not Found", 
                                      f"The location does not exist:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open location:\n{str(e)}")
            
    def select_all(self):
        """Select all cleaning locations"""
        for location_data in self.cleaning_locations.values():
            location_data['selected'].set(True)
        self.update_selected_count()
        
    def deselect_all(self):
        """Deselect all cleaning locations"""
        for location_data in self.cleaning_locations.values():
            location_data['selected'].set(False)
        self.update_selected_count()
        
    def update_selected_count(self):
        """Update the count of selected locations"""
        count = sum(1 for loc in self.cleaning_locations.values() if loc['selected'].get())
        self.locations_label.value_label.config(text=str(count))
        
    def create_mac_button(self, parent, color, command):
        canvas = tk.Canvas(parent, width=12, height=12, 
                          bg='#0a0a0a', highlightthickness=0)
        canvas.create_oval(2, 2, 10, 10, fill=color, outline='')
        canvas.bind('<Button-1>', lambda e: command())
        return canvas
        
    def draw_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)
        
    def create_stat_box(self, parent, value, label, color):
        frame = tk.Frame(parent, bg='#0f0f0f', 
                        highlightbackground='#FFD700',
                        highlightthickness=1)
        
        value_label = tk.Label(frame, text=value, 
                              font=('Segoe UI', 18, 'bold'), 
                              fg=color, bg='#0f0f0f')
        value_label.pack(pady=(8, 0))
        
        text_label = tk.Label(frame, text=label, 
                             font=('Segoe UI', 8), 
                             fg='#DAA520', bg='#0f0f0f')
        text_label.pack(pady=(0, 8))
        
        # Store references for updating
        frame.value_label = value_label
        frame.text_label = text_label
        
        return frame
        
    def close_window(self):
        self.root.destroy()
        
    def minimize_window(self):
        self.root.iconify()
        
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def get_folder_size(self, folder_path):
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
        except:
            pass
        return total_size
        
    def clean_folder(self, folder_path, description):
        files_deleted = 0
        size_freed = 0
        
        try:
            if os.path.exists(folder_path):
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    try:
                        if os.path.isfile(item_path):
                            size = os.path.getsize(item_path)
                            os.unlink(item_path)
                            files_deleted += 1
                            size_freed += size
                        elif os.path.isdir(item_path):
                            size = self.get_folder_size(item_path)
                            shutil.rmtree(item_path)
                            files_deleted += 1
                            size_freed += size
                    except Exception as e:
                        pass
        except Exception as e:
            pass
            
        return files_deleted, size_freed
        
    def clean_recycle_bin(self):
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            return 1, 0
        except:
            return 0, 0
                
    def start_cleaning(self):
        if self.is_cleaning:
            return
        
        # Check if any location is selected
        selected_count = sum(1 for loc in self.cleaning_locations.values() if loc['selected'].get())
        if selected_count == 0:
            messagebox.showwarning("No Selection", 
                                  "Please select at least one location to clean!")
            return
            
        if not self.is_admin():
            messagebox.showwarning("Admin Rights Required", 
                                  "Please run this application as Administrator for full cleaning capabilities.")
            
        self.is_cleaning = True
        self.clean_btn.config(state='disabled', text="⏳ VIP Cleaning...")
        self.status_text.config(text="Cleaning in progress...")
        
        # Run cleaning in separate thread
        thread = threading.Thread(target=self.perform_cleaning)
        thread.daemon = True
        thread.start()
        
    def perform_cleaning(self):
        total_files = 0
        total_size = 0
        cleaned_locations = []
        
        # Clean only selected locations
        for location_name, location_data in self.cleaning_locations.items():
            if not location_data['selected'].get():
                continue
                
            self.update_status(f"Cleaning {location_name}...")
            
            if location_name == 'Recycle Bin':
                files, size = self.clean_recycle_bin()
            else:
                files, size = self.clean_folder(location_data['path'], location_name)
            
            if files > 0:
                cleaned_locations.append(location_name)
            total_files += files
            total_size += size
        
        # Update final statistics
        self.files_cleaned = total_files
        self.space_freed = total_size / (1024 * 1024)  # Convert to MB
        
        self.root.after(0, lambda: self.cleaning_complete(cleaned_locations))
        
    def update_status(self, message):
        self.root.after(0, lambda: self.status_text.config(text=message))
        self.root.after(0, self.update_statistics)
        
    def update_statistics(self):
        # Update Files Cleaned
        self.files_label.value_label.config(text=str(self.files_cleaned))
        
        # Update Space Freed
        if self.space_freed < 1024:
            space_text = f"{self.space_freed:.1f} MB"
        else:
            space_text = f"{self.space_freed/1024:.2f} GB"
        self.space_label.value_label.config(text=space_text)
        
        # Update selected count
        self.update_selected_count()
        
    def cleaning_complete(self, cleaned_locations):
        self.is_cleaning = False
        self.clean_btn.config(state='normal', text="💎  Start VIP Cleaning")
        self.status_text.config(text="VIP Cleaning completed!")
        self.update_statistics()
        
        locations_text = "\n".join([f"✓ {loc}" for loc in cleaned_locations])
        
        messagebox.showinfo("VIP Cleaning Complete", 
                           f"💎 Successfully cleaned {self.files_cleaned} files!\n"
                           f"💎 Space freed: {self.space_freed:.2f} MB\n\n"
                           f"Cleaned Locations:\n{locations_text}")

def main():
    root = tk.Tk()
    app = VIPSystemCleaner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
