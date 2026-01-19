"""
modern_viewers.py - Modern table viewers for SMS and Call logs
"""

import tkinter as tk
from tkinter import ttk
import os
from config import *


class ModernSMSViewer(tk.Frame):
    """Professional SMS viewer with table and search."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=PRIMARY_BG)
        self.sms_data = []
        self.filtered_data = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create viewer UI."""
        # Header
        header = tk.Frame(self, bg=HEADER_BG, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="📨 SMS Messages", bg=HEADER_BG, 
                        fg=ACCENT_BLUE, font=('Segoe UI', 16, 'bold'))
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Stats
        self.stats_label = tk.Label(header, text="Total: 0", bg=HEADER_BG,
                                    fg=TEXT_SECONDARY, font=('Segoe UI', 10))
        self.stats_label.pack(side=tk.LEFT, padx=20)
        
        # Search bar
        search_frame = tk.Frame(self, bg=SECONDARY_BG, height=50)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        search_frame.pack_propagate(False)
        
        tk.Label(search_frame, text="🔍", bg=SECONDARY_BG, fg=TEXT_SECONDARY,
                font=('Segoe UI', 12)).pack(side=tk.LEFT, padx=(15, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.do_search())
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg=PANEL_BG, fg=TEXT_PRIMARY, relief=tk.FLAT,
                               font=('Segoe UI', 10), width=50)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        
        # Table
        table_frame = tk.Frame(self, bg=PRIMARY_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ('type', 'contact', 'date', 'time', 'message')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                yscrollcommand=vsb.set, selectmode='browse')
        
        self.tree.heading('type', text='Type')
        self.tree.heading('contact', text='Contact')
        self.tree.heading('date', text='Date')
        self.tree.heading('time', text='Time')
        self.tree.heading('message', text='Message')
        
        self.tree.column('type', width=80, minwidth=80)
        self.tree.column('contact', width=150, minwidth=100)
        self.tree.column('date', width=100, minwidth=80)
        self.tree.column('time', width=80, minwidth=60)
        self.tree.column('message', width=400, minwidth=200)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.config(command=self.tree.yview)
        
        # Apply styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=PANEL_BG, foreground=TEXT_PRIMARY,
                       fieldbackground=PANEL_BG, borderwidth=0, font=('Segoe UI', 9))
        style.configure("Treeview.Heading", background=HEADER_BG, foreground=ACCENT_BLUE,
                       borderwidth=1, font=('Segoe UI', 9, 'bold'))
        style.map('Treeview', background=[('selected', ACCENT_BLUE)],
                 foreground=[('selected', '#11111b')])
    
    def load_data(self, sms_records):
        """Load SMS data into table."""
        self.sms_data = sms_records
        self.filtered_data = sms_records
        self.refresh_table()
        self.update_stats()
    
    def refresh_table(self):
        """Refresh table display."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for record in self.filtered_data:
            self.tree.insert('', tk.END, values=(
                record.get('type', ''),
                record.get('contact', ''),
                record.get('date', ''),
                record.get('time', ''),
                record.get('message', '')[:100]  # Limit message length
            ))
    
    def do_search(self):
        """Filter data based on search query."""
        query = self.search_var.get().lower()
        
        if not query:
            self.filtered_data = self.sms_data
        else:
            self.filtered_data = [
                r for r in self.sms_data
                if query in str(r.get('contact', '')).lower() or
                   query in str(r.get('message', '')).lower() or
                   query in str(r.get('date', '')).lower()
            ]
        
        self.refresh_table()
        self.update_stats()
    
    def update_stats(self):
        """Update statistics label."""
        total = len(self.filtered_data)
        received = sum(1 for r in self.filtered_data if r.get('type') == 'Received')
        sent = sum(1 for r in self.filtered_data if r.get('type') == 'Sent')
        self.stats_label.config(text=f"Total: {total}  |  Received: {received}  |  Sent: {sent}")


class ModernCallViewer(tk.Frame):
    """Professional call log viewer with table and search."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=PRIMARY_BG)
        self.call_data = []
        self.filtered_data = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create viewer UI."""
        # Header
        header = tk.Frame(self, bg=HEADER_BG, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="📞 Call Logs", bg=HEADER_BG,
                        fg=ACCENT_BLUE, font=('Segoe UI', 16, 'bold'))
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Stats
        self.stats_label = tk.Label(header, text="Total: 0", bg=HEADER_BG,
                                    fg=TEXT_SECONDARY, font=('Segoe UI', 10))
        self.stats_label.pack(side=tk.LEFT, padx=20)
        
        # Search bar
        search_frame = tk.Frame(self, bg=SECONDARY_BG, height=50)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        search_frame.pack_propagate(False)
        
        tk.Label(search_frame, text="🔍", bg=SECONDARY_BG, fg=TEXT_SECONDARY,
                font=('Segoe UI', 12)).pack(side=tk.LEFT, padx=(15, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.do_search())
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg=PANEL_BG, fg=TEXT_PRIMARY, relief=tk.FLAT,
                               font=('Segoe UI', 10), width=50)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        
        # Table
        table_frame = tk.Frame(self, bg=PRIMARY_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ('type', 'contact', 'date', 'time', 'duration')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                yscrollcommand=vsb.set, selectmode='browse')
        
        self.tree.heading('type', text='Call Type')
        self.tree.heading('contact', text='Contact')
        self.tree.heading('date', text='Date')
        self.tree.heading('time', text='Time')
        self.tree.heading('duration', text='Duration')
        
        self.tree.column('type', width=100, minwidth=80)
        self.tree.column('contact', width=200, minwidth=150)
        self.tree.column('date', width=100, minwidth=80)
        self.tree.column('time', width=80, minwidth=60)
        self.tree.column('duration', width=80, minwidth=60)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.config(command=self.tree.yview)
        
        # Apply styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=PANEL_BG, foreground=TEXT_PRIMARY,
                       fieldbackground=PANEL_BG, borderwidth=0, font=('Segoe UI', 9))
        style.configure("Treeview.Heading", background=HEADER_BG, foreground=ACCENT_BLUE,
                       borderwidth=1, font=('Segoe UI', 9, 'bold'))
        style.map('Treeview', background=[('selected', ACCENT_BLUE)],
                 foreground=[('selected', '#11111b')])
    
    def load_data(self, call_records):
        """Load call data into table."""
        self.call_data = call_records
        self.filtered_data = call_records
        self.refresh_table()
        self.update_stats()
    
    def refresh_table(self):
        """Refresh table display."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for record in self.filtered_data:
            self.tree.insert('', tk.END, values=(
                record.get('type', ''),
                record.get('contact', ''),
                record.get('date', ''),
                record.get('time', ''),
                record.get('duration', '')
            ))
    
    def do_search(self):
        """Filter data based on search query."""
        query = self.search_var.get().lower()
        
        if not query:
            self.filtered_data = self.call_data
        else:
            self.filtered_data = [
                r for r in self.call_data
                if query in str(r.get('contact', '')).lower() or
                   query in str(r.get('type', '')).lower() or
                   query in str(r.get('date', '')).lower()
            ]
        
        self.refresh_table()
        self.update_stats()
    
    def update_stats(self):
        """Update statistics label."""
        total = len(self.filtered_data)
        incoming = sum(1 for r in self.filtered_data if r.get('type') == 'Incoming')
        outgoing = sum(1 for r in self.filtered_data if r.get('type') == 'Outgoing')
        missed = sum(1 for r in self.filtered_data if r.get('type') == 'Missed')
        self.stats_label.config(
            text=f"Total: {total}  |  Incoming: {incoming}  |  Outgoing: {outgoing}  |  Missed: {missed}"
        )


