import sys, os
from modules.bootstrap import install_dependencies
install_dependencies()

def run(script):
    os.system(f"python modules/{script}")

def menu():
    print("\n🧪 Fuzzing CLI")
    print("1. Detect class methods in api/")
    print("2. Configure fuzzing input types")
    print("3. Run fuzzing tests")
    print("4. Generate HTML + pie chart report")
    print("5. Run manual edge-case tests")
    print("0. Exit")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("Select option: ").strip()
        if choice == "1": run("detect_methods.py")
        elif choice == "2": run("configure_methods.py")
        elif choice == "3": run("fuzz_runner.py")
        elif choice == "4": run("generate_report.py")
        elif choice == "5": run("manual_edge_tests.py")
        elif choice == "0":
            print("👋 Exiting CLI.")
            break
        else:
            print("⚠️ Invalid selection.")
