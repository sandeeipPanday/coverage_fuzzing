import subprocess
import sys
import importlib

REQUIRED_PACKAGES = [
    "atheris",
    "matplotlib",
    "rich"
]

def install_dependencies():
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError:
            print(f"📦 Installing missing package: {pkg}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
