# Python Module Documentation

Complete documentation for all Python modules in the Android Forensic Tool.

---

## 📁 Core Modules

### `main.py` - Application Entry Point

**Purpose**: Main entry point that initializes the GUI and orchestrates all components.

**Key Functions**:

| Function | Description |
|----------|-------------|
| `categorize_logcat_logs()` | Categorizes logcat entries into sub-tabs based on log type |
| `extract_logs()` | Extracts all log types from connected Android device |
| `extract_logs_threaded()` | Thread wrapper for `extract_logs()` to prevent GUI freezing |
| `apply_filter()` | Applies keyword/time/severity filters to logs |
| `update_live_monitor(log)` | Updates live monitoring widget with new log entry |
| `process_log_queue()` | Processes queued log entries for GUI display |

**Usage**:
```bash
python main.py
```

---

### `config.py` - Configuration Settings

**Purpose**: Central configuration for theme colors, log types, and regex patterns.

**Key Constants**:

| Constant | Description | Example |
|----------|-------------|---------|
| `PRIMARY_BG` | Main background color | `#1e1e2e` |
| `ACCENT_BLUE` | Primary accent color | `#89b4fa` |
| `LOG_TYPES` | Dictionary of log type patterns | See below |
| `COMPILED_LOG_PATTERNS` | Pre-compiled regex for performance | Auto-generated |

**Log Types Configuration**:
```python
LOG_TYPES = {
    "Application": {
        "description": "Application-specific logs",
        "pattern": r'ActivityManager|PackageManager|ApplicationContext',
        "color": "blue"
    },
    "System": {
        "description": "System-level logs",
        "pattern": r'SystemServer|System\.err|...',
        "color": "green"
    },
    # ... 8 total log types
}
```

**Shared State**:
- `monitoring_active`: Boolean flag for live monitoring state
- `log_queue`: Queue for thread-safe log updates

---

### `gui.py` - GUI Components

**Purpose**: Creates and manages all Tkinter GUI components.

**Key Functions**:

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `create_main_window()` | None | `tk.Tk` | Creates root window with title |
| `setup_style(root)` | root: `tk.Tk` | None | Configures ttk styles |
| `create_tabs(root)` | root: `tk.Tk` | `dict` | Creates notebook with all tabs |
| `create_widgets(tabs)` | tabs: `dict` | `dict` | Creates text widgets for each tab |
| `create_live_monitoring_buttons(tab)` | tab: widget | `dict` | Start/Stop monitoring buttons |
| `create_graph_controls(tab)` | tab: widget | `dict` | Graph type and time range controls |
| `create_filter_controls(tab)` | tab: widget | `dict` | Filter input controls |
| `create_export_frame(root)` | root: `tk.Tk` | `dict` | Export buttons frame |
| `create_menu(root, notebook)` | root, notebook | None | Application menu bar |

**Tab Structure**:
```
├── Extract      - Log extraction
├── Call Logs    - Call history viewer
├── SMS          - SMS message viewer
├── Location     - Location data viewer
├── Logcat       - Raw logcat viewer
├── Filter       - Log filtering
├── Graphs       - Data visualization
├── Live Monitor - Real-time log stream
└── Threats      - Threat analysis
```

---

### `device_interface.py` - Device Abstraction

**Purpose**: Abstract base class defining the interface for device implementations.

**Class**: `DeviceInterface(ABC)`

| Method | Returns | Description |
|--------|---------|-------------|
| `detect_device()` | `bool` | Check if device is connected |
| `get_device_info()` | `dict` | Get model, OS version |
| `extract_system_logs(path)` | `bool` | Extract system logs |
| `extract_crash_reports(dir)` | `bool` | Extract crash reports |
| `get_platform()` | `str` | Get platform name |

**Helper Functions**:

| Function | Returns | Description |
|----------|---------|-------------|
| `detect_connected_devices()` | `List[DeviceInterface]` | Auto-detect all connected devices |
| `get_primary_device()` | `DeviceInterface \| None` | Get first connected device |

---

### `android_device.py` - Android Implementation

**Purpose**: Concrete implementation of `DeviceInterface` for Android devices.

**Class**: `AndroidDevice(DeviceInterface)`

