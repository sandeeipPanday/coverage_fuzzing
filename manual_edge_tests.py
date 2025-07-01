import json
import importlib.util
import os
import traceback
import time

with open("function_list.json") as f:
    funcs = json.load(f)

EDGE_CASES = [
    b"", b"A"*1000000, b"\x00\xff\xfe", None
]

def load_function(path, name):
    try:
        mod = os.path.splitext(os.path.basename(path))[0]
        full = os.path.join("api", path)
        spec = importlib.util.spec_from_file_location(mod, full)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, name)
    except Exception:
        traceback.print_exc()
        return None

for item in funcs:
    func = load_function(item["file"], item["function"])
    if not func:
        continue
    for i, edge in enumerate(EDGE_CASES):
        try:
            t0 = time.perf_counter()
            func(edge)
            print("✅ {} #{} ran in {:.2f}s".format(item["function"], i+1, time.perf_counter()-t0))
        except Exception as e:
            print("❌ {} test #{}: {}".format(item["function"], i+1, e))
