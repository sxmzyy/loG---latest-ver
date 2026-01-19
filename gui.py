# gui.py
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox
from config import (BG_COLOR, FG_COLOR, TEXT_BG_COLOR, TEXT_FG_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, FONT, LOG_TYPES,
                   PRIMARY_BG, SECONDARY_BG, PANEL_BG, TEXT_PRIMARY, TEXT_SECONDARY, HEADER_BG,
                   ACCENT_BLUE, ACCENT_LAVENDER, SUCCESS_GREEN, WARNING_ORANGE, ERROR_RED, INFO_CYAN)

def create_main_window():
    root = tk.Tk()
    root.title("Android Forensic Tool - Professional Edition")
    root.geometry("1200x750")
    root.configure(bg=PRIMARY_BG)
    return root

def setup_style(root):
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure("TNotebook", background=PRIMARY_BG, borderwidth=0)
    style.configure("TNotebook.Tab", 
                   background=SECONDARY_BG, 
                   foreground=TEXT_SECONDARY,
                   padding=[15, 8],
                   borderwidth=0)
    style.map("TNotebook.Tab", 
             background=[("selected", ACCENT_BLUE)],
             foreground=[("selected", "#11111b")])
    style.configure("TFrame", background=PRIMARY_BG)

def create_tabs(root):
    tab_control = ttk.Notebook(root)
    tabs = {}
    tabs["Extract"] = ttk.Frame(tab_control)
    tabs["ModernSMS"] = ttk.Frame(tab_control)  # NEW: Modern SMS view
    tabs["ModernCalls"] = ttk.Frame(tab_control)  # NEW: Modern Calls view
    tabs["ModernLocation"] = ttk.Frame(tab_control)  # NEW: Modern Location view
    tabs["Map"] = ttk.Frame(tab_control)  # NEW: Map view
    tabs["Live"] = ttk.Frame(tab_control)
    tabs["AllLogs"] = ttk.Frame(tab_control)
    tabs["Logcat"] = ttk.Frame(tab_control)
    tabs["LogcatTypes"] = ttk.Frame(tab_control)
    tabs["Filter"] = ttk.Frame(tab_control)
    tabs["Graphs"] = ttk.Frame(tab_control)
    tabs["Threats"] = ttk.Frame(tab_control)
    
    tab_control.add(tabs["Extract"], text="Extract Logs")
    tab_control.add(tabs["ModernSMS"], text="📨 SMS Messages")  # NEW
    tab_control.add(tabs["ModernCalls"], text="📞 Call Logs")  # NEW
    tab_control.add(tabs["ModernLocation"], text="📍 Location")  # NEW
    tab_control.add(tabs["Map"], text="🗺️ Map View")  # NEW
    tab_control.add(tabs["Live"], text="Live Monitoring")
    tab_control.add(tabs["AllLogs"], text="All Logs")
    tab_control.add(tabs["Logcat"], text="Logcat Logs")
    tab_control.add(tabs["LogcatTypes"], text="Logcat Types")
    tab_control.add(tabs["Filter"], text="Filter Logs")
    tab_control.add(tabs["Graphs"], text="Activity Graphs")
    tab_control.add(tabs["Threats"], text="🔒 Threat Detection")
    tab_control.pack(expand=1, fill="both")
    return tabs, tab_control

