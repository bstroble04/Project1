# ADM Peer Comparables — Project 1 Step 3

## Scope and method

This documentation and `adm_peer_comps.py` are standalone Step 3 deliverables. They do not change the prior labs or the Step 2 integrated model. All monetary amounts and share counts are USD millions except per-share amounts and multiples. The common stock-price date is September 24, 2026. Price sources provide the closing prices of $110.21 for BG, $96.49 for INGR, and the Step 2 input of $81.88 for ADM.

FY2025 is the common EBITDA and P/E earnings period. The latest balance sheets publicly available before September 24, 2026 were the June 30, 2026 BG and INGR Forms 10-Q. This creates a date mismatch between FY2025 EBITDA and June 2026 balance-sheet inputs; it is disclosed rather than hidden. INGR’s 10-Q reports the share count as of August 5, 2026 (63.064m), not exactly June 30. BG reports 192.107m shares issued and outstanding at June 30.

## Peer-selection policy

Lab 8 already contained a contemporaneous peer-selection policy dated September 10, 2026. It required publicly traded operating companies with meaningful agricultural-commodity, processing, merchandising, food-ingredient, or related exposure and excluded companies with substantially different primary economics, unusable annual diluted EPS, or unavailable public information. This Step 3 document applies and expands that policy; it does not backdate a new peer-selection policy.

BG is the closer operating peer because of agricultural commodity origination, processing, merchandising, logistics, and oilseed exposure. Key limitations are its distinct geography and the Viterra transaction’s material effect on capital structure and share count. INGR offers agricultural raw-material processing and food/nutrition ingredient exposure, but its specialty-ingredient focus and much lower commodity-merchandising exposure make it a less direct ADM peer. Neither company is a perfect comparable, and two peers are too few for a broad market conclusion.

## P/E comparables

| Company | September 24, 2026 close | FY2025 diluted EPS | P/E | ADM implied value/share |
|---|---:|---:|---:|---:|
| BG | $110.21 | $4.91 | 22.45x | $50.05 |
| INGR | $96.49 | $11.18 | 8.63x | $19.25 |

Peer P/E equals peer closing price divided by FY2025 reported diluted EPS. Implied ADM price equals the peer P/E multiplied by ADM FY2025 diluted EPS of $2.23. These values differ from Lab 8 only because Lab 8 used September 10, 2026 prices ($124.59 BG and $101.13 INGR); its FY2025 EPS definitions were unchanged.

