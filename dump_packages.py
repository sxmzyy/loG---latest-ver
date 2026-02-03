
import subprocess

def dump_packages():
    print("Dumping packages...")
    with open("logs/full_package_dump_utf8.txt", "w", encoding="utf-8") as f:
        subprocess.run(["adb", "shell", "pm", "list", "packages", "-f", "-U"], stdout=f, check=True)
    print("Dump complete: logs/full_package_dump_utf8.txt")

if __name__ == "__main__":
    dump_packages()