| Method | Returns | Description |
|--------|---------|-------------|
| `detect_device()` | `bool` | Check ADB connection via `adb devices` |
| `get_device_info()` | `dict` | Model, Android version, device ID |
| `extract_system_logs(path)` | `bool` | Extract logcat to file |
| `extract_crash_reports(dir)` | `bool` | Extract crash reports |
| `extract_call_logs()` | `bool` | Extract call history |
| `extract_sms_logs()` | `bool` | Extract SMS messages |

**Dependencies**:
- `scripts/android_logs.py` - Low-level ADB commands
- `scripts/detect_log_buffer.py` - Buffer detection

---

## 📁 Processing Modules

### `filtering.py` - Log Filtering Engine

**Purpose**: Advanced log filtering with multiple criteria.

**Key Functions**:

| Function | Parameters | Description |
|----------|------------|-------------|
| `filter_logs(...)` | input_file, keyword, time_range, severity, subtype, output_file | Main filtering function |
| `load_filtered_logs(widget)` | filter_output_widget | Load filtered logs into display |
| `save_filtered_logs()` | None | Save filtered logs to file |

**Filter Criteria**:
- **Keyword**: Text search (case-insensitive)
- **Time Range**: 1 Hour, 24 Hours, 7 Days, All Time
- **Severity**: V(erbose), D(ebug), I(nfo), W(arning), E(rror), F(atal)
- **Subtype**: Application, System, Crash, GC, Network, etc.

---

### `parsers.py` - Log Format Parsers

**Purpose**: Parse raw log data into structured records.

**Functions**:

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `parse_sms_logs(content)` | Raw SMS log | `List[dict]` | Parse SMS records |
| `parse_call_logs(content)` | Raw call log | `List[dict]` | Parse call records |
| `parse_location_logs(content)` | Dumpsys location | `List[dict]` | Parse location data |

**SMS Record Structure**:
```python
{
    'contact': str,    # Phone number
    'date': str,       # YYYY-MM-DD
    'time': str,       # HH:MM:SS
    'type': str,       # 'Sent' or 'Received'
    'message': str     # Message body
}
```

**Call Record Structure**:
```python
{
    'contact': str,    # Phone number
    'date': str,       # YYYY-MM-DD
    'time': str,       # HH:MM:SS
    'duration': str,   # M:SS format
    'type': str        # 'Incoming', 'Outgoing', 'Missed'
}
```

**Location Record Structure**:
```python
{
    'provider': str,   # 'gps', 'network', 'fused'
    'latitude': str,
    'longitude': str,
    'accuracy': str,   # e.g., '10m'
    'time': str,       # Timestamp
    'context': str,    # Additional context
    'raw': str         # First 100 chars of raw line
}
```

---

### `graphing.py` - Data Visualization

**Purpose**: Generate charts and graphs for log analysis.

**Functions**:

| Function | Parameters | Description |
|----------|------------|-------------|
| `get_timestamps_from_file(filepath)` | Log file path | Extract timestamps and lines |
| `apply_time_filter(timestamps, lines, time_range)` | Data + filter | Filter by time range |
| `plot_graph(ax, canvas, log_type, time_range)` | Matplotlib objects | Plot log frequency over time |
| `plot_frequent_callers(ax, canvas, time_range)` | Matplotlib objects | Bar chart of top callers |
| `export_chart(fig, filename)` | Figure + path | Export chart to PNG/PDF |
| `export_graph_data(ax, time_combo, log_type)` | Graph data | Export underlying data to CSV |

**Supported Visualizations**:
- Time series frequency charts
- Top callers/contacts bar charts
- Log type distribution pie charts

---

### `log_monitor.py` - Live Monitoring

**Purpose**: Real-time log streaming from connected device.

**Functions**:

| Function | Parameters | Description |
|----------|------------|-------------|
| `start_monitoring(callback, queue)` | Update function, log queue | Start live monitoring thread |
| `stop_monitoring(callback)` | Update function | Stop monitoring gracefully |
| `monitor_thread(callback, queue)` | Update function, queue | Background thread that reads logs |

**Usage**:
```python
import queue
log_queue = queue.Queue()

def update_display(log):
    print(log)

start_monitoring(update_display, log_queue)
# ... later
stop_monitoring(update_display)
```

---

## 📁 Analysis Modules

