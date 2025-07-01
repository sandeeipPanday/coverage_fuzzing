import sys
import os
import atheris
import importlib.util
import json
import traceback
import time

LOG_FILE = "fuzz_log.jsonl"
FUNC_LIST_FILE = "function_list.json"

def load_function(file_path, function_name):
    try:
        mod_name = os.path.splitext(os.path.basename(file_path))[0]
        full_path = os.path.join("api", file_path)
        spec = importlib.util.spec_from_file_location(mod_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, function_name)
    except Exception:
        traceback.print_exc()
        return None

def build_targets():
    if not os.path.exists(FUNC_LIST_FILE):
        print("❌ Run detect_functions.py first.")
        sys.exit(1)
    with open(FUNC_LIST_FILE) as f:
        entries = json.load(f)
    targets = []
    for entry in entries:
        func = load_function(entry["file"], entry["function"])
        if func:
            targets.append({"func": func, "info": entry})
    return targets

def log_crash(info, data, error):
    crash = {
        "file": info["file"],
        "function": info["function"],
        "input": repr(data),
        "error": str(error)
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(crash) + "\n")

def TestOneInput(data):
    for target in targets:
        try:
            start = time.perf_counter()
            target["func"](data)
            elapsed = time.perf_counter() - start
            if elapsed > 0.5:
                log_crash(target["info"], data, "⚠️ Slow execution: {:.3f}s".format(elapsed))
        except Exception as e:
            log_crash(target["info"], data, e)

if __name__ == "__main__":
    open(LOG_FILE, "w").close()
    targets = build_targets()
    print("🔬 Fuzzing {} functions...".format(len(targets)))
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()
