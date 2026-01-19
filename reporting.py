import os
import re
from datetime import datetime
from collections import Counter
from tkinter import messagebox
from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys

# Fix Windows encoding issues with emoji characters
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Make weasyprint optional (requires GTK on Windows which can be difficult to install)
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"⚠️  WeasyPrint not available: {e}")
    print("   PDF export will be disabled. HTML export will still work.")

def get_todays_logs(log_lines):
    """Filters log entries to include only those from the current day."""
    today_str = datetime.now().strftime("%m-%d")
    todays_logs = []
    for line in log_lines:
        # Check if the line starts with the month-day format (e.g., "08-26")
        if line.strip().startswith(today_str):
            todays_logs.append(line)
    return todays_logs

def _load_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()

def _summarize_calls():
    lines = _load_lines("logs/call_logs.txt")
    incoming = sum(1 for line in lines if re.search(r'type:\s*1|INCOMING', line, re.IGNORECASE))
    outgoing = sum(1 for line in lines if re.search(r'type:\s*2|OUTGOING', line, re.IGNORECASE))
    missed = sum(1 for line in lines if re.search(r'type:\s*3|MISSED', line, re.IGNORECASE))
    numbers = []
    for line in lines:
        match = re.search(r'(?:number=|from:|to:)\s*(\+?\d+)', line, re.IGNORECASE)
        if match:
            numbers.append(match.group(1))
    top_callers = Counter(numbers).most_common(5)
    return {
        "total": len(lines),
        "incoming": incoming,
        "outgoing": outgoing,
        "missed": missed,
        "top_callers": top_callers,
    }

def _summarize_sms():
    lines = _load_lines("logs/sms_logs.txt")
    incoming = sum(1 for line in lines if re.search(r'type:\s*1|INCOMING|from:', line, re.IGNORECASE))
    outgoing = sum(1 for line in lines if re.search(r'type:\s*2|OUTGOING|to:', line, re.IGNORECASE))
    senders = []
    for line in lines:
        match = re.search(r'from:\s*(\+?\d+)', line, re.IGNORECASE)
        if match:
            senders.append(match.group(1))
    top_senders = Counter(senders).most_common(5)
    return {
        "total": len(lines),
        "incoming": incoming,
        "outgoing": outgoing,
        "top_senders": top_senders,
    }

def _summarize_logcat():
    lines = _load_lines("logs/android_logcat.txt")
    todays = get_todays_logs(lines)
    recent = todays[:50] if todays else lines[:50]
    return {
        "total": len(lines),
        "recent_sample": [line.strip() for line in recent],
        "recent_label": "Today" if todays else "Recent",
    }

def _collect_context():
    now = datetime.now()
    device_info = {
        "model": "Unknown",
        "android_version": "Unknown",
        "kernel": "Unknown",
    }
    raw_log = "".join(_load_lines("logs/android_logcat.txt"))
    model_match = re.search(r'model=([^,\s]+)', raw_log)
    if model_match:
        device_info["model"] = model_match.group(1)
    version_matches = re.findall(r'Android\s+(\d+(?:\.\d+)?)', raw_log)
    for ver in version_matches:
        try:
            if float(ver) < 15:
                device_info["android_version"] = ver
                break
        except ValueError:
            continue
    kernel_match = re.search(r'Linux\s+version\s+([^\s]+)', raw_log)
    if kernel_match:
        device_info["kernel"] = kernel_match.group(1)

    return {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "case_number": "123456",
        "examiner": "Digital Forensic Analyst",
        "device": device_info,
        "calls": _summarize_calls(),
        "sms": _summarize_sms(),
        "logcat": _summarize_logcat(),
        "chain_of_custody": [
            "Evidence acquired from the Android device using approved ADB tools.",
            "Logs extracted include Android Logcat, Call Logs, and SMS Logs.",
            "Files verified with cryptographic hashes immediately after acquisition.",
            "Analysis steps documented to preserve chain-of-custody integrity.",
        ],
        "methodology": [
            "ADB-based acquisition of logcat, call, and SMS datasets.",
            "Filtering by time range, keyword, severity, and subtype for targeted review.",
            "Visualization of temporal activity and frequency distributions.",
            "Threat triage and report packaging for court-ready evidence.",
        ],
    }

def _render_html(context):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(
        loader=FileSystemLoader(os.path.join(base_dir, "templates")),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("report_template.html")
    return template.render(**context)

def export_full_report():
    try:
        os.makedirs("logs/exports", exist_ok=True)
        context = _collect_context()
        html = _render_html(context)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if WEASYPRINT_AVAILABLE:
            # Export as PDF
            filepath = f"logs/exports/forensic_report_{timestamp}.pdf"
            HTML(string=html, base_url=os.path.abspath(".")).write_pdf(filepath)
            messagebox.showinfo("Report Generated", f"Forensic report exported to {filepath}")
        else:
            # Fallback to HTML export
            filepath = f"logs/exports/forensic_report_{timestamp}.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            messagebox.showinfo("Report Generated", 
                f"Forensic report exported to {filepath}\n\n"
                "Note: PDF export unavailable. Install GTK libraries for PDF support.")
    except Exception as e:
        messagebox.showerror("Report Generation Failed", f"Failed to generate report: {str(e)}")
