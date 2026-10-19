# ADM Integrated Model Documentation

## Scope and units

`adm_integrated_model.py` is a standalone FIN 43900 Project 1 Step 2 model. It leaves `proforma_adm.py` unchanged. Amounts are USD millions except per-share values and percentages. The model forecasts FY2026E–FY2030E and recalculates the income statement, balance sheet, cash flow statement, FCFF, DCF, scenarios, sensitivity, and reverse DCF when an editable `INPUTS` assumption changes.

## Current Step 2 model results

The model was extended rather than replaced. The FY2025 opening balance sheet is decomposed from the FY2025 Form 10-K rather than using residual “Other assets” and “Other liabilities” balances. The current model uses FY2025 cash of $1,015m; short-term marketable securities of $32m; segregated cash and investments of $8,432m; trade receivables of $3,021m; inventory of $10,369m; other current assets of $3,796m; PP&E of $11,179m; and other non-current assets of $14,545m. It separately presents $8,410m interest-bearing debt; $5,195m trade payables; $8,919m brokerage-customer payables; $3,313m accrued expenses and other payables; $1,348m lease liabilities; $1,135m deferred taxes; $1,042m other non-current liabilities; $287m temporary equity; and $22,740m shareholders’ equity.

The program was run successfully after these updates. Base FCFF is $108.4m, $254.1m, $286.6m, $319.4m, and $352.4m from 2026E–2030E. Base WACC is **6.69%**; PV of explicit FCFF is $1,062.3m; PV of terminal value is $6,237.6m; EV is $7,299.9m; equity value is **negative $357.1m**; and value per 482m shares is **negative $0.74**. Terminal value is 85.45% of EV.

| Scenario | WACC | EV ($m) | Equity value ($m) | Value/share | 2030 facility ($m) | Funding |
|---|---:|---:|---:|---:|---:|---|
| Low | 7.51% | 758.3 | -6,898.7 | -$14.31 | 6,873.6 | FAIL |
| Base | 6.69% | 7,299.9 | -357.1 | -$0.74 | 5,144.2 | PASS |
| High | 6.07% | 19,351.4 | 11,694.4 | $24.26 | 3,126.3 | PASS |

The reverse DCF uses the sourced $81.88 September 24, 2026 closing price and solves for a **13.87%** uniform gross margin, versus the 6.75% base assumption. It reports a 2030 facility balance of $0.0m and PASS funding. The WACC sensitivity, scenarios, and reverse DCF each rerun the linked financial model rather than using static valuation values.

## Historical reconciliation and operating working capital

The opening-balance-sheet reconciliation is **PASS, $0.00m difference**. The historical CFO reconciliation is also **PASS, $0.00m difference**:

`$1,073m net earnings including NCI + $1,181m D&A + $361m impairment + $285m loss/gain on asset sales and investment revaluations − $211m other net + $2,763m other changes in operating assets and liabilities = $5,452m CFO`.

Operating NWC equals trade receivables + inventory + other current assets − trade payables − accrued expenses and other payables. Forecast receivables equal revenue × DSO / 365, using a base 13.73 DSO calculated from $3,021m / $80,269m × 365. Inventory retains the existing 51-day COGS driver. Trade payables equal COGS × DPO / 365, using a base 25.21 DPO calculated from $5,195m / $75,236m × 365. Other current assets and accrued expenses use their FY2025 percentages of revenue, 4.73% and 4.13%, respectively. These are transparent default drivers, not claims that ADM issued guidance for those ratios.

Segregated cash and investments and brokerage-customer payables remain paired, flat balances and are excluded from ordinary operating NWC. ADM states that brokerage-customer payables have corresponding segregated cash, investment, and customer-omnibus-receivable balances. The model does not treat ADM’s receivables securitization program as funded debt because ADM accounts for transferred receivables as sales and classifies related cash flows as operating activities.

