# ADM Step 5 — Sensitivity and Assumption Challenge

## Scope and reproducibility

Run `python adm_step5_sensitivity.py` from this directory to regenerate this report. The script uses `adm_valuation_model.run_workbench()` for the seven adapter-supported drivers and the unmodified `adm_integrated_model` only for the Step-5 tax-rate extension. It does not alter any prior model or lab file. Amounts are USD millions except per-share values and percentages.

Each operating control is applied uniformly to FY2026E–FY2030E, consistent with the existing adapter. Every sensitivity changes one independent driver only; statement outputs, FCFF, WACC for the tax cases, and facility borrowing are resulting dependent calculations.

## Base-case verification

Exact adapter base controls: revenue growth 2.00%; gross margin 6.75%; SG&A/gross profit 65.00%; inventory 51 days; CapEx $1,400m; WACC 6.6894040788%; terminal growth 2.50%. The Step 2 tax rate is 18.00%.

| Measure | Exact model output |
|---|---:|
| 2030E operating income | $838.871703m |
| 2030E FCFF | $352.414617m |
| DCF equity value/share | -$0.740876 |
| 2030E facility balance | $5,144.234317m |
| Facility validation | PASS — $500m minimum-cash policy and $6,000m facility limit preserved |

The reported base value is the current Step 2 residual equity value (about −$0.74/share), not the superseded Lab 11 $33.70/share result.

## One-driver-at-a-time sensitivity results

All differences are scenario minus the exact Step 2 base case. A failed facility result retains raw accounting and valuation outputs for diagnostics, but its valuation is not an investable or validated outcome.

| Case | Independent input passed to model | 2030E EBIT | 2030E FCFF | DCF $/share | 2030E facility | Facility | First failure / diagnostic | Δ EBIT | Δ FCFF | Δ $/share | Δ facility |
|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---:|
| Revenue growth |  |  |  |  |  |  |  |  |  |  |  |
| Lower | 0.00% | $641.5m | $380.9m | $1.08 | $4,668.8m | PASS | — | -197.4m | +28.5m | +1.83 | -475.4m |
| Base | 2.00% | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | 4.00% | $1,052.3m | $306.4m | -$3.29 | $5,670.1m | PASS | — | +213.5m | -46.0m | -2.55 | +525.8m |
| Gross margin |  |  |  |  |  |  |  |  |  |  |  |
| Lower | 6.25% | $683.8m | $224.6m | -$6.54 | $5,831.7m | PASS | — | -155.1m | -127.8m | -5.80 | +687.4m |
| Base | 6.75% | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | 7.25% | $994.0m | $480.2m | $5.06 | $4,456.8m | PASS | — | +155.1m | +127.8m | +5.80 | -687.4m |
| SG&A / gross profit |  |  |  |  |  |  |  |  |  |  |  |
| Lower | 60.00% | $1,138.0m | $597.7m | $10.28 | $3,886.7m | PASS | — | +299.1m | +245.3m | +11.02 | -1,257.5m |
| Base | 65.00% | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | 70.00% | $539.8m | $107.1m | -$11.77 | $6,418.6m | FAIL | 2030E; $6,418.6m; +$418.6m | -299.1m | -245.3m | -11.02 | +1,274.4m |
| Inventory days |  |  |  |  |  |  |  |  |  |  |  |
| Lower | 49 days | $838.9m | $361.3m | $0.46 | $4,632.1m | PASS | — | +0.0m | +8.9m | +1.20 | -512.2m |
| Base | 51 days | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | 53 days | $838.9m | $343.5m | -$1.94 | $5,656.4m | PASS | — | +0.0m | -8.9m | -1.20 | +512.2m |
| Annual CapEx |  |  |  |  |  |  |  |  |  |  |  |
| Lower | $1,200m | $910.5m | $539.5m | $7.79 | $4,111.7m | PASS | — | +71.7m | +187.1m | +8.53 | -1,032.6m |
| Base | $1,400m | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | $1,600m | $767.2m | $165.3m | -$9.27 | $6,176.8m | FAIL | 2030E; $6,176.8m; +$176.8m | -71.7m | -187.1m | -8.53 | +1,032.6m |
| WACC |  |  |  |  |  |  |  |  |  |  |  |
| Lower | 6.189404% | $838.9m | $352.4m | $1.40 | $5,144.2m | PASS | — | +0.0m | +0.0m | +2.14 | +0.0m |
| Base | 6.689404% | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | 7.189404% | $838.9m | $352.4m | -$2.42 | $5,144.2m | PASS | — | +0.0m | +0.0m | -1.68 | +0.0m |
| Terminal growth |  |  |  |  |  |  |  |  |  |  |  |
| Lower | 2.00% | $838.9m | $352.4m | -$2.18 | $5,144.2m | PASS | — | +0.0m | +0.0m | -1.44 | +0.0m |
| Base | 2.50% | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | 3.00% | $838.9m | $352.4m | $1.08 | $5,144.2m | PASS | — | +0.0m | +0.0m | +1.83 | +0.0m |
| Effective tax rate |  |  |  |  |  |  |  |  |  |  |  |
| Lower | 16.00% | $838.9m | $369.2m | -$0.05 | $5,110.2m | PASS | — | +0.0m | +16.8m | +0.69 | -34.0m |
| Base | 18.00% | $838.9m | $352.4m | -$0.74 | $5,144.2m | PASS | — | +0.0m | +0.0m | +0.00 | +0.0m |
| Higher | 20.00% | $838.9m | $335.6m | -$1.43 | $5,178.2m | PASS | — | +0.0m | -16.8m | -0.69 | +33.9m |

### Financing validation

The model continues to enforce the Step 2 $500m minimum cash policy and $6,000m facility limit. No borrowing is capped or hidden. For every `FAIL` above, the displayed facility balance and excess are the raw linked-model diagnostic; the scenario is excluded from any valid valuation comparison.

The Lab 11 file is retained as historical context only. It reported failure balances of $6,229.3m for 6.25% gross margin and $6,539.8m for $1,600m CapEx under the older model. This Step 5 analysis compares those results only qualitatively; it does not expect equality because the current Step 2 integrated model, FCFF framework, and valuation bridge were revised.

### Tax-rate methodology

The Step 5 tax cases change only `tax_rate` in a deep copy of the preserved Step 2 inputs. This is consistent with the model’s existing formulas: `FCFF = EBIT × (1 − tax rate) + depreciation − CapEx − change in operating NWC`, and `WACC = equity weight × cost of equity + debt weight × cost of debt × (1 − tax rate)`. Therefore, a tax-rate change affects both NOPAT/FCFF and WACC through the after-tax cost of debt. Cost of equity, capital weights, and all non-tax independent assumptions remain unchanged; the WACC movement is a dependent model calculation, not a separate methodology change.

| Tax rate | 2030E NOPAT | 2030E FCFF | Model WACC | DCF $/share |
|---:|---:|---:|---:|---:|
| 16.00% | $704.7m | $369.2m | 6.706282% | -$0.05 |
| 18.00% | $687.9m | $352.4m | 6.689404% | -$0.74 |
| 20.00% | $671.1m | $335.6m | 6.672526% | -$1.43 |

### Revenue-growth mechanics

The higher-growth result is not a data error. With gross margin, SG&A/gross profit, CapEx, days, and other ratios held constant, the model increases revenue in each forecast year. It also scales receivables, inventory, and other current assets with revenue (while trade payables scale with COGS and accrued payables scale with revenue). The resulting operating-NWC build can exceed the incremental NOPAT in the final year.

| Revenue growth | 2030E revenue | 2030E EBIT | 2030E NOPAT | 2030E increase in operating NWC | 2030E CFO | 2030E FCFF | 2030E facility draw | 2030E facility | DCF $/share |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00% | $80,269.0m | $641.5m | $526.0m | $0.0m | $1,331.6m | $380.9m | $1,071.0m | $4,668.8m | $1.08 |
| 2.00% | $88,623.5m | $838.9m | $687.9m | $190.3m | $1,288.9m | $352.4m | $1,113.7m | $5,144.2m | -$0.74 |
| 4.00% | $97,659.5m | $1,052.3m | $862.9m | $411.4m | $1,227.7m | $306.4m | $1,174.9m | $5,670.1m | -$3.29 |

