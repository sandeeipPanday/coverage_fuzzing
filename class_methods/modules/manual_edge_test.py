import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.bootstrap import install_dependencies
install_dependencies()

import json, importlib.util, traceback, time

EDGE_CASES = [b"", b"A" * 1000000, b"\x00\xff\xfe", None]

def load_method(file, cls, method):
    try:
        mod_name = os.path.splitext(os.path.basename(file))[0]
        full_path = os.path.join("api", file)
        spec = importlib.util.spec_from_file_location(mod_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        instance = getattr(module, cls)()
        return getattr(instance, method)
    except Exception:
        traceback.print_exc()
        return None

with open("modules/method_list.json") as f:
    methods = json.load(f)

for entry
