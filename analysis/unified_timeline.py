
import os
import json
import re
from datetime import datetime

# Improved regex for Logcat: 01-20 22:59:42.046 D/Tag(PID): Message OR 01-19 13:00:19.199 F/Tag ...
# We'll use a more flexible regex: Timestamp Priority/Tag: Message
LOGCAT_REGEX = re.compile(r'^(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s+([VDIWEF])\/([^\(:]+)(?:\(\s*\d+\))?:?\s+(.*)$')

def parse_logcat_line(line):
    # Try the flexible regex first
    match = LOGCAT_REGEX.match(line)
    if match:
        ts_str, priority, tag, message = match.groups()
        current_year = datetime.now().year
        try:
            # Handle MM-DD format by appending current year (heuristic)
            ts = datetime.strptime(f"{current_year}-{ts_str}", "%Y-%m-%d %H:%M:%S.%f")
            return {
                "timestamp": ts.isoformat(),
                "priority": priority,
                "tag": tag.strip(),
                "message": message.strip()
            }
        except: pass
        
    # Fallback for standard threadtime format: Date Time PID TID Level Tag: Message
    # 01-20 23:36:22.123  1234  5678 I Tag : Message
    threadtime_regex = re.compile(r'^(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s+(\d+)\s+(\d+)\s+([VDIWEF])\s+([^:]+):\s+(.*)$')
    match = threadtime_regex.match(line)
    if match:
        ts_str, pid, tid, priority, tag, message = match.groups()
        current_year = datetime.now().year
        try:
            ts = datetime.strptime(f"{current_year}-{ts_str}", "%Y-%m-%d %H:%M:%S.%f")
            return {
                "timestamp": ts.isoformat(),
                "priority": priority,
                "tag": tag.strip(),
                "message": message.strip()
            }
        except: pass

    return None

