import json
from datetime import datetime

INPUT_FILE = "fuzz_log.jsonl"
OUTPUT_FILE = "fuzz_report.html"

def load_logs():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def to_html(logs):
    rows = ""
    for entry in logs:
        rows += "<tr><td>{}</td><td>{}</td><td><pre>{}</pre></td><td><pre>{}</pre></td></tr>\n".format(
            entry["file"], entry["function"],
            entry["input"].replace("<", "&lt;"),
            entry["error"].replace("<", "&lt;")
        )
    return f"""
    <html>
    <head>
        <title>Atheris Fuzzing Report</title>
        <style>
            body {{ font-family: Arial; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            pre {{ margin: 0; font-family: monospace; white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <h2>Atheris Fuzzing Report</h2>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <table>
            <tr><th>File</th><th>Function</th><th>Input</th><th>Error</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """

if __name__ == "__main__":
    logs = load_logs()
    if logs:
        html = to_html(logs)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ HTML report saved to", OUTPUT_FILE)
    else:
        print("ℹ️ No crashes found.")
