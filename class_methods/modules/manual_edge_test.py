import json, importlib.util, os, time, traceback

EXCLUDED_PREFIXES = ["upload_", "send_file", "uploadfile", "upload"]

def should_exclude(name):
    return any(name.lower().startswith(p) for p in EXCLUDED_PREFIXES)

with open("modules/method_list.json") as f:
    methods = json.load(f)

EDGE_CASES = [b"", b"A" * 1000000, b"\x00\xff\xfe", None]

def load_method(file, cls, method):
    try:
        module_name = os.path.splitext(os.path.basename(file))[0]
        full = os.path.join("api", file)
        spec = importlib.util.spec_from_file_location(module_name, full)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        instance = getattr(module, cls)()
        return getattr(instance, method)
    except Exception:
        traceback.print_exc()
        return None

for entry in methods:
    if should_exclude(entry["method"]):
        continue
    method = load_method(entry["file"], entry["class"], entry["method"])
    if not method:
        continue
    for i, edge in enumerate(EDGE_CASES):
        try:
            t0 = time.perf_counter()
            method(edge)
            t1 = time.perf_counter() - t0
            print(f"✅ {entry['method']} test #{i+1} ran in {t1:.2f}s")
        except Exception as e:
            print(f"❌ {entry['method']} test #{i+1}: {e}")