From 2% to 4% growth, 2030E EBIT increases from $838.9m to $1,052.3m and NOPAT increases from $687.9m to $862.9m. However, the operating-NWC increase rises from $190.3m to $411.4m, a $221.1m additional cash use that exceeds the $175.1m NOPAT increase. With depreciation and CapEx unchanged in the growth-only test, FCFF falls from $352.4m to $306.4m. CFO falls from $1,288.9m to $1,227.7m, the 2030 facility draw rises from $1,113.7m to $1,174.9m, and the ending facility balance rises from $5,144.2m to $5,670.1m. Facility draws maintain the $500m cash floor but are financing cash flow; they are excluded from FCFF and the current-date DCF bridge. The lower FCFF also lowers terminal value, producing the lower DCF value/share. Both growth endpoints remain within the $6,000m facility limit.

## Driver importance — endpoint spans

A lower-to-higher span is `higher output − lower output`. It is sensitive to the chosen test range and units; it is not a probability-weighted forecast or a universal importance ranking. Where any endpoint fails financing, the value/share span is explicitly diagnostic only and is not used to rank investable outcomes.

| Driver | EBIT span | FCFF span | $/share span | Valuation-use status |
|---|---:|---:|---:|---|
| Revenue growth | +410.9m | -74.5m | -4.37 | valid three-case span |
| Gross margin | +310.2m | +255.6m | +11.60 | valid three-case span |
| SG&A / gross profit | -598.2m | -490.5m | -22.05 | diagnostic only; ≥1 endpoint fails |
| Inventory days | +0.0m | -17.8m | -2.39 | valid three-case span |
| Annual CapEx | -143.3m | -374.2m | -17.06 | diagnostic only; ≥1 endpoint fails |
| WACC | +0.0m | +0.0m | -3.82 | valid three-case span |
| Terminal growth | +0.0m | +0.0m | +3.26 | valid three-case span |
| Effective tax rate | +0.0m | -33.6m | -1.38 | valid three-case span |

Among the fully funded three-case tests, the largest endpoint span is Revenue growth for EBIT, Gross margin for FCFF, and Gross margin for value/share. That finding is conditional on these test widths, not a claim that the same driver is always most economically important.

Mechanically, margin and SG&A change operating profit; revenue growth changes the revenue base; inventory days change operating working capital; CapEx changes reinvestment and later depreciation; tax changes NOPAT and the debt tax shield in WACC; and WACC/terminal growth affect DCF discounting and terminal value. Financing stress is a separate feasibility constraint, not a reason to treat the raw failed valuation as valid.

## Assumption-challenge table

| Driver | Exact base assumption | Source or basis | Specific challenge / uncertainty | Evidence that would cause revision | Decision | Implication for recommendation |
|---|---:|---|---|---|---|---|
| Revenue growth | 2.00% | Analyst assumption in Step 2; FY2025 revenue is $80,269m in the ADM FY2025 10-K as documented in `adm_model_documentation.md`. | Uniform 2% growth may miss commodity-cycle and volume/price mix changes. | Updated ADM guidance, segment volume/pricing evidence, and subsequent filings. | Investigate | Higher durable growth can improve operating outputs, but does not itself prove the DCF supports market price. |
| Gross margin | 6.75% | Analyst assumption; Lab 11 cites approximately 8.00% (2023), 6.76% (2024), and 6.27% (2025). | Sustainability through commodity cycles is not established by the model. | Reconcile additional 10-K/quarterly gross-profit evidence and management/industry margin evidence; no guidance is asserted here. | Investigate | Primary research priority; lower-margin cases can impair funding feasibility. |
| SG&A / gross profit | 65.00% | Step 2 analyst operating assumption. | Ratio-based forecast may not reflect fixed-cost behavior or cost actions. | Segment/expense disclosures and management cost commentary, if verified. | Investigate | Can materially change EBIT and FCFF; avoid treating a tested range as a probability. |
| Inventory days | 51 days | Step 2 analyst working-capital assumption; business rationale is commodity inventory intensity. | Days may move with commodity prices, volumes, and inventory mix. | Updated inventory, COGS, and working-capital disclosures. | Investigate | Slower conversion increases cash needs and facility draws. |
| Annual CapEx | $1,400m | Step 2 analyst reinvestment assumption; Lab 11 selected it because ADM requires significant capital investment. | Required maintenance versus growth CapEx is not separated. | Company capital-spending plans and cash-flow disclosures, verified from filings. | Investigate | Higher CapEx reduces FCFF and can create financing stress. |
| Effective tax rate | 18.00% | Step 2 analyst assumption (`INPUTS['tax_rate']`); Step 5 direct-model extension. | Jurisdictional mix, discrete items, and loss utilization could differ. | Effective-tax-rate reconciliation and updated tax disclosures. | Investigate | Changes NOPAT and the after-tax debt component of WACC. |
| WACC | 6.6894040788% | Step 2 calculation: 9/24/2026 price, 482m June-2026 shares, 0.61 beta, 4.75% risk-free rate, 4.14% ERP, and 4.80% pre-tax debt cost; sources documented in `adm_model_documentation.md`. | Market inputs are dated and beta/ERP provider choices are judgmental. | Updated price, shares, rates, beta/ERP policy, and debt-cost evidence. | Revise when evidence updates | Discount-rate changes can materially change DCF value; not an operating forecast. |
| Terminal growth | 2.50% | Step 2 analyst perpetual-growth assumption. | Long-run growth is inherently judgmental and terminal value is a large share of EV. | Long-run nominal growth/inflation evidence and a documented terminal-value policy. | Investigate | A higher terminal rate can increase DCF value but must remain below WACC and be economically supportable. |

Sourced historical facts and dated market observations are identified above; all other forward values are analyst assumptions or model calculations. No unverified management guidance, quote, or date is presented as evidence.

## Lab 12 partner feedback and response

`Lab12-notes.md` documents the exchange with an **Ulta Beauty analyst partner**; the materials do not provide the partner’s name, so this report does not invent one. The documented questions were why gross margin and CapEx were chosen, whether the ranking changes when test ranges change, and why the prior model value differed from market price. The partner also identified stronger support for the gross-margin assumption as an improvement.

**Kept:** the $6,000m facility constraint and the practice of marking over-limit cases as unavailable for investment interpretation. **Revised:** the valuation discussion now uses the current Step 2 base of about −$0.74/share, not Lab 11’s superseded $33.70/share, and explains that DCF/peer/market differences reflect different assumptions rather than an automatic error by any one method. **Investigate:** sustainable gross margin, CapEx requirements, working-capital conversion, and the financing/refinancing policy. The broader eight-driver analysis also implements the partner’s range-ranking caution: a span changes when the test range or units change.

Additional analyst challenges (not attributed to the partner) are whether the $500m cash floor and facility stress-test policy are suitable for a terminal valuation framework, whether leases/affiliates require a bridge-policy adjustment, and whether forecast DSO/DPO assumptions remain appropriate. These are documented model limitations, not new facts.

## Recommendation

Maintain the provisional **watch/defer** recommendation. The current Step 2 DCF base has negative residual equity value while the peer documentation reports a wide, method-dependent range and a September 24, 2026 ADM market price of $81.88. These methods should not be mechanically averaged. A change in recommendation would require evidence that supports sustainably stronger margins, cash conversion, growth, or a defensible capital/terminal-value policy while retaining a feasible funding path; conversely, weaker margins, slower inventory conversion, higher CapEx, or tighter financing evidence would reinforce deferral.

## Verification performed by the script

- Reproduces the adapter base case and checks the exact Step 2 base controls before sensitivity runs.
- Runs lower/base/higher cases for all eight requested drivers and verifies the requested value reaches the model.
- Verifies that all non-facility accounting validations pass; facility `PASS`/`FAIL`, first failure year, balance, and excess are recorded separately.
- Verifies only one independent driver changes in each case. For WACC, cost of equity is the adapter’s dependent translation; for tax, the model’s WACC is a dependent calculation.
- Keeps raw failed-case outputs only as diagnostics and labels failed valuation spans as non-investable.
- Creates only this script and this report; it does not write to prior project files.

## AI-use disclosure

Codex assisted with structuring this reproducible Step 5 script and report, reading the existing project documentation and Lab 11/12 materials, and running the model checks. The student remains responsible for verifying all source evidence, selecting assumptions, and making the investment recommendation.
