import re

# Test parsing
with open("logs/dump_package.txt", "r", encoding="utf-8", errors="replace") as f:
    current_package = None
    package_data = {}
    count = 0
    
    for line in f:
        if "Package [" in line and "] (" in line:
            # Process previous
            if current_package:
                print(f"\nPackage: {current_package}")
                print(f"  Installer: {package_data.get('installer', 'NOT FOUND')}")
                print(f"  System: {package_data.get('is_system', False)}")
                print(f"  Install Time: {package_data.get('install_time', 'NOT FOUND')}")
                
                if package_data.get("installer") == "null" and not package_data.get("is_system", False):
                    print("  >>> SIDELOAD DETECTED!")
                    count += 1
            
            # Start new
            match = re.search(r'Package \[([^\]]+)\]', line)
            if match:
                current_package = match.group(1)
                package_data = {}
        
        elif current_package:
            if "pkgFlags=[ SYSTEM" in line or "privateFlags=[ SYSTEM" in line or "flags=[ SYSTEM" in line:
                package_data["is_system"] = True
            
            if "installerPackageName=" in line:
                match = re.search(r'installerPackageName=([^\s]+)', line)
                if match:
                    package_data["installer"] = match.group(1)
            
            if "firstInstallTime=" in line:
                match = re.search(r'firstInstallTime=(.+)', line)
                if match:
                    package_data["install_time"] = match.group(1).strip()
    
    # Last package
    if current_package:
        print(f"\nPackage: {current_package}")
        print(f"  Installer: {package_data.get('installer', 'NOT FOUND')}")
        print(f"  System: {package_data.get('is_system', False)}")
        if package_data.get("installer") == "null" and not package_data.get("is_system", False):
            print("  >>> SIDELOAD DETECTED!")
            count += 1

print(f"\n\nTotal sideloads found: {count}")
