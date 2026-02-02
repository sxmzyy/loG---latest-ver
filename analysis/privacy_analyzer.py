
import os
import json
import re

def analyze_privacy(logs_dir="logs", output_file="logs/privacy_profile.json"):
    logcat_path = os.path.join(logs_dir, "android_logcat.txt")
    if not os.path.exists(logcat_path):
        return

    profile = {
        "location": [],
        "camera": [],
        "microphone": [],
        "contacts": [],
        "biometrics": [],
        "clipboard": [],
        "summary": {}
    }

    # Expanded patterns including more specific and modern Android services
    patterns = {
        "location": r'LocationManager|gps|LocationService|fused|GnssLocationProv|getLastLocation',
        "camera": r'CameraService|CameraDevice|Camera2|CameraManager',
        "microphone": r'AudioRecord|AudioSource|Microphone|AudioService.*startRecording',
        "contacts": r'ContactsProvider|ContactMetadata|Querying content://com\.android\.contacts',
        "biometrics": r'BiometricService|FingerprintService|FaceService|auth_biometric',
        "clipboard": r'ClipboardService|setPrimaryClip|getPrimaryClip'
    }

    # Regex to catch package names in logcat (often in square brackets or as 'pkg=...')
    PKG_REGEX = re.compile(r'(?:pkg=|packageName=|\[)([a-z][a-z0-9_]*\.[a-z0-9_.]*[a-z0-9_])', re.I)

    with open(logcat_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            for key, pattern in patterns.items():
                if re.search(pattern, line, re.I):
                    pkg_match = PKG_REGEX.search(line)
                    pkg_name = pkg_match.group(1) if pkg_match else "System/Unknown"
                    
                    profile[key].append({
                        "package": pkg_name,
                        "content": line.strip()
                    })

    # Count hits
    for key in patterns.keys():
        profile["summary"][key] = len(profile[key])

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)
    
    print("Generated enhanced privacy profile.")

if __name__ == "__main__":
    analyze_privacy()
