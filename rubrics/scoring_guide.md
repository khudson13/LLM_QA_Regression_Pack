# Scoring Guide

This harness uses a simple PASS / FAIL judgment model.

## PASS

Mark a case as PASS when:

- the response satisfies the most important expectations of the case
- any minor imperfections do not materially reduce correctness or usefulness
- no significant unsupported claims are introduced
- required structure or formatting is preserved closely enough for intended use

## FAIL

Mark a case as FAIL when one or more significant issues occur, including:

- explicit instruction not followed
- unsupported or invented factual content
- schema-breaking output
- incorrect handling of ambiguity
- omission of required content that materially harms usefulness

## Notes on Judgment

This project is intentionally lightweight. It does not attempt to remove all human judgment.

Use automated checks where possible, but apply final judgment based on whether the output would be acceptable in a practical QA setting.

## Severity

- `low` — minor issue, limited practical impact
- `medium` — noticeable issue that reduces reliability or usefulness
- `high` — major issue that would likely break workflow trust or output usability