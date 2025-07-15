from modules.bootstrap import install_dependencies
install_dependencies()

import json
import os

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
    print("📋 First-time fuzzing setup. Define expected input type.\n")
    for method in methods:
        name = f"{method['file']}::{method['class']}::{method['method']}"
        print(f"⚙️ {name}")
        for k, v in TYPES.items():
            print(f"   {k}. {v}")
        choice = ""
        while choice not in TYPES:
            choice = input("   Select input type [1-5]: ").strip()
        entry = {"input_type": TYPES[choice]}
        if TYPES[choice] == "custom":
            entry["seed_input"] = input("   Example input (string): ")
        config[name] = entry
        print("✅ Saved.\n")

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"🧠 Configurations saved to {CONFIG_FILE}")

if __name__ == "__main__":
    if os.path.exists(CONFIG_FILE):
        print(f"✅ Config exists at {CONFIG_FILE}.")
    else:
        prompt_config()
