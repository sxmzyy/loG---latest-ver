# Troubleshooting Guide

This guide covers common issues and their solutions.

---

## Device Connection Issues

### Problem: "No devices connected" in System Health

**Symptoms**:
- ADB status shows ⚠️ WARNING
- Dashboard shows "Device: Not Connected"

**Diagnosis**:
```powershell
adb devices
```

If output shows `List of devices attached` with nothing below it, device is not detected.

**Solutions**:

1. **Enable USB Debugging**
   - Settings → About Phone
   - Tap "Build Number" 7 times
   - Settings → Developer Options
   - Enable "USB Debugging"

2. **Authorize Computer**
   - Unlock device
   - Look for "Allow USB debugging?" prompt
   - Tap "Always allow from this computer"
   - Tap "OK"

3. **Try Different USB Port/Cable**
   - Use USB 2.0 port (sometimes USB 3.0 causes issues)
   - Use original cable or high-quality cable
   - Avoid USB hubs

4. **Restart ADB Server**
   ```powershell
   adb kill-server
   adb start-server
   adb devices
   ```

5. **Reinstall USB Drivers** (Windows)
   - Device Manager → Android Device → Uninstall
   - Unplug and re-plug device
   - Windows will reinstall drivers

6. **Check Device is in MTP/File Transfer Mode**
   - Pull down notification shade
   - Tap "USB for charging"
   - Select "File Transfer" or "MTP"

---

## Extraction Failures

### Problem: "Permission Denied" when extracting logs

**Symptoms**:
- Extraction fails with permission error
- Some logs extract but others fail

**Solutions**:

1. **For SMS/Call Logs**: Device must be rooted
   - If not rooted, these extractions will fail
   - Alternative: Use backup extraction methods

2. **For Logcat**: Check READ_LOGS permission
   ```powershell
   adb shell pm grant com.android.shell android.permission.READ_LOGS
   ```

3. **Run PowerShell as Administrator**
   - Right-click PowerShell icon
   - Select "Run as administrator"
   - Re-run extraction

---

## Python/Script Errors

### Problem: "Python not found" or "python: command not found"

**Diagnosis**:
```powershell
python --version
```

If error appears, Python is not in PATH.

**Solutions**:

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, **CHECK** "Add Python to PATH"
   - Restart computer

