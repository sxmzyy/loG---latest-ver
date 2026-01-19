import sys
import tkinter as tk
import traceback

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import tkintermapview
    print("✅ tkintermapview imported successfully")
    print(f"Location: {tkintermapview.__file__}")
except ImportError as e:
    print(f"❌ Failed to import tkintermapview: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error during import: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    root = tk.Tk()
    map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
    print("✅ TkinterMapView widget created successfully")
    root.destroy()
except Exception as e:
    print(f"❌ Failed to create map widget: {e}")
    traceback.print_exc()
