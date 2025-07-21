import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.bootstrap import install_dependencies
install_dependencies()

import json, matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from html import escape

INPUT_FILE = "fuzz_log.jsonl"
OUTPUT_HTML = "fuzz_report.html"
OUTPUT_PIE = "results_pie.png"

def load_logs():
    if not os.path.exists(INPUT_FILE):
        print(f"⚠️ No log file found at {INPUT_FILE}. Run fuzzing tests first.")
        return []
    with open(INPUT_FILE) as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def summarize(logs):
    stats = defaultdict(lambda: {"pass": 0, "fail": 0, "errors": []})
    for log in logs:
        key = f"{log['file']}::{log['class']}::{log['method']}"
        if log.get("status") == "pass":
            stats[key]["pass"] += 1
        elif log.get("status") == "fail":
            stats[key]["fail"] += 1
            if log.get("error"):
                stats[key]["errors"].append(log["error"])
    return stats

def draw_pie(stats):
    total_pass = sum(s["pass"] for s in stats.values())
    total_fail = sum(s["fail"] for s in stats.values())
    if total_pass + total_fail == 0:
        print("⚠️ No data to generate pie chart.")
        return
    plt.figure()
    plt.pie(
        [total_fail, total_pass],
        labels=["Fail", "Pass"],
        colors=["#FF4C4C", "#4CAF50"],
        autopct='%1.1f%%',
        startangle=90
    )
    plt.title("Fuzzing Results")
    plt.axis('equal')
    plt.savefig(OUTPUT_PIE)
    plt.close()

def write_html(stats):
    rows = ""
    for key, data in stats.items():
        f, c, m = key.split("::")
        total = data["pass"] + data["fail"]
        pct = 100 * data["pass"] / total if total > 0 else 0
        error_block = ""
        if data["errors"]:
            error_list = "".join(f"<li>{escape(err)}</li>" for err in data["errors"][:5])
            error_block = f"<details><summary>Failure Reasons</summary><ul>{error_list}</ul></details>"
        rows += (
            f"<tr><td>{escape(f)}</td><td>{escape(c)}</td><td>{escape(m)}</td>"
            f"<td>{data['pass']} / {total}</td><td>{pct:.1f}%</td><td>{error_block}</td></tr>\n"
        )
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<html><head><title>Fuzz Report</title>
    <style>body{{font-family:sans-serif}}table{{border-collapse:collapse;width:100%}}
    td,th{{border:1px solid #ccc;padding:8px;vertical-align:top}}details{{margin-top:4px}}</style></head>
    <body><h2>🐞 Fuzzing Results Summary</h2>
    <p><strong>Generated:</strong> {ts}</p>
    <img src="{OUTPUT_PIE}" width="300"><br><br>
    <table><tr><th>File</th><th>Class</th><th>Method</th><th>Pass / Total</th><th>Success %</th><th>Failure Reasons</th></tr>
    {rows}</table></body></html>"""
    with open(OUTPUT_HTML, "w") as f:
        f.write(html)
    print(f"✅ Report saved to {OUTPUT_HTML}")

if __name__ == "__main__":
    logs = load_logs()
    if not logs:
        print("⚠️ No logs found. Skipping report.")
        sys.exit(0)
    stats = summarize(logs)
    draw_pie(stats)
    write_html(stats)