2. **Manually Add to PATH**
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add Python installation folder (e.g., `C:\Python39\`)
   - Restart terminal

3. **Use Full Path**
   ```powershell
   C:\Python39\python.exe main.py
   ```

### Problem: "ModuleNotFoundError" when running scripts

**Symptoms**:
```
ModuleNotFoundError: No module named 'numpy'
```

**Solution**:
```powershell
cd C:\path\to\loG---latest-ver
pip install -r requirements.txt
```

If `pip` not found:
```powershell
python -m pip install -r requirements.txt
```

---

## Web Interface Issues

### Problem: "This site can't be reached" at http://127.0.0.1:8080

**Diagnosis**:
Check if PHP server is running:
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*php*"}
```

**Solutions**:

1. **Start the Server**
   ```powershell
   cd C:\path\to\loG---latest-ver
   powershell -ExecutionPolicy Bypass -File start-server.ps1
   ```

2. **Port Already in Use**
   ```powershell
   netstat -ano | findstr :8080
   ```
   If port is in use, edit `start-server.ps1`:
   ```powershell
   # Change port from 8080 to 8081
   php.exe -S 127.0.0.1:8081 -t web
   ```

3. **Firewall Blocking**
   - Windows Defender → Allow an app
   - Add PHP executable

### Problem: Pages load but show "No data available"

**Symptoms**:
- Forensic modules show empty tables
- Dashboard shows 0 logs

**Diagnosis**:
Check if log files exist:
```powershell
ls logs\
```

**Solutions**:

1. **Extract Logs First**
   - Navigate to "Extract Logs"
   - Run extraction
   - Wait for completion

2. **Run Analysis Scripts**
   ```powershell
   cd analysis
   python run_analysis.py
   ```

3. **Check File Permissions**
   - Ensure `logs/` directory has write permissions
   - Run as administrator if needed

---

## Analysis Errors

### Problem: Analysis scripts time out or hang

**Symptoms**:
- Scripts run for more than 60 seconds
- Orchestrator shows "TIMEOUT"

**Solutions**:

1. **Large Log Files** (> 100MB)
   - Split logcat into smaller chunks
   - Or increase timeout in `run_analysis.py`:
     ```python
     timeout=120  # Increase from 60 to 120 seconds
     ```

2. **Check Error Log**
   ```powershell
   cat logs\error_log.json
   ```

3. **Run Individual Scripts**
   ```powershell
   cd analysis
   python unified_timeline.py
   ```
   This will show detailed error output.

### Problem: Hash verification shows "TAMPERED"

**Symptoms**:
- System Health shows red ✗ for hash verification
- Specific files marked as tampered

**CRITICAL**: This indicates possible evidence corruption.

**Investigation Steps**:

1. **Check When File Was Last Modified**
   ```powershell
   ls -l logs\android_logcat.txt
   ```

2. **Review Audit Log**
   - System Health → Export Audit Log
   - Look for unauthorized access

3. **Compare with Backup**
   - If you have backups, compare hashes

4. **Regenerate Hash** (if legitimate modification)
   ```powershell
   cd analysis
   python evidence_hasher.py hash
   ```

**IMPORTANT**: Document why hash changed before regenerating.

---

## Performance Issues

### Problem: Web interface is slow or laggy

**Symptoms**:
- Pages take > 5 seconds to load
- Browser becomes unresponsive

**Solutions**:

1. **Large Dataset**
   - Enable pagination in DataTables (already default)
   - Filter by date range before viewing

2. **Clear Browser Cache**
   - Ctrl+Shift+Delete
   - Clear cached images and files

3. **Use Chrome or Edge**
   - Better JavaScript performance than Firefox for large tables

### Problem: Extraction takes very long (> 5 minutes)

**Symptoms**:
- Logcat extraction seems frozen

**Solutions**:

1. **Large Logcat Buffer**
   - Normal for devices with weeks of logs
   - Consider using time-based filtering:
     ```powershell
     adb logcat -t '01-15 00:00:00.000' > logs\recent_logcat.txt
     ```

2. **Slow USB Connection**
   - Use USB 2.0 port
   - Avoid USB hubs

---

## Data Accuracy Issues

### Problem: Some SMS or calls are missing

**Possible Causes**:
- **Deleted Messages**: Tool can only extract existing data
- **Non-Rooted Device**: SMS/Call extraction requires root on some devices
- **Encrypted Backups**: Cannot read encrypted content

**Workaround**:
- Use bugreport extraction (captures more data on non-rooted devices):
  ```powershell
  adb bugreport bugreport.zip
  ```
  Then import via "Import Bugreport" feature

### Problem: PII Detector shows false positives

**Symptoms**:
- Test emails or fake data flagged as PII
- System-generated UUIDs flagged

**Expected Behavior**: 
- Some false positives are normal
- Review each finding manually

**Mitigation**:
- The detector includes basic filtering for common false positives
- Focus on contextually relevant findings

---

## System Health Warnings

### Problem: "Disk Space" shows WARNING (>90% used)

**Solutions**:

1. **Clear Old Exports**
   ```powershell
   rm exports\* -Force
   ```

2. **Archive Old Cases**
   - Move old `logs/` data to external drive
   - Work on one case at a time

3. **Free Up System Space**
   - Empty Recycle Bin
   - Run Disk Cleanup

### Problem: Audit log growing too large

**Symptoms**:
- `audit_log.json` > 10MB

**Solution**:
- Automatic rotation already implemented (keeps last 10,000 entries)
- If still concerned, export and archive old logs:
  ```powershell
  mv logs\audit_log.json archive\audit_log_2026-01-20.json
  ```

---

## Advanced Troubleshooting

### Enable Debug Mode

Add to `config.php`:
```php
error_reporting(E_ALL);
ini_set('display_errors', 1);
```

### Check PHP Error Log

```powershell
cat web\php_error.log
```

### View Python Error Traceback

```powershell
python analysis\script_name.py 2>&1 | Out-File -FilePath debug.txt
```

### Verify All Dependencies

```powershell
python -c "import numpy, pandas; print('Dependencies OK')"
```

---

## Getting Help

If problem persists:

1. **Check System Health**: All checks should be green
2. **Review Error Logs**: `logs/error_log.json`
3. **Check Audit Log**: Look for system errors
4. **Document the Issue**:
   - What were you trying to do?
   - What happened instead?
   - Error messages (exact text)
   - Steps to reproduce

---

## Emergency Recovery

### Tool Won't Start At All

1. Verify Python installation: `python --version`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check for port conflicts: `netstat -ano | findstr :8080`
4. Run as administrator

### Data Loss Concerns

**Extracted logs are safe** as long as:
- `logs/` directory exists
- Hash verification passes
- Audit log shows no unauthorized modifications

**Recovery**: 
- Re-extract from device (if still available)
- Restore from backup

---

## Prevention Tips

✅ **Regular Backups**: Back up `logs/` after each extraction
✅ **Hash Immediately**: Generate hashes right after extraction
✅ **System Health Checks**: Check before critical operations
✅ **Keep Audit Logs**: Export periodically
✅ **Update Regularly**: Check for tool updates

---

**Remember**: When in doubt, check System Health first. It provides real-time diagnostics for most issues.
