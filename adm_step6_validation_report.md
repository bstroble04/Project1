# ADM Step 6 — Validation Report

Run date: October 17, 2026. Amounts are USD millions except per-share values and percentages. Permitted tests were run with `py adm_step6_validation.py` logic against the existing Step 2 linked model; the separately authorized $1,300m post-lock test is documented in the Step 6.3 post-test section.

## 6.1 ABG known-answer test — PASS

`Proforma.py` is the original ABG training model: its module description identifies an “ABG five-year three-statement projection and FCFE valuation,” and it uses an ABG-specific FY2025 opening balance sheet and five-year assumptions. It was inspected and run without modifying code or assumptions.

### Inputs and calculations inspected

- Opening December 31, 2025 balances (USD millions): cash $40.4m, inventory $2,135.8m, floor-plan financing $2,027.0m, PP&E $3,070.4m, debt $3,572.0m, other liabilities $2,127.5m, and equity $3,891.7m.
- Core forecast inputs: FY2025 revenue $17,999.0m; 1.8% annual growth; 17.05% gross margin; SG&A at 66.5%, 65.5%, then 64.5% of gross profit; $250m annual CapEx; $150m annual debt repayment and buyback; 25.5% tax rate; 10.0% cost of equity; 2.5% terminal growth; and 17.951349m shares.
- The script projects income statement, balance sheet, and cash flow for 2026–2030; calculates FCFE as net income + depreciation + impairment − CapEx − working-capital changes + floor-plan change − debt repayment; validates each balance sheet and the cash minimum; discounts annual FCFE; then adds the discounted terminal value using 2030 FCFE plus the final debt repayment.

### Reproducible execution record

- Execution date/time: October 17, 2026, 3:01:03 PM EDT (UTC−04:00).
- Python: 3.13.15.
- Exact command: `py Proforma.py`
- Source file: `Proforma.py`; SHA-256 before and after execution: `DF494460AE933CD7DB278BE99F7C32820FF97FC0D646D9CF03AB0CF895B67147` (unchanged).
- Actual run output: all 2026–2030 assets-minus-liabilities-and-equity gaps displayed `$0.0m`; all five cash-minimum checks displayed `PASS`; equity value displayed `$5,237.34m`; share of value after 2030 displayed `79.76%`; and value per share displayed **$291.75**.

| Valuation comparison | Per-share amount |
|---|---:|
| Actual, unrounded Python calculation | $291.751666 |
| Actual, script display | $291.75 |
| Published known answer (approximately) | $291.75 |
| Difference | +$0.001666 |
| Percentage difference | +0.000571% |

Tolerance: **$0.01/share**. The known answer is stated as approximate and the program displays values rounded to cents, so one cent is a reasonable deterministic rounding tolerance. The unrounded difference of $0.001666/share is below that tolerance. **Result: PASS.**

## 6.2 Independent SEC input verification — PASS

The SEC filing was opened and checked on October 17, 2026:

| Field | SEC filing | Model | Difference |
|---|---:|---:|---:|
| Total revenues, FY ended Dec. 31, 2025 | $80,269m | $80,269m | $0.00m (0.0000%) |

- Filing: Archer-Daniels-Midland Company Form 10-K, fiscal year ended December 31, 2025, accession 0000007084-26-000011, filed February 17, 2026.
- Definition and units: consolidated **Revenues**, stated in millions (not a segment-only revenue measure).
- Location: Consolidated Statements of Earnings, page 45, “Revenues.”
- URL: [SEC filing](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm).
- Model location: `adm_integrated_model.py`, `HISTORICAL[2025]["Revenue"]` and the forecast opening revenue.
- Tolerance: $0.01m; PASS because the displayed input is an exact match. This is a source-to-model input check, not an audit of every filing-derived model component.

## 6.3 Locked changed-input record — PASS (post-lock test)

The initial validation run intentionally excluded the $1,300m CapEx test. After the prediction lock was verified, the separately authorized post-lock execution was completed; its commit/timestamp evidence, command, actual results, and prediction comparison appear in the Step 6.3 post-test section below.

After you explicitly authorize execution, use exactly:

```powershell
py adm_step6_validation.py --post-lock-capex 1300 --confirm-independent-lock --output adm_step6_3_results.json
```

