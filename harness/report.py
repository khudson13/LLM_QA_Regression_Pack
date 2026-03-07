from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def build_markdown_report(
    model_name: str,
    results: List[Dict[str, Any]],
) -> str:
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    by_category = defaultdict(list)
    tag_counter: Counter[str] = Counter()
    severity_counter: Counter[str] = Counter()

    for result in results:
        by_category[result["category"]].append(result)
        for tag in result.get("failure_tags_applied", []):
            tag_counter[tag] += 1
        severity_counter[result["severity"]] += 1

    lines: List[str] = []
    lines.append(f"# LLM QA Regression Report")
    lines.append("")
    lines.append(f"- **Model:** {model_name}")
    lines.append(f"- **Generated:** {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- **Total cases:** {total}")
    lines.append(f"- **Pass:** {passed}")
    lines.append(f"- **Fail:** {failed}")
    lines.append(f"- **Pass rate:** {(passed / total * 100):.1f}%" if total else "- **Pass rate:** N/A")
    lines.append("")

    lines.append("## Results by Category")
    lines.append("")
    lines.append("| Category | Total | Pass | Fail | Pass Rate |")
    lines.append("|---|---:|---:|---:|---:|")

    for category, items in sorted(by_category.items()):
        cat_total = len(items)
        cat_pass = sum(1 for i in items if i["status"] == "PASS")
        cat_fail = cat_total - cat_pass
        cat_rate = (cat_pass / cat_total * 100) if cat_total else 0.0
        lines.append(f"| {category} | {cat_total} | {cat_pass} | {cat_fail} | {cat_rate:.1f}% |")

    lines.append("")
    lines.append("## Failure Tags")
    lines.append("")
    if tag_counter:
        lines.append("| Tag | Count |")
        lines.append("|---|---:|")
        for tag, count in tag_counter.most_common():
            lines.append(f"| {tag} | {count} |")
    else:
        lines.append("No failure tags recorded.")
    lines.append("")

    lines.append("## Severity Distribution")
    lines.append("")
    if severity_counter:
        lines.append("| Severity | Count |")
        lines.append("|---|---:|")
        for severity, count in severity_counter.most_common():
            lines.append(f"| {severity} | {count} |")
    else:
        lines.append("No severity data recorded.")
    lines.append("")

    lines.append("## Case-by-Case Results")
    lines.append("")
    for result in results:
        lines.append(f"### {result['case_id']} — {result['title']}")
        lines.append(f"- **Category:** {result['category']}")
        lines.append(f"- **Severity:** {result['severity']}")
        lines.append(f"- **Status:** {result['status']}")
        if result.get("auto_failures"):
            lines.append("- **Automated check failures:**")
            for item in result["auto_failures"]:
                lines.append(f"  - {item}")
        if result.get("failure_tags_applied"):
            lines.append(f"- **Failure tags applied:** {', '.join(result['failure_tags_applied'])}")
        if result.get("notes"):
            lines.append(f"- **Notes:** {result['notes']}")
        lines.append("")

    return "\n".join(lines)


def write_report(output_path: str | Path, content: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")