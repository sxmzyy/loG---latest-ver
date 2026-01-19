# Troubleshooting Guide

Solutions for common issues with the Android Forensic Tool.

---

## 🔌 Connection Issues

### Device Not Detected

**Symptoms:**
- `adb devices` shows empty list
- "No device connected" in application

**Solutions:**

1. **Check USB cable**
   - Use a data-capable USB cable (not charge-only)
   - Try a different cable or USB port

2. **Enable USB debugging**
   ```
   Settings → Developer Options → USB Debugging → ON
   ```

3. **Restart ADB server**
   ```powershell
   adb kill-server
   adb start-server
   adb devices
   ```

4. **Install USB drivers**
   - Samsung: [Samsung USB Drivers](https://developer.samsung.com/android-usb-driver)
   - Google: [Google USB Driver](https://developer.android.com/studio/run/win-usb)
   - Other: Use Universal ADB Driver or device manufacturer's driver

5. **Check Windows Device Manager**
   - Look for "ADB Interface" under "Android Device"
   - If showing error, reinstall drivers

---

### Device Shows "unauthorized"

**Symptoms:**
- `adb devices` shows `XXXXXX    unauthorized`

**Solutions:**

1. **Approve on device**
   - Look for "Allow USB debugging?" popup on device
   - Check "Always allow from this computer"
   - Tap "Allow"

2. **Revoke and re-authorize**
   ```
   Settings → Developer Options → Revoke USB debugging authorizations
   ```
   Then reconnect and approve again.

3. **Check ADB keys**
   ```powershell
   # Remove old keys
   Remove-Item ~\.android\adbkey*
   
   # Restart ADB
   adb kill-server
   adb start-server
   ```

---

### Device Shows "offline"

**Symptoms:**
- `adb devices` shows `XXXXXX    offline`

**Solutions:**

1. **Restart ADB**
   ```powershell
   adb kill-server
   adb start-server
   ```

2. **Restart device**
   - Reboot the Android device

3. **Check USB mode**
   - Pull down notification shade
   - Change USB mode to "File Transfer" or "MTP"

---

## 📝 Log Extraction Issues

### "No logs found" or Empty Logs

**Symptoms:**
- Extraction completes but files are empty
- "⚠️ No call logs found" message

**Solutions:**

1. **Check permissions**
   - SMS/Call logs may require root or special permissions
   - Try enabling "USB debugging (Security settings)" in Developer Options

2. **Verify log files exist**
   ```powershell
   dir logs\
   ```

3. **Check logcat buffer**
   - Some devices have small log buffers
   - Try extracting immediately after device reboot

4. **Test ADB manually**
   ```powershell
   # Test logcat
   adb logcat -d -t 10
   
   # Test call logs (may fail without permissions)
   adb shell content query --uri content://call_log/calls --projection _id
   ```

---

### Extraction Takes Too Long

**Symptoms:**
- Extraction hangs or takes many minutes
- Progress bar stuck

**Solutions:**

1. **Reduce time range**
   - Large log buffers can contain millions of lines
   - Filter by time range in the application

2. **Check device responsiveness**
   - Ensure device is unlocked and responsive
   - Close memory-intensive apps on device

3. **Check USB connection speed**
   - Use USB 3.0 port
   - Avoid USB hubs

---

## 🖥️ GUI Issues

### GUI Won't Start / Tkinter Error

**Symptoms:**
- `ModuleNotFoundError: No module named 'tkinter'`
- GUI window doesn't appear

**Solutions:**

1. **Reinstall Python with Tkinter**
   - Re-run Python installer
   - Ensure "tcl/tk and IDLE" is checked under Optional Features

2. **Install Tkinter separately (Linux)**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   ```

3. **Check display variable (Linux/WSL)**
   ```bash
   export DISPLAY=:0
   ```

---

### GUI Freezes During Operation

**Symptoms:**
- "Not Responding" in title bar
- GUI unresponsive during extraction

**Solutions:**

1. **Wait for operation to complete**
   - Long operations run in background threads
   - GUI may appear frozen but is processing

2. **Check terminal for errors**
   - Run from command line to see error messages
   ```powershell
   python main.py
   ```

3. **Update to latest code**
   - Older versions may not have threading fixes

---

### Charts Not Displaying

**Symptoms:**
- Graph area is blank
- Matplotlib errors in console

**Solutions:**

1. **Install matplotlib backend**
   ```powershell
   pip install matplotlib
   ```

2. **Check for data**
   - Ensure log files contain data before plotting

3. **Try different backend**
   ```python
   # Add to top of main.py
   import matplotlib
   matplotlib.use('TkAgg')
   ```

---

## 🌐 Web Interface Issues

### PHP Server Won't Start

**Symptoms:**
- "php is not recognized" error
- Port already in use

**Solutions:**

1. **Add PHP to PATH**
   ```powershell
   $env:Path += ";C:\php"
   php -S localhost:8000
   ```

2. **Use different port**
   ```powershell
   php -S localhost:8080 -t web
   ```

3. **Check PHP installation**
   ```powershell
   php --version
   ```

---

### API Returns 500 Error

**Symptoms:**
- Extraction fails via web interface
- JSON error response with 500 status

**Solutions:**

1. **Enable error display**
   Edit `web/includes/config.php`:
   ```php
   define('DEBUG_MODE', true);
   ini_set('display_errors', 1);
   ```

2. **Check PHP error log**
   ```powershell
   type php_error.log
   ```

3. **Check permissions**
   - Ensure `logs/` directory is writable
   - Run PHP server with appropriate permissions

---

### Maps Not Loading

**Symptoms:**
- Location page shows blank map
- Leaflet tiles not loading

**Solutions:**

1. **Check internet connection**
   - Maps require OpenStreetMap tile server access

2. **Check browser console**
   - Press F12 → Console tab
   - Look for CORS or network errors

3. **Try different browser**
   - Some ad blockers may block map tiles

---

## 🛡️ Threat Scanner Issues

### Scanner Reports No Threats (False Negative)

**Solutions:**

1. **Ensure logs are extracted**
   - Threat scanner requires logcat data

2. **Check log content**
   - Very short logs may not contain detectable threats

3. **Update threat signatures**
   - Check `threat_signatures.py` for latest patterns

---

### Scanner Reports Too Many Threats (False Positive)

**Solutions:**

1. **Review whitelist**
   - Add safe packages to `SAFE_PACKAGES` in `threat_signatures.py`

2. **Adjust patterns**
   - Some patterns may be too broad for your use case

---

## 📄 Report Generation Issues

### PDF Export Fails

**Symptoms:**
- "WeasyPrint not available" message
- Falls back to HTML export

**Solutions:**

WeasyPrint requires GTK libraries on Windows, which can be difficult to install.

1. **Option 1: Use HTML export instead**
   - HTML reports are fully functional
   - Can be printed to PDF from browser

2. **Option 2: Install GTK (Advanced)**
   ```powershell
   # Using MSYS2
   pacman -S mingw-w64-x86_64-gtk3
   pip install weasyprint
   ```

3. **Option 3: Use Linux/WSL**
   ```bash
   # On Ubuntu
   sudo apt-get install python3-weasyprint
   ```

---

### Report Template Not Found

**Symptoms:**
- Jinja2 TemplateNotFound error

**Solutions:**

1. **Check template exists**
   ```powershell
   dir templates\report_template.html
   ```

2. **Check working directory**
   - Run from project root directory

---

## ⚡ Performance Issues

### Application is Slow

**Solutions:**

1. **Enable NumPy acceleration**
   ```powershell
   pip install numpy pandas
   ```

2. **Filter logs before analysis**
   - Use time range filters
   - Use keyword filters

3. **Increase system resources**
   - Close unnecessary applications
   - Ensure adequate RAM (8GB+ recommended)

---

### High Memory Usage

**Solutions:**

1. **Process smaller log files**
   - Extract recent logs only
   - Clear old logs periodically

2. **Close unused tabs**
   - Each viewer tab consumes memory

---

## 🔄 General Troubleshooting Steps

1. **Restart the application**

2. **Check terminal output**
   ```powershell
   python main.py
   # Watch for error messages
   ```

3. **Verify dependencies**
   ```powershell
   pip check
   pip install -r requirements.txt --upgrade
   ```

4. **Check file permissions**
   ```powershell
   # Ensure logs directory is writable
   mkdir logs 2>$null
   echo "test" > logs\test.txt
   ```

5. **Review log files**
   - Check `output.log` if present
   - Check PHP error logs for web issues

6. **Reset configuration**
   - Delete any cached/config files
   - Restart with fresh settings

---

## 📞 Getting More Help

If issues persist:

1. **Collect diagnostic info**
   ```powershell
   python --version
   pip list
   adb version
   adb devices
   ```

2. **Check documentation**
   - [INSTALLATION.md](INSTALLATION.md)
   - [ARCHITECTURE.md](ARCHITECTURE.md)

3. **Report the issue**
   - Include error messages
   - Include steps to reproduce
   - Include system information
