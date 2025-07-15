import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(script_dir, "..")))
from modules.bootstrap import install_dependencies
install_dependencies()

import json

CONFIG_FILE = "fuzz_config.json"
METHODS_FILE = "modules/method_list.json"

TYPES = {
    "1": "str",
    "2": "int",
    "3": "bytes",
    "4": "json",
    "5": "custom"
}

def prompt_config():
    if not os.path.exists(METHODS_FILE):
        print("❌ Run detect_methods.py first.")
        return

    with open(METHODS_FILE, "r", encoding="utf-8") as f:
        methods = json.load(f)

    config = {}
    print("📋 Configure fuzzing input types per method.\n")
    for method in methods:
        name = f"{method['file']}::{method['class']}::{method['method']}"
        print(f"⚙️ {name}")
        for k, v in TYPES.items():
            print(f"   {k}. {v}")
        choice = ""
        while choice not in TYPES:
            choice = input("   Select [1-5]: ").strip()
        entry = {"input_type": TYPES[choice]}
        if TYPES[choice] == "custom":
            entry["seed_input"] = input("   Example input string: ")
        config[name] = entry
        print("✅ Saved.\n")

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"🧠 Configuration saved to {CONFIG_FILE}")

if __name__ == "__main__":
    if os.path.exists(CONFIG_FILE):
        print(f"✅ Configuration already exists at {CONFIG_FILE}")
    else:
        prompt_config()
