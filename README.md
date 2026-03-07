---

# LLM QA Regression Pack (Example Evaluation Suite)

## Overview

This repository contains a small but structured **LLM regression testing suite** designed to evaluate core reliability behaviors in modern language models.

The goal of the project is to demonstrate how evaluation cases can be organized into a repeatable **QA-style regression workflow**, similar to automated test suites used in traditional software engineering.

Rather than evaluating exact output strings, the suite evaluates **behavioral properties of model responses**, including:

* instruction adherence
* grounding and hallucination resistance
* structured output reliability
* ambiguity handling
* product-style workflow behaviors

Each evaluation case defines expected behavior and failure conditions, allowing model outputs to be judged consistently over time.

This structure allows evaluators to answer an important question:

> **Did the model get worse after a change?**

---

## How to Run

This project is designed as a lightweight local regression harness for manual or semi-manual LLM evaluation.

Requirements

Python 3.10+ recommended

No third-party packages required for the current version

Run from repository root
python run_pack.py
Workflow

For each test case, the harness will:

* display the prompt and any provided context

* show expected behavior

* ask you to paste the model response

* run any configured automated checks

* ask for a final PASS/FAIL judgment

* optionally record failure tags and notes

At the end of the run, the harness writes:

* a timestamped JSONL log to runs/

* a timestamped Markdown summary report to reports/

## Example output
runs/results_20260306_153000.jsonl
reports/report_20260306_153000.md
Notes

This version uses a human-in-the-loop workflow rather than fully automated inference. That is intentional: many important LLM quality dimensions still require human judgment, especially for grounding, ambiguity handling, and subtle hallucination detection.

##Example Files

This repository includes example outputs for reviewers who may not run the harness directly.

* runs/results_sample.jsonl — sample run log with case-level judgments

* reports/sample_report.md — sample Markdown regression report showing how findings are summarized

These examples are included to demonstrate the intended evaluator workflow and reporting style without requiring live inference.

## Model Under Test

The initial regression pack targets:

**Qwen3-4B-Instruct**

Reason for selection:

* small enough for reliable local inference
* capable general instruction-following model
* representative of modern instruction-tuned LLM behavior

Using a local model makes the regression pack reproducible without API dependencies.

The evaluation framework is model-agnostic and could be run against other models such as:

* Qwen variants
* LLaMA-based models
* local instruction-tuned assistants
* API-based models

---

# Evaluation Categories

The regression pack is organized into five categories covering different reliability behaviors.

These categories were chosen to represent **common failure modes in real-world LLM deployments**.

---

# 1. Instruction-Following and Constraint Compliance

These tests evaluate whether the model correctly follows explicit user instructions.

Typical constraints include:

* sentence limits
* required or forbidden phrases
* exact bullet counts
* output format restrictions
* preservation of quoted text

Example tests:

| Case ID | Test                                      |
| ------- | ----------------------------------------- |
| INF-001 | Two sentence summary constraint           |
| INF-002 | Bullet list with exact item count         |
| INF-003 | Email containing required phrase          |
| INF-004 | Rewrite preserving quoted text            |
| INF-005 | Category classification from allowed list |
| INF-006 | Response length limit                     |

Why this matters:

Many real product failures occur when a model **ignores or partially follows instructions**, even when the response otherwise appears reasonable.

These tests are partially automatable using:

* sentence counting
* regex checks
* word count limits
* substring presence/absence

---

# 2. Grounding and Hallucination Resistance

These tests evaluate whether the model remains **faithful to a provided source document**.

The model must:

* answer questions using only supplied context
* avoid inventing facts not present in the source
* explicitly state when information is missing

Example tests:

| Case ID | Test                                        |
| ------- | ------------------------------------------- |
| GRD-001 | Answer questions from project note only     |
| GRD-002 | Summary without adding missing details      |
| GRD-003 | Identify project owner when absent          |
| GRD-004 | Extract decisions from meeting note         |
| GRD-005 | Respond "not stated" when answer is missing |

