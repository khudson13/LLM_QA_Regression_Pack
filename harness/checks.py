from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Tuple


def count_sentences(text: str) -> int:
    parts = re.split(r"[.!?]+(?:\s+|$)", text.strip())
    return len([p for p in parts if p.strip()])


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def check_must_contain(response: str, required: List[str]) -> List[str]:
    failures: List[str] = []
    lowered = response.lower()
    for item in required:
        if item.lower() not in lowered:
            failures.append(f"Missing required text: {item}")
    return failures


def check_must_not_contain(response: str, forbidden: List[str]) -> List[str]:
    failures: List[str] = []
    lowered = response.lower()
    for item in forbidden:
        if item.lower() in lowered:
            failures.append(f"Contains forbidden text: {item}")
    return failures


def check_sentence_count(response: str, expected: int) -> List[str]:
    actual = count_sentences(response)
    if actual != expected:
        return [f"Sentence count mismatch: expected {expected}, got {actual}"]
    return []


def check_min_words(response: str, minimum: int) -> List[str]:
    actual = count_words(response)
    if actual < minimum:
        return [f"Word count too low: expected at least {minimum}, got {actual}"]
    return []


def check_max_words(response: str, maximum: int) -> List[str]:
    actual = count_words(response)
    if actual > maximum:
        return [f"Word count too high: expected at most {maximum}, got {actual}"]
    return []


def check_valid_json(response: str) -> Tuple[List[str], Any | None]:
    try:
        parsed = json.loads(response)
        return [], parsed
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON: {exc}"], None


def check_required_keys(parsed: Any, required_keys: List[str]) -> List[str]:
    if not isinstance(parsed, dict):
        return ["JSON root is not an object"]
    failures: List[str] = []
    for key in required_keys:
        if key not in parsed:
            failures.append(f"Missing required key: {key}")
    return failures


def check_no_extra_keys(parsed: Any, allowed_keys: List[str]) -> List[str]:
    if not isinstance(parsed, dict):
        return ["JSON root is not an object"]
    failures: List[str] = []
    allowed = set(allowed_keys)
    for key in parsed.keys():
        if key not in allowed:
            failures.append(f"Unexpected extra key: {key}")
    return failures


def check_enum_values(parsed: Any, enum_checks: Dict[str, List[str]]) -> List[str]:
    if not isinstance(parsed, dict):
        return ["JSON root is not an object"]
    failures: List[str] = []
    for field, allowed_values in enum_checks.items():
        if field in parsed and parsed[field] is not None:
            if parsed[field] not in allowed_values:
                failures.append(
                    f"Field '{field}' has invalid value '{parsed[field]}'; "
                    f"allowed: {allowed_values}"
                )
    return failures


def check_regex_fields(parsed: Any, regex_checks: Dict[str, str]) -> List[str]:
    if not isinstance(parsed, dict):
        return ["JSON root is not an object"]
    failures: List[str] = []
    for field, pattern in regex_checks.items():
        if field in parsed and parsed[field] is not None:
            value = str(parsed[field])
            if re.fullmatch(pattern, value) is None:
                failures.append(
                    f"Field '{field}' value '{value}' does not match regex '{pattern}'"
                )
    return failures


def run_auto_checks(case: Dict[str, Any], response: str) -> List[str]:
    auto = case.get("auto_checks", {})
    failures: List[str] = []

    if not auto:
        return failures

    if "must_contain" in auto:
        failures.extend(check_must_contain(response, auto["must_contain"]))

    if "must_not_contain" in auto:
        failures.extend(check_must_not_contain(response, auto["must_not_contain"]))

    if "sentence_count" in auto:
        failures.extend(check_sentence_count(response, auto["sentence_count"]))

    if "min_words" in auto:
        failures.extend(check_min_words(response, auto["min_words"]))

    if "max_words" in auto:
        failures.extend(check_max_words(response, auto["max_words"]))

    parsed = None
    needs_json = any(
        key in auto
        for key in [
            "valid_json",
            "required_keys",
            "allowed_keys",
            "enum_checks",
            "regex_fields",
        ]
    )

    if needs_json:
        json_failures, parsed = check_valid_json(response)
        failures.extend(json_failures)

    if parsed is not None:
        if auto.get("valid_json") is True:
            pass

        if "required_keys" in auto:
            failures.extend(check_required_keys(parsed, auto["required_keys"]))

        if "allowed_keys" in auto:
            failures.extend(check_no_extra_keys(parsed, auto["allowed_keys"]))

        if "enum_checks" in auto:
            failures.extend(check_enum_values(parsed, auto["enum_checks"]))

        if "regex_fields" in auto:
            failures.extend(check_regex_fields(parsed, auto["regex_fields"]))

    return failures