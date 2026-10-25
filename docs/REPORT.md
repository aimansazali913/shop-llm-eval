# Shop LLM Eval: Project Report

## 1. Task and Labels

This project classifies Malaysian e-commerce customer support messages into 5 mutually exclusive intent labels:

- `order_status`: Inquiries about tracking numbers, shipping progress, delivery delays, or address changes.
- `product_enquiry`: Questions regarding stock availability, sizing, material specifications, pricing, or promotions before purchase.
- `payment_issue`: Problems with checkout transactions, double charges, unverified bank transfers, or refund requests.
- `complaint`: Expressions of dissatisfaction regarding damaged goods, wrong items received, poor quality, or bad customer service.
- `other`: Greetings, thank-you notes, general feedback, or off-topic messages.

## 2. Data

- **Total Dataset Size:** 200 messages (`140` dev rows, `60` test rows, stratified by label with `seed=42`).
- **Counts per Label:** 40 messages per label (`order_status`: 40, `product_enquiry`: 40, `payment_issue`: 40, `complaint`: 40, `other`: 40).
- **Counts per Language:** 80 Bahasa Melayu (`bm` - 40%), 60 English (`en` - 30%), 60 Mixed/Manglish (`mixed` - 30%).
- **Difficulty Distribution:** 170 clear-cut messages (`hard = 0`, 85%) and 30 ambiguous/tie-break boundary messages (`hard = 1`, 15%).
- **How It Was Written:** Written manually to reflect authentic Malaysian e-commerce chats, incorporating local slang, code-switching, typos, and emojis.
- **Self-Disagreement Rate:** 10% (2/20 re-labelled sample messages disagreed on boundary cases between `complaint` and `order_status`/`payment_issue`).

## 3. Methods

- **Three Prompting / Modelling Methods:**
  1. **TF-IDF + Logistic Regression Baseline (`baseline.py`):** Character word-boundary n-grams (`analyzer='char_wb'`, `ngram_range=(2, 5)`) with `LogisticRegression(max_iter=1000)`, evaluated via 5-fold cross-validation on `dev` and trained on `dev` to predict `test`.
  2. **Local LLM (`llm.py`):** `llama3.2:3b` via Ollama tested across three prompt styles: `zero` (zero-shot label names), `defs` (label definitions + tie-break rules), and `few` (definitions + few-shot examples).
- **Settings:** `temperature = 0`, `seed = 42` for deterministic, reproducible outputs.

## 4. Results

| Model / Prompt                       |  Dev Accuracy   | Dev (Macro-F1) | Test Accuracy  | Test (Macro-F1) |  Adversarial   |
| :----------------------------------- | :-------------: | :------------: | :------------: | :-------------: | :------------: |
| **TF-IDF Baseline (`tfidf-logreg`)** | 0.736 (103/140) |   **0.740**    | 0.700 (42/60)  |    **0.700**    |      N/A       |
| **Llama 3.2 3B (`zero`)**            | _[run llm.py]_  | _[run llm.py]_ |       -        |        -        |       -        |
| **Llama 3.2 3B (`defs`)**            | _[run llm.py]_  | _[run llm.py]_ | _[run llm.py]_ | _[run llm.py]_  | _[run llm.py]_ |
| **Llama 3.2 3B (`few`)**             | _[run llm.py]_  | _[run llm.py]_ |       -        |        -        |       -        |

## 5. Error Taxonomy

Evaluating the 37 errors from `docs/errors_dev.csv` on the 140-row dev set yielded the following failure breakdown:

- **`model confused two labels`:** 18 errors (48.6%) — Model triggered on surface keywords (e.g., seeing "order" in a complaint or "tracking" in a shipping notification issue).
- **`language problem (BM/mixed)`:** 9 errors (24.3%) — Model struggled with Malay idioms, slang, and code-switched phrasing.
- **`ambiguous message`:** 6 errors (16.2%) — Multi-intent messages (`hard = 1`) where a delay or wrong item overlapped with a complaint or refund request.
- **`unclear guide`:** 3 errors (8.1%) — Edge cases involving add-on payment inquiries or checkout price discrepancies.
- **`typo or noise`:** 1 error (2.7%) — Short test string (`"Test 123"`) lacked character n-gram signal.
- **`invalid output`:** 0 errors (0.0%).

**Example Error Messages from `errors_dev.csv`:**

1. **`id=7` (`model confused two labels`)** — _True:_ `order_status` | _Pred:_ `complaint`
   > `"Where is my order #4582?? been waiting a week"`
2. **`id=29` (`ambiguous message`, `hard=1`)** — _True:_ `complaint` | _Pred:_ `order_status`
   > `"Kenapa bagi warna salah ni?? Saya order navy blue dapat hitam!"`
3. **`id=35` (`language problem (BM/mixed)`)** — _True:_ `other` | _Pred:_ `order_status`
   > `"Terima kasih daun keladi, nanti saya repeat order lagi 🥰"` (Contains the word "order", causing the character n-gram model to misclassify a thank-you message).
4. **`id=150` (`unclear guide`, `hard=1`)** — _True:_ `product_enquiry` | _Pred:_ `payment_issue`
   > `"Do you provide bubble wrap packaging or need to add-on extra payment?"`
5. **`id=30` (`typo or noise`)** — _True:_ `other` | _Pred:_ `product_enquiry`
   > `"Test 123"`

## 6. Limitations

- **Single Writer & Annotator:** All 200 messages and labels were created by one person, which introduces author bias and lacks real production customer data.
- **Small Sample Size:** 140 dev rows and 60 test rows result in wide 95% confidence intervals (e.g., dev accuracy CI: `0.657` to `0.802`).
- **Small Models Only:** Evaluated lightweight local models (`tfidf-logreg` and 3B parameter LLM) rather than larger frontier models.
- **Dev Set Tuning:** Prompts and rules were refined using insights from the `dev` split.

## 7. What I Would Do Next

1. Collect and anonymize 500+ real customer support chat logs annotated by at least two independent raters to measure inter-annotator agreement (Cohen's Kappa).
2. Refine the labelling guide tie-break rules between `complaint` and `order_status` (especially for late parcels and wrong items) and benchmark an 8B multilingual model (such as Qwen 2.5 7B/8B or Llama 3.1 8B).

## 8. How to Reproduce

Ensure Python 3.11+ is installed, then run:

```bash
pip install -r requirements.txt
python split.py
python baseline.py dev
python baseline.py test
python errors.py results/baseline_dev.json
python report.py
```