That command uses the existing linked model and records 2026–2030 EBIT, FCFF, ending cash, facility balances and first failure, DCF value/share, each accounting validation, and a financing/recommendation implication. Copy the actual output into the two blank fields in `adm_step6_locked_prediction.md`; do not replace the pre-test prediction or timestamp.

## 6.4 Accounting and valuation validation — PASS, with stated limits

Tolerance for statement/bridge arithmetic is $0.01m, consistent with `adm_integrated_model.TOL` and million-dollar model units.

| Test | Actual result | Status |
|---|---|---|
| Assets = liabilities + equity, 2026–30 | gaps: $0.000000, $0.000000, $0.000000000007, $0.000000000007, $0.000000000007m | PASS |
| Cash-flow ending cash = balance-sheet ending cash | $0.000000m in every forecast year | PASS |
| Historical FY2025 balance sheet reconciliation | $0.000000m | PASS |
| Historical FY2025 CFO reconciliation | $5,452m calculated vs $5,452m stated; $0.00m difference | PASS |
| EV-to-equity bridge / diluted shares | EV $7,299.898m + cash/securities $1,047m − debt $8,410m − other claims $294m = equity $(357.102)m; / 482.0m shares = $(0.740876)/share | PASS |
| Higher WACC lowers value | 6.1894%: $1.3968; 6.6894%: $(0.7409); 7.1894%: $(2.4217) per share | PASS |
| Higher terminal growth raises value, with WACC > g | 2.0%: $(2.1771); 2.5%: $(0.7409); 3.0%: $1.0846 per share; base WACC 6.6894% exceeds every g | PASS |
| Peer P/E, EV/EBITDA, dates/units/bridges | Existing `adm_peer_comps.py` defines USD millions, Sept. 24, 2026 price date, FY2025 earnings, and validates price×shares, EV bridge, EBITDA construction, dates, and ADM implied-equity/share bridge | PASS when run; see cold-run commands |
| Cash/debt/other claims policy | $1,015m cash + $32m marketable securities included; $8,410m interest-bearing debt and $294m temporary equity/NCI deducted; segregated cash, brokerage payables, leases, and affiliates excluded under documented policy | PASS as consistently implemented; NEEDS MANUAL VERIFICATION as a valuation-policy choice |

Base facility headroom is $5,289.492m, $4,186.370m, $3,079.661m, $1,969.423m, and $855.766m for 2026–30; all are PASS. The historical CFO check uses the model’s documented grouped earnings-release reconciliation and is not a full line-by-line independently re-performed filing reconciliation.

## 6.5 Highest-risk failure — FAIL (expected stress result)

The documented compound facility stress was reproduced from `failure_test_assumptions()`: 0% revenue growth, 6.25% gross margin, 53 inventory days, $1,600m annual CapEx, 2.0% terminal growth, and its associated 7.5137% WACC. The first breach is 2030: facility balance **$6,873.550m**, which is **$873.550m over** the $6,000m limit.

All statement-balance, cash-to-balance-sheet, minimum-cash, retained-earnings, and debt-roll-forward checks still PASS. Facility compliance passes in 2026–29 (headroom $4,678.331m, $3,360.275m, $2,003.975m, and $593.423m) and FAILS in 2030. This is financially infeasible because the model needs borrowing beyond its stated liquidity cap to maintain the $500m cash floor; its $(14.31)/share output is diagnostic only and not an investable valuation. It reinforces the provisional watch/defer recommendation.

The individual Step 5 endpoints also fail in 2030: 70% SG&A gives $6,418.594m facility ($418.594m over), and $1,600m CapEx gives $6,176.790m ($176.790m over). Their raw share values ($(11.77) and $(9.27), respectively) are likewise not investable valuations.

## 6.6 Cold run — PASS

An isolated Windows virtual environment was created at `.venv-step6-cold` and confirmed with `include-system-site-packages = false`. It used Python 3.13.15 and only `pip==26.2.1`; the new `requirements.txt` documents that no third-party dependencies are required. To preserve the existing Step 5 output, required scripts ran from an independent byte-matched project copy using that fresh interpreter.

