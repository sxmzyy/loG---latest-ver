# Getting Started with Android Forensic Tool

Welcome to the Android Forensic Tool! This guide will help you get started with extracting and analyzing forensic data from Android devices.

---

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Windows Operating System** (Windows 10 or later)
2. **Python 3.7+** installed and added to PATH
3. **ADB (Android Debug Bridge)** installed
4. **USB Debugging enabled** on the target Android device
5. **Proper legal authorization** to analyze the device

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Launch the Tool

1. Navigate to the project directory:
   ```powershell
   cd C:\path\to\loG---latest-ver
   ```

2. Start the Python GUI (runs in background):
   ```powershell
   python main.py
   ```

3. Start the web interface:
   ```powershell
   powershell -ExecutionPolicy Bypass -File start-server.ps1
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8080
   ```

### Step 2: Connect Your Device

1. Connect the Android device via USB
2. Enable **USB Debugging** on the device
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings → Developer Options
   - Enable "USB Debugging"

3. Authorize the computer on the device when prompted

4. Verify connection:
   - Click **System Health** in the sidebar
   - Check that "ADB Connection" shows green ✅

### Step 3: Extract Logs

1. Click **Extract Logs** in the sidebar
2. Select what to extract:
   - ✅ Logcat (system logs)
   - ✅ SMS Messages
   - ✅ Call Logs
   - ✅ Location Data
3. Click **Start Extraction**
4. Wait for completion (usually 30-60 seconds)

### Step 4: Run Analysis

1. The tool will automatically run all forensic analyses
2. Or manually run: Navigate to **System Health** and let the orchestrator run

### Step 5: View Results

Explore the forensic intelligence modules in the sidebar:

- **Advanced Timeline** - Chronological view of all events
- **Privacy Profiler** - Apps accessing sensitive permissions
- **Network Intel** - External connections and IPs
- **PII Leak Detector** - Sensitive data leaks
- **Social Link Graph** - Communication network
- **Power Forensics** - Device usage patterns
- **Intent Hunter** - Navigation and URL recovery
- **Beacon Map** - WiFi/Bluetooth location inference
- **Clipboard Recovery** - Clipboard data
- **App Sessionizer** - Screen time analysis

---

## 📊 Dashboard Overview

The **Dashboard** (home page) shows:
- Device connection status
- Total logs extracted (SMS, Calls, Logcat entries)
- Recent activity summary
- Quick access cards

---

## ⚖️ Legal Requirements

**BEFORE YOU BEGIN:**

1. Click **Legal Disclaimer** in the sidebar
2. Read and understand all legal requirements
3. Ensure you have proper authorization:
   - Court order/search warrant, OR
   - Written consent from device owner, OR
   - Corporate authorization (company device), OR
   - Parental/guardian rights (minor's device)

**WARNING**: Unauthorized access is a federal crime in most jurisdictions.

---

## 🔒 Evidence Integrity

### Generating Hashes (After Extraction)

Hashes are automatically generated after each extraction. To manually verify:

```powershell
cd analysis
python evidence_hasher.py hash
```

### Verifying Hashes (Before Court Presentation)

1. Go to **System Health** in the sidebar
2. Click **Verify Hashes** button
3. Check results:
   - ✅ All verified = Evidence untampered
   - ✗ Tampered detected = Evidence may be compromised

Or via command line:
```powershell
cd analysis
python evidence_hasher.py verify
```

---

## 📤 Exporting Evidence

### Export Full Report

1. Click **Export Report** in the sidebar
2. Select format (PDF, HTML, or CSV)
3. Save to secure location

### Export Audit Log

1. Go to **System Health**
2. Click **Export Audit Log**
3. Choose format (JSON or CSV)
4. Include with evidence package for chain of custody

---

## 🩺 Troubleshooting

### Device Not Detected

**Symptoms**: "No devices connected" in System Health

**Solutions**:
1. Ensure USB Debugging is enabled on device
2. Try a different USB cable or port
3. Re-authorize the computer on the device
4. Run `adb devices` in PowerShell to verify
5. Restart ADB server:
   ```powershell
   adb kill-server
   adb start-server
   ```

### Python Not Found

**Symptoms**: "Python not found in PATH"

**Solution**:
1. Download Python from [python.org](https://www.python.org/)
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Verify: `python --version`

### Permission Denied Errors

**Symptoms**: Cannot write to logs directory

**Solution**:
1. Run PowerShell as Administrator
2. Check disk space (System Health → Disk Space)
3. Ensure antivirus is not blocking writes

### Web Interface Won't Load

**Symptoms**: Browser shows "Can't connect" at http://127.0.0.1:8080

**Solution**:
1. Ensure `start-server.ps1` is running
2. Check if port 8080 is available:
   ```powershell
   netstat -ano | findstr :8080
   ```
3. Try different port in `start-server.ps1`

---

## 💡 Pro Tips

1. **Always verify hashes** before presenting evidence in court
2. **Export audit logs** with every evidence package
3. **Document everything** - screenshots, notes, timestamps
4. **Use System Health** before critical operations
5. **Keep backups** of extracted data in encrypted storage

---

## 📞 Support

For technical issues or feature requests:
- Check the **Troubleshooting** guide
- Review system logs in `logs/error_log.json`
- Ensure you're running the latest version

---

## ✅ Checklist for First Use

- [ ] Python 3.7+ installed
- [ ] ADB installed and in PATH
- [ ] Device connected with USB Debugging enabled
- [ ] Legal authorization obtained
- [ ] Read Legal Disclaimer
- [ ] Verified ADB connection in System Health
- [ ] Successfully extracted logs
- [ ] Generated evidence hashes
- [ ] Reviewed at least one forensic module

**You're ready to conduct forensic analysis!** 🎉
