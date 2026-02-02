# Android Forensic Tool - Architecture Documentation

## System Architecture

This document describes the high-level architecture and design patterns used in the Android Forensic Tool.

---

## 🏛️ Architectural Overview

### Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                                │
│  ┌────────────────────────┐    ┌─────────────────────────────────────┐  │
│  │    Desktop GUI         │    │         Web Interface               │  │
│  │    (Tkinter)           │    │    (PHP 8+ / AdminLTE 4)           │  │
│  │  • main.py             │    │  • index.php (Dashboard)           │  │
│  │  • gui.py              │    │  • pages/*.php (Feature Pages)     │  │
│  │  • modern_viewers.py   │    │  • assets/ (CSS/JS)                │  │
│  └────────────────────────┘    └─────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│                        BUSINESS LOGIC LAYER                              │
│  ┌─────────────────┐  ┌───────────────┐  ┌───────────────────────────┐  │
│  │  Log Processing │  │ Threat Engine │  │    Analysis Engine        │  │
│  │  • filtering.py │  │ • scanner.py  │  │  • numpy_analyzer.py      │  │
│  │  • parsers.py   │  │ • signatures  │  │  • graphing.py            │  │
│  │  • log_parser   │  │   .py         │  │  • reporting.py           │  │
│  └─────────────────┘  └───────────────┘  └───────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│                        DATA ACCESS LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                    Device Interface                                  ││
│  │  • device_interface.py (Abstract Base Class)                        ││
│  │  • android_device.py (Android Implementation)                       ││
│  │  • scripts/android_logs.py (ADB Commands)                           ││
│  │  • scripts/detect_log_buffer.py (Buffer Detection)                  ││
│  └─────────────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────────────┤
│                        EXTERNAL INTERFACES                               │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                    Android Debug Bridge (ADB)                        ││
│  │  • adb logcat        • adb shell content query                      ││
│  │  • adb shell dumpsys • adb shell getprop                            ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Descriptions

### 1. Device Interface Layer

The device abstraction layer provides a unified interface for device operations.

```
DeviceInterface (ABC)
        │
        ▼
AndroidDevice
    │
    ├── detect_device()      → Check ADB connection
    ├── get_device_info()    → Model, OS version
    ├── extract_system_logs()→ Logcat extraction
    ├── extract_call_logs()  → Call history
    ├── extract_sms_logs()   → SMS messages
    └── extract_crash_reports()→ Crash data
```

**Design Pattern**: Strategy Pattern (allows for future iOS support)

### 2. Log Extraction Pipeline

```
Device → ADB Commands → Raw Logs → Parsers → Structured Data → Storage
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Log Files     │
                              │ (logs/*.txt)  │
                              └───────────────┘
```

**Log Types Extracted**:
| Log Type | Source | ADB Command |
|----------|--------|-------------|
| Logcat | System logs | `adb logcat -d -v time` |
| Call Logs | Call history | `adb shell content query --uri content://call_log/calls` |
| SMS | Text messages | `adb shell content query --uri content://sms` |
| Location | GPS/Cell/WiFi | `adb shell dumpsys location` |

### 3. Threat Detection Engine

```
                    ┌─────────────────────────┐
                    │   ThreatScanner         │
                    │   (threat_scanner.py)   │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐     ┌─────────────────┐     ┌───────────────┐
│ Malware       │     │ Data Exfil      │     │ Privilege     │
│ Signatures    │     │ Patterns        │     │ Escalation    │
└───────────────┘     └─────────────────┘     └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                    ┌─────────────────────────┐
                    │   Risk Score (0-100)    │
                    │   + Detailed Report     │
                    └─────────────────────────┘
```

**Threat Categories**:
- Known malware packages
- Data exfiltration indicators
- Privilege escalation attempts
- Network anomalies
- Suspicious app behaviors

### 4. Analysis Engine

```
┌─────────────────────────────────────────────────────────────┐
│                    Analysis Pipeline                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Raw Logs → Timestamp Parsing → Time Series Binning →        │
│                                                              │
│           → Frequency Analysis → Statistical Analysis →      │
│                                                              │
│           → Visualization (Charts/Graphs) → Reports          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**NumPy-Accelerated Operations**:
- Vectorized timestamp parsing
- Time series binning
- Frequency analysis
- Outlier detection
- Rolling averages

---

## 🔄 Data Flow Diagrams

### Log Extraction Flow

```
┌──────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐
│  User    │───▶│ GUI/Web     │───▶│ Python      │───▶│  ADB     │
│  Action  │    │ Interface   │    │ Engine      │    │  Command │
└──────────┘    └─────────────┘    └─────────────┘    └────┬─────┘
                                                           │
     ┌─────────────────────────────────────────────────────┘
     ▼
┌──────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐
│  Android │───▶│ Raw Log     │───▶│  Parser     │───▶│ Structured│
│  Device  │    │ Data        │    │             │    │ Data     │
└──────────┘    └─────────────┘    └─────────────┘    └──────────┘
```

### Threat Scanning Flow

```
┌───────────┐
│ Log File  │
└─────┬─────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Line-by-Line Scan                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Malware     │  │ Exfil       │  │ Priv Esc    │ ...          │
│  │ Check       │  │ Check       │  │ Check       │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                       │
│                 ┌────────────────┐                               │
│                 │ Threat Found?  │                               │
│                 └───────┬────────┘                               │
│                   Yes   │   No                                   │
│                   ┌─────┴─────┐                                  │
│                   ▼           ▼                                  │
│             ┌──────────┐  ┌──────────┐                           │
│             │Add Threat│  │ Continue │                           │
│             └──────────┘  └──────────┘                           │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────┐
│ Threat Report   │
│ + Risk Score    │
└─────────────────┘
```

---

## 🌐 Web Interface Architecture

### PHP Application Structure

```
web/
├── index.php              # Dashboard (Main entry)
├── includes/
│   ├── config.php         # Configuration settings
│   ├── header.php         # HTML head + navbar
│   ├── sidebar.php        # Navigation sidebar
│   └── footer.php         # Footer + scripts
├── api/
│   ├── extract.php        # Log extraction API
│   ├── device-status.php  # Device connection status
│   ├── filter.php         # Log filtering API
│   ├── scan-threats.php   # Threat scanning API
│   ├── stats.php          # Statistics API
│   ├── live-stream.php    # Real-time log streaming
│   ├── export-report.php  # Report generation
│   └── clear-data.php     # Data cleanup
└── pages/
    ├── extract-logs.php   # Log extraction page
    ├── filter-logs.php    # Filtering interface
    ├── live-monitor.php   # Real-time monitoring
    ├── logcat.php         # Logcat viewer
    ├── sms-messages.php   # SMS viewer
    ├── call-logs.php      # Call log viewer
    ├── location.php       # Location data + map
    ├── threats.php        # Threat analysis page
    └── graphs.php         # Data visualization
```

### Frontend Stack

- **Framework**: AdminLTE 4 (Bootstrap 5)
- **Charts**: Chart.js
- **Maps**: Leaflet.js
- **Icons**: Font Awesome 6
- **JavaScript**: Vanilla JS (ES6+)

---

## 🔧 Configuration System

### Python Configuration (`config.py`)

```python
# Theme Colors
PRIMARY_BG = "#1e1e2e"
ACCENT_BLUE = "#89b4fa"
...

# Log Type Patterns
LOG_TYPES = {
    "Application": {
        "pattern": r'ActivityManager|PackageManager|...',
        "color": "blue"
    },
    ...
}

# Pre-compiled Regex (30-50% performance boost)
COMPILED_LOG_PATTERNS = {...}
```

### PHP Configuration (`includes/config.php`)

Mirrors Python configuration for consistency:
- Theme colors
- Log type patterns
- Severity levels
- Time range options

---

## ⚡ Performance Optimizations

### 1. Threaded Operations
All long-running operations run in background threads:
- Log extraction
- Threat scanning
- Graph plotting
- Report generation

### 2. Pre-compiled Regex
Regular expressions are compiled once at startup and reused.

### 3. NumPy Vectorization
When available, NumPy provides 10-100x speedups for:
- Timestamp parsing
- Time series analysis
- Statistical computations

### 4. Lazy Loading
Web interface loads data asynchronously via AJAX calls.

---

## 🔒 Security Considerations

1. **ADB Authorization**: Requires device USB debugging enabled
2. **Local Processing**: All data processed locally, no cloud uploads
3. **Chain of Custody**: Report includes forensic methodology documentation
4. **Access Control**: Tool requires physical access to device

---

## 📊 Database Schema (Optional SQLite Extension)

```sql
-- Sessions table
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    device_id TEXT,
    device_model TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP
);

-- Log entries
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    session_id INTEGER,
    log_type TEXT,
    severity TEXT,
    timestamp TIMESTAMP,
    content TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Threats detected
CREATE TABLE threats (
    id INTEGER PRIMARY KEY,
    session_id INTEGER,
    threat_type TEXT,
    severity TEXT,
    line_number INTEGER,
    description TEXT,
    detected_at TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

---

## 🔄 Extension Points

### Adding New Log Sources
1. Add pattern to `config.py` LOG_TYPES
2. Implement extraction in `scripts/android_logs.py`
3. Add parser in `parsers.py`
4. Update web API if needed

### Adding New Threat Signatures
1. Add patterns to `threat_signatures.py`
2. Add scanner method in `threat_scanner.py`

### Adding iOS Support (Future)
1. Create `IOSDevice` class implementing `DeviceInterface`
2. Implement iOS-specific extraction methods
3. Add to `detect_connected_devices()` in `device_interface.py`
