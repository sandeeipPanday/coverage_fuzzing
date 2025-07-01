import os
import ast

def list_functions_in_repo(repo_path):
    functions = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        node = ast.parse(f.read(), filename=file_path)
                        for item in ast.walk(node):
                            if isinstance(item, ast.FunctionDef):
                                functions.append({
                                    "file": os.path.relpath(file_path, repo_path),
                                    "function": item.name
                                })
                except (SyntaxError, UnicodeDecodeError) as e:
                    print(f"⚠️ Skipping {file_path} due to parsing error: {e}")

    return functions

# Example usage
repo_directory = os.path.join(os.getcwd(), "app")  # Adjusts to current working directory + /app
functions = list_functions_in_repo(repo_directory)

if functions:
    print("✅ Functions found:")
    for func in functions:
        print(f"{func['file']} → {func['function']}")
else:
    print("❌ No functions found in the specified folder.")