All required commands completed successfully on October 17, 2026, beginning 3:03:15 PM EDT: `Proforma.py` reproduced $291.75/share; `adm_integrated_model.py` reproduced the base $(0.74)/share display; `adm_peer_comps.py` printed all PASS checks; `adm_step5_sensitivity.py` reproduced $(0.740876)/share and its two expected 2030 financing failures; and `adm_step6_validation.py` reproduced the base PASS and documented financing FAIL cases. No execution errors or code repairs occurred. See `adm_step6_cold_run.md` for commands, package evidence, logs, and observed outputs.

## 6.7 AI-output decision — NEEDS EVIDENCE

Evidence exists that Codex helped create the linked model, validations, FCFF/scenarios, and documentation (`adm_model_documentation.md`, “AI assistance”; `Lab10-notes.md`, “AI Disclosure”). The student’s QUALIFY decision is now personally confirmed in `adm_step6_ai_decision.md`. However, the project contains an AI-assisted Step 5 explanation, not a preserved, verified verbatim original Codex response; this report does not represent it as one.

Evidence-gathering is complete for the documented Step 5 candidate: the “Revenue-growth mechanics” explanation in `adm_step5_sensitivity_report.md`, whose matching narrative source is `adm_step5_sensitivity.py` and whose report discloses Codex assistance. Independent linked-model runs confirm that, from 2% to 4% revenue growth, 2030 EBIT rises from $838.871703m to $1,052.348381m and NOPAT rises from $687.874797m to $862.925672m, while operating working-capital investment rises from $190.317766m to $411.378884m. FCFF therefore falls from $352.414617m to $306.404374m and DCF value/share declines from −$0.740876 to −$3.288931. Both cases pass financing, although the 4% case has only $329.938464m of facility headroom. The confirmed classification is **QUALIFY**. Step 6.7 remains **NEEDS EVIDENCE** only for a preserved original AI-output record, if the assignment requires a verified original Codex response rather than an AI-assisted project explanation.

## Final checklist

| Requirement | Status | Remaining work |
|---|---|---|
| 6.1 ABG known answer | PASS | `Proforma.py` reproduced $291.751666/share, displayed $291.75. |
| 6.2 SEC verification | PASS | None for the selected revenue input. |
| 6.3 locked changed-input test | PASS | Authorized $1,300m CapEx test completed; see post-test section below. |
| 6.4 accounting/valuation validation | PASS | Arithmetic, monotonicity, peer bridges, and the documented cash/debt/claims policy were reproduced; valuation-policy limitations remain disclosed. |
| 6.5 $6,000m failure | PASS | Expected financial-infeasibility failure reproduced; do not use failed values as investable. |
| 6.6 cold run | PASS | Fresh isolated environment ran all five required scripts and reproduced documented results. |
| 6.7 AI decision | NEEDS EVIDENCE | Personal QUALIFY decision is confirmed, but a preserved original verbatim Codex output is not available; the documented source is AI-assisted only. |

No existing model, notebook, report, or lab file was intentionally edited. Git is unavailable on this machine, so a repository-status comparison could not be performed; this is **NEEDS MANUAL VERIFICATION** after Git is available.

## 6.3 post-test results — PASS

**Execution date/time:** October 17, 2026, 2:57:50 PM EDT (UTC−04:00).

