
import json
import os
from datetime import datetime, timedelta

def inject_data():
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # 1. Inject Notification Timeline Data
    notif_file = os.path.join(logs_dir, "notification_timeline.json")
    
    # Generate some timestamps relative to now
    now = datetime.now()
    
    notifications = [
        {
            "timestamp": (now - timedelta(minutes=10)).isoformat(),
            "package": "com.google.android.apps.messaging",
            "app_name": "Messages",
            "title": "HDFC-BANK",
            "text": "Your OTP is 123456 for transaction at Amazon.",
            "category": "OTP"
        },
        {
            "timestamp": (now - timedelta(minutes=45)).isoformat(),
            "package": "com.phonepe.app",
            "app_name": "PhonePe",
            "title": "Payment Received",
            "text": "Received Rs. 5000 from Ravi Kumar.",
            "category": "UPI"
        },
        {
            "timestamp": (now - timedelta(hours=2)).isoformat(),
            "package": "com.android.systemui",
            "app_name": "System UI",
            "title": "USB Debugging",
            "text": "USB Debugging connected",
            "category": "General"
        }
    ]
    
    with open(notif_file, "w") as f:
        json.dump(notifications, f, indent=4)
    print(f"Injected {len(notifications)} notifications.")

    # 2. Inject Dual Space Security Data
    mule_file = os.path.join(logs_dir, "dual_space_analysis.json")
    
    mule_data = {
        "risk_score": 85,
        "risk_level": "CRITICAL",
        "cloned_apps": ["com.whatsapp", "com.phonepe.app"],
        "sim_swaps": [
            {
                "timestamp": (now - timedelta(days=1)).isoformat(),
                "details": "SIM State changed from LOADED to ABSENT"
            }
        ]
    }
    
    with open(mule_file, "w") as f:
        json.dump(mule_data, f, indent=4)
    print("Injected Dual Space analysis data.")

if __name__ == "__main__":
    inject_data()
