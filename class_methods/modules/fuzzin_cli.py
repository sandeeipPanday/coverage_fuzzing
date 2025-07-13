import os, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
MODULES = os.path.join(BASE, "modules")

def run(script):
    subprocess.run([sys.executable, os.path.join(MODULES, script)])

def menu():
    print("\n🧪 Fuzzing CLI Menu")
    print("1. Detect class methods in api/")
    print("2. Configure fuzz input types")
    print("3. Run Atheris fuzzing")
    print("4. Generate fuzzing report")
    print("5. Run manual edge tests")
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
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid option.")
