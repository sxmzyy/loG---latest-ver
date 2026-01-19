"""
device_interface.py

Abstract base class for Android device forensic analysis.
Provides unified interface for Android devices.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List


class DeviceInterface(ABC):
    """Abstract base class for mobile devices."""
    
    def __init__(self):
        self.device_id: Optional[str] = None
        self.device_model: Optional[str] = None
        self.os_version: Optional[str] = None
        self.is_connected: bool = False
    
    @abstractmethod
    def detect_device(self) -> bool:
        """
        Check if device is connected and accessible.
        
        Returns:
            bool: True if device detected and accessible
        """
        pass
    
    @abstractmethod
    def get_device_info(self) -> Dict[str, str]:
        """
        Get device information (model, OS version, etc.).
        
        Returns:
            dict: Device information
        """
        pass
    
    @abstractmethod
    def extract_system_logs(self, output_path: str) -> bool:
        """
        Extract system logs from the device.
        
        Args:
            output_path: Path to save logs
        
        Returns:
            bool: True if successful
        """
        pass
    
    @abstractmethod
    def extract_crash_reports(self, output_dir: str) -> bool:
        """
        Extract crash reports from the device.
        
        Args:
            output_dir: Directory to save crash reports
        
        Returns:
            bool: True if successful
        """
        pass
    
    def get_platform(self) -> str:
        """Get platform name (android)."""
        return self.__class__.__name__.replace('Device', '').lower()


def detect_connected_devices() -> List[DeviceInterface]:
    """
    Auto-detect all connected Android devices.
    
    Returns:
        List of connected devices
    """
    from android_device import AndroidDevice
    
    devices = []
    
    # Check for Android devices
    android = AndroidDevice()
    if android.detect_device():
        devices.append(android)
    
    return devices


def get_primary_device() -> Optional[DeviceInterface]:
    """
    Get the first connected device.
    
    Returns:
        DeviceInterface or None if no devices connected
    """
    devices = detect_connected_devices()
    return devices[0] if devices else None


if __name__ == '__main__':
    print("Device Interface - Testing auto-detection\n")
    
    devices = detect_connected_devices()
    
    if not devices:
        print("❌ No devices detected")
        print("   Connect an Android device and try again.")
    else:
        print(f"✅ Found {len(devices)} device(s):\n")
        for device in devices:
            info = device.get_device_info()
            print(f"   Platform: {device.get_platform().upper()}")
            print(f"   Model: {info.get('model', 'Unknown')}")
            print(f"   OS Version: {info.get('os_version', 'Unknown')}")
            print()
