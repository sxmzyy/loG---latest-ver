import sys
import os

# Add parent directory to path to import reporting
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import reporting
    print("Generating full report...")
    reporting.export_full_report()
    print("Report generation triggered.")
except Exception as e:
    print(f"Failed to generate report: {e}")
    sys.exit(1)