### `numpy_analyzer.py` - High-Performance Analysis

**Purpose**: NumPy-accelerated analysis for large log files.

**Availability Check**:
```python
from numpy_analyzer import is_available
if is_available():
    # Use vectorized operations
```

**Functions**:

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `parse_timestamps_vectorized(lines, pattern)` | Log lines, regex | `np.array` | Fast timestamp parsing |
| `time_series_binning(timestamps, bin_size)` | Timestamps, size | (edges, counts) | Bin timestamps for visualization |
| `frequency_analysis_vectorized(items)` | List of items | (unique, counts) | Fast frequency counting |
| `statistical_analysis(values)` | Numeric array | `dict` | Mean, median, std, percentiles |
| `detect_outliers(values, threshold)` | Values, z-threshold | (indices, values) | Z-score outlier detection |
| `time_range_filter(ts, vals, start, end)` | Data + range | Filtered data | Filter by time range |
| `rolling_average(values, window)` | Values, window size | Smoothed array | Moving average |
| `activity_heatmap_data(timestamps, by_hour)` | Timestamps, bool | Heatmap data | Activity pattern analysis |

---

### `threat_scanner.py` - Security Analysis

**Purpose**: Scan logs for security threats and generate risk assessments.

**Class**: `ThreatScanner`

| Method | Description |
|--------|-------------|
| `__init__()` | Initialize scanner with empty threat list |
| `scan_logs(log_file_path)` | Main scanning function |
| `_scan_malware_packages(line, num)` | Check for known malware |
| `_scan_data_exfiltration(line, num)` | Check for data exfil patterns |
| `_scan_privilege_escalation(line, num)` | Check for priv esc attempts |
| `_scan_network_threats(line, num)` | Check for network anomalies |
| `_scan_suspicious_behaviors(line, num)` | Check for suspicious activity |
| `_scan_crashes(line, num)` | Track crash patterns |
| `_calculate_risk_score()` | Compute overall risk (0-100) |
| `get_risk_level()` | Get risk category string |
| `generate_report()` | Generate detailed threat report |

**Risk Levels**:
- `LOW` (0-25): Minimal concerns
- `MEDIUM` (26-50): Some suspicious activity
- `HIGH` (51-75): Significant threats detected
- `CRITICAL` (76-100): Severe security issues

**Quick Scan Helper**:
```python
from threat_scanner import quick_scan
results = quick_scan('logs/android_logcat.txt')
print(results['report'])
```

---

### `threat_signatures.py` - Threat Database

**Purpose**: Collection of threat signatures and IoC patterns.

**Signature Categories**:

| Category | Variable | Description |
|----------|----------|-------------|
| Known Malware | `KNOWN_MALWARE_PACKAGES` | Dict of package→description |
| Suspicious Patterns | `SUSPICIOUS_PACKAGE_PATTERNS` | Regex patterns + descriptions |
| Data Exfiltration | `DATA_EXFILTRATION_PATTERNS` | Network upload patterns |
| Privilege Escalation | `PRIVILEGE_ESCALATION_PATTERNS` | Root/su attempts |
| Network Threats | `NETWORK_THREAT_PATTERNS` | Suspicious network activity |
| Suspicious Behaviors | `SUSPICIOUS_BEHAVIORS` | General red flags |
| Crash Patterns | `CRASH_PATTERNS` | Crash/ANR signatures |
| Whitelist | `SAFE_PACKAGES` | Known safe system packages |

**Helper Functions**:
```python
from threat_signatures import is_whitelisted, get_all_threat_patterns

# Check if package is safe
if is_whitelisted('com.google.android.gms'):
    print("Safe package")

# Get consolidated patterns
patterns = get_all_threat_patterns()
```

---

## 📁 Utility Modules

### `modern_viewers.py` - Table Viewers

**Purpose**: Professional table widgets for displaying structured data.

**Classes**:

| Class | Description |
|-------|-------------|
| `ModernSMSViewer` | SMS message table with search |
| `ModernCallViewer` | Call log table with search |
| `ModernLocationViewer` | Location data table with map integration |

**Common Methods** (all viewers):
- `create_widgets()` - Build UI components
- `load_data(records)` - Populate table
- `refresh_table()` - Redraw table
- `do_search()` - Filter by search query
- `update_stats()` - Update statistics label