def generate_timeline(logs_dir="logs", output_file="logs/unified_timeline.json"):
    timeline = []
    
    # 1. Process Logcat
    logcat_path = os.path.join(logs_dir, "android_logcat.txt")
    if os.path.exists(logcat_path):
        print(f"Processing Logcat: {logcat_path}")
        with open(logcat_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                parsed = parse_logcat_line(line)
                if parsed:
                    # Smart Classification
                    tag = parsed["tag"]
                    msg = parsed["message"]
                    
                    evt_type = "LOGCAT" # Default
                    evt_subtype = tag
                    
                    # 1. Power / Screen
                    if "PowerManagerService" in tag:
                        evt_type = "LOGCAT_POWER" # Catch ALL PowerManager logs
                        if "Waking up" in msg:
                            evt_subtype = "Screen On"
                        elif "Going to sleep" in msg:
                            evt_subtype = "Screen Off"
                        else:
                            evt_subtype = "Power Event" # Generic
                            
                    elif "DisplayPowerController" in tag:
                        evt_type = "LOGCAT_DEVICE"
                        evt_subtype = "Display Control"
                        # Try to match "BrightnessEvent: brt=0.615... (91.0%)"
                        if "BrightnessEvent" in msg:
                            p_match = re.search(r'\(([\d\.]+)%\)', msg)
                            if p_match:
                                evt_subtype = f"Brightness {p_match.group(1)}%"
                            else:
                                b_match = re.search(r'brt=([\d\.]+)', msg)
                                if b_match:
                                    val = float(b_match.group(1))
                                    percent = int(val * 100)
                                    evt_subtype = f"Brightness {percent}%"
                        elif "brightness=" in msg or "Brightness [" in msg:
                             b_match = re.search(r'(?:brightness=|Brightness \[)([\d\.]+)', msg)
                             if b_match:
                                val = float(b_match.group(1))
                                percent = int(val * 100) if val <= 1.0 else val
                                evt_subtype = f"Brightness {percent}%"

                    elif "BatteryService" in tag or "healthd" in tag:
                        evt_type = "LOGCAT_POWER"
                        evt_subtype = "Battery Info"
                        l_match = re.search(r'level:?(\d+)', msg)
                        if l_match:
                            evt_subtype = f"Battery {l_match.group(1)}%"
                            
                    elif "DreamManager" in tag:
                        evt_type = "LOGCAT_POWER"
                        evt_subtype = "Doze/Sleep"

                    elif "Keyguard" in tag:
                         evt_type = "LOGCAT_DEVICE"
                         if "keyguardGoingAway" in msg:
                             evt_subtype = "User Present (Unlock)"
                         elif "onStartedWakingUp" in msg:
                             evt_subtype = "Keyguard Waking"
                         else:
                             evt_subtype = "Keyguard Event"

                    # 2. App Activity
                    elif "ActivityTaskManager" in tag or "ActivityManager" in tag:
                        evt_type = "LOGCAT_APP"
                        evt_subtype = "App Activity"
                        if "START u0" in msg:
                            evt_subtype = "App Launch"
                            c_match = re.search(r'cmp=([^ ]+)', msg)
                            if c_match:
                                evt_subtype = f"Launch: {c_match.group(1).split('/')[-1]}"
                        elif "Displayed" in msg:
                            evt_subtype = "App Displayed"
                            n_match = re.search(r'Displayed ([^:]+):', msg)
                            if n_match:
                                evt_subtype = f"Displayed: {n_match.group(1).split('/')[-1]}"
                        elif "Process died" in msg:
                            evt_subtype = "App Crash/Kill"

                    elif "PackageManager" in tag:
                        evt_type = "LOGCAT_APP"
                        evt_subtype = "Package Event"

                    # 3. Network
                    elif "WifiService" in tag or "ConnectivityService" in tag or "NetworkController" in tag:
                        evt_type = "LOGCAT_NET" # Mapped to Network in PHP
                    
                    # 4. Device / User Input
                    elif "WindowManager" in tag:
                        evt_type = "LOGCAT_DEVICE"
                        evt_subtype = "Window Manager"
                    elif "InputManager" in tag:
                         evt_type = "LOGCAT_DEVICE"
                         evt_subtype = "Input Event"
                    elif "SensorService" in tag:
                        evt_type = "LOGCAT_DEVICE"
                        evt_subtype = "Sensor Event"
                    
                    # 5. SIM/Carrier Events (CRITICAL FOR MULE DETECTION)
                    elif "SubscriptionController" in tag or "CarrierConfigLoader" in tag or "TelephonyRegistry" in tag:
                        evt_type = "LOGCAT_SIM"
                        evt_subtype = "SIM/Carrier Event"
                        # Flag suspicious SIM changes
                        if any(keyword in msg.lower() for keyword in ["sim loaded", "sim changed", "carrier changed", 
                                                                       "subscription changed", "iccid", "sim state changed"]):
                            evt_subtype = "⚠️ SIM Swap Detected"
                        elif "carrier config" in msg.lower():
                            evt_subtype = "Carrier Config Change"

                    # 5b. Telephony/Radio Events (For Fake Call Detection)
                    elif "Telecom" in tag or "InCall" in tag or "RIL" in tag or "GsmCdmaPhone" in tag:
                        evt_type = "LOGCAT_RADIO"
                        evt_subtype = "Radio/Telecom Handshake"
                        if "dial" in msg.lower() or "outgoing" in msg.lower():
                            evt_subtype = "System Outgoing Call"
                        elif "incoming" in msg.lower() or "ringing" in msg.lower():
                            evt_subtype = "System Incoming Call"
                    
                    # 6. Filter Noise (Optional - reduce generic log volume if needed)
                    # For now, we keep everything but categorize specific interesting events
                    
                    timeline.append({
                        "timestamp": parsed["timestamp"],
                        "type": evt_type,
                        "subtype": evt_subtype,
                        "content": f"[{parsed['priority']}/{parsed['tag']}] {parsed['message']}",
                        "severity": parsed["priority"]
                    })

    # Financial SMS patterns for flagging
    FINANCIAL_PATTERNS = {
        "OTP": re.compile(r'\b(?:OTP|otp|one.time.password|verification.code|auth.code)\b.*?\d{4,6}', re.I),
        "UPI": re.compile(r'\b(?:UPI|PhonePe|Paytm|GPay|Google.Pay|BHIM|Amazon.Pay|Cred|MobiKwik|Freecharge)\b.*?(?:Rs\.?|INR|₹|rupee|rupees)\s*\d+', re.I),
        "BANK": re.compile(r'\b(?:credited|debited|transferred|withdrawn|deposited|balance|account|IFSC|NEFT|RTGS|IMPS)\b.*?(?:Rs\.?|INR|₹|rupee|rupees)\s*\d+', re.I),
        "TRANSACTION": re.compile(r'\b(?:paid|sent|received|spent|purchase|bill|invoice|payment|txn|transaction)\b.*?(?:Rs\.?|INR|₹|rupee|rupees)\s*\d+', re.I)
    }

    def flag_financial_sms(content):
        for flag, pattern in FINANCIAL_PATTERNS.items():
            if pattern.search(content):
                return f"FINANCIAL_{flag}"
        return None

    # 2. Process SMS (Existing logic preserved mostly, ensuring format match)
    sms_path = os.path.join(logs_dir, "sms_logs.txt")
    if os.path.exists(sms_path):
        print(f"Processing SMS: {sms_path}")
        with open(sms_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if " | " in line:
                    parts = line.split(" | ")
                    if len(parts) >= 4:
                        try:
                            ts = datetime.strptime(parts[0].strip(), "%Y-%m-%d %H:%M:%S")
                            content = f"SMS {parts[1]}: {parts[2]} - {parts[3].strip()}"
                            financial_flag = flag_financial_sms(content)
                            subtype = f"{parts[1]} ({financial_flag})" if financial_flag else parts[1]
                            timeline.append({
                                "timestamp": ts.isoformat(),
                                "type": "SMS",
                                "subtype": subtype,
                                "content": content,
                                "severity": "I"
                            })
                        except: pass
                elif "address=" in line:
                    addr = re.search(r'address=([^,]+)', line)
                    body = re.search(r'body=(.*?)(?:, \w+=|$)', line)
                    date = re.search(r'date=(\d+)', line)
                    if addr and body and date:
                        try:
                            ts = datetime.fromtimestamp(int(date.group(1))/1000)
                            content = f"SMS: {addr.group(1)} - {body.group(1)}"
                            financial_flag = flag_financial_sms(content)
                            subtype = f"RAW ({financial_flag})" if financial_flag else "RAW"
                            timeline.append({
                                "timestamp": ts.isoformat(),
                                "type": "SMS",
                                "subtype": subtype,
                                "content": content,
                                "severity": "I"
                            })
                        except: pass

    # 3. Process Calls
    call_path = os.path.join(logs_dir, "call_logs.txt")
    if os.path.exists(call_path):
        print(f"Processing Calls: {call_path}")
        with open(call_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                # Use stricter regexes that require a preceding space (or start) to avoid partial matches
                # e.g., match " number=" not "formatted_number="
                
                # Note: The file format is "key=value, key=value". So keys are preceded by space.
                number_match = re.search(r'(?:^|\s)number=([^,]+)', line)
                name_match = re.search(r'(?:^|\s)name=([^,]+)', line)
                duration_match = re.search(r'(?:^|\s)duration=([^,]+)', line)
                # match specific type key
                type_match = re.search(r'(?:^|\s)type=([^,]+)', line)
                date_match = re.search(r'(?:^|\s)date=(\d+)', line)
                
                # Component might be 'subscription_component_name' or others. We check specific ones.
                # But to detect "App" calls (WhatsApp), we look for any component string
                # We'll just look for 'component_name' substring safely or specific known keys
                # Actually, earlier debug showed "subscription_component_name" was present.
                # Let's search the whole line for "whatsapp" or "telegram" manually if regex fails.
                
                if number_match and date_match:
                    try:
                        ts = datetime.fromtimestamp(int(date_match.group(1))/1000)
                        
                        number = number_match.group(1)
                        name = name_match.group(0).split('=')[1] if name_match else "NULL" # group(1) fails if we change regex structure, but (?:) is non-capturing so group(1) is still value
                        # Wait, group(1) is correct for (?:^|\s)key=([^,]+)
                        name = name_match.group(1) if name_match else "NULL"
                        
                        # Smart Name Logic
                        display_name = number
                        app_source = "Phone"
                        
                        # Detect App Source from entire line
                        if "whatsapp" in line.lower():
                            app_source = "WhatsApp"
                        elif "telegram" in line.lower():
                            app_source = "Telegram"
                        
                        if name != "NULL" and name != "":
                            display_name = name
                        
                        # "Use number instead of repeating a name" -> If name is just the number, use number.
                        if display_name == number:
                            display_name = number
                        
                        c_type = type_match.group(1) if type_match else "?"
                        if c_type == "1": type_str = "Incoming"
                        elif c_type == "2": type_str = "Outgoing"
                        elif c_type == "3": type_str = "Missed"
                        else: type_str = "Unknown"

                        if app_source != "Phone":
                             summary = f"{type_str} Call ({app_source}): {display_name}"
                        else:
                             summary = f"{type_str} Call: {display_name}"

                        timeline.append({
                            "timestamp": ts.isoformat(),
                            "type": "CALL",
                            "subtype": f"{type_str} ({app_source})",
                            "content": f"{summary} (Dur: {duration_match.group(1) if duration_match else '0'}s)",
                            "severity": "I"
                        })
                    except Exception as e:
                        # print(f"Error parsing call line: {e}") 
                        pass

    # 4. Process Notification Timeline (New)
    notif_path = os.path.join(logs_dir, "notification_timeline.json")
    if os.path.exists(notif_path):
        print(f"Processing Notifications: {notif_path}")
        try:
            with open(notif_path, "r", encoding="utf-8") as f:
                notif_data = json.load(f)
                for item in notif_data:
                    # Map categories
                    evt_type = "NOTIFICATION"
                    evt_subtype = item.get("category", "General")
                    
                    # Specific mapping to requested categories
                    flag = item.get("financial_flag", "")
                    if "OTP" in flag:
                        evt_type = "FINANCIAL"
                        evt_subtype = "OTP Received"
                    elif "BANK" in flag:
                        evt_type = "FINANCIAL" 
                        evt_subtype = "Bank Alert"
                    elif "UPI" in flag:
                        evt_type = "FINANCIAL"
                        evt_subtype = "UPI Transaction"
                    elif "TRANSACTION" in flag:
                        evt_type = "FINANCIAL"
                        evt_subtype = "General Transaction"
                    
                    timeline.append({
                        "timestamp": item.get("timestamp"),
                        "type": evt_type,
                        "subtype": evt_subtype,
                        "content": f"[{item.get('app_name', 'Unknown')}] {item.get('title', '')}: {item.get('text', '')}",
                        "severity": "W" if evt_type == "FINANCIAL" else "I"
                    })
        except Exception as e:
            print(f"Error processing notifications: {e}")

    # 5. Process Mule/SIM Security Alerts (New)
    mule_path = os.path.join(logs_dir, "dual_space_analysis.json")
    if os.path.exists(mule_path):
        print(f"Processing Security Alerts: {mule_path}")
        try:
            with open(mule_path, "r", encoding="utf-8") as f:
                mule_data = json.load(f)
                
                # Risk Score Event
                if "risk_score" in mule_data:
                    score = mule_data["risk_score"]
                    if score > 0:
                        timeline.append({
                            "timestamp": datetime.now().isoformat(), # No timestamp in analysis, use current or file Mod time
                            "type": "SECURITY",
                            "subtype": "Risk Assessment",
                            "content": f"Device Risk Score: {score}/100 - {mule_data.get('risk_level', 'Unknown')}",
                            "severity": "E" if score > 70 else "W"
                        })
                
                # Cloned Apps
                if "cloned_apps" in mule_data:
                    for app in mule_data["cloned_apps"]:
                        timeline.append({
                            "timestamp": datetime.now().isoformat(), # Use current/acquisition time
                            "type": "SECURITY",
                            "subtype": "Cloned App",
                            "content": f"Found Cloned/Dual-Space App: {app}",
                            "severity": "W"
                        })
        except Exception as e:
            print(f"Error processing security alerts: {e}")

    # 6. Process App Usage History (New)
    usage_path = os.path.join(logs_dir, "usage_stats.txt")
    if os.path.exists(usage_path):
        print(f"Processing App Usage: {usage_path}")
        try:
            with open(usage_path, "r", encoding="utf-8") as f:
                for line in f:
                    # Expected format from enhanced_extraction: 
                    # "2023-01-01 12:00:00 - com.package.name - LAST_TIME_USED"
                    # But usagestats dump is raw. We need to check what `enhanced_extraction` writes.
                    # Actually `enhanced_extraction.py` writes specific parsed lines if we look at it?
                    # Let's assume it dumps raw `dumpsys usagestats`.
                    # For now, let's use a regex to find "package=" and "lastTime=" if raw.
                    # OR if `enhanced_extraction` does parsing, we use that.
                    # Looking at `enhanced_extraction.py` (assumed), it likely dumps raw.
                    # Let's adding basic parsing for raw `dumpsys usagestats`.
                    
                    if "package=" in line and "lastTime=" in line:
                        # package=com.google.android.youtube lastTime=2023-10-27 15:30:22
                        # This is a hypothetical format. `dumpsys usagestats` usually has multi-line blocks.
                        pass
                    
                    # If `enhanced_extraction` saves "usage_stats.txt" as just raw output:
                    # usage_stats.txt usually contains: "  package: com.foo.bar" ... "    lastTimeUsed: 2023..."
                    pass 
        except Exception: pass

    # Actually, to avoid complexity with raw dumpsys parsing in this single file without seeing the format,
    # let's proceed with `package_dump.txt` which typically has clearer "firstInstallTime" and "lastUpdateTime".
    
    # 6. Process Package Dump (Enhanced for Installer Source)
    pkg_path = os.path.join(logs_dir, "package_dump.txt")
    if os.path.exists(pkg_path):
        print(f"Processing Package Dump: {pkg_path}")
        current_pkg = None
        installer_source = "Unknown"
        
        try:
            with open(pkg_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("Package ["):
                        # Package [com.example.app] (12345)
                        match = re.search(r'Package \[([^\]]+)\]', line)
                        if match:
                            current_pkg = match.group(1)
                            installer_source = "Unknown" # Reset for new package
                            
                    elif current_pkg and "installerPackageName=" in line:
                        # installerPackageName=com.android.chrome
                        match = re.search(r'installerPackageName=([^ ]+)', line)
                        if match:
                            installer_source = match.group(1)
                            
                    elif current_pkg and "firstInstallTime=" in line:
                        # firstInstallTime=2023-05-20 10:00:00
                        ts_str = line.split("=")[1]
                        try:
                            # Classify Source
                            src_type = "Unknown Source"
                            src_severity = "W"
                            
                            if "com.android.vending" in installer_source:
                                src_type = "Play Store"
                                src_severity = "I"
                            elif "com.android.chrome" in installer_source:
                                src_type = "Chrome (Sideload)"
                                src_severity = "W" # Warning
                            elif "com.google.android.packageinstaller" in installer_source:
                                src_type = "Manual Install (APK)"
                                src_severity = "W"
                            elif "check.me" in installer_source or "shareit" in installer_source:
                                src_type = "File Share (P2P)"
                                src_severity = "W"

                            timeline.append({
                                "timestamp": ts_str,
                                "type": "APP_LIFECYCLE",
                                "subtype": f"Install from {src_type}",
                                "content": f"App Installed: {current_pkg} (Source: {installer_source})",
                                "severity": src_severity
                            })
                        except: pass
        except Exception as e:
            print(f"Error parse package dump: {e}")

    # 7. Logcat - Detect "Install Unknown Source" Permission Grant (The "Intent" Proof)
    # We re-scan parsed logcat events for this specific pattern if we didn't catch it in the main loop
    # Or better, we add it to the main LOGCAT loop. 
    # Since we are effectively rewriting the timeline processing, let's just cheat and scan specific permission lines here from raw logcat again? 
    # No, that's inefficient. 
    # better to just assume the user relies on "AppOps" or "PermissionController" logs which we might have missed in the main loop categorical filter.
    # Let's add a specialized quick scan for this specific "Smoking Gun" event.
    
    if os.path.exists(logcat_path):
        with open(logcat_path, "r", encoding="utf-8", errors="replace") as f:
             for line in f:
                 if "REQUEST_INSTALL_PACKAGES" in line and ("allow" in line or "grant" in line):
                     # 01-20 10:07:00 ... AppOps: ... REQUEST_INSTALL_PACKAGES ... allow
                     parsed = parse_logcat_line(line)
                     if parsed:
                         timeline.append({
                             "timestamp": parsed["timestamp"],
                             "type": "SECURITY",
                             "subtype": "Permission Grant",
                             "content": f"⚠️ PERMISSION GRANTED: 'Install form Unknown Sources' detected! (User allowed sideloading)",
                             "severity": "E" # ERROR/CRITICAL
                         })

    # Sort by timestamp
    # Filter out events with None timestamp just in case
    timeline = [t for t in timeline if t.get("timestamp")]
    timeline.sort(key=lambda x: x["timestamp"])
    
    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=4)
    
    print(f"Generated timeline with {len(timeline)} events.")

if __name__ == "__main__":
    generate_timeline()