class ModernLocationViewer(tk.Frame):
    """Professional location viewer with table and search."""
    
    def __init__(self, parent, map_widget=None):
        super().__init__(parent, bg=PRIMARY_BG)
        self.location_data = []
        self.filtered_data = []
        self.map_widget = map_widget
        self.create_widgets()
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def create_widgets(self):
        """Create viewer UI."""
        # Header
        header = tk.Frame(self, bg=HEADER_BG, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="📍 Location History", bg=HEADER_BG,
                        fg=ACCENT_BLUE, font=('Segoe UI', 16, 'bold'))
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Stats
        self.stats_label = tk.Label(header, text="Total: 0", bg=HEADER_BG,
                                    fg=TEXT_SECONDARY, font=('Segoe UI', 10))
        self.stats_label.pack(side=tk.LEFT, padx=20)
        
        # Info Label
        tk.Label(header, text="ℹ️ Coordinates may be redacted by OS", bg=HEADER_BG,
                 fg=WARNING_ORANGE, font=('Segoe UI', 9, 'italic')).pack(side=tk.RIGHT, padx=20)
        
        # Launch Maps Button
        btn_maps = tk.Button(header, text="🚀 Launch Maps to Refresh", bg=ACCENT_BLUE, fg="white",
                             font=('Segoe UI', 9, 'bold'), relief=tk.FLAT,
                             command=self.launch_maps)
        btn_maps.pack(side=tk.RIGHT, padx=5)
        
        # Search bar
        search_frame = tk.Frame(self, bg=SECONDARY_BG, height=50)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        search_frame.pack_propagate(False)
        
        tk.Label(search_frame, text="🔍", bg=SECONDARY_BG, fg=TEXT_SECONDARY,
                font=('Segoe UI', 12)).pack(side=tk.LEFT, padx=(15, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.do_search())
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg=PANEL_BG, fg=TEXT_PRIMARY, relief=tk.FLAT,
                               font=('Segoe UI', 10), width=50)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        
        # Table
        table_frame = tk.Frame(self, bg=PRIMARY_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ('time', 'provider', 'context', 'lat', 'lon', 'accuracy')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                yscrollcommand=vsb.set, selectmode='browse')
        
        self.tree.heading('time', text='Time')
        self.tree.heading('provider', text='Provider')
        self.tree.heading('context', text='Context / App')
        self.tree.heading('lat', text='Latitude')
        self.tree.heading('lon', text='Longitude')
        self.tree.heading('accuracy', text='Accuracy')
        
        self.tree.column('time', width=150, minwidth=120)
        self.tree.column('provider', width=100, minwidth=80)
        self.tree.column('context', width=200, minwidth=150)
        self.tree.column('lat', width=100, minwidth=80)
        self.tree.column('lon', width=100, minwidth=80)
        self.tree.column('accuracy', width=80, minwidth=60)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.config(command=self.tree.yview)
        
        # Apply styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=PANEL_BG, foreground=TEXT_PRIMARY,
                       fieldbackground=PANEL_BG, borderwidth=0, font=('Segoe UI', 9))
        style.configure("Treeview.Heading", background=HEADER_BG, foreground=ACCENT_BLUE,
                       borderwidth=1, font=('Segoe UI', 9, 'bold'))
        style.map('Treeview', background=[('selected', ACCENT_BLUE)],
                 foreground=[('selected', '#11111b')])
    
    def load_data(self, location_records):
        """Load location data into table."""
        self.location_data = location_records
        self.filtered_data = location_records
        self.refresh_table()
        self.update_stats()
    
    def refresh_table(self):
        """Refresh table display."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for record in self.filtered_data:
            self.tree.insert('', tk.END, values=(
                record.get('time', ''),
                record.get('provider', ''),
                record.get('context', ''),
                record.get('latitude', ''),
                record.get('longitude', ''),
                record.get('accuracy', '')
            ))
    
    def do_search(self):
        """Filter data based on search query."""
        query = self.search_var.get().lower()
        
        if not query:
            self.filtered_data = self.location_data
        else:
            self.filtered_data = [
                r for r in self.location_data
                if query in str(r.get('provider', '')).lower() or
                   query in str(r.get('time', '')).lower() or
                   query in str(r.get('context', '')).lower()
            ]
        
        self.refresh_table()
        self.update_stats()
    
    def update_stats(self):
        """Update statistics label."""
        total = len(self.filtered_data)
        gps = sum(1 for r in self.filtered_data if 'gps' in str(r.get('provider', '')).lower())
        network = sum(1 for r in self.filtered_data if 'network' in str(r.get('provider', '')).lower())
        self.stats_label.config(
            text=f"Total: {total}  |  GPS: {gps}  |  Network: {network}"
        )

    def launch_maps(self):
        """Launch Google Maps to trigger location update."""
        from scripts.android_logs import trigger_location_update
        from tkinter import messagebox
        
        if trigger_location_update():
            messagebox.showinfo("Location Update", 
                "🚀 Google Maps launched!\n\n"
                "1. Unlock your device if needed.\n"
                "2. Wait a few seconds for location to fix.\n"
                "3. Click 'Extract Logs' again to see new data.")
        else:
            messagebox.showerror("Error", "Failed to launch Google Maps. Check ADB connection.")

    def on_select(self, event):
        """Handle row selection to update map."""
        if not self.map_widget:
            return
            
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        item = selected_items[0]
        values = self.tree.item(item, 'values')
        # values: (time, provider, context, lat, lon, accuracy)
        
        try:
            lat_str = values[3]
            lon_str = values[4]
            
            if lat_str == "Request" or lon_str == "Request":
                return
                
            lat = float(lat_str)
            lon = float(lon_str)
            
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_marker(lat, lon, text=f"Time: {values[0]}")
            self.map_widget.set_zoom(15)
        except (ValueError, IndexError):
            pass
