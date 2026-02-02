import tkinter as tk  # <-- Added so we can reference tk.END, tk.* etc.
import re
from datetime import datetime, timedelta
import os
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
import threading

def filter_logs(input_file, keyword=None, time_range=None, severity=None, subtype=None, output_file="logs/filtered_logs.txt"):
    try:
        # Check if the input file exists; if not, create an empty one to avoid errors.
        if not os.path.exists(input_file):
            with open(input_file, "w", encoding="utf-8") as f_temp:
                f_temp.write("")
        with open(input_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        now = datetime.now()
        filtered_lines = []
        
        # PERFORMANCE: Pre-compile patterns once
        severity_patterns = {
            "Error": re.compile(r'E/|ERROR|Exception|FATAL', re.IGNORECASE),
            "Warning": re.compile(r'W/|WARN|WARNING', re.IGNORECASE),
            "Info": re.compile(r'I/|INFO', re.IGNORECASE),
            "Debug": re.compile(r'D/|DEBUG', re.IGNORECASE),
            "Verbose": re.compile(r'V/|VERBOSE', re.IGNORECASE)
        }
        
        subtype_patterns = {
            "Activity": re.compile(r'Activity|startActivity', re.IGNORECASE),
            "Fragment": re.compile(r'Fragment', re.IGNORECASE),
            "View": re.compile(r'View|Inflate', re.IGNORECASE),
            "Lifecycle": re.compile(r'onCreate|onStart|onResume|onPause|onStop|onDestroy', re.IGNORECASE),
            
            "Boot": re.compile(r'boot|start up|startup|starting', re.IGNORECASE),
            "Memory": re.compile(r'memory|heap|ram', re.IGNORECASE),
            "CPU": re.compile(r'cpu|processor', re.IGNORECASE),
            "Battery": re.compile(r'battery|power', re.IGNORECASE),
            
            "NullPointer": re.compile(r'NullPointerException', re.IGNORECASE),
            "OutOfMemory": re.compile(r'OutOfMemoryError', re.IGNORECASE),
            "IllegalState": re.compile(r'IllegalStateException', re.IGNORECASE),
            "ANR": re.compile(r'ANR|Not Responding', re.IGNORECASE),
            
            "WiFi": re.compile(r'wifi|wlan', re.IGNORECASE),
            "Mobile": re.compile(r'mobile|cellular|data connection', re.IGNORECASE),
            "HTTP": re.compile(r'http|https|URL', re.IGNORECASE),
            "Socket": re.compile(r'socket|tcp|udp', re.IGNORECASE),
            
            "Dalvik GC": re.compile(r'dalvikvm.*GC', re.IGNORECASE),
            "ART GC": re.compile(r'art.*GC', re.IGNORECASE),
            "Explicit GC": re.compile(r'Explicit GC', re.IGNORECASE),
            "Concurrent GC": re.compile(r'Concurrent GC', re.IGNORECASE),
            
            "System": re.compile(r'android\.intent\.action|system broadcast', re.IGNORECASE),
            "App": re.compile(r'com\.', re.IGNORECASE),
            "Sticky": re.compile(r'sticky|registerReceiver', re.IGNORECASE),
            "Ordered": re.compile(r'ordered broadcast', re.IGNORECASE),
            
            "Start": re.compile(r'startService', re.IGNORECASE),
            "Stop": re.compile(r'stopService', re.IGNORECASE),
            "Bind": re.compile(r'bindService|onBind', re.IGNORECASE),
            "Unbind": re.compile(r'unbindService|onUnbind', re.IGNORECASE),
            
            "Power": re.compile(r'power|PowerManager|wake|sleep', re.IGNORECASE),
            "Sensor": re.compile(r'sensor|Sensor', re.IGNORECASE),
            "Camera": re.compile(r'camera|Camera', re.IGNORECASE),
            "Location": re.compile(r'location|LocationManager|GPS', re.IGNORECASE)
        }
        
        for line in lines:
            include = True
            
            # Apply time filter
            if time_range and time_range != "All Time":
                date_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                unix_match = re.search(r'date=(\d+)', line)
                logcat_match = re.search(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                
                has_timestamp = False
                if date_match:
                    try:
                        ts = datetime.strptime(date_match.group(), "%Y-%m-%d %H:%M:%S")
                        has_timestamp = True
                    except:
                        pass
                elif unix_match:
                    try:
                        ts = datetime.fromtimestamp(int(unix_match.group(1)) / 1000)
                        has_timestamp = True
                    except:
                        pass
                elif logcat_match:
                    try:
                        today = datetime.now()
                        date_str = f"{today.year}-{logcat_match.group(1)}"
                        ts = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        if ts > today:
                            ts = ts.replace(year=today.year - 1)
                        has_timestamp = True
                    except:
                        pass
                
                if has_timestamp:
                    if time_range == "Past 1 Hour" and (now - ts) > timedelta(hours=1):
                        include = False
                    elif time_range == "Past 24 Hours" and (now - ts) > timedelta(hours=24):
                        include = False
                    elif time_range == "Past 7 Days" and (now - ts) > timedelta(days=7):
                        include = False
            
            # Apply keyword filter
            if include and keyword and keyword.strip():
                if keyword.lower() not in line.lower():
                    include = False
            
            # Apply severity filter (using compiled patterns)
            if include and severity and severity != "All":
                pattern = severity_patterns.get(severity)
                if pattern and not pattern.search(line):
                    include = False
            
            # Apply subtype filter (using compiled patterns)
            if include and subtype and subtype != "All":
                pattern = subtype_patterns.get(subtype)
                if pattern and not pattern.search(line):
                    include = False
            
            if include:
                filtered_lines.append(line)
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(filtered_lines)
        
        return len(filtered_lines)
    
    except Exception as e:
        print(f"Error filtering logs: {e}")
        raise

def load_filtered_logs(filter_output_widget):
    try:
        # We reference tk here
        filter_output_widget.delete(1.0, tk.END)
        
        # Check if the filtered log file exists; if not, notify the user gracefully.
        if not os.path.exists("logs/filtered_logs.txt"):
            filter_output_widget.insert(tk.END, "No logs match the selected filters.\n")
            return
        
        with open("logs/filtered_logs.txt", "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            
        if not lines:
            filter_output_widget.insert(tk.END, "No logs match the selected filters.\n")
            return
        
        # Show lines
        for i, line in enumerate(lines):
            filter_output_widget.insert(tk.END, f"{i+1}: {line}")
        
        filter_output_widget.insert(tk.END, f"\n\n✅ Found {len(lines)} matching log entries.\n")
    except Exception as e:
        filter_output_widget.delete(1.0, tk.END)
        filter_output_widget.insert(tk.END, f"❌ Error loading filtered logs: {str(e)}\n")

def save_filtered_logs():
    from tkinter import filedialog, messagebox
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Filtered Logs"
        )
        
        if not file_path:
            return
        
        with open("logs/filtered_logs.txt", "r", encoding="utf-8", errors="replace") as src_file:
            with open(file_path, "w", encoding="utf-8") as dst_file:
                dst_file.write(src_file.read())
                
        messagebox.showinfo("Save Successful", f"Filtered logs saved to {file_path}")
    
    except Exception as e:
        messagebox.showerror("Save Failed", f"Failed to save filtered logs: {str(e)}")
