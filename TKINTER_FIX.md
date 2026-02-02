# Tkinter Installation Fix for macOS (pyenv)

## Problem
Your Python installation (via pyenv) was compiled without tkinter support.

## Solution

### Option 1: Reinstall Python with tkinter support (Recommended)

```bash
# Install tcl-tk via Homebrew
brew install tcl-tk

# Set environment variables for pyenv
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/usr/local/opt/tcl-tk/lib/pkgconfig"

# Reinstall Python 3.11.9 with tkinter
pyenv uninstall 3.11.9
pyenv install 3.11.9

# Verify tkinter works
python -c "import tkinter; print('tkinter works!')"
```

### Option 2: Use system Python (Quick fix)

```bash
# Use macOS system Python (has tkinter built-in)
/usr/bin/python3 main.py

# If dependencies missing, install them:
/usr/bin/python3 -m pip install --user -r requirements.txt
```

### Option 3: Use Python 3 from Homebrew

```bash
# Install Python via Homebrew (includes tkinter)
brew install python@3.11

# Use it directly
/usr/local/bin/python3 main.py

# Or set it as default temporarily
alias python="/usr/local/bin/python3"
```

## Verify Installation

After fixing, test with:
```bash
python -c "import tkinter; print('✅ tkinter works!')"
```

## Then Run the Tool

```bash
cd /Users/fsociety/Downloads/android-forensic-tool-master
python main.py
```
