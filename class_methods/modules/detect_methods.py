import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.bootstrap import install_dependencies
install_dependencies()

import ast, json

EXCLUDE_KEYWORDS = [
    "decrypt",
    "password",
    "auth",
    "token",
    "login",
    "key",
    "private",
    "ssl",
    "certificate"
]

def should_exclude(method_name, args):
    name = method_name.lower()
    arg_names = [a.arg.lower() for a in args if isinstance(a, ast.arg)]
    keywords_in_args = any(kw in arg for kw in EXCLUDE_KEYWORDS for arg in arg_names)
    return any(kw in name for kw in EXCLUDE_KEYWORDS) or keywords_in_args

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
                    if isinstance(item, ast.FunctionDef) and item.name != "__init__":
                        if not should_exclude(item.name, item.args.args):
                            class_methods.append({
                                "file": rel_path,
                                "class": node.name,
                                "method": item.name
                            })
                        else:
                            print(f"🔒 Skipped method needing auth: {rel_path}::{node.name}::{item.name}")
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
    print(f"✅ Saved {len(results)} fuzzable methods to method_list.json")