Sources: [Bunge FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1996862/000162828026009842/bg-20251231.htm), [Bunge historical prices](https://sg.finance.yahoo.com/quote/BG/history/), [Ingredion FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1046257/000162828026008603/ingr-20251231.htm), and [Ingredion historical prices](https://ca.finance.yahoo.com/quote/INGR/history/).

## EV/EBITDA policy

Enterprise value is market capitalization plus interest-bearing debt plus non-common claims, less cash and short-term investments. The policy excludes operating-lease liabilities for all companies because the denominator is not restated to a lease-capitalized EBITDA basis. It includes redeemable noncontrolling interests, noncontrolling interests, and INGR redeemable share-based payments because those claims sit ahead of common equity. This is a consistently applied book-value claim convention, not an assertion that each liability has market value equal to carrying value.

Affiliate investments are not separately deducted from EV. BG’s $1,307m investments in affiliates are operating-related on the June 30 balance sheet, and the filings do not establish a market value or a consistently non-operating classification. The same policy is used for all companies. A later analyst may elect to value material non-operating assets separately, but must do so with evidence and apply it consistently.

Cash is limited to cash and cash equivalents plus disclosed short-term investments. Restricted, segregated, trade-finance, and other non-cash current assets are not subtracted. BG’s $593m is cash and cash equivalents only; its $45m trade-finance time deposits and $3m restricted cash are excluded. INGR’s $952m is $948m cash and cash equivalents plus $4m short-term investments. ADM retains the $1,047m cash-and-marketable-securities input used by the current Step 2 bridge.

## EV/EBITDA inputs and calculations

| Company | Price date / price | Shares used | Balance-sheet date | Market cap | Debt | Cash / short-term investments | Other claims | Enterprise value | FY2025 EBITDA | EV/EBITDA |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| ADM | 9/24/2026 / $81.88 | 482.000 | Current Step 2 bridge | $39,466.2 | $8,410.0 | $1,047.0 | $294.0 | $47,123.2 | $2,882.0 | 16.35x |
| BG | 9/24/2026 / $110.21 | 192.107 | 6/30/2026 | $21,172.1 | $15,214.0 | $593.0 | $1,457.0 | $37,250.1 | $2,236.0 | 16.66x |
| INGR | 9/24/2026 / $96.49 | 63.064 | 6/30/2026; shares 8/5/2026 | $6,085.0 | $1,783.0 | $952.0 | $49.0 | $6,965.0 | $1,238.0 | 5.63x |

Calculation: `EV = (price × shares) + debt + other claims − cash/short-term investments`.

ADM’s FY2025 EBITDA is $1,073m net earnings including NCI + $446m interest on borrowings + $182m income-tax expense + $1,181m depreciation and amortization = $2,882m. It follows the current Step 2 model’s bridge and is not independently re-modeled here.

BG’s FY2025 EBITDA is $1,533m reported Total EBIT + $703m depreciation, depletion, and amortization = $2,236m. “Total EBIT” is Bunge’s reported measure, so it should not be mistaken for a standardized GAAP operating-income measure. BG debt is $4,588m short-term debt + $1,200m current long-term debt + $9,426m long-term debt = $15,214m. Other claims are $1,389m noncontrolling interests + $68m redeemable NCI.

INGR’s FY2025 EBITDA is $1,016m GAAP operating income + $222m depreciation and amortization = $1,238m. Debt is $41m short-term borrowings + $1,742m long-term debt = $1,783m. Its $49m share-based payments subject to redemption is included as an other claim; the June 30 balance sheet reports no redeemable or non-redeemable noncontrolling interest. The EBITDA definitions are not identical: BG uses reported Total EBIT, while ADM and INGR use an operating-income-style construction. This definition difference remains a comparability limitation.

Sources: [ADM FY2025 10-K](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm), [BG FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1996862/000162828026009842/bg-20251231.htm), [BG Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1996862/000162828026050540/bg-20260630.htm), [INGR FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1046257/000162828026008603/ingr-20251231.htm), and [INGR Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1046257/000162828026054722/ingr-20260630.htm).

## EV/EBITDA implied ADM values

The peer multiple is applied to ADM’s $2,882m EBITDA. The common ADM bridge is `implied EV − $8,410m debt − $294m other claims + $1,047m cash`, followed by division by 482m ADM shares.

| Peer multiple | Implied ADM enterprise value | Implied ADM equity value | Implied ADM value/share |
|---|---:|---:|---:|
| BG 16.66x | $48,012.0 | $40,355.0 | $83.72 |
| INGR 5.63x | $16,214.3 | $8,557.3 | $17.75 |

The calculations are arithmetic outputs, not price targets. The spread is economically informative: BG’s agriculture-merchant profile is closer to ADM but its Viterra-altered capital structure and reported Total EBIT definition matter; INGR’s specialty ingredients and lower leverage yield a much lower multiple.

## Reconciliation with P/E, DCF, and market price

| Method | ADM value/share | Interpretation |
|---|---:|---|
| BG EV/EBITDA implied | $83.72 | Closest peer’s FY2025 EBITDA multiple, with post-Viterra BG balance sheet |
| BG P/E implied | $50.05 | Peer market pricing of FY2025 earnings |
| INGR P/E implied | $19.25 | Specialty-ingredient peer’s FY2025 earnings multiple |
| INGR EV/EBITDA implied | $17.75 | Specialty-ingredient peer’s FY2025 EBITDA multiple |
| Step 2 DCF base | -$0.74 | Negative modeled residual equity value, not a literal tradable stock price |
| Step 2 DCF high | $24.26 | Higher operating/reinvestment scenario |
| ADM market price, September 24, 2026 | $81.88 | Observed closing market price |

The methods answer different questions and should not be mechanically averaged. The DCF values forecast unlevered cash flow and are highly sensitive to margins, CapEx, working capital, WACC, and terminal growth. P/E reflects peer earnings after financing and taxes. EV/EBITDA reflects peer capital structures and the treatment of non-common claims, but here it also carries an FY2025-versus-June-2026 timing mismatch and non-identical EBITDA definitions.

The evidence does not support an initiate recommendation at $81.88. The sole close-operating peer’s EV/EBITDA output is near the market price, but the other peer outputs ($17.75–$19.25), BG P/E ($50.05), and the current Step 2 DCF range are materially lower. Given the two-peer sample, Viterra comparability issue, and unresolved definition/timing limitations, the appropriately qualified conclusion is **watch/defer**, not a price target or a mechanical blend.

## Program validation and remaining limitations

Running `python adm_peer_comps.py` recalculates P/E, market capitalization, each EV bridge, EBITDA construction, EV/EBITDA, implied ADM EV/equity/per-share outputs, and validation checks. The program verifies units by maintaining all inputs in millions; confirms the disclosed price, balance-sheet, and share dates; checks EV bridges; checks EBITDA constructions; and checks the implied equity and per-share bridges.

Remaining judgment items are whether a later valuation should capitalize leases, separately value affiliate investments, use a different treatment for redeemable share awards, or harmonize BG’s Total EBIT to a GAAP operating-income-style denominator. The student should also independently preserve/download the historical-price evidence for September 24, 2026, because free historical-price pages can revise presentation or access. These limitations do not make the calculations pending; they limit the strength of an investment conclusion.

## AI assistance

Codex inspected the existing Lab 7 and Lab 8 materials, maintained the September 10, 2026 peer-selection policy, retrieved the cited SEC filings and historical-price inputs, completed this separate program and documentation, and ran its arithmetic validations. The student remains responsible for verifying sources, choosing the policy judgments, and making any investment conclusion.
