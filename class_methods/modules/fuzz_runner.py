import sys, os, atheris, importlib.util, json, traceback, time

LOG_FILE = "fuzz_log.jsonl"
METHOD_LIST_FILE = "modules/method_list.json"
CORPUS_DIR = "corpus"

MAX_EXECUTIONS = 5000
MAX_CORPUS_FILES = 1000
MAX_LEN = 1024
exec_counter = [0]

def load_class_method(file_path, class_name, method_name):
    try:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        full_path = os.path.join("api", file_path)
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls = getattr(module, class_name)
        instance = cls()
        return getattr(instance, method_name)
    except Exception:
        traceback.print_exc()
        return None

def build_targets():
    with open(METHOD_LIST_FILE, "r") as f:
        entries = json.load(f)
    targets = []
    for entry in entries:
        m = load_class_method(entry["file"], entry["class"], entry["method"])
        if m:
            targets.append({"method": m, "info": entry})
    return targets

def log_crash(info, data, error):
    crash = {
        "file": info["file"],
        "class": info["class"],
        "method": info["method"],
        "input": repr(data),
        "error": str(error),
        "type": "atheris-class"
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(crash) + "\n")
    if not os.path.exists(CORPUS_DIR):
        os.makedirs(CORPUS_DIR)
    if len(os.listdir(CORPUS_DIR)) < MAX_CORPUS_FILES:
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
    try:
        decoded = data.decode("utf-8", errors="ignore")
    except Exception:
        return
    for target in targets:
        try:
            start = time.perf_counter()
            target["method"](decoded)
            elapsed = time.perf_counter() - start
            if elapsed > 0.5:
                log_crash(target["info"], data, f"⚠️ Slow: {elapsed:.3f}s")
        except Exception as e:
            log_crash(target["info"], data, e)

if __name__ == "__main__":
    open(LOG_FILE, "w").close()
    targets = build_targets()
    atheris.Setup([sys.argv[0], CORPUS_DIR], TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()
