import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.bootstrap import install_dependencies
install_dependencies()

import atheris, importlib.util, json, traceback, time

LOG_FILE = "fuzz_log.jsonl"
METHOD_LIST_FILE = "modules/method_list.json"
CONFIG_FILE = "fuzz_config.json"
CORPUS_DIR = "corpus"
MAX_EXECUTIONS = 5000
MAX_LEN = 1024
exec_counter = [0]

def load_class_method(file_path, class_name, method_name):
    try:
        mod_name = os.path.splitext(os.path.basename(file_path))[0]
        full_path = os.path.join("api", file_path)
        spec = importlib.util.spec_from_file_location(mod_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        instance = getattr(module, class_name)()
        return getattr(instance, method_name)
    except Exception:
        traceback.print_exc()
        return None

def build_targets():
    with open(METHOD_LIST_FILE) as f:
        entries = json.load(f)
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    targets = []
    for entry in entries:
        method = load_class_method(entry["file"], entry["class"], entry["method"])
        key = f"{entry['file']}::{entry['class']}::{entry['method']}"
        if method and key in config:
            targets.append({
                "method": method,
                "info": entry,
                "config": config[key]
            })
    return targets

def mutate_input(data, input_type, seed=None):
    try:
        decoded = data.decode("utf-8", errors="ignore")
        if input_type == "int":
            return int(decoded) if decoded.strip().isdigit() else 0
        elif input_type == "bytes":
            return data
        elif input_type == "json":
            import json5
            return json5.loads(decoded)
        elif input_type == "custom" and seed:
            return seed.replace("FUZZ", decoded)
        return decoded
    except Exception:
        return None

def log_event(info, data, error=None, status="fail"):
    err_msg = ""
    if error:
        err_type = type(error).__name__
        err_msg = f"{err_type}: {str(error)}"
    record = {
        "file": info["file"],
        "class": info["class"],
        "method": info["method"],
        "input": repr(data),
        "error": err_msg,
        "status": status,
        "type": "atheris-class"
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")
    if status == "fail":
        os.makedirs(CORPUS_DIR, exist_ok=True)
        if len(os.listdir(CORPUS_DIR)) < 1000:
            ts = int(time.time() * 1000)
            with open(os.path.join(CORPUS_DIR, f"crash_{ts}.input"), "wb") as f:
                f.write(data)

def TestOneInput(data):
    exec_counter[0] += 1
    if exec_counter[0] > MAX_EXECUTIONS:
        print(f"\n🛑 Stopping after {MAX_EXECUTIONS}")
        os._exit(0)
    if len(data) > MAX_LEN:
        return
    for target in targets:
        try:
            fuzzed = mutate_input(data, target["config"]["input_type"], target["config"].get("seed_input"))
            if fuzzed is None:
                continue
            target["method"](fuzzed)
            log_event(target["info"], data, status="pass")
        except Exception as e:
            log_event(target["info"], data, error=e, status="fail")

if __name__ == "__main__":
    os.makedirs(CORPUS_DIR, exist_ok=True)
    open(LOG_FILE, "w").close()
    targets = build_targets()
    atheris.Setup([sys.argv[0], CORPUS_DIR], TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()
