# AI Email Triage: Keyword Filter vs LLM

Classifying a small business inbox (customer enquiries, existing clients, suppliers, spam, and sales pitches **disguised as real enquiries**) and measuring which approach you can actually trust.

Built from a real problem: a UK electrical contractor receives ~100 emails a day, and sales pitches like *"Hi, I'd like a quote for your website..."* pass keyword filters and hide real customers.

## Results

| Approach | All 20 emails | **Unseen 10 emails** (honest test) |
|---|---|---|
| Keyword rules | 10/20 (50%) | **1/10 (10%)** |
| Claude + validation guard | 20/20 (100%) | **10/10 (100%)** |

The keyword rules looked fine (9/10) on the emails they were written for, then collapsed to 1/10 on new emails. That is overfitting. The LLM understands intent ("they are selling to us" vs "they want to buy from us"), so it held up on emails it had never seen.

## How it works

```
email ─► Claude (system prompt + JSON output) ─► validation guard ─► decision
                                                   ├─ not valid JSON        → "other", human review
                                                   ├─ unknown category      → "other", human review
                                                   ├─ confidence < 0.7      → keep category, human review
                                                   └─ OK                    → automatic
```

The model's output is **checked, not trusted**. If the answer is malformed or the model is unsure, the email goes to a person instead of being silently misfiled. In a real inbox, that is what keeps customers out of the spam folder.

## Files

| File | Purpose |
|---|---|
| `dataset.jsonl` | 20 labelled emails, including disguised sales pitches |
| `classifier.py` | `parse_decision`: the validation guard (JSON parsing, allowed categories, confidence threshold) |
| `test_classifier.py` | Unit tests for the guard: valid answer, garbage, unknown category, low confidence |
| `run_eval.py` | Keyword-rule baseline and its accuracy |
| `ask_claude.py` | Claude call with structured JSON output |
| `compare.py` | Runs both approaches on every email and reports accuracy |

## Run it

```bash
pip install anthropic python-dotenv
```

Create a `.env` file with `ANTHROPIC_API_KEY=...` (it is git-ignored), then:

```bash
python -m unittest -v
python compare.py
```

## What I learned

- Measure before trusting: a labelled test set showed the real accuracy, not "it seems to work".
- Hold out unseen data. Rules tuned on known examples give a false sense of quality.
- Treat LLM output as untrusted input: validate the structure, restrict categories, and route low-confidence cases to a human.
- Handle API realities: model deprecations (404), overload (503), and response blocks you didn't expect (thinking blocks before text).

## Next steps

- Retries with backoff for 503 errors
- Cost and latency per email
- Larger test set from real (anonymised) inbox data
- FastAPI endpoint and Docker

---

**Alina Kremenchutska**, AI Automation Engineer, founder of [Ali & AI](https://ali-and-ai.com)
