# Evaluation Report: Shop LLM Eval

## 1. Objective

To evaluate and compare a traditional ML baseline (TF-IDF + Logistic Regression) against a local LLM (Llama 3.2 3B) for classifying Malaysian e-commerce customer support messages into 5 intent categories.

## 2. Dataset

- **Total messages:** 200 (140 dev, 60 test).
- **Adversarial set:** 25 stress-test messages (prompt injections, heavy Manglish, typos, multi-intent traps).
- **Self-disagreement rate:** 10% (2 of 20 messages differed). Note: This was a same-day relabelling check, not a week-apart blind check.

## 3. Methods

- **Baseline:** TF-IDF vectorization paired with a Logistic Regression classifier.
- **LLM:** One local 3B model (`llama3.2:3b`) evaluated across three prompts (`zero`, `defs`, `fewshot`).
- **Configuration Freeze:** The `defs` prompt was locked in based on highest dev performance before evaluating the test set.

## 4. Results

| model        | prompt  | split       | n   | accuracy | 95% CI      | macro-F1 | invalid | sec/call |
| ------------ | ------- | ----------- | --- | -------- | ----------- | -------- | ------- | -------- |
| tfidf-logreg | none    | adversarial | 25  | 0.720    | 0.524-0.857 | 0.695    | 0.00    | 0.00     |
| tfidf-logreg | none    | dev         | 140 | 0.736    | 0.657-0.802 | 0.740    | 0.00    | 0.00     |
| tfidf-logreg | none    | test        | 60  | 0.700    | 0.575-0.801 | 0.700    | 0.00    | 0.00     |
| llama3.2:3b  | defs    | adversarial | 25  | 0.680    | 0.484-0.828 | 0.687    | 0.00    | 8.00     |
| llama3.2:3b  | defs    | dev         | 140 | 0.750    | 0.672-0.814 | 0.747    | 0.02    | 4.19     |
| llama3.2:3b  | defs    | test        | 60  | 0.750    | 0.628-0.842 | 0.747    | 0.02    | 4.97     |
| llama3.2:3b  | fewshot | dev         | 140 | 0.714    | 0.635-0.783 | 0.693    | 0.00    | 4.47     |
| llama3.2:3b  | zero    | dev         | 140 | 0.321    | 0.250-0.403 | 0.254    | 0.00    | 3.64     |

## 5. Key Findings

- **Performance parity:** The LLM's `defs` prompt achieved a test macro-F1 of 0.747 vs the baseline's 0.700[cite: 16]. However, because the 95% confidence intervals overlap heavily (0.628-0.842 vs 0.575-0.801)[cite: 16], the difference is within statistical noise. The models are effectively comparable.
- **Zero-shot collapse:** The basic `zero` prompt failed completely, predicting the 'other' class 107 out of 140 times on the dev set.
- **Adversarial robustness:** The baseline handled the 25 adversarial messages slightly better than the LLM (0.695 vs 0.687 macro-F1)[cite: 16], highlighting the fragility of small LLMs to prompt injections and hostile formatting.

## 6. Error Taxonomy

A manual review of errors across the evaluation splits revealed the following breakdown:

- **Baseline Dev Errors (37 total):**
  - Model confused labels (complaint vs order_status)
  - Language/slang problems (heavy Manglish/BM shorthand)
  - Ambiguous multi-intent messages
- **LLM Test Errors (15 total):**
  - _(Replace this line with 1-2 main categories you found in `errors_test.csv`)_
- **LLM Adversarial Errors (8 total):**
  - _(Replace this line with 1-2 main categories you found in `errors_adversarial.csv`)_

## 7. Limitations

- **Dataset size:** 200 messages is too small to prove statistical superiority (wide confidence intervals).
- **Single annotator:** Labelling and self-disagreement check (same-day) performed by one person.
- **Prompt tuning bias:** Prompts were repeatedly tuned against the dev set.
- **Model scale:** Only evaluated a 3B parameter model; larger models (7B-8B) were not tested due to hardware constraints.