def create_widgets(tabs):
    widgets = {}
    widgets["output_text"] = scrolledtext.ScrolledText(tabs["Extract"], wrap=tk.WORD, bg=PRIMARY_BG, fg=TEXT_PRIMARY, font=FONT)
    widgets["output_text"].pack(fill=tk.BOTH, expand=True, pady=5)
    
    widgets["live_text"] = scrolledtext.ScrolledText(tabs["Live"], wrap=tk.WORD, bg=PRIMARY_BG, fg=TEXT_PRIMARY, font=FONT)
    widgets["live_text"].pack(fill=tk.BOTH, expand=True, pady=5)
    
    widgets["all_logs_text"] = scrolledtext.ScrolledText(tabs["AllLogs"], wrap=tk.WORD, bg=PRIMARY_BG, fg=TEXT_PRIMARY, font=FONT)
    widgets["all_logs_text"].pack(fill=tk.BOTH, expand=True, pady=5)
    
    widgets["logcat_text"] = scrolledtext.ScrolledText(tabs["Logcat"], wrap=tk.WORD, bg=PRIMARY_BG, fg=TEXT_PRIMARY, font=FONT)
    widgets["logcat_text"].pack(fill=tk.BOTH, expand=True, pady=5)
    
    # Build notebook for logcat types
    logcat_type_notebook = ttk.Notebook(tabs["LogcatTypes"])
    logcat_type_notebook.pack(expand=1, fill="both")
    widgets["logcat_type_notebook"] = logcat_type_notebook
    logcat_type_texts = {}
    for log_type in LOG_TYPES:
        frame = ttk.Frame(logcat_type_notebook)
        logcat_type_notebook.add(frame, text=log_type)
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, font=FONT)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=5)
        logcat_type_texts[log_type] = text_widget
    widgets["logcat_type_texts"] = logcat_type_texts
    
    # NEW: Map View
    try:
        import tkintermapview
        map_widget = tkintermapview.TkinterMapView(tabs["Map"], width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # Google Maps
        widgets["map_widget"] = map_widget
    except Exception as e:
        print(f"Map Import Error: {e}")
        tk.Label(tabs["Map"], text=f"Map Error: {e}", bg=PRIMARY_BG, fg="red").pack(pady=20)
        widgets["map_widget"] = None
    
    # NEW: Modern SMS and Call viewers
    from modern_viewers import ModernSMSViewer, ModernCallViewer, ModernLocationViewer
    
    widgets["modern_sms_viewer"] = ModernSMSViewer(tabs["ModernSMS"])
    widgets["modern_sms_viewer"].pack(fill=tk.BOTH, expand=True)
    
    widgets["modern_call_viewer"] = ModernCallViewer(tabs["ModernCalls"])
    widgets["modern_call_viewer"].pack(fill=tk.BOTH, expand=True)

    widgets["modern_location_viewer"] = ModernLocationViewer(tabs["ModernLocation"], map_widget=widgets.get("map_widget"))
    widgets["modern_location_viewer"].pack(fill=tk.BOTH, expand=True)
    
    # NEW: Threat Detection widget
    widgets["threat_text"] = scrolledtext.ScrolledText(tabs["Threats"], wrap=tk.WORD, bg=BG_COLOR, fg="#FF5555", font=FONT)
    widgets["threat_text"].pack(fill=tk.BOTH, expand=True, pady=5)
    widgets["threat_text"].insert(tk.END, "🔒 THREAT DETECTION MODULE\n\n")
    widgets["threat_text"].insert(tk.END, "Extract logs first, then click 'Scan for Threats' button.\n")
    widgets["threat_text"].config(state=tk.DISABLED)
    
    return widgets

def create_live_monitoring_buttons(tab_live):
    frame = tk.Frame(tab_live, bg=BG_COLOR)
    frame.pack(fill=tk.X, pady=5)
    start_btn = tk.Button(frame, text="Start Live Monitoring", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    start_btn.pack(side=tk.LEFT, padx=10)
    stop_btn = tk.Button(frame, text="Stop Live Monitoring", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    stop_btn.pack(side=tk.LEFT, padx=10)
    return start_btn, stop_btn

def create_graph_controls(tab_graphs):
    frame = tk.Frame(tab_graphs, bg="black")
    frame.pack(pady=10)
    tk.Label(frame, text="Select Time Range:", bg="black", fg="#00FF00").grid(row=0, column=0, padx=5)
    time_combo = ttk.Combobox(frame, values=["Past 1 Hour", "Past 24 Hours", "Past 7 Days", "All Time"])
    time_combo.set("Past 24 Hours")
    time_combo.grid(row=0, column=1, padx=5)
    
    tk.Label(frame, text="Log Type:", bg="black", fg="#00FF00").grid(row=0, column=2, padx=5)
    from config import LOG_TYPES
    graph_types = ["Call Logs", "SMS Logs", "Top SMS Senders", "Logcat Activity"] + list(LOG_TYPES.keys())
    logtype_combo = ttk.Combobox(frame, values=graph_types)
    logtype_combo.set("Call Logs")
    logtype_combo.grid(row=0, column=3, padx=5)
    
    graph_btn = tk.Button(frame, text="Generate Graph", bg="gray", fg="black")
    graph_btn.grid(row=0, column=4, padx=10)
    freq_btn = tk.Button(frame, text="Most Frequent Callers", bg="gray", fg="black")
    freq_btn.grid(row=0, column=5, padx=10)
    
    return {"time_combo": time_combo, "logtype_combo": logtype_combo, "graph_btn": graph_btn, "freq_btn": freq_btn}

def create_filter_controls(tab_filter):
    frame = tk.Frame(tab_filter, bg=BG_COLOR)
    frame.pack(fill=tk.X, pady=10)
    
    tk.Label(frame, text="Log Type", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=0, column=0, padx=5, pady=5)
    from config import LOG_TYPES
    filter_types = ["Logcat", "Calls", "SMS"] + list(LOG_TYPES.keys())
    logtype_combo = ttk.Combobox(frame, values=filter_types, width=15)
    logtype_combo.set("Logcat")
    logtype_combo.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Time Range", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=0, column=2, padx=5, pady=5)
    time_combo = ttk.Combobox(frame, values=["Past 1 Hour", "Past 24 Hours", "Past 7 Days", "All Time"], width=15)
    time_combo.set("Past 24 Hours")
    time_combo.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(frame, text="Keyword", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=1, column=0, padx=5, pady=5)
    keyword_entry = tk.Entry(frame, width=30)
    keyword_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
    
    tk.Label(frame, text="Sub-Type", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=1, column=3, padx=5, pady=5)
    subtype_combo = ttk.Combobox(frame, values=["All"], width=15)
    subtype_combo.set("All")
    subtype_combo.grid(row=1, column=4, padx=5, pady=5)
    
    tk.Label(frame, text="Severity", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=0, column=4, padx=5, pady=5)
    severity_combo = ttk.Combobox(frame, values=["All", "Error", "Warning", "Info", "Debug", "Verbose"], width=15)
    severity_combo.set("All")
    severity_combo.grid(row=0, column=5, padx=5, pady=5)
    
    apply_btn = tk.Button(frame, text="Apply Filter", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    apply_btn.grid(row=2, column=1, padx=5, pady=5)
    save_btn = tk.Button(frame, text="Save Filtered Logs", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    save_btn.grid(row=2, column=2, padx=5, pady=5)
    
    return {"logtype": logtype_combo, "time": time_combo, "keyword": keyword_entry,
            "subtype": subtype_combo, "severity": severity_combo, "apply": apply_btn, "save": save_btn}

def create_filter_output(tab_filter):
    filter_output = scrolledtext.ScrolledText(tab_filter, width=80, height=25, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, font=FONT)
    filter_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    return filter_output

def create_export_frame(root):
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
    btn_full = tk.Button(frame, text="Export Full Report", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_png = tk.Button(frame, text="Export Current Graph (PNG)", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_pdf = tk.Button(frame, text="Export Current Graph (PDF)", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_csv = tk.Button(frame, text="Export Current Graph Data (CSV)", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_full.pack(side=tk.LEFT, padx=10)
    btn_png.pack(side=tk.LEFT, padx=10)
    btn_pdf.pack(side=tk.LEFT, padx=10)
    btn_csv.pack(side=tk.LEFT, padx=10)
    return {"full": btn_full, "png": btn_png, "pdf": btn_pdf, "csv": btn_csv}

def create_menu(root, notebook):
    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    
    file_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Import Logs", command=lambda: None)
    file_menu.add_command(label="Export Full Report", command=lambda: None)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    graph_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="Visualize", menu=graph_menu)
    graph_menu.add_command(label="Graph Call Logs", command=lambda: None)
    graph_menu.add_command(label="Graph SMS Logs", command=lambda: None)
    graph_menu.add_command(label="Graph Logcat Data", command=lambda: None)
    
    analysis_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="Analysis", menu=analysis_menu)
    analysis_menu.add_command(label="Call Log Analysis", command=lambda: notebook.select(0))
    analysis_menu.add_command(label="SMS Analysis", command=lambda: notebook.select(1))
    analysis_menu.add_command(label="Logcat Analysis", command=lambda: notebook.select(2))
    analysis_menu.add_command(label="Advanced Filter", command=lambda: notebook.select(3))
    
    help_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", 
                    "Android Forensic Analyzer v1.0\nDeveloped for digital forensic analysis of Android logs."))
    help_menu.add_command(label="Documentation", command=lambda: messagebox.showinfo("Documentation", 
                    "Please refer to the README.md file for detailed documentation."))
    
    return main_menu
