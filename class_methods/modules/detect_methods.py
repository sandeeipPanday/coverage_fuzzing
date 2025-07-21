import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.bootstrap import install_dependencies
install_dependencies()

import ast, json

EXCLUDE_KEYWORDS = [
    "decrypt",
    "load_pem_private_key",
    "load_key",
    "get_private_key",
    "sign",
    "verify",
    "ssl",
    "certificate",
    "private"
]

def should_exclude(method_name):
    method_name_lower = method_name.lower()
    return any(kw in method_name_lower for kw in EXCLUDE_KEYWORDS)

def extract_class_methods(file_path, repo_path):
    class_methods = []
    rel_path = os.path.relpath(file_path, repo_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name != "__init__" and not should_exclude(item.name):
                            class_methods.append({
                                "file": rel_path,
                                "class": node.name,
                                "method": item.name
                            })
    except Exception as e:
        print(f"⚠️ Skipped {file_path}: {e}")
    return class_methods

def scan_repo(repo_path):
    all_methods = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                all_methods.extend(extract_class_methods(full_path, repo_path))
    return all_methods

if __name__ == "__main__":
    base_dir = os.path.join(os.getcwd(), "api")
    results = scan_repo(base_dir)
    with open("modules/method_list.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Detected {len(results)} usable methods. Crypto/decryption methods excluded.")
