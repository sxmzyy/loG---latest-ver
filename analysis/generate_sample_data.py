"""
Sample Data Generator for Android Forensic Tool
Creates realistic test data for all forensic modules for demo/testing purposes
"""

import os
import json
import random
from datetime import datetime, timedelta

class SampleDataGenerator:
    def __init__(self, output_dir="logs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Sample data pools
        self.sample_apps = [
            "com.whatsapp", "com.facebook.katana", "com.instagram.android",
            "com.twitter.android", "com.snapchat.android", "com.spotify.music",
            "com.netflix.mediaclient", "com.google.android.youtube",
            "com.android.chrome", "com.android.vending"
        ]
        
        self.sample_contacts = [
            "+1234567890", "+9876543210", "+1122334455",
            "+5544332211", "+9988776655", "+1231231234"
        ]
        
        self.sample_ssids = [
            "HomeWiFi_5G", "Starbucks_Guest", "Airport_Free_WiFi",
            "Office_Network", "Hotel_Lobby", "Neighbor_WiFi"
        ]
        
        self.sample_domains = [
            "api.example.com", "cdn.contentserver.net", "analytics.tracker.io",
            "api.socialnetwork.com", "updates.appstore.com"
        ]
        
        self.base_time = datetime.now() - timedelta(days=7)
    
    def generate_all(self):
        """Generate all sample data files"""
        print("🔄 Generating sample forensic data...")
        print("=" * 60)
        
        self.generate_logcat()
        self.generate_sms()
        self.generate_calls()
        self.generate_unified_timeline()
        self.generate_privacy_profile()
        self.generate_pii_leaks()
        self.generate_network_activity()
        self.generate_social_graph()
        self.generate_power_forensics()
        self.generate_intent_hunter()
        self.generate_beacon_map()
        self.generate_clipboard_forensics()
        self.generate_app_sessions()
        self.generate_evidence_metadata()
        
        print("=" * 60)
        print("✅ Sample data generation complete!")
        print(f"📁 Data saved to: {os.path.abspath(self.output_dir)}")
    
    def random_timestamp(self, days_ago_max=7):
        """Generate random timestamp within last N days"""
        offset = random.randint(0, days_ago_max * 24 * 60 * 60)
        return (self.base_time + timedelta(seconds=offset)).isoformat()
    
    def generate_logcat(self):
        """Generate sample logcat file"""
        print("📝 Generating logcat...")
        lines = []
        
        for i in range(500):
            timestamp = self.random_timestamp()
            pid = random.randint(1000, 9999)
            tid = random.randint(1000, 9999)
            priority = random.choice(['V', 'D', 'I', 'W', 'E'])
            tag = random.choice(self.sample_apps + ['System', 'ActivityManager', 'WifiManager'])
            message = f"Sample log message {i}"
            
            line = f"{timestamp[-19:]} {pid:5d} {tid:5d} {priority} {tag}: {message}\n"
            lines.append(line)
        
        with open(os.path.join(self.output_dir, "android_logcat.txt"), "w") as f:
            f.writelines(lines)
        
        print(f"  ✓ Created {len(lines)} logcat entries")
    
    def generate_sms(self):
        """Generate sample SMS logs"""
        print("💬 Generating SMS logs...")
        lines = []
        
        for i in range(50):
            timestamp = self.random_timestamp()
            direction = random.choice(['INBOX', 'SENT'])
            contact = random.choice(self.sample_contacts)
            message = f"Sample SMS message {i}"
            
            line = f"{timestamp} | {direction} | {contact} | {message}\n"
            lines.append(line)
        
        with open(os.path.join(self.output_dir, "sms_logs.txt"), "w") as f:
            f.writelines(lines)
        
        print(f"  ✓ Created {len(lines)} SMS entries")
    
    def generate_calls(self):
        """Generate sample call logs"""
        print("📞 Generating call logs...")
        lines = []
        
        for i in range(30):
            timestamp = self.random_timestamp()
            call_type = random.choice(['INCOMING', 'OUTGOING', 'MISSED'])
            contact = random.choice(self.sample_contacts)
            duration = random.randint(10, 600)
            
            line = f"{timestamp} | {call_type} | {contact} | {duration}\n"
            lines.append(line)
        
        with open(os.path.join(self.output_dir, "call_logs.txt"), "w") as f:
            f.writelines(lines)
        
        print(f"  ✓ Created {len(lines)} call entries")
    
    def generate_unified_timeline(self):
        """Generate unified timeline JSON"""
        print("📅 Generating unified timeline...")
        
        events = []
        for i in range(100):
            event = {
                "timestamp": self.random_timestamp(),
                "type": random.choice(['logcat', 'sms', 'call']),
                "source": random.choice(self.sample_apps),
                "message": f"Timeline event {i}"
            }
            events.append(event)
        
        events.sort(key=lambda x: x['timestamp'])
        
        with open(os.path.join(self.output_dir, "unified_timeline.json"), "w") as f:
            json.dump(events, f, indent=4)
        
        print(f"  ✓ Created {len(events)} timeline events")
    
    def generate_privacy_profile(self):
        """Generate privacy profile JSON"""
        print("🔒 Generating privacy profile...")
        
        categories = {
            "Location": random.randint(10, 50),
            "Camera": random.randint(5, 20),
            "Microphone": random.randint(3, 15),
            "Contacts": random.randint(8, 25),
            "Biometrics": random.randint(2, 10),
            "Clipboard": random.randint(5, 15)
        }
        
        details = []
        for category, count in categories.items():
            for i in range(count):
                details.append({
                    "category": category,
                    "package": random.choice(self.sample_apps),
                    "timestamp": self.random_timestamp(),
                    "raw": f"Access to {category} by app"
                })
        
        data = {"summary": categories, "details": details}
        
        with open(os.path.join(self.output_dir, "privacy_profile.json"), "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"  ✓ Created privacy profile with {sum(categories.values())} access events")
    
    def generate_pii_leaks(self):
        """Generate PII leaks JSON"""
        print("🔍 Generating PII leaks...")
        
        leaks = []
        pii_types = ["EMAIL", "AUTH_TOKEN", "GPS_COORDINATE", "API_KEY"]
        
        for i in range(15):
            leaks.append({
                "type": random.choice(pii_types),
                "value": f"sample_pii_{i}@example.com" if "EMAIL" in pii_types else f"sample_value_{i}",
                "timestamp": self.random_timestamp(),
                "line": random.randint(100, 5000),
                "raw": f"Log line containing PII {i}"
            })
        
        with open(os.path.join(self.output_dir, "pii_leaks.json"), "w") as f:
            json.dump(leaks, f, indent=4)
        
        print(f"  ✓ Created {len(leaks)} PII leak entries")
    
    def generate_network_activity(self):
        """Generate network activity JSON"""
        print("🌐 Generating network activity...")
        
        connections = []
        for i in range(30):
            connections.append({
                "type": random.choice(["IP", "DOMAIN"]),
                "value": random.choice(self.sample_domains) if random.random() > 0.5 else f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
                "count": random.randint(1, 20),
                "last_context": f"Connection attempt {i}"
            })
        
        with open(os.path.join(self.output_dir, "network_activity.json"), "w") as f:
            json.dump(connections, f, indent=4)
        
        print(f"  ✓ Created {len(connections)} network connections")
    
    def generate_social_graph(self):
        """Generate social graph JSON"""
        print("👥 Generating social graph...")
        
        nodes = [{"id": "DEVICE", "label": "This Device", "value": 10, "group": "device"}]
        edges = []
        
        for contact in self.sample_contacts[:5]:
            nodes.append({"id": contact, "label": contact, "value": random.randint(1, 10), "group": "contact"})
            edges.append({"from": "DEVICE", "to": contact, "value": random.randint(1, 20)})
        
        data = {"nodes": nodes, "edges": edges}
        
        with open(os.path.join(self.output_dir, "social_graph.json"), "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"  ✓ Created social graph with {len(nodes)} nodes")
    
    def generate_power_forensics(self):
        """Generate power forensics JSON"""
        print("🔋 Generating power forensics...")
        
        events = []
        event_types = ["SCREEN_ON", "SCREEN_OFF", "PLUGGED_AC", "UNPLUGGED", "USER_PRESENT"]
        
        for i in range(40):
            events.append({
                "timestamp": self.random_timestamp(),
                "event": random.choice(event_types),
                "raw": f"Power event log line {i}"
            })
        
        events.sort(key=lambda x: x['timestamp'])
        
        with open(os.path.join(self.output_dir, "power_forensics.json"), "w") as f:
            json.dump(events, f, indent=4)
        
        print(f"  ✓ Created {len(events)} power events")
    
    def generate_intent_hunter(self):
        """Generate intent hunter JSON"""
        print("🎯 Generating intent hunter...")
        
        findings = []
        actions = ["VIEW", "SEARCH", "SEND", "DIAL"]
        
        for i in range(20):
            findings.append({
                "type": random.choice(["INTENT", "URL"]),
                "action": random.choice(actions),
                "data": f"https://example.com/page{i}",
                "component": random.choice(self.sample_apps),
                "line": random.randint(100, 5000),
                "raw": f"Intent log line {i}"
            })
        
        with open(os.path.join(self.output_dir, "intent_hunter.json"), "w") as f:
            json.dump(findings, f, indent=4)
        
        print(f"  ✓ Created {len(findings)} intent/URL entries")
    
    def generate_beacon_map(self):
        """Generate beacon map JSON"""
        print("📡 Generating beacon map...")
        
        wifi = []
        for ssid in self.sample_ssids:
            wifi.append({
                "ssid": ssid,
                "count": random.randint(1, 50),
                "first_seen": self.random_timestamp(),
                "last_seen": self.random_timestamp(),
                "contexts": [f"WiFi scan log {i}" for i in range(3)]
            })
        
        bluetooth = []
        for i in range(5):
            bluetooth.append({
                "identifier": f"BT:DEVICE:{i}",
                "name": f"Bluetooth Device {i}",
                "address": f"AA:BB:CC:DD:EE:{i:02X}",
                "count": random.randint(1, 30),
                "first_seen": self.random_timestamp(),
                "last_seen": self.random_timestamp(),
                "contexts": [f"BT scan log {i}"]
            })
        
        data = {
            "wifi_networks": wifi,
            "bluetooth_devices": bluetooth,
            "summary": {
                "total_wifi_networks": len(wifi),
                "total_bluetooth_devices": len(bluetooth),
                "total_wifi_events": sum(w["count"] for w in wifi),
                "total_bluetooth_events": sum(b["count"] for b in bluetooth)
            }
        }
        
        with open(os.path.join(self.output_dir, "beacon_map.json"), "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"  ✓ Created beacon map with {len(wifi)} WiFi + {len(bluetooth)} BT")
    
    def generate_clipboard_forensics(self):
        """Generate clipboard forensics JSON"""
        print("📋 Generating clipboard forensics...")
        
        clipboard_events = []
        ime_events = []
        
        for i in range(10):
            clipboard_events.append({
                "type": "CLIPBOARD",
                "content": f"Sample copied text {i}",
                "package": random.choice(self.sample_apps),
                "is_sensitive": random.random() < 0.3,
                "timestamp": self.random_timestamp(),
                "line": random.randint(100, 5000),
                "raw": f"Clipboard log {i}"
            })
        
        for i in range(15):
            ime_events.append({
                "type": "IME",
                "event_type": random.choice(["TEXT_LENGTH", "TEXT_CONTENT"]),
                "content": f"{random.randint(10, 100)} chars",
                "is_sensitive": random.random() < 0.2,
                "timestamp": self.random_timestamp(),
                "line": random.randint(100, 5000),
                "raw": f"IME log {i}"
            })
        
        data = {
            "clipboard_events": clipboard_events,
            "ime_events": ime_events,
            "summary": {
                "total_clipboard_events": len(clipboard_events),
                "total_ime_events": len(ime_events),
                "sensitive_clipboard_events": sum(1 for e in clipboard_events if e["is_sensitive"]),
                "sensitive_ime_events": sum(1 for e in ime_events if e["is_sensitive"])
            }
        }
        
        with open(os.path.join(self.output_dir, "clipboard_forensics.json"), "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"  ✓ Created clipboard data with {len(clipboard_events)} + {len(ime_events)} events")
    
    def generate_app_sessions(self):
        """Generate app sessions JSON"""
        print("⏱️ Generating app sessions...")
        
        sessions = []
        app_stats = []
        
        for app in self.sample_apps[:6]:
            session_count = random.randint(3, 10)
            total_duration = 0
            
            for i in range(session_count):
                duration = random.randint(30, 1800)
                total_duration += duration
                
                sessions.append({
                    "package": app,
                    "start_time": self.random_timestamp(),
                    "end_time": self.random_timestamp(),
                    "duration_seconds": duration,
                    "duration_human": f"{duration // 60}m {duration % 60}s",
                    "start_line": random.randint(100, 5000),
                    "end_line": random.randint(100, 5000)
                })
            
            app_stats.append({
                "package": app,
                "total_duration": total_duration,
                "session_count": session_count,
                "first_use": self.random_timestamp(),
                "last_use": self.random_timestamp(),
                "avg_session_duration": total_duration // session_count,
                "total_duration_human": f"{total_duration // 3600}h {(total_duration % 3600) // 60}m",
                "avg_session_duration_human": f"{(total_duration // session_count) // 60}m"
            })
        
        data = {
            "sessions": sessions,
            "app_statistics": app_stats,
            "summary": {
                "total_sessions": len(sessions),
                "unique_apps": len(app_stats),
                "total_usage_time": sum(s["duration_seconds"] for s in sessions),
                "total_usage_time_human": "12h 34m"
            }
        }
        
        with open(os.path.join(self.output_dir, "app_sessions.json"), "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"  ✓ Created {len(sessions)} app sessions")
    
    def generate_evidence_metadata(self):
        """Generate evidence metadata JSON with hashes"""
        print("🔐 Generating evidence metadata...")
        
        import hashlib
        
        files = {}
        log_files = [
            "android_logcat.txt", "sms_logs.txt", "call_logs.txt",
            "unified_timeline.json", "privacy_profile.json", "pii_leaks.json",
            "network_activity.json", "social_graph.json", "power_forensics.json",
            "intent_hunter.json", "beacon_map.json", "clipboard_forensics.json",
            "app_sessions.json"
        ]
        
        for filename in log_files:
            filepath = os.path.join(self.output_dir, filename)
            if os.path.exists(filepath):
                # Generate real hash
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                files[filename] = {
                    "hash": file_hash,
                    "size_bytes": os.path.getsize(filepath),
                    "created": datetime.now().isoformat(),
                    "modified": datetime.now().isoformat(),
                    "description": f"Sample {filename}",
                    "verified": True,
                    "last_verification": datetime.now().isoformat()
                }
        
        metadata = {
            "files": files,
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        with open(os.path.join(self.output_dir, "evidence_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)
        
        print(f"  ✓ Generated metadata for {len(files)} files")

if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.generate_all()
    
    print("\n💡 Tip: Now navigate to the web interface to see the sample data!")
    print("   All forensic modules will show realistic test data.")