---

### `performance_utils.py` - Profiling Tools

**Purpose**: Performance measurement and optimization utilities.

**Decorators**:
```python
@timer
def my_function():
    # Function execution time will be printed
    pass

@profile("output.prof")
def my_profiled_function():
    # Detailed profiling stats saved to file
    pass
```

**Context Manager**:
```python
with PerformanceMonitor("Log Extraction"):
    extract_logs()
# Prints: "✅ Completed: Log Extraction in 2.3456 seconds"
```

**Benchmarking**:
```python
from performance_utils import run_performance_test, benchmark_comparison

# Single function test
stats = run_performance_test(my_function, iterations=100)

# Compare two implementations
results = benchmark_comparison(func1, func2, iterations=100)
```

---

### `reporting.py` - Report Generation

**Purpose**: Generate forensic reports in PDF/HTML format.

**Functions**:

| Function | Description |
|----------|-------------|
| `get_todays_logs(lines)` | Filter to today's entries |
| `_summarize_calls()` | Summarize call log statistics |
| `_summarize_sms()` | Summarize SMS statistics |
| `_summarize_logcat()` | Summarize logcat entries |
| `_collect_context()` | Gather all report data |
| `_render_html(context)` | Render HTML using Jinja2 |
| `export_full_report()` | Generate and save report |

**Report Contents**:
- Device information (model, OS, kernel)
- Call log summary with top callers
- SMS summary with top senders
- Recent logcat sample
- Chain of custody documentation
- Methodology description

**Dependencies**:
- `jinja2` - Template rendering
- `weasyprint` (optional) - PDF generation

---

## 📁 Script Modules (`scripts/`)

### `android_logs.py` - ADB Commands

**Purpose**: Low-level ADB command execution for log extraction.

**Functions**:

| Function | Description |
|----------|-------------|
| `get_logcat()` | Extract logcat with auto-detected buffer duration |
| `get_call_logs()` | Query call log content provider |
| `get_sms_logs()` | Query SMS content provider |
| `get_location_logs()` | Get dumpsys location output |
| `trigger_location_update()` | Launch Maps app to trigger location update |
| `monitor_logs(callback)` | Continuous logcat streaming |

---

### `detect_log_buffer.py` - Buffer Detection

**Purpose**: Detect available log buffer duration on device.

**Functions**:

| Function | Returns | Description |
|----------|---------|-------------|
| `detect_buffer()` | `dict` | Oldest timestamp, duration in hours/days |
| `get_device_info()` | `dict` | Device model and Android version |

**Return Structure**:
```python
{
    'success': bool,
    'oldest_timestamp': datetime | None,
    'duration_hours': float | None,
    'duration_days': float | None,
    'error': str | None
}
```

---

### `log_parser.py` - Basic Parser

**Purpose**: Simple log filtering (alternative to main filtering module).

**Function**:
```python
def filter_logs(
    input_file: str,
    keyword: str = "",
    time_range: str = None,
    output_file: str = "logs/filtered_logs.txt"
) -> None
```

---

## 📝 Usage Examples

### Complete Extraction Workflow

```python
from android_device import AndroidDevice
from threat_scanner import ThreatScanner

# 1. Connect to device
device = AndroidDevice()
if device.detect_device():
    print(f"Connected to {device.get_device_info()['model']}")
    
    # 2. Extract logs
    device.extract_system_logs("logs/logcat.txt")
    device.extract_call_logs()
    device.extract_sms_logs()
    
    # 3. Scan for threats
    scanner = ThreatScanner()
    results = scanner.scan_logs("logs/logcat.txt")
    print(scanner.generate_report())
```

### Custom Log Analysis

```python
from numpy_analyzer import (
    parse_timestamps_vectorized,
    frequency_analysis_vectorized,
    statistical_analysis
)

# Load log file
with open("logs/android_logcat.txt") as f:
    lines = f.readlines()

# Parse timestamps
timestamps = parse_timestamps_vectorized(lines)

# Analyze frequency
items, counts = frequency_analysis_vectorized([line[:20] for line in lines])

# Statistical summary
stats = statistical_analysis(counts)
print(f"Mean: {stats['mean']:.2f}, Std: {stats['std']:.2f}")
```