Why this matters:

Hallucinated information is one of the most significant reliability issues in deployed LLM systems, particularly for:

* document assistants
* enterprise knowledge tools
* retrieval-augmented generation systems

These tests detect unsupported claims and fabricated details.

---

# 3. Structured Output and Schema Reliability

These tests evaluate whether the model can produce **machine-readable structured output** that conforms to a defined schema.

Example tasks include:

* JSON extraction
* field normalization
* required/optional field handling
* enum classification

Example tests:

| Case ID | Test                             |
| ------- | -------------------------------- |
| SCH-001 | Extract customer data to JSON    |
| SCH-002 | Normalize dates to ISO format    |
| SCH-003 | Null handling for missing fields |
| SCH-004 | Allowed category enum validation |
| SCH-005 | Reject extra keys in schema      |

Why this matters:

Many LLM-powered systems depend on structured outputs for:

* automation pipelines
* tool invocation
* workflow integration
* API calls

Even a correct answer becomes unusable if it breaks the schema.

These tests are highly automatable using JSON validation and schema checks.

---

# 4. Ambiguity and Edge Case Handling

These tests evaluate how the model behaves when input is **ambiguous, messy, or incomplete**.

Real users frequently provide:

* contradictory information
* unclear references
* partial requests
* informal language

Example tests:

| Case ID | Test                                     |
| ------- | ---------------------------------------- |
| AMB-001 | Ambiguous pronoun resolution             |
| AMB-002 | Conflicting dates in meeting notes       |
| AMB-003 | Near-duplicate classification            |
| AMB-004 | Incomplete request requiring uncertainty |

These tests evaluate whether the model:

* acknowledges ambiguity
* avoids unsupported assumptions
* avoids overconfident responses

This category is less automatable but provides important insight into real-world reliability.

---

# 5. Product-Style Workflow Tests

These tests simulate common tasks a **document-grounded workplace assistant** might perform.

The fictional product context for these tests is:

> A workplace assistant that helps users summarize project notes, extract action items, and draft follow-up communications based on internal documents.

Example tests:

| Case ID | Test                              |
| ------- | --------------------------------- |
| PW-001  | Meeting note summary              |
| PW-002  | Action item extraction            |
| PW-003  | Follow-up email drafting          |
| PW-004  | Customer account brief            |
| PW-005  | Source-bounded question answering |

These tests evaluate higher-level behaviors combining several evaluation dimensions:

* instruction following
* grounding
* structured output
* realistic workflow tasks

They help determine whether a model is suitable for **practical business assistant workflows**.

---

# Evaluation Workflow

Each test case defines:

* the prompt
* optional context
* expected behavior
* automated checks
* human evaluation criteria
* failure tags

Typical evaluation flow:

```
prompt
   ↓
model response
   ↓
automated checks
   ↓
human or rubric evaluation
   ↓
PASS / FAIL with failure tags
```

Results are logged for analysis and summarized in generated reports.

---

# Regression Testing

The evaluation suite is designed to be rerun across model versions.

Example regression comparison:

| Category              | Pass Rate v1 | Pass Rate v2 |
| --------------------- | ------------ | ------------ |
| Instruction Following | 92%          | 85%          |
| Grounding             | 88%          | 76%          |
| Schema Reliability    | 94%          | 93%          |

Such comparisons help identify behavioral regressions introduced by model updates or prompt changes.

---

# Purpose of This Project

This repository demonstrates how LLM behavior can be evaluated using **structured QA principles** similar to traditional software testing.

The goal is to illustrate:

* repeatable evaluation case design
* failure categorization
* reproducible evaluation workflows
* regression-style testing for generative models

While the evaluation harness included here is intentionally lightweight, the same concepts scale to larger evaluation systems used in production AI development.

---

# Future Improvements

Potential future additions include:

* automated LLM-judge scoring
* expanded regression case library
* multi-model comparison runs
* visualization dashboards for evaluation metrics

---