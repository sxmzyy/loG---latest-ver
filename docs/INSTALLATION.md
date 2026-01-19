# Installation Guide

Complete installation instructions for the Android Forensic Tool.

---

## 📋 Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.8+ | Core application |
| PHP | 8.0+ | Web interface |
| ADB | Latest | Android device communication |
| Git | Any | Version control (optional) |

### Operating System

- **Windows 10/11** (Primary target)
- Linux/macOS (Should work with path adjustments)

---

## 🐍 Python Installation

### Step 1: Install Python

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```powershell
   python --version
   # Expected: Python 3.8.x or higher
   ```

### Step 2: Create Virtual Environment (Recommended)

```powershell
# Navigate to project directory
cd "c:\Users\91912\Downloads\android log extract\Log-analysis-main"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate

# You should see (.venv) in your prompt
```

### Step 3: Install Python Dependencies

```powershell
# With virtual environment activated
pip install -r requirements.txt
```

**Required packages** (`requirements.txt`):
```
matplotlib>=3.5.0
numpy>=1.21.0
pandas>=1.3.0
jinja2>=3.0.0
fpdf>=1.7.2
```

**Optional packages** (for enhanced features):
```
# PDF report generation (requires GTK on Windows)
weasyprint>=52.0

# Map visualization in desktop GUI
tkintermapview>=1.22
```

### Step 4: Verify Python Installation

```powershell
python -c "import matplotlib, numpy, jinja2; print('✅ All packages installed!')"
```

---

## 📱 ADB Installation

### Option A: Using PowerShell Script (Recommended for Windows)

```powershell
# Run the included installer script
.\install_adb.ps1
```

This script will:
1. Download Android Platform Tools
2. Extract to a local directory
3. Add to system PATH

### Option B: Manual Installation

1. Download [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
2. Extract to a permanent location (e.g., `C:\Android\platform-tools`)
3. Add to PATH:
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"
   - Under "Path", click "Edit" → "New"
   - Add: `C:\Android\platform-tools`
   - Click OK on all dialogs

### Option C: Install via Chocolatey

```powershell
# Install Chocolatey first if needed
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install ADB
choco install adb
```

### Verify ADB Installation

```powershell
adb version
# Expected: Android Debug Bridge version X.X.X
```

---

## 🌐 PHP Installation (For Web Interface)

### Option A: Standalone PHP

1. Download PHP 8+ from [windows.php.net](https://windows.php.net/download/)
2. Extract to `C:\php`
3. Add `C:\php` to system PATH
4. Copy `php.ini-development` to `php.ini`
5. Enable required extensions in `php.ini`:
   ```ini
   extension=mbstring
   extension=fileinfo
   extension=json  ; Usually enabled by default
   ```

### Option B: XAMPP (Easier)

1. Download [XAMPP](https://www.apachefriends.org/download.html) with PHP 8+
2. Install to default location
3. Start Apache from XAMPP Control Panel
4. Copy `web/` folder to `C:\xampp\htdocs\forensic-tool\`
5. Access at `http://localhost/forensic-tool/`

### Option C: Use Included PHP (Project-Specific)

The project includes a PHP distribution in the `php/` folder:
```powershell
cd "c:\Users\91912\Downloads\android log extract\Log-analysis-main"
.\php\php.exe -S localhost:8000 -t web
```

### Verify PHP Installation

```powershell
php --version
# Expected: PHP 8.x.x
```

---

## 📲 Android Device Setup

### Enable Developer Options

1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Enter your PIN/pattern if prompted
4. You'll see "You are now a developer!"

### Enable USB Debugging

1. Go to **Settings** → **Developer Options**
2. Enable **USB Debugging**
3. (Optional) Enable **USB Debugging (Security settings)** for SMS/Call access

### Connect Device

1. Connect Android device via USB cable
2. On device, approve "Allow USB debugging" prompt
3. Check "Always allow from this computer"
4. Verify connection:
   ```powershell
   adb devices
   # Expected: XXXXXXXXX    device
   ```

### Troubleshooting Connection

If device shows as "unauthorized":
1. Revoke USB debugging authorizations on device
2. Reconnect and re-approve

If device not detected:
1. Try different USB cable (use data cable, not charge-only)
2. Try different USB port
3. Install device-specific USB drivers
4. Restart ADB server:
   ```powershell
   adb kill-server
   adb start-server
   adb devices
   ```

---

## 🚀 Running the Application

### Desktop GUI

```powershell
# Navigate to project directory
cd "c:\Users\91912\Downloads\android log extract\Log-analysis-main"

# Activate virtual environment (if used)
.\.venv\Scripts\Activate

# Run the application
python main.py
```

### Web Interface

```powershell
# Start PHP development server
cd "c:\Users\91912\Downloads\android log extract\Log-analysis-main\web"
php -S localhost:8000

# Or from project root using included PHP
cd "c:\Users\91912\Downloads\android log extract\Log-analysis-main"
.\php\php.exe -S localhost:8000 -t web
```

Then open http://localhost:8000 in your browser.

---

## 📂 Directory Structure After Installation

```
Log-analysis-main/
├── .venv/                 # Python virtual environment
├── logs/                  # Created after first extraction
│   ├── android_logcat.txt
│   ├── call_logs.txt
│   ├── sms_logs.txt
│   └── location_logs.txt
├── docs/                  # Documentation
├── scripts/               # ADB scripts
├── templates/             # Report templates
├── web/                   # PHP web interface
├── php/                   # Included PHP distribution
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
└── install_adb.ps1        # ADB installer
```

---

## ✅ Verification Checklist

Run these commands to verify your installation:

```powershell
# 1. Python
python --version
# ✅ Python 3.8+

# 2. Python packages
python -c "import matplotlib, numpy, jinja2; print('OK')"
# ✅ OK

# 3. ADB
adb version
# ✅ Android Debug Bridge version X.X.X

# 4. ADB device connection
adb devices
# ✅ XXXXXXXXX    device

# 5. PHP (optional)
php --version
# ✅ PHP 8.x.x

# 6. Run application
python main.py
# ✅ GUI opens without errors
```

---

## 🔧 Common Installation Issues

| Issue | Solution |
|-------|----------|
| `python` not recognized | Add Python to PATH or reinstall with "Add to PATH" checked |
| `adb` not recognized | Add platform-tools to PATH or reinstall ADB |
| Device "unauthorized" | Re-authorize USB debugging on device |
| Missing Python package | Run `pip install package-name` |
| tkinter not found | Reinstall Python with tcl/tk component |
| PHP exec() disabled | Enable in php.ini: `disable_functions = ` (empty) |

---

## 🆘 Getting Help

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system understanding
3. Open an issue on the project repository