**Prediction-lock verification:** The GitHub history for `adm_step6_locked_prediction.md` shows commit [`402802fe2c75f9936fe8c366ceaf14cf7f6a0519`](https://github.com/bstroble04/TICKER-research/commit/402802fe2c75f9936fe8c366ceaf14cf7f6a0519), authored and committed by GitHub at October 17, 2026, 18:52:42 UTC (2:52:42 PM EDT). The locked file itself records a 2:49 PM pre-test prediction, so the committed record predates this 2:57:50 PM test execution.

**Exact command run:**

```powershell
py adm_step6_validation.py --post-lock-capex 1300 --confirm-independent-lock
```

The gated runner changed only the uniform annual CapEx input from $1,400m to $1,300m for 2026–2030 and retained all other independent Step 2 inputs.

| 2030 measure | $1,400m base | $1,300m test | Change |
|---|---:|---:|---:|
| Operating income (EBIT) | $838.87m | $874.71m | +$35.84m |
| FCFF | $352.41m | $445.96m | +$93.55m |
| DCF value/share | $(0.74) | $3.52 | +$4.27 |
| Liquidity facility balance | $5,144.23m | $4,627.96m | −$516.28m |

Facility validation is **PASS**: the 2030 balance is $4,627.96m, leaving $1,372.04m headroom against the $6,000m limit; there is no failing forecast year. The balance-sheet, cash-to-balance-sheet, minimum-cash, retained-earnings, and debt-roll-forward validations all PASS for 2026–2030. The largest statement gap is $0.000000000007m, well within the $0.01m tolerance; every cash reconciliation, retained-earnings roll-forward, and debt roll-forward difference is $0.00m.

### Prediction comparison

The locked prediction anticipated approximately +$35m EBIT, +$90m FCFF, +$4/share DCF value, and about a $500m reduction in financing, while retaining PASS financing. The actual changes are +$35.84m, +$93.55m, +$4.27/share, and −$516.28m, respectively; the financing PASS prediction was correct. Relative to the stated approximate predictions, the differences are +$0.84m EBIT, +$3.55m FCFF, +$0.27/share, and a $16.28m larger facility reduction. These are comparison differences, not model errors.

### Recommendation implication

The scenario remains funded and improves the model’s residual equity value, but $3.52/share is still substantially below the model’s documented September 24, 2026 market-price observation of $81.88/share. The result supports retaining—not changing—the provisional **watch/defer** recommendation. It is one sensitivity result, not evidence by itself that the lower CapEx assumption is sustainable or that the broader valuation-policy limitations have been resolved.

The original `adm_step6_locked_prediction.md` was not modified or overwritten.

## Final Step 6 audit — October 17, 2026

| Requirement | Audit status | Evidence reviewed | Remaining issue |
|---|---|---|---|
| 6.1 ABG known-answer reproduction | PASS | Unchanged `Proforma.py` run: $291.751666/share, displayed $291.75; $0.001666 (0.000571%) from the approximate $291.75 known answer, within $0.01/share tolerance. | None identified. |
| 6.2 Independent SEC input verification | PASS | SEC FY2025 Form 10-K was opened and checked; consolidated revenues on page 45 are $80,269m, equal to the model input. | Verification covers the selected material revenue input, not every filing-derived value. |
| 6.3 Timestamped prediction and post-lock test | PASS | GitHub commit `402802fe2c75f9936fe8c366ceaf14cf7f6a0519` was timestamped 2:52:42 PM EDT, after the 2:49 PM prediction and before the 2:57:50 PM test; the $1,300m case records actual results and a prediction comparison. | None identified. |
| 6.4 Accounting and valuation validations | PASS | Forecast balance-sheet/cash reconciliation, FY2025 reconciliation, EV-to-equity/share bridge, WACC/growth monotonicity, and peer bridge checks passed within stated tolerances. | Lease, affiliate, and bridge-policy choices remain disclosed valuation limitations, not arithmetic failures. |
| 6.5 $6,000m financing-failure test | PASS | Compound stress first fails in 2030 at $6,873.550m ($873.550m over); 70% SG&A and $1,600m CapEx endpoint failures were also reproduced. | Failed-scenario values remain diagnostic only, not investable valuations. |
| 6.6 Fresh-environment cold run | PASS | Isolated Python 3.13.15 environment with `include-system-site-packages = false` ran ABG, integrated ADM, peers, Step 5, and Step 6 scripts; documented outputs and expected failures reproduced. | Temporary console logs are outside the project folder; the cold-run record contains their paths and observed results. |
| 6.7 AI-output decision | NEEDS EVIDENCE | Student’s QUALIFY decision is personally confirmed; calculations support the documented AI-assisted Step 5 revenue-growth explanation. | A preserved, verified verbatim original Codex response does not exist in the project. The cited explanation is AI-assisted, not verified original-output evidence. |

### Submission and next-step conclusion

Step 6 is **not fully ready for strict submission** if the grading rubric requires a genuine original AI-output artifact for 6.7. The only material evidence gap is that original-output record. The documented AI-assisted explanation, linked calculations, and confirmed personal qualification are available, but they are not a substitute for a saved original Codex response.

You **can proceed to Step 7** while preserving this report, but return to Step 6.7 before final submission if the instructor requires that original AI-output evidence. All other Step 6 requirements have PASS evidence, subject to the disclosed valuation-policy limitations.
