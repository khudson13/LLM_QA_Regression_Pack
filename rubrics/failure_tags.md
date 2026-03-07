# Failure Tags

This project uses a compact failure-tag taxonomy intended for lightweight QA regression work.

## Core Tags

- `instruction_noncompliance`  
  The model failed to follow one or more explicit instructions.

- `hallucination`  
  The response introduced unsupported facts not present in the source material.

- `unsupported_inference`  
  The response made an inference that goes beyond what the provided context justifies.

- `format_error`  
  The output violated a required format, such as bullet count or sentence count.

- `schema_violation`  
  The structured output did not conform to the expected schema.

- `invalid_json`  
  The output was not parseable as valid JSON.

- `missing_required_field`  
  A required field was omitted from structured output.

- `extra_field`  
  Structured output included keys that were not allowed.

- `incorrect_normalization`  
  A value was extracted but not normalized correctly, such as a date in the wrong format.

- `overconfident_answer`  
  The model presented an uncertain or unsupported claim with unjustified confidence.

- `incorrect_disambiguation`  
  The model resolved an ambiguous reference incorrectly or without acknowledging ambiguity.

- `missed_uncertainty`  
  The model should have signaled uncertainty or insufficiency of evidence, but did not.