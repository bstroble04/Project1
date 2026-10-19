# Archer-Daniels-Midland Company (ADM) — Investment Committee Memo

**Valuation date:** October 16, 2026  
**Observed ADM close:** $82.61 per share  
**Recommendation:** **WATCH/DEFER — do not initiate a position at this time**

All amounts are USD millions except per-share values, rates, and multiples. This memo uses only project evidence and public information available on or before October 16, 2026.

## 1. Executive Recommendation

The confirmed recommendation is **WATCH/DEFER**. At the October 16, 2026 closing price of $82.61, the price is not supported by the project’s October 16 linked-model Base case or funded High case. The Base case produces a negative mathematical residual equity value of **-$0.756951 per share** and the funded High case produces **$24.219192 per share**. The Low case produces **-$14.315280 per share** but fails the model’s $6,000m financing-facility constraint, so it is diagnostic only and is not used as an investable value. [StockAnalysis historical prices](https://stockanalysis.com/stocks/adm/history/) and [ChartExchange historical prices](https://chartexchange.com/symbol/nyse-adm/historical/) both report the $82.61 October 16 close; the linked scenario evidence is in `adm_step7_decision_analysis.md` and `adm_step7_oct16_scenarios.py`.

The negative Base output is a mathematical residual from the model’s enterprise-to-equity bridge, not a claim that ADM shares can trade at a negative price. In the Base case, enterprise value plus the bridge’s included cash and securities is below defined debt and other claims. The result signals that the stated forecast, discount-rate, and bridge assumptions do not support a positive common-equity residual; it is not a tradable price target.

The main challenge to WATCH/DEFER is that the BG EV/EBITDA comparison implies $83.72 per ADM share, close to the observed price, and ADM’s August 4, 2026 release raised FY2026 adjusted-EPS guidance to approximately $5.15–$5.60. Those facts justify continued monitoring and a model refresh when supported operating evidence arrives. They do not, by themselves, resolve the DCF’s margin, working-capital, reinvestment, and bridge limitations or establish an initiate case. [ADM Q2 2026 release](https://investors.adm.com/news/news-details/2026/ADM-Reports-Second-Quarter-2026-Results/default.aspx)

## 2. Company Overview

ADM’s documented business scope includes agricultural commodity origination, processing, merchandising, transportation, and nutrition/ingredient businesses. That mix exposes operating results to commodity prices, processing margins, inventory levels, logistics, and the cash required to move product through the supply chain. [ADM FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm); `Lab08-notes.md`; `Lab10-notes.md`.

The project therefore treats ADM as a commodity-exposed, working-capital-intensive business. Revenue, gross margin, inventory days, receivable days, payable days, other current assets, and accrued-payable ratios are linked through a five-year three-statement forecast. This is important because forecast revenue growth can increase operating profit while also requiring more cash in receivables, inventory, and other operating working-capital accounts.

The model’s FY2025 opening balance sheet contains $10,369m of inventory, $3,021m of trade receivables, and $5,195m of trade payables. Forecast operating working capital is defined as trade receivables plus inventory plus other current assets, less trade payables and accrued expenses/other payables. The model uses a 51-day inventory assumption, 13.73 days sales outstanding, and 25.21 days payable outstanding; the latter two are calculated from FY2025 balances and flows. These are transparent forecast drivers, not management guidance. [ADM FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm); `adm_model_documentation.md`.

Capital spending is equally material. The October 16 Base case assumes $1,400m annual CapEx, while ADM’s August 4 release stated a $1.3bn–$1.5bn CapEx projection. Because FCFF deducts CapEx and operating-working-capital investment, changes to either can affect both cash generation and modeled facility usage. `adm_integrated_model.py`; [ADM Q2 2026 release](https://investors.adm.com/news/news-details/2026/ADM-Reports-Second-Quarter-2026-Results/default.aspx).

## 3. Historical Financial Evidence

The historical inputs below are preserved in `adm_integrated_model.py` from the project’s Lab 10 evidence; the FY2025 opening balance sheet and cash-flow reconciliation were checked against ADM’s FY2025 Form 10-K. No independent normalization has been applied to the FY2023–FY2025 income-statement series in this memo.

| Fiscal year | Revenue | Gross profit | Gross margin | SG&A | Net income attributable to ADM | Inventory | PP&E, net | Shareholders’ equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023A | $93,935 | $7,513 | 8.00% | $3,456 | $3,483 | $11,957 | $10,508 | $24,145 |
| 2024A | $85,530 | $5,778 | 6.76% | $3,706 | $1,800 | $11,572 | $10,837 | $22,178 |
| 2025A | $80,269 | $5,033 | 6.27% | $3,609 | $1,078 | $10,369 | $11,179 | $22,740 |

**Source:** `adm_integrated_model.py`, `HISTORICAL`; FY2025 supporting reconciliation and source links in `adm_model_documentation.md` and [ADM FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm).

Revenue, gross profit, gross margin, and net income declined across the displayed period, while PP&E increased from $10,508m to $11,179m. This history supports treating margin sustainability, working-capital conversion, and reinvestment needs as key valuation questions rather than assuming that higher sales automatically become higher FCFF. The model separately holds paired segregated cash/investments and brokerage-customer payables outside ordinary operating working capital; this is a classification policy based on the FY2025 filing, not an adjustment to reported historical earnings. `adm_model_documentation.md`.

## 4. Valuation Methodology

The integrated model forecasts FY2026E–FY2030E income statements, balance sheets, and cash-flow statements. FCFF is calculated as:

`EBIT × (1 − tax rate) + depreciation − CapEx − change in operating NWC`.

The final Base case uses 2.0% annual revenue growth, 6.75% gross margin, SG&A equal to 65.0% of gross profit, 51 inventory days, $1,400m annual CapEx, an 18.0% tax rate, 2.5% terminal growth, a $500m minimum-cash policy, and a $6,000m liquidity-facility test. The October 16 Base WACC is **6.693679%**, recalculated in memory using the $82.61 closing price and the existing 482.0m share-count basis; the earlier September 24 WACC of 6.689404% is retained only as historical comparison evidence. `adm_step7_oct16_scenarios.py`; `adm_step7_wacc_comparison.py`; `adm_step7_decision_analysis.md`.

The DCF discounts explicit FCFF and a Gordon-growth terminal value. The terminal-growth assumption is 2.5%, below the 6.693679% Base WACC. The original Base model reports terminal value as a substantial portion of enterprise value, so the terminal-growth and discount-rate assumptions require judgment. `adm_integrated_model.py`; `adm_model_documentation.md`.

The enterprise-to-equity bridge adds $1,047m of cash and short-term marketable securities, then subtracts $8,410m of defined interest-bearing debt and $294m of temporary equity/noncontrolling claims. It excludes segregated cash, does not capitalize leases, and does not separately value affiliate investments. On the October 16 Base case, enterprise value is $7,292.15m and the bridge yields equity value of -$364.85m, or -$0.756951 per 482.0m shares. This negative residual is an output of the specified bridge and assumptions, not a conventional negative share-price estimate. `adm_step7_decision_analysis.md`; `adm_model_documentation.md`.

## 5. Comparable Company Analysis

The peer work compares ADM with Bunge Global SA (BG) and Ingredion Incorporated (INGR). It uses September 24, 2026 share prices, FY2025 reported earnings/EBITDA, and the latest then-available peer balance sheets. The timing and definition differences are retained rather than hidden.

| Method | ADM implied value/share | Interpretation |
|---|---:|---|
| BG P/E | $50.05 | Below the October 16 ADM price; based on BG’s FY2025 reported diluted EPS and a 22.45x P/E. |
| INGR P/E | $19.25 | Below the October 16 price; based on INGR’s FY2025 reported diluted EPS and an 8.63x P/E. |
| BG EV/EBITDA | $83.72 | Close to the $82.61 market price; uses BG’s 16.66x multiple and its reported Total EBIT plus D&A EBITDA construction. |
| INGR EV/EBITDA | $17.75 | Well below the October 16 price; reflects a different business mix and EBITDA construction. |

**Source:** `adm_peer_comps.py`, `adm_peer_comps_documentation.md`. Supporting filings: [BG FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1996862/000162828026009842/bg-20251231.htm), [BG Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1996862/000162828026050540/bg-20260630.htm), [INGR FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1046257/000162828026008603/ingr-20251231.htm), and [INGR Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1046257/000162828026054722/ingr-20260630.htm).

The outputs are not averaged. The DCF forecasts unlevered cash flow and uses a defined enterprise-to-equity bridge; P/E measures after-financing and after-tax peer earnings; EV/EBITDA also depends on capital structure and non-common claims. BG’s result is the most favorable peer indication, but it uses a different EBITDA definition and a post-Viterra balance sheet. The two-peer sample, FY2025 earnings basis, and balance-sheet-date mismatch limit its use as a stand-alone valuation conclusion. `adm_peer_comps_documentation.md`; `adm_step7_decision_analysis.md`.

## 6. Scenario and Sensitivity Analysis

The October 16 scenarios rerun the linked model with October 16 market capitalization. Scenario-specific WACCs retain the original scenario-specific cost-of-equity assumptions, while each uses October 16 capital weights.

| Scenario | Key operating inputs | WACC | DCF value/share | 2030 facility | Funding result | Investment interpretation |
|---|---|---:|---:|---:|---|---|
| Low | 0% growth; 6.25% margin; 53 inventory days; $1,600m CapEx; 2.0% terminal growth | 7.519299% | -$14.315280 | $6,873.55 | **FAIL**; $873.55m over limit | Diagnostic only; not investable. |
| Base | 2% growth; 6.75% margin; 51 inventory days; $1,400m CapEx; 2.5% terminal growth | 6.693679% | -$0.756951 | $5,144.23 | PASS; $855.77m headroom | Negative bridge residual, not a tradable negative price. |
| Funded High | 3% growth; 7.25% margin; 49 inventory days; $1,200m CapEx; 3.0% terminal growth | 6.074464% | $24.219192 | $3,126.30 | PASS; $2,873.70m headroom | Funded model output, still below the $82.61 close. |

**Source:** `adm_step7_oct16_scenarios.py`; `adm_step7_decision_analysis.md`.

The Step 5 one-driver tests reinforce that cash conversion is as important as earnings. These tests use the earlier September 24 WACC basis and should be read as sensitivities, not as the final October 16 scenarios.

| Step 5 one-driver case | 2030 FCFF | DCF value/share | 2030 facility | Status / implication |
|---|---:|---:|---:|---|
| 70% SG&A / gross profit | $107.1 | -$11.77 | $6,418.6 | **FAIL**; $418.6m over the facility limit. |
| $1,600m annual CapEx | $165.3 | -$9.27 | $6,176.8 | **FAIL**; $176.8m over the facility limit. |
| 53 inventory days | $343.5 | -$1.94 | $5,656.4 | PASS, but lower FCFF and reduced headroom. |
| 6.189404% / 7.189404% WACC | $352.4 / $352.4 | $1.40 / -$2.42 | $5,144.2 / $5,144.2 | Discount-rate changes affect value without changing operating cash flow. |
| 2.0% / 3.0% terminal growth | $352.4 / $352.4 | -$2.18 / $1.08 | $5,144.2 / $5,144.2 | Terminal-growth choice materially affects value without changing operating cash flow. |

**Source:** `adm_step5_sensitivity_report.md`. Failed cases retain raw model outputs for diagnosis but are not valid investable valuations.

The authorized Step 6.3 $1,300m CapEx test is also relevant: relative to the $1,400m Base case, 2030 EBIT increased $35.84m, FCFF increased $93.55m, DCF value/share increased $4.27, and the facility balance fell $516.28m to $4,627.96m. It passed all stated accounting validations. This supports using lower CapEx as a monitored model input, not assuming that the lower spend level is sustainable. `adm_step6_validation_report.md`.

## 7. Validation and Limitations

| Validation item | Result | Evidence |
|---|---|---|
| ABG known-answer reproduction | **PASS** | Unchanged `Proforma.py` reproduced $291.751666/share, displayed as $291.75, within a $0.01/share tolerance. |
| Selected SEC-input verification | **PASS** | FY2025 ADM consolidated revenue of $80,269m was opened and checked against the model input. |
| Locked $1,300m CapEx prediction and test | **PASS** | GitHub commit `402802fe2c75f9936fe8c366ceaf14cf7f6a0519` predates the authorized test; results and prediction comparison are documented. |
| Forecast accounting and valuation checks | **PASS** | Forecast balance-sheet and cash reconciliation, FY2025 reconciliation, bridge/share arithmetic, and WACC/terminal-growth monotonicity passed within stated tolerances. |
| Financing stress tests | **PASS as expected failures** | The compound Low case fails at $6,873.550m in 2030; 70% SG&A and $1,600m CapEx cases also reproduce financing failures. |
| Fresh-environment cold run | **PASS** | An isolated Python 3.13.15 environment ran the ABG, integrated ADM, peer, Step 5, and Step 6 scripts and reproduced documented outputs. |

**Source:** `adm_step6_validation_report.md`; `adm_step6_cold_run.md`.

Important limitations remain. Forecast growth, margin, CapEx, DSO/DPO, other-current-account ratios, tax rate, terminal growth, and the facility policy are assumptions or model inputs, not company guidance unless separately cited. The October 16 WACC only reweights existing market inputs using the October 16 market capitalization; beta, risk-free rate, ERP, debt-cost inputs, and the 482.0m share-count basis are retained. The bridge excludes segregated cash, does not capitalize leases, and does not separately value affiliate investments.

There is also a real-world/model discrepancy to monitor: ADM’s August 4 release raised adjusted-EPS guidance to $5.15–$5.60, while the DCF uses FCFF and its own operating assumptions. Adjusted EPS is non-GAAP and does not directly determine FCFF, working-capital needs, terminal value, or the bridge. The guidance is therefore evidence for review, not a substitute for linked-model inputs. [ADM Q2 2026 release](https://investors.adm.com/news/news-details/2026/ADM-Reports-Second-Quarter-2026-Results/default.aspx).

Finally, Step 6.7 has an unresolved evidence gap: the project documents an AI-assisted Step 5 explanation and a personally confirmed **QUALIFY** decision, but does not preserve a verified verbatim original Codex response. This limitation is disclosed rather than represented as resolved. `adm_step6_ai_decision.md`; `adm_step6_validation_report.md`.

## 8. Recommendation Conditions and Monitoring

Meeting any individual condition below does **not** automatically justify initiating a position. Each is a trigger for evidence review and, where applicable, a linked-model refresh.

| Condition type | Confirmed threshold | Evidence window and review frequency | Action if triggered |
|---|---|---|---|
| Valuation diagnostic | Sustained uniform gross margin of at least **13.9453%** for the five-year forecast period, versus 6.75% Base. | Review each quarterly release and the FY2026 annual filing; require management guidance plus reported-margin evidence, not one quarter. | Rebuild the DCF and reconsider whether an initiate case is supportable. This is not a quarterly operating target. |
| Model-refresh trigger | CapEx at the **$1.3bn** low end of guidance, linked-model 2030 FCFF of at least **$445.964m**, and facility balance no higher than **$4,627.956m** (at least **$1,372.044m** headroom). | Review 3Q and FY2026 releases; monitor each earnings release and recompute after each 10-Q/10-K. | Reassess cash conversion and reinvestment; rerun the model. |
| Model-based liquidity rule | Refreshed five-year facility balance at or below **$3,126.30m**, with at least **$2,873.70m** headroom and no year above $6,000m. | Recompute after each quarterly filing using updated working-capital balances and cash flow. | Reconsider whether funding risk has fallen enough to upgrade research priority; do not use a valuation if the facility fails. |
| Operating-performance monitoring rule | FY2026 adjusted EPS delivered or reaffirmed at least at **$5.15**. | Review 3Q and FY2026 earnings releases; monitor each earnings release. | Reconsider forecast margins, tax, CapEx, and cash-conversion inputs, then rerun the model. Adjusted EPS is not a direct DCF input. |

**Source:** `adm_step7_decision_analysis.md`; [ADM Q2 2026 release](https://investors.adm.com/news/news-details/2026/ADM-Reports-Second-Quarter-2026-Results/default.aspx).

## 9. AI-Use Disclosure and Source References

ChatGPT/Codex assisted with organizing financial data, developing and troubleshooting reproducible Python models, checking calculations, structuring sensitivity and validation reports, and improving written presentation. The student personally confirmed the Step 7 WATCH/DEFER decision, October 16 valuation date, 6.693679% Base WACC policy, retention of the September 24 comparison, and all four monitoring rules. AI assistance did not replace those personal decisions.

For Step 6.7, the project preserves an AI-assisted explanation of revenue-growth mechanics and the student’s confirmed **QUALIFY** decision. It does **not** preserve a verified verbatim original Codex response. The memo therefore does not claim that such an original response exists. `adm_step6_ai_decision.md`; `adm_step6_validation_report.md`.

Primary project references:

- `adm_integrated_model.py` and `adm_model_documentation.md` — linked statements, DCF, WACC, bridge, historical inputs, and model limitations.
- `adm_peer_comps.py` and `adm_peer_comps_documentation.md` — peer P/E and EV/EBITDA calculations, sources, dates, and comparability limits.
- `adm_step5_sensitivity_report.md` — one-driver sensitivity and financing-test results.
- `adm_step6_validation_report.md` and `adm_step6_ai_decision.md` — reproducibility, validation, locked-test, cold-run, and AI-use evidence.
- `adm_step7_decision_analysis.md`, `adm_step7_oct16_scenarios.py`, and `adm_step7_wacc_comparison.py` — final October 16 valuation-date analysis, scenarios, and historical WACC comparison.
- `README.md` — reproducible run sequence and dependency statement.

Primary external references:

- [ADM FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm)
- [ADM Q2 2026 results and guidance](https://investors.adm.com/news/news-details/2026/ADM-Reports-Second-Quarter-2026-Results/default.aspx)
- [StockAnalysis ADM historical prices](https://stockanalysis.com/stocks/adm/history/) and [ChartExchange ADM historical prices](https://chartexchange.com/symbol/nyse-adm/historical/)
- [BG FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1996862/000162828026009842/bg-20251231.htm) and [BG Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1996862/000162828026050540/bg-20260630.htm)
- [INGR FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1046257/000162828026008603/ingr-20251231.htm) and [INGR Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1046257/000162828026054722/ingr-20260630.htm)

No source published after October 16, 2026 is used.
