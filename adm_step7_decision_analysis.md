# ADM Step 7 — Final Decision Analysis

## Scope and valuation date

This is an evidence-first final analysis for a fund that owns no ADM shares. The student's confirmed investment recommendation is WATCH/DEFER. The final valuation date is October 16, 2026.

Two independent historical-price pages report the same October 16, 2026 NYSE close: **$82.61/share**. StockAnalysis reports an $83.38 open, $84.03 high, $82.34 low, $82.61 close, and 2,852,347 volume; [StockAnalysis historical prices](https://stockanalysis.com/stocks/adm/history/) identifies the close and date. [ChartExchange historical prices](https://chartexchange.com/symbol/nyse-adm/historical/) independently reports the same OHLC and $82.61 close.

The **final Step 7 analysis** uses an in-memory October 16 market capitalization of $39,818.02m ($82.61 × the existing 482.0m shares) and the confirmed 6.693679% base WACC. The original September 24 $81.88 / 6.689404% WACC and all original model outputs remain preserved as historical comparison evidence; no original model input was overwritten.

Reproduce the original-scenario evidence with:

```powershell
py adm_step7_scenarios.py
```

The runner imports `adm_integrated_model.py` and `adm_peer_comps.py`, makes copies of inputs only in memory, and does not change prior model calculations or reports.

Reproduce the October 16 final-scenario analysis with:

```powershell
py adm_step7_oct16_scenarios.py
```

The October 16 date treatment is consistent across every scenario: each scenario uses the October 16 market capitalization and recalculates its capital weights from that value. The Low and High cases retain their original scenario-specific costs of equity, so their resulting WACCs (7.519299% and 6.074464%) appropriately differ from the 6.693679% October 16 Base WACC; they are not being mixed with September 24 capital weights.

## Evidence reviewed

- `adm_integrated_model.py` and `adm_model_documentation.md`: linked FY2026–2030 statements, FCFF DCF, scenario inputs, bridge policy, and accounting checks.
- `adm_step5_sensitivity_report.md`: one-driver sensitivities, facility constraints, and the distinction between valid and failed-case valuation outputs.
- `adm_step6_validation_report.md`: ABG known-answer, selected SEC-input, locked-test, validation, stress-test, and cold-run evidence.
- `adm_peer_comps.py` and `adm_peer_comps_documentation.md`: FY2025 P/E and EV/EBITDA peer calculations, dates, bridge policy, and comparability limits.
- ADM's [August 4, 2026 second-quarter release](https://investors.adm.com/news/news-details/2026/ADM-Reports-Second-Quarter-2026-Results/default.aspx), available before the valuation date: reported 2Q adjusted EPS of $1.84, raised FY2026 adjusted-EPS guidance to approximately $5.15–$5.60 from $4.15–$4.70, and continued to project $1.3–$1.5bn CapEx. Adjusted EPS is non-GAAP and is not substituted for the model's FCFF or DCF inputs.

No public information dated after October 16, 2026 is used in this analysis.

## Existing-model valuation evidence

All amounts are USD millions except per-share values and rates.

| Existing scenario | Key inputs | Per-share output | 2030 facility | Funding result | Interpretation |
|---|---|---:|---:|---|---|
| Downside / Low | 0% growth; 6.25% gross margin; 53 inventory days; $1,600m CapEx; 7.519299% WACC; 2.0% terminal growth | -$14.315280 | $6,873.55 | **FAIL**; $873.55m over limit | Diagnostic only; not an investable valuation. |
| Base | 2% growth; 6.75% gross margin; 51 inventory days; $1,400m CapEx; 6.693679% WACC; 2.5% terminal growth | -$0.756951 | $5,144.23 | PASS; $855.77m headroom | Negative residual equity value, not a literal negative stock price. |
| Upside / High | 3% growth; 7.25% gross margin; 49 inventory days; $1,200m CapEx; 6.074464% WACC; 3.0% terminal growth | $24.219192 | $3,126.30 | PASS; $2,873.70m headroom | Funded existing high scenario; still $58.39/share below the October 16 close. |

The table is a scenario framework, not an arbitrary price range. The downside output cannot be included in an investable valuation range because it violates the model's $6,000m liquidity-facility limit. The funded October 16 scenario evidence spans a negative base mathematical residual to a $24.219192 high case; that is not a tradable range or price target. The $82.61 market price is $83.37 above the base residual and $58.39 above the funded high case.

Negative equity results occur because the DCF enterprise value plus $1,047m cash/securities is less than the $8,410m defined debt plus $294m temporary equity/noncontrolling claims in the model's enterprise-to-equity bridge. They signal that these assumptions do not support positive common equity value; they do not mean ADM shares should trade below zero.

### Reverse-DCF check at the as-of price

With all October 16 base assumptions retained except a uniform FY2026–2030 gross margin, `adm_step7_oct16_scenarios.py` solves for a **13.9453%** margin to produce $82.61/share. That is **7.1953 percentage points** above the 6.75% base gross margin. The resulting 2030 facility is $0.0m and passes the facility test. The prior September 24 reverse-DCF hurdle was 13.9366%; the 0.0086-percentage-point change is not material. This is a valuation diagnostic, not a quarterly operating target or a forecast that ADM will achieve that margin.

### Read-only October 16 market-capitalization comparison

The historical September 24 versus October 16 sensitivity can be reproduced with:

```powershell
py adm_step7_wacc_comparison.py
```

The calculation makes an in-memory copy of the existing base inputs and changes **only** market capitalization from the documented September 24 close times the existing 482.0m share count to the October 16 close times that same share count. It holds the operating assumptions, debt, risk-free rate, beta, equity-risk premium, cost of debt, tax rate, and terminal growth unchanged. It does not overwrite `adm_integrated_model.py` or its inputs. The table is retained as historical comparison evidence; the October 16 scenario table above is the final decision-analysis basis.

| Measure | September 24 basis ($81.88) | October 16 basis ($82.61) | Change |
|---|---:|---:|---:|
| Market capitalization | $39,466.16m | $39,818.02m | +$351.86m |
| WACC | 6.689404% | 6.693679% | +0.004275 percentage points |
| Enterprise value | $7,299.90m | $7,292.15m | -$7.75m |
| Equity value | -$357.10m | -$364.85m | -$7.75m |
| DCF value/share | -$0.740876 | -$0.756951 | -$0.016075 |
| 2030 facility balance | $5,144.23m | $5,144.23m | $0.00m |

The higher market capitalization slightly increases the equity weight. Because the existing 7.2754% cost of equity exceeds the 3.9395% after-tax cost of debt, WACC rises slightly and the DCF value falls slightly. This is a sensitivity comparison, not a claim that all market inputs should be updated mechanically. The confirmed policy for this analysis is to reweight the existing WACC inputs using the October 16 market capitalization while retaining the disclosed beta, risk-free rate, ERP, debt inputs, and 482.0m share-count basis.

## Peer-evidence reconciliation

The existing peer work uses September 24, 2026 prices, FY2025 earnings/EBITDA, and June/August 2026 balance-sheet/share inputs. It should not be mechanically averaged with an FCFF DCF or with the October 16 market price.

| Existing peer method | ADM implied value/share | Comparison with $82.61 as-of close | Key limitation |
|---|---:|---:|---|
| BG P/E | $50.05 | $32.56 below | FY2025 EPS; closer operating peer but Viterra changed capital structure. |
| INGR P/E | $19.25 | $63.36 below | Specialty-ingredients economics are less directly comparable. |
| BG EV/EBITDA | $83.72 | $1.11 above | Closest output to market, but uses BG reported Total EBIT, FY2025 EBITDA, and a later balance sheet. |
| INGR EV/EBITDA | $17.75 | $64.86 below | Different business mix, leverage, and EBITDA construction. |
| October 16 DCF base / funded high | -$0.76 / $24.22 | $83.37 / $58.39 below | Five-year FCFF, terminal value, working-capital, reinvestment, and bridge assumptions. |

The DCF uses forecast unlevered cash flow and a policy-defined equity bridge. P/E uses peer after-tax, after-financing earnings. EV/EBITDA carries capital-structure and claim-policy differences; here it also has FY2025-versus-2026 timing mismatch and non-identical EBITDA definitions. The BG EV/EBITDA result is the strongest valuation challenge to watch/defer, while the remaining peer outputs and all funded DCF outputs are materially lower. Neither the small two-peer sample nor the divergent methods justify averaging them.

## Final investment recommendation — WATCH/DEFER

**Final decision: WATCH/DEFER; do not initiate now.** The price of $82.61 is not supported by the base or funded high existing DCF cases, and the reverse DCF requires a 13.94% uniform gross margin under all other base assumptions. The downside operating scenario is financially infeasible under the model's facility constraint. Peer evidence is mixed: the BG EV/EBITDA implication is near market, but both P/E methods, the INGR EV/EBITDA method, and the existing DCF results are lower.

The strongest challenge to this conclusion is the August 4 guidance increase to $5.15–$5.60 adjusted EPS, supported by strong 2Q execution and favorable crushing/ethanol/biofuels conditions, together with the BG EV/EBITDA comparison. These facts warrant monitoring and a model refresh; they do not establish that ADM can sustain the margins, working-capital conversion, or capital intensity implied by the market price.

## Confirmed measurable reversal or reconsideration conditions

**All four conditions below are confirmed monitoring and model-refresh rules.** They are not automatic instructions to initiate ADM. Each should prompt a documented rerun of the linked model using supported, updated inputs.

| Condition | Threshold and model support | Evidence window / frequency | Reconsidered action if triggered |
|---|---|---|---|
| Market-implied profitability diagnostic | Evidence supports a sustained uniform gross margin of at least **13.9453%** for the five-year forecast period, versus 6.75% base. This is the October 16 reverse-DCF threshold that produces $82.61/share with all other base inputs unchanged. | Each quarterly release and FY2026 annual filing; require management guidance plus reported margin evidence, not one quarter alone. | Rebuild the DCF and reconsider whether an initiate case is supportable. |
| Guided CapEx, FCFF, and financing | CapEx at the **$1.3bn low end** of ADM's $1.3–$1.5bn guidance range, with a linked-model 2030 FCFF of at least **$445.964m** and facility balance no higher than **$4,627.956m** (at least **$1,372.044m** headroom). This is the reproducible October 16 $1.3bn case, versus base FCFF $352.415m and $855.766m headroom. | At 3Q and FY2026 earnings releases; monitor each earnings release and recompute after each 10-Q/10-K. | Reconsider whether cash conversion and reinvestment support a more constructive watch-list posture; rerun the linked model, not an automatic initiation. |
| Liquidity and cash conversion | The refreshed five-year linked model ends with a facility balance at or below **$3,126.30m** (at least **$2,873.70m** headroom), the funded October 16 High-case benchmark, and never exceeds the $6,000m limit. | Recompute after each quarterly filing using updated working-capital balances and cash flow. | Reconsider whether funding risk has fallen enough to upgrade research priority; do not use a valuation if the facility fails. |
| Near-term earnings confirmation | FY2026 adjusted EPS is delivered or reaffirmed at least at the official **$5.15** lower-guidance bound. The threshold comes from the August 4 release; it is operating confirmation, not a DCF valuation input. The October 16 funded High DCF remains only $24.22/share, so this trigger requires a model rerun rather than an automatic initiation. | At 3Q and FY2026 earnings releases; monitor each earnings release. | Reconsider forecast margins, tax, CapEx, and cash conversion assumptions, then rerun the linked model. |

### Reversal-condition audit

| Condition | Classification | Audit conclusion |
|---|---|---|
| 13.9453% reverse-DCF gross margin | Model-implied valuation hurdle | Fully reproducible in `adm_step7_oct16_scenarios.py`; it is not a practical single-quarter operating rule because it assumes five years of uniform margin with every other base input fixed. It is a strong valuation diagnostic, not a forecast. |
| $1.3bn guided CapEx / $445.964m FCFF / $4,627.956m facility | Mixed reported-operating and model-monitoring rule | Reproducible in the October 16 $1.3bn CapEx case. The $1.3bn CapEx level is the low end of company guidance; FCFF and facility thresholds are model outputs, not reported company targets. It improves cash conversion versus base but produces only $3.50/share, so it should trigger a model refresh, not initiation. |
| Facility at or below $3,126.30m / $2,873.70m headroom | Model-derived liquidity-monitoring rule | Reproducible as the High-case facility result. It is useful only after an updated linked forecast; facility balance is not a directly reported operating metric. The hard constraint remains no modeled year above $6,000m. |
| FY2026 adjusted EPS at least $5.15 | Practical operating-monitoring rule | Supported by the August 4 guidance and practical to check at earnings releases. It is weak as a valuation reversal condition because adjusted EPS is non-GAAP and does not directly specify FCFF, gross margin, working capital, or the equity bridge. It should trigger an input review and rerun, not initiation. |

## Missing evidence, discrepancies, and judgment calls

- The DCF's WACC/market-capitalization calculation uses a September 24 $81.88 price, while this Step 7 comparison uses October 16 $82.61. Reweighting WACC, selecting a new beta/ERP observation, and matching share-count dates require a documented policy choice.
- The August guidance is adjusted EPS and does not directly provide the model's FCFF, gross-margin, DSO/DPO, or working-capital inputs. Converting it into a DCF assumption would require personal judgment and evidence.
- The peer set has only BG and INGR; BG is closer operationally but Viterra and its Total-EBIT definition affect comparability. No peer output is treated as a target or averaged with the DCF.
- The equity bridge excludes segregated cash, excludes lease capitalization, and does not separately value affiliate investments. Those are disclosed model-policy limitations.
- Step 6.7 retains a separate evidence gap: the documented explanation is AI-assisted, not a preserved verified original Codex output. This does not alter the calculation results but may affect the broader project’s submission evidence.

## Confirmed decisions and submission checks

1. **Confirmed final investment recommendation:** WATCH/DEFER; do not initiate ADM at the October 16, 2026 price of $82.61.
2. **Confirmed valuation policy:** use the October 16 market-capitalization basis and 6.693679% Base WACC for this final analysis; retain the September 24 valuation and 6.689404% WACC as historical comparison evidence.
3. **Confirmed monitoring rule:** $1.3bn CapEx / $445.964m FCFF / $4,627.956m facility balance (or $1,372.044m headroom) is a linked-model refresh trigger.
4. **Confirmed remaining monitoring rules:** 13.9453% reverse-DCF gross margin is a valuation diagnostic only; $3,126.30m facility / $2,873.70m headroom is a model-based liquidity rule; and adjusted EPS of at least $5.15 is a reported operating-performance monitoring rule, not direct valuation evidence.
5. Retain the cited historical-price pages and August 4 release with the submission, since public web pages can change.
6. Retain the Step 6.7 disclosure: its documented explanation is AI-assisted, not a preserved verified original Codex output.

## Step 7 completion audit

| Component | Status | Audit evidence |
|---|---|---|
| 7.1 — Valuation-date evidence and model basis | **COMPLETE** | October 16, 2026 closing price of $82.61 is cited from two historical-price sources; the 6.693679% October 16 Base WACC and original September 24 comparison are documented and reproducible. |
| 7.2 — Valuation analysis and investment conclusion | **COMPLETE** | The October 16 Base, Low, and High linked-model cases, peer reconciliation, bridge limitation, facility constraint, and confirmed WATCH/DEFER conclusion are documented. The failed Low case and negative equity residuals are not presented as tradable values. |
| 7.3 — Monitoring and reconsideration rules | **COMPLETE** | All four confirmed rules include numerical thresholds, evidence windows, monitoring frequency, and the investment action to reconsider; classifications distinguish valuation diagnostics, model rules, and reported operating metrics. |

Step 7 is complete for this analysis. The disclosed Step 6.7 original-AI-output evidence gap remains a separate project-level submission limitation and is not resolved or hidden here.
