import os
import ast
import sys

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
                    print(u"Skipping {} due to parsing error: {}".format(file_path, e))

    return functions

if __name__ == "__main__":
    base_dir = os.path.join(os.getcwd(), "app")
    if not os.path.exists(base_dir):
        print("The 'app' folder was not found in the current directory.")
        sys.exit(1)

    results = list_functions_in_repo(base_dir)

    if results:
        print("Functions found in 'app' and subfolders:")
        for func in results:
            print("{} → {}".format(func["file"], func["function"]))
    else:
        print("No functions found.")
