import sys
import os

# Add parent directory to path to import reporting
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import reporting
    print("Successfully imported reporting module.")
except Exception as e:
    print(f"Failed to import reporting: {e}")
    sys.exit(1)

try:
    print("Calling _collect_context()...")
    context = reporting._collect_context()
    device = context.get("device", {})
    
    print("\n--- Device Information ---")
    print(f"Model: {device.get('model')}")
    print(f"Android Version: {device.get('android_version')}")
    print(f"Kernel: {device.get('kernel')}")
    
    if device.get("model") == "Unknown" or device.get("android_version") == "Unknown":
        print("\nFAILURE: Device info is still Unknown.")
        sys.exit(1)
    else:
        print("\nSUCCESS: Device info retrieved.")
        sys.exit(0)

except Exception as e:
    print(f"\nError during verification: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
