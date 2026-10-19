# ADM Pro-Forma Valuation Workbench — Step 4

## Purpose and interface design

`adm_valuation_workbench.ipynb` is an interactive, semi-adjustable pro-forma valuation workbench for FIN 43900 Project 1. It uses `ipywidgets` sliders for seven analyst-controlled assumptions and immediately refreshes the five-year statements, FCFF, DCF valuation, liquidity funding, and validation table. Amounts are USD millions except percentages and per-share amounts.

The controls are intentionally uniform FY2026E–FY2030E values. That retains the Step 2 base-case convention (each selected Step 2 operating assumption is repeated for the five forecast years) while making scenario adjustment concise. The interface has two buttons:

- **Reset to Base** restores the exact unrounded Step 2 values.
- **Run documented failure test** loads a financially infeasible Low-style stress case and leaves the failure visible.

The display shows the WACC, enterprise value, equity value, implied value per share, difference from base per share, annual EBIT and FCFF, facility balance, full linked statements, and validation results. A red warning appears whenever a facility balance exceeds its limit; borrowing is not clipped or hidden.

## Model integration

The original `adm_integrated_model.py` is preserved without modification. It remains the sole source of the operating forecast, three statements, FCFF, DCF, enterprise-to-equity bridge, liquidity facility calculation, and statement checks.

`adm_valuation_model.py` is a small callable adapter, not a replacement model. Its `run_workbench(assumptions)` function:

1. starts with a deep copy of the existing Step 2 `INPUTS`;
2. applies the selected operating inputs uniformly across the existing five forecast years;
3. translates the selected WACC into the existing model's cost-of-equity input by solving the original capital-weights equation;
4. calls the original `run_model()` and `dcf()` functions; and
5. returns the income statement, balance sheet, cash-flow statement, annual EBIT, FCFF, DCF, per-share valuation, facility balances, validation results, and any facility-limit failures.

This design means the notebook does not contain a second financial-statement or valuation engine, and it does not hard-code valuation outputs.

## Adjustable assumptions and guardrails

| Control | Exact Step 2 base | Workbench range | Rationale |
|---|---:|---:|---|
| Revenue growth | 2.00% | −5.00% to 10.00% | Broad contraction-to-recovery range without extreme revenue forecasts. |
| Gross margin | 6.75% | 3.00% to 15.00% | Encompasses substantial pressure and a strong recovery around ADM's low-margin base. |
| SG&A / gross profit | 65.00% | 40.00% to 85.00% | Allows material operating leverage or deleverage while preserving a non-negative operating-cost ratio. |
| Inventory days | 51 | 30 to 80 days | Brackets faster and slower working-capital conversion around the Step 2 base. |
| Annual CapEx | $1,400m | $500m to $2,500m | Covers materially lower and higher investment without making capital spending implausibly negative. |
| WACC | 6.6894040788% | 5.00% to 12.00% | Covers a reasonable discount-rate sensitivity range. |
| Terminal growth | 2.50% | 0.00% to 4.50% | Conservative perpetual-growth range. The maximum is below the minimum WACC. |

The adapter also explicitly rejects terminal growth greater than or equal to WACC. The widget ranges prevent that combination in normal use, and the model-level check remains a second protection.

## Base-case reproduction

With untouched base controls, the adapter returns these unrounded Step 2-model results:

| Measure | Result | Displayed approximation |
|---|---:|---:|
| WACC | 0.06689404078802966 | 6.69% |
| Enterprise value | 7,299.89786373014 | $7,299.9m |
| Equity value | −357.10213626985933 | −$357.1m |
| Implied value/share | −0.7408758013897496 | −$0.74 |
| FY2030 facility balance | 5,144.234317141196 | $5,144.2m |

The notebook derives the difference-from-base metric using this freshly calculated base result, not a typed valuation constant. Reset assigns the exact `base_assumptions()` values and triggers the same model calculation again.

## Documented facility failure scenario

The failure button applies the existing Step 2 Low-style stress: 0.0% revenue growth, 6.25% gross margin, 65.0% SG&A/gross profit, 53 inventory days, $1,600m annual CapEx, 7.5137425387% WACC, and 2.0% terminal growth. This runs through the current integrated model rather than reusing a prior-lab failure number.

The resulting FY2030 facility balance is $6,873.550439m, versus the $6,000m facility limit—an excess of $873.550439m. The notebook presents this as a prominent **FAIL — FINANCIALLY INFEASIBLE** warning with forecast year, actual borrowing, limit, excess borrowing, and the explanation that current financing assumptions cannot fund the forecast.

## Validation results and local tests

The following local tests passed against the created callable adapter:

- Base model reproduction: exact model WACC and reported base-case EV, equity value, per-share value, and FY2030 facility balance matched the Step 2 calculations shown above.
- Stress scenario: the current integrated model returned a FY2030 facility failure of $6,873.550439m, above the $6,000m limit.
- Financial-statement validation: for each forecast year, balance-sheet gap, cash-flow-to-balance-sheet cash reconciliation, retained-earnings roll-forward, and debt roll-forward were zero within the Step 2 $0.01 tolerance. Minimum-cash compliance passed. Base facility-limit compliance passed in every forecast year.
- Driver sensitivity: changing revenue growth, margin, SG&A percentage, inventory days, CapEx, WACC, or terminal growth changes one or more linked statement, FCFF, DCF, or liquidity outputs through `run_workbench()`.
- Reset equivalence: passing the exact base assumptions to `run_workbench()` returns the same outputs as calling it with no assumptions.
- Notebook integrity: the `.ipynb` parses as valid notebook JSON and all ordinary Python cells compile locally. The upload/setup cell contains a Colab shell command and is intentionally not valid in a plain Python compiler.

Google Colab itself was not available in this environment, so its browser rendering and file-upload interaction were not claimed as tested.

## How to use in Google Colab

1. Upload `adm_valuation_workbench.ipynb` to Google Colab and open it.
2. Run the **Colab setup** cell. When prompted, upload `adm_integrated_model.py` and `adm_valuation_model.py` from the same project directory.
3. Run the import/base-case cell, then the controls cell.
4. Adjust a slider and review the immediately refreshed calculations and validation checks.
5. Use **Reset to Base** to return to the Step 2 case, or **Run documented failure test** to demonstrate the financing-limit warning.

## Known limitations

- The workbench exposes only seven drivers requested for Step 4. Other Step 2 inputs (tax, dividends, DSO/DPO, other current accounts, cash floor, facility limit, and share count) remain as modeled in Step 2.
- Widget operating inputs are uniform across the five forecast years, not year-specific.
- WACC is implemented by deriving cost of equity within the original Step 2 capital-weight methodology; it does not change debt weights or other capital-market assumptions.
- The facility is a Step 2 liquidity stress-test balance, not a fully specified forecast refinancing or terminal-capital-structure policy. The existing Step 2 valuation policy excludes projected facility draws from FCFF and the current-date equity bridge.
- Colab compatibility depends on the user uploading both local Python files, because the notebook deliberately has no Windows-specific paths or public repository dependency.

## AI assistance disclosure

Codex created the separate callable adapter, interactive notebook, documentation, and local validation checks. It did not modify the original Step 2 model, prior labs, or Step 3 files. The student remains responsible for reviewing assumptions, sources, model policy, and submitted conclusions.
