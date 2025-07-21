import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.bootstrap import install_dependencies
install_dependencies()

import ast, json

def extract_class_methods(file_path, repo_path):
    class_methods = []
    rel_path = os.path.relpath(file_path, repo_path)
    try:
        with open(file_path, "r") as f:
            source = f.read()
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name != "__init__":
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
                all_methods.extend(extract_class_methods(os.path.join(root, file), repo_path))
    return all_methods

if __name__ == "__main__":
    base_dir = os.path.join(os.getcwd(), "api")
    results = scan_repo(base_dir)
    with open("modules/method_list.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Found {len(results)} class methods. Saved to method_list.json")
