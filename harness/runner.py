from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from harness.checks import run_auto_checks
from harness.report import build_markdown_report, write_report


CASE_FILES = [
    "cases/instruction_following.jsonl",
    "cases/grounding.jsonl",
    "cases/schema_output.jsonl",
    "cases/ambiguity_edge_cases.jsonl",
    "cases/product_workflows.jsonl",
]


def load_jsonl(path: str | Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                items.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path} line {line_number}: {exc}") from exc
    return items


def validate_case(case: Dict[str, Any]) -> None:
    required_fields = [
        "case_id",
        "category",
        "title",
        "prompt",
        "expected_behavior",
        "failure_tags",
        "severity",
    ]
    missing = [field for field in required_fields if field not in case]
    if missing:
        raise ValueError(f"Case {case.get('case_id', '<unknown>')} missing fields: {missing}")

    if not isinstance(case["expected_behavior"], list):
        raise ValueError(f"Case {case['case_id']} expected_behavior must be a list")

    if not isinstance(case["failure_tags"], list):
        raise ValueError(f"Case {case['case_id']} failure_tags must be a list")


def collect_cases(case_files: List[str]) -> List[Dict[str, Any]]:
    all_cases: List[Dict[str, Any]] = []
    for file_path in case_files:
        cases = load_jsonl(file_path)
        for case in cases:
            validate_case(case)
            all_cases.append(case)
    return all_cases


def filter_cases_by_id(
    cases: List[Dict[str, Any]],
    allowed_case_ids: List[str],
) -> List[Dict[str, Any]]:
    allowed = set(allowed_case_ids)
    return [case for case in cases if case["case_id"] in allowed]


def prompt_for_multiline(label: str) -> str:
    print(f"\n{label}")
    print("(Paste text. Enter a single line with END when finished.)")
    lines: List[str] = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def choose_failure_tags(available_tags: List[str]) -> List[str]:
    if not available_tags:
        print("No failure tags available for this case.")
        return []

    while True:
        print("\nAvailable failure tags for this case:")
        for i, tag in enumerate(available_tags, start=1):
            print(f"  {i}. {tag}")

        raw = input(
            "Enter comma-separated tag numbers to apply "
            "(at least one required for FAIL): "
        ).strip()

        if not raw:
            print("At least one failure tag is required for a FAIL result.")
            continue

        chosen: List[str] = []
        seen = set()

        for token in raw.split(","):
            token = token.strip()
            if not token:
                continue

            if not token.isdigit():
                print(f"Ignoring invalid entry: {token}")
                continue

            idx = int(token)
            if 1 <= idx <= len(available_tags):
                tag = available_tags[idx - 1]
                if tag not in seen:
                    chosen.append(tag)
                    seen.add(tag)
            else:
                print(f"Ignoring out-of-range entry: {token}")

        if chosen:
            return chosen

        print("At least one valid failure tag is required for a FAIL result.")


def main() -> None:
    print("LLM QA Regression Pack")
    print("======================")

    model_name = input("Model under test [Qwen3-4B-Instruct]: ").strip() or "Qwen3-4B-Instruct"

    cases = collect_cases(CASE_FILES)
    cases = filter_cases_by_id(cases, ["INF-001", "SCH-002", "GRD-003"])
    results: List[Dict[str, Any]] = []

    print(f"\nLoaded {len(cases)} cases.")

    for index, case in enumerate(cases, start=1):
        print("\n" + "=" * 80)
        print(f"Case {index}/{len(cases)}: {case['case_id']} — {case['title']}")
        print(f"Category: {case['category']}")
        print(f"Severity: {case['severity']}")
        print("\nPrompt:")
        print(case["prompt"])

        context = case.get("context")
        if context:
            print("\nContext:")
            print(context)

        print("\nExpected behavior:")
        for item in case["expected_behavior"]:
            print(f"- {item}")

        response = prompt_for_multiline("Paste model response")
        auto_failures = run_auto_checks(case, response)

        if auto_failures:
            print("\nAutomated check failures detected:")
            for failure in auto_failures:
                print(f"- {failure}")
        else:
            print("\nNo automated check failures detected.")

        status = input("Final status [PASS/FAIL]: ").strip().upper()
        while status not in {"PASS", "FAIL"}:
            status = input("Please enter PASS or FAIL: ").strip().upper()

        applied_tags: List[str] = []
        if status == "FAIL":
            applied_tags = choose_failure_tags(case.get("failure_tags", []))

        notes = input("Notes (optional): ").strip()

        results.append(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "model_name": model_name,
                "case_id": case["case_id"],
                "category": case["category"],
                "title": case["title"],
                "severity": case["severity"],
                "status": status,
                "auto_failures": auto_failures,
                "failure_tags_applied": applied_tags,
                "notes": notes,
            }
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    runs_dir = Path("runs")
    reports_dir = Path("reports")
    runs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    raw_output_path = runs_dir / f"results_{timestamp}.jsonl"
    with raw_output_path.open("w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    report_text = build_markdown_report(model_name=model_name, results=results)
    report_path = reports_dir / f"report_{timestamp}.md"
    write_report(report_path, report_text)

    print("\nDone.")
    print(f"Saved run results to: {raw_output_path}")
    print(f"Saved report to: {report_path}")