import os
import ast
import json

def list_functions_in_repo(repo_path):
    functions = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        source = f.read()
                    node = ast.parse(source, filename=file_path)
                    for item in ast.walk(node):
                        if isinstance(item, ast.FunctionDef):
                            functions.append({
                                "file": os.path.relpath(file_path, repo_path),
                                "function": item.name
                            })
                except (SyntaxError, UnicodeDecodeError) as e:
                    print("Skipping {} due to parsing error: {}".format(file_path, e))
    return functions

if __name__ == "__main__":
    base_dir = os.path.join(os.getcwd(), "api")
    results = list_functions_in_repo(base_dir)
    if results:
        with open("function_list.json", "w") as f:
            json.dump(results, f, indent=2)
        print("✅ Found {} functions. Saved to function_list.json".format(len(results)))
    else:
        print("❌ No functions found.")
