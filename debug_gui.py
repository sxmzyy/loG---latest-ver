import tkinter as tk
from tkinter import ttk
import gui
print(f"GUI File: {gui.__file__}")

root = tk.Tk()
tabs = {}
tab_control = ttk.Notebook(root)
tabs["Extract"] = ttk.Frame(tab_control)
tabs["ModernSMS"] = ttk.Frame(tab_control)
tabs["ModernCalls"] = ttk.Frame(tab_control)
tabs["ModernLocation"] = ttk.Frame(tab_control)
tabs["Map"] = ttk.Frame(tab_control)
tabs["Live"] = ttk.Frame(tab_control)
tabs["AllLogs"] = ttk.Frame(tab_control)
tabs["Logcat"] = ttk.Frame(tab_control)
tabs["LogcatTypes"] = ttk.Frame(tab_control)
tabs["Filter"] = ttk.Frame(tab_control)
tabs["Graphs"] = ttk.Frame(tab_control)
tabs["Threats"] = ttk.Frame(tab_control)

print("Calling create_widgets...")
try:
    gui.create_widgets(tabs)
    print("create_widgets completed")
except Exception as e:
    print(f"Error in create_widgets: {e}")

root.destroy()
