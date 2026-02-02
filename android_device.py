"""
android_device.py

Android device implementation using ADB.
Wraps existing Android functionality into the unified device interface.
"""

import subprocess
import os
from device_interface import DeviceInterface
from scripts.android_logs import get_logcat, get_call_logs, get_sms_logs
from scripts.detect_log_buffer import get_device_info as get_android_device_info


class AndroidDevice(DeviceInterface):
    """Android device implementation."""
    
    def __init__(self):
        super().__init__()
        self.platform = "android"
    
    def detect_device(self) -> bool:
        """Check if Android device is connected via ADB."""
        try:
            result = subprocess.run(
                ['adb', 'devices'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Parse output for connected devices
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            connected_devices = [line for line in lines if 'device' in line and 'offline' not in line]
            
            self.is_connected = len(connected_devices) > 0
            
            if self.is_connected and connected_devices:
                # Get device ID
                self.device_id = connected_devices[0].split('\t')[0]
            
            return self.is_connected
            
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self.is_connected = False
            return False
    
    def get_device_info(self) -> dict:
        """Get Android device information."""
        if not self.is_connected:
            return {'error': 'Device not connected'}
        
        try:
            # Use existing get_device_info from detect_log_buffer
            info = get_android_device_info()
            
            if info['success']:
                self.device_model = info['device_model']
                self.os_version = f"Android {info['android_version']}"
                
                return {
                    'platform': 'Android',
                    'model': self.device_model,
                    'os_version': self.os_version,
                    'device_id': self.device_id
                }
            else:
                return {'error': info.get('error', 'Unknown error')}
                
        except Exception as e:
            return {'error': str(e)}
    
    def extract_system_logs(self, output_path: str) -> bool:
        """Extract Android logcat."""
        try:
            # Ensure logs directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Use existing get_logcat function
            get_logcat()
            
            return True
        except Exception as e:
            print(f"Error extracting Android logs: {e}")
            return False
    
    def extract_crash_reports(self, output_dir: str) -> bool:
        """Extract Android crash reports from logcat."""
        # Android crash info is in logcat with "AndroidRuntime: FATAL EXCEPTION"
        # Already extracted with system logs
        return True
    
    def extract_call_logs(self) -> bool:
        """Extract call logs."""
        try:
            get_call_logs()
            return True
        except Exception as e:
            print(f"Error extracting call logs: {e}")
            return False
    
    def extract_sms_logs(self) -> bool:
        """Extract SMS logs."""
        try:
            get_sms_logs()
            return True
        except Exception as e:
            print(f"Error extracting SMS logs: {e}")
            return False


if __name__ == '__main__':
    print("Android Device Module Test\n")
    
    device = AndroidDevice()
    
    if device.detect_device():
        print("✅ Android device detected!")
        info = device.get_device_info()
        print(f"   Model: {info.get('model')}")
        print(f"   OS: {info.get('os_version')}")
        
        print("\nExtracting logs...")
        device.extract_system_logs("logs/android_logcat.txt")
        print("✅ Logs extracted!")
    else:
        print("❌ No Android device connected")
        print("   Connect device via USB and enable USB debugging")