Sources: [ADM FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm) and [ADM FY2025 results release](https://investors.adm.com/news/news-details/2026/ADM-Reports-Fourth-Quarter-and-Full-year-2025-Results-Provides-2026-Guidance/default.aspx).

## Assumptions, WACC, and valuation policy

The editable operating assumptions remain 2.0% annual revenue growth, 6.75% gross margin, SG&A equal to 65.0% of gross profit, 51 inventory days, depreciation equal to 10.5% of opening PP&E, annual CapEx of $1,400m, an 18.0% tax rate, a $500m minimum cash balance, and a $6,000m liquidity-facility limit. Dividends are $2.08 per share. The forecast DSO/DPO and other-current-account ratios are editable assumptions derived from FY2025 balances.

The base WACC uses a September 24, 2026 ADM closing price of $81.88 and 482m shares outstanding reported for June 30, 2026, yielding $39,466m market capitalization. It uses a 0.61 five-year-monthly beta, a 4.75% September 1, 2026 U.S.-dollar risk-free rate, and Damodaran’s 4.14% implied U.S. equity-risk premium. CAPM cost of equity is 7.28%. The 4.80% pre-tax cost of debt is calculated as ADM’s $446m FY2025 interest expense on borrowings divided by average FY2024–FY2025 defined interest-bearing debt of $9,283.5m. At an 18% tax rate and market debt/equity weights of 17.57%/82.43%, WACC is **6.69%**.

Sources: [ADM historical stock prices](https://www.investors.adm.com/stock-information/default.aspx), [Yahoo Finance beta observation](https://finance.yahoo.com/quote/ADM/), [Damodaran implied ERP](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm), and [ADM FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm). The September price date and June share-count reporting date do not exactly match; this is a disclosed judgment limitation.

The liquidity facility is a **liquidity stress test**, not a funded terminal-capital-structure assumption. It is financing cash flow only, excluded from FCFF and terminal FCFF, and not subtracted in the current-date bridge because opening facility debt is zero. The model still prints and tests the facility balance against the $6,000m limit. A model that instead treats facility draws as forecast debt requires a debt maturity/refinancing schedule and a revised terminal equity bridge.

The enterprise-to-equity bridge adds $1,015m cash and $32m short-term marketable securities, subtracts $8,410m defined interest-bearing debt, and subtracts $294m of temporary equity plus non-controlling interests. It does not add restricted or segregated cash and does not capitalize leases because the model does not separately convert lease expense to an operating metric. Investments in affiliates and leases require an explicit valuation-policy decision before any further bridge adjustment.

## Validation results

All current base-model validation checks printed PASS:

| Check | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---:|---:|---:|---:|---:|
| Assets − liabilities − equity | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 |
| Cash flow ending cash vs. balance-sheet cash | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 |
| Minimum cash compliance | PASS 0.00 | PASS -0.00 | PASS -0.00 | PASS -0.00 | PASS -0.00 |
| Facility compliance headroom | PASS 5,289.49 | PASS 4,186.37 | PASS 3,079.66 | PASS 1,969.42 | PASS 855.77 |
| Retained earnings roll-forward | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 |
| Debt roll-forward | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 | PASS 0.00 |

The low scenario is clearly identified as invalidly funded because its $6,873.6m 2030 facility balance exceeds the $6,000m limit.

## Step 2 — Model Findings and Investment Implications

The integrated financial model provides a foundation for evaluating whether ADM's current market price is supported by projected operating performance. The model connects the 2026–2030 financial statements to an FCFF discounted cash flow valuation, allowing changes in operating assumptions to flow directly into calculated equity value.

Under the current base assumptions, ADM produces an enterprise value of $7,299.9m and a negative residual equity value of $357.1m, equivalent to a model-implied value of **-$0.74 per share**. The upside scenario produces **$24.26 per share**, while the downside scenario exceeds the modeled $6,000m liquidity-facility limit and is therefore not considered a feasible funded case.

The reverse DCF indicates that ADM would need a gross margin of approximately **13.87%**, compared with the 6.75% base assumption, to justify the September 24, 2026 market price of $81.88 per share, holding the other reverse-DCF assumptions constant.

These results suggest that ADM's market valuation requires substantially stronger operating performance than the base forecast assumes. However, the model remains sensitive to profitability, capital expenditures, working-capital requirements, WACC, and terminal growth. These findings should be considered alongside peer valuation evidence and additional financial analysis before developing a final investment recommendation.

The accounting checks passed for all five forecast years. This confirms that the financial statements are internally consistent, although valuation still depends on assumptions and accounting classifications that require judgment.

## Remaining judgment calls

- Long-run DSO/DPO and other-current-account ratios.
- Treatment of leases and affiliate investments in the valuation bridge.
- Use of a June 2026 share count with a September 2026 share price.
- Beta and ERP provider selection.
- The 18% tax rate, terminal growth rate, dividend policy, and facility-stress-test policy.

## AI assistance

Codex assisted in creating the new integrated Python model, preserving the supplied Lab 10 inputs, implementing linked statements and validations, separating FCFF from financing, running the program, and drafting this documentation. The student remains responsible for filing verification, source citations, assumptions, and conclusions.

## Appendix — Superseded Model Results and Audit History

This appendix preserves the original audit trail and pre-update model output for transparency. The figures below are superseded by the current Step 2 results above and must not be presented as the current model results.

### Original model architecture and evidence gaps

The original version used FY2025 cash of $1,015m, inventory of $10,369m, PP&E of $11,179m, an aggregate $29,826m “Other assets” balance, $8,410m debt, aggregate $21,239m “Other liabilities,” and $22,740m equity. It did not separately forecast accounts receivable or trade payables; operating NWC reflected inventory only. The original audit identified FY2025 trade receivables of $3,021m, trade payables of $5,195m, other current assets of $3,796m, segregated cash and investments of $8,432m, short-term marketable securities of $32m, investments in affiliates of $5,560m, goodwill of $4,769m, intangible assets of $1,976m, right-of-use assets of $1,322m, other non-current assets of $918m, brokerage-customer payables of $8,919m, accrued expenses and other payables of $3,313m, lease liabilities, deferred taxes, temporary equity, and non-controlling interests. These filing facts supported the subsequent decomposition of the opening balance sheet.

The original FCFF formula was `EBIT × (1 − tax rate) + depreciation − CapEx − change in operating NWC`; it excluded interest expense, dividends, and facility draws. This distinction corrected the prior Lab 11 FCFE issue in which facility borrowing offset operating changes at the cash floor. The original bridge added only opening cash and subtracted $8,410m of interest-bearing debt. It did not double-count the facility because opening facility debt was zero. The audit noted that the projected facility balance should not be subtracted again from a current-date FCFF bridge without changing the valuation framework, while also noting that a persistent financing assumption would require a terminal net-debt reconciliation.

### Original, superseded valuation results

The prior model used a 7.01% WACC based on book-value capital weights, an 8.0% cost of equity, a 5.3% pre-tax cost of debt, and an 18.0% tax rate. It calculated FCFF of $98.6m, $220.0m, $252.0m, $284.0m, and $316.3m from 2026E–2030E; PV of explicit FCFF of $931.8m; PV of terminal value of $5,118.5m; EV of $6,050.4m; equity value of negative $1,344.6m; and base value of **negative $2.78 per share**. Its terminal value was $7,183.5m at 2030 and 84.60% of EV.

| Scenario | WACC | Enterprise value ($m) | Equity value ($m) | Value/share | 2030 facility ($m) | Funding |
|---|---:|---:|---:|---:|---:|---|
| Low | 7.74% | 703.1 | -6,691.9 | -$13.83 | 7,109.2 | FAIL |
| Base | 7.01% | 6,050.4 | -1,344.6 | -$2.78 | 5,507.2 | PASS |
| High | 6.28% | 16,654.1 | 9,259.1 | $19.13 | 3,551.0 | PASS |

The prior reverse DCF used a $82.42 intraday market-price input dated September 24, 2026 and solved for a **14.58%** uniform gross margin. The prior sensitivity table used a 6.0%–8.0% WACC range and 1.5%–3.0% terminal-growth range. Its reported facility headroom declined from $5,241.39m in 2026E to $492.80m in 2030E; all original base-model balance-sheet, cash-flow-cash, minimum-cash, facility, retained-earnings, and debt-roll-forward checks passed.

### Original audit sources

The original audit relied on [ADM FY2025 Form 10-K consolidated statements](https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm), including the balance sheet, cash-flow statement, debt note, and receivables-sale note.
