# Android Forensic Tool

A comprehensive forensic analysis tool for extracting, analyzing, and visualizing Android device logs. This tool provides both a desktop GUI (Python/Tkinter) and a modern web interface (PHP/AdminLTE) for forensic investigators.

## 🎯 Key Features

- **Log Extraction**: Extract logcat, call logs, SMS messages, and location data from Android devices via ADB
- **Threat Detection**: Automated scanning for malware signatures, data exfiltration attempts, and suspicious behaviors
- **Real-time Monitoring**: Live logcat streaming with categorization and filtering
- **Data Visualization**: Charts and graphs for temporal analysis and frequency distributions
- **Location Tracking**: GPS coordinates, cell tower info, and WiFi network analysis
- **Report Generation**: Export forensic reports in PDF/HTML format with chain-of-custody documentation

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Android Forensic Tool                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │   Desktop GUI   │    │    Web UI       │                     │
│  │  (Tkinter)      │    │  (PHP/AdminLTE) │                     │
│  └────────┬────────┘    └────────┬────────┘                     │
│           │                      │                               │
│  ┌────────▼──────────────────────▼────────┐                     │
│  │            Core Python Engine           │                     │
│  │  • Device Interface  • Log Extraction   │                     │
│  │  • Threat Scanner   • Data Parsers      │                     │
│  │  • NumPy Analyzer   • Report Generator  │                     │
│  └────────────────────┬───────────────────┘                     │
│                       │                                          │
│  ┌────────────────────▼───────────────────┐                     │
│  │              ADB Interface              │                     │
│  │       (Android Debug Bridge)            │                     │
│  └────────────────────┬───────────────────┘                     │
│                       │                                          │
└───────────────────────┼─────────────────────────────────────────┘
                        │
              ┌─────────▼─────────┐
              │  Android Device   │
              │  (USB/WiFi ADB)   │
              └───────────────────┘
```

## 📁 Project Structure

```
Log-analysis-main/
├── main.py                 # Application entry point
├── config.py               # Configuration and theme settings
├── gui.py                  # Tkinter GUI components
├── device_interface.py     # Abstract device interface
├── android_device.py       # Android device implementation
├── filtering.py            # Log filtering engine
├── graphing.py             # Data visualization
├── log_monitor.py          # Live monitoring
├── modern_viewers.py       # Table viewers for SMS/Call/Location
├── numpy_analyzer.py       # High-performance data analysis
├── parsers.py              # Log format parsers
├── performance_utils.py    # Profiling and optimization
├── reporting.py            # Report generation
├── threat_scanner.py       # Security threat detection
├── threat_signatures.py    # Threat signature database
├── scripts/
│   ├── android_logs.py     # ADB log extraction
│   ├── detect_log_buffer.py# Buffer detection
│   └── log_parser.py       # Basic log parsing
├── templates/
│   └── report_template.html# HTML report template
├── web/                    # PHP web interface
│   ├── index.php           # Dashboard
│   ├── api/                # REST API endpoints
│   ├── includes/           # Common PHP includes
│   ├── pages/              # Feature pages
│   └── assets/             # CSS/JS assets
└── logs/                   # Extracted log files
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** with required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Android SDK Platform Tools** (for ADB):
   - Windows: Run `install_adb.ps1`
   - Or download from: https://developer.android.com/studio/releases/platform-tools

3. **PHP 8+** (for web interface):
   ```bash
   php -S localhost:8000 -t web
   ```

### Running the Desktop GUI

```bash
python main.py
```

### Running the Web Interface

```bash
cd web
php -S localhost:8000
```
Then open http://localhost:8000 in your browser.

## 📖 Documentation

- [Architecture Documentation](ARCHITECTURE.md)
- [Python Module Documentation](PYTHON_MODULES.md)
- [Web Interface Documentation](WEB_MODULES.md)
- [API Reference](API_REFERENCE.md)

## ⚠️ Legal Notice

This tool is intended for authorized forensic investigations only. Ensure you have proper authorization before extracting data from any device.

## 📝 License

This project is for educational and authorized forensic use only.
