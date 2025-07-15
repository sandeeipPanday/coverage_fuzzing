from modules.bootstrap import install_dependencies
install_dependencies()

import json, matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

INPUT_FILE = "fuzz_log.jsonl"
OUTPUT_HTML = "fuzz_report.html"
OUTPUT_PIE = "results_pie.png"

def load_logs():
    with open(INPUT_FILE) as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def summary(logs):
    stats = defaultdict(lambda: {"total": 0, "fail": 0})
    for log in logs:
        key = f"{log['file']}::{log['class']}::{log['method']}"
        stats[key]["total"] += 1
        stats[key]["fail"] += 1
    return stats

def draw_pie(logs):
    fail = len(logs)
    total = 5000
    pass_ = total - fail
    plt.figure()
    plt.pie([fail, pass_], labels=["Fail", "Pass"], colors=["#FF4C4C", "#4CAF50"],
            autopct='%1.1f%%', startangle=90)
    plt.title("Fuzzing Results")
    plt.axis('equal')
    plt.savefig(OUTPUT_PIE)
    plt.close()

def write_html(logs, stats):
    rows = ""
    for k, s in stats.items():
        parts = k.split("::")
        success = s["total"] - s["fail"]
        pct = 100 * success / s["total"] if s["total"] else 0
        rows += f"<tr><td>{parts[0]}</td><td>{parts[1]}</td><td>{parts[2]}</td><td>{success}/{s['total']}</td><td>{pct:.1f}%</td></tr>\n"

    html = f"""<html><head><title>Fuzz Report</title>
    <style>table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px}}</style>
    </head><body>
    <h2>🐞 Fuzzing Results Summary</h2>
    <img src="{
