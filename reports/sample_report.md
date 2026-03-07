# LLM QA Regression Report

- **Model:** Qwen3-4B-Instruct
- **Generated:** 2026-03-06T14:35:00
- **Total cases:** 6
- **Pass:** 1
- **Fail:** 5
- **Pass rate:** 16.7%

## Results by Category

| Category | Total | Pass | Fail | Pass Rate |
|---|---:|---:|---:|---:|
| ambiguity_edge_cases | 1 | 0 | 1 | 0.0% |
| grounding | 1 | 0 | 1 | 0.0% |
| instruction_following | 2 | 1 | 1 | 50.0% |
| product_workflows | 1 | 0 | 1 | 0.0% |
| schema_output | 1 | 0 | 1 | 0.0% |

## Failure Tags

| Tag | Count |
|---|---:|
| overconfident_answer | 2 |
| hallucination | 2 |
| instruction_noncompliance | 1 |
| format_error | 1 |
| missed_uncertainty | 1 |
| incorrect_normalization | 1 |
| schema_violation | 1 |
| incorrect_disambiguation | 1 |
| missing_required_field | 1 |

## Severity Distribution

| Severity | Count |
|---|---:|
| medium | 3 |
| high | 3 |

## Summary

This sample run shows a realistic mixed evaluation pattern for a small local instruction model. The model performed adequately on a straightforward summarization constraint test, but several recurring reliability issues appeared across higher-value categories.

The most notable failure patterns were:

- **Overconfidence under ambiguity**
- **Hallucinated or unsupported details**
- **Schema-adjacent formatting errors**
- **Incorrect normalization of extracted values**

These are meaningful QA findings because they represent failure modes that would materially affect trust in a workplace assistant workflow.

## Key Findings

### 1. Constraint compliance is decent but not perfectly reliable

The model passed a basic two-sentence summary case, suggesting that it can follow simple surface-level instructions. However, it failed a short drafting task by exceeding the requested word cap. This kind of issue is common in production systems where a response may appear reasonable to a human reviewer but still violate downstream UI or workflow constraints.

### 2. Grounding remains a major weakness

In the grounding case, the model invented an owner even though the source note explicitly did not provide one. This is a high-severity behavior because it turns absent information into asserted fact rather than signaling uncertainty.

### 3. Structured extraction is usable but brittle

The model returned valid JSON in the date-normalization case, but failed to convert the source date into the required ISO format. This is an example of a response that might look "mostly correct" to a casual reviewer while still breaking automation assumptions.

### 4. Ambiguity handling needs human-style caution

The ambiguous pronoun case showed that the model was willing to commit to an interpretation without acknowledging uncertainty. This is especially important in workplace and support settings, where many user inputs are incomplete or ambiguous.

### 5. Product-style workflow behavior degrades under composite demands

In the action-item extraction workflow, the model produced a superficially useful answer but invented a deadline and handled missing data inconsistently. This illustrates why product-shaped regression tests matter: they reveal failures that do not always appear in isolated toy prompts.

## Case-by-Case Results

### INF-001 — Two sentence project summary
- **Category:** instruction_following
- **Severity:** medium
- **Status:** PASS
- **Notes:** Followed the two-sentence constraint and remained grounded in the source.

### INF-003 — Short decline email with required phrase
- **Category:** instruction_following
- **Severity:** medium
- **Status:** FAIL
- **Automated check failures:**
  - Word count too high: expected at most 70, got 78
- **Failure tags applied:** instruction_noncompliance, format_error
- **Notes:** Included the required phrase but exceeded the length limit and did not end cleanly with a question.

### GRD-003 — Owner absent should not be invented
- **Category:** grounding
- **Severity:** high
- **Status:** FAIL
- **Failure tags applied:** hallucination, overconfident_answer, missed_uncertainty
- **Notes:** Named an owner even though the note did not specify one.

### SCH-002 — Normalize date to ISO
- **Category:** schema_output
- **Severity:** medium
- **Status:** FAIL
- **Automated check failures:**
  - Field 'due_date' value 'June 7, 2026' does not match regex '\d{4}-\d{2}-\d{2}'
- **Failure tags applied:** incorrect_normalization, schema_violation
- **Notes:** Returned valid JSON but failed to normalize the date.

### AMB-001 — Ambiguous pronoun reference
- **Category:** ambiguity_edge_cases
- **Severity:** high
- **Status:** FAIL
- **Failure tags applied:** incorrect_disambiguation, overconfident_answer
- **Notes:** Resolved the pronoun to Maya without acknowledging ambiguity.

### PW-002 — Action item extraction
- **Category:** product_workflows
- **Severity:** high
- **Status:** FAIL
- **Failure tags applied:** hallucination, missing_required_field
- **Notes:** Produced plausible JSON but invented a concrete deadline for legal review and omitted null handling for one missing field.

## Why include a sample report?

A portfolio reviewer may never run the harness. This sample report shows what the project produces and demonstrates the intended style of QA analysis:

- structured failure identification
- category-level quality reporting
- mixed automated and human-reviewed judgments
- practical interpretation of model weaknesses