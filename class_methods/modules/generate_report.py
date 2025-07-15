import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(script_dir, "..")))
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
    passed = total - fail
    plt.figure()
    plt.pie([fail, passed], labels=["Fail", "Pass"], colors=["#FF4C4C", "#4CAF50"],
            autopct='%1.1f%%', startangle=90)
    plt.title("Fuzzing Results")
    plt.axis('equal')
    plt.savefig(OUTPUT_PIE)
    plt.close()

def write_html(logs, stats):
    rows = ""
    for k, s in stats.items():
        f, c, m = k.split("::")
        success = s["total"] - s["fail"]
        pct = 100 * success / s["total"] if s["total"] else 0
        rows += f"<tr><td>{f}</td><td>{c}</td><td>{m}</td><td>{success}/{s['total']}</td><td>{pct:.1f}%</td></tr>\n"

    html = f"""<html><head><title>Fuzz Report</title>
    <style>body{{font-family:sans-serif}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px}}</style>
    </head><body>
    <h2>🐞 Fuzzing Results Summary</h2>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <img src="{OUTPUT_PIE}" width="300"><br><br>
    <table><tr><th>File</th><th>Class</th><th>Method</th><th>Pass / Total</th><th>Success %</th></tr>
    {rows}</table></body></html>
    """
    with open(OUTPUT_HTML, "w") as f:
        f.write(html)
    print(f"✅ Report saved to {OUTPUT_HTML}")

if __name__ == "__main__":
    logs = load_logs()
    stats = summary(logs)
    draw_pie(logs)
    write_html(logs, stats)
