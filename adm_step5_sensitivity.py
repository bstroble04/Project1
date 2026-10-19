"""Step 5: reproducible one-driver ADM sensitivity and assumption challenge.

Run from this project directory:
    python adm_step5_sensitivity.py

The seven workbench-supported drivers are passed through adm_valuation_model.
Effective tax rate is intentionally handled here (rather than by changing the
adapter): a deep copy of the Step 2 inputs is changed only for tax and then
run through the existing Step 2 linked model and DCF functions.
"""
from copy import deepcopy
from pathlib import Path

import adm_integrated_model as step2
from adm_valuation_model import base_assumptions, run_workbench, validation_results


OUTPUT_FILE = Path(__file__).with_name("adm_step5_sensitivity_report.md")
DRIVER_ORDER = (
    "revenue_growth", "gross_margin", "sga_pct_gross_profit", "inventory_days",
    "capex", "wacc", "terminal_growth", "tax_rate",
)
DRIVERS = {
    "revenue_growth": ("Revenue growth", "0.00%", "2.00%", "4.00%", (0.00, 0.02, 0.04)),
    "gross_margin": ("Gross margin", "6.25%", "6.75%", "7.25%", (0.0625, 0.0675, 0.0725)),
    "sga_pct_gross_profit": ("SG&A / gross profit", "60.00%", "65.00%", "70.00%", (0.60, 0.65, 0.70)),
    "inventory_days": ("Inventory days", "49 days", "51 days", "53 days", (49.0, 51.0, 53.0)),
    "capex": ("Annual CapEx", "$1,200m", "$1,400m", "$1,600m", (1200.0, 1400.0, 1600.0)),
    "wacc": ("WACC", "base − 0.50 pp", "exact base", "base + 0.50 pp", None),
    "terminal_growth": ("Terminal growth", "2.00%", "2.50%", "3.00%", (0.02, 0.025, 0.03)),
    "tax_rate": ("Effective tax rate", "16.00%", "18.00%", "20.00%", (0.16, 0.18, 0.20)),
}


def facility_status(result):
    """Return a funding label and the first failure details, if any."""
    failures = result["facility_failures"]
    if not failures:
        return "PASS", None, None, None
    year = min(failures)
    balance = failures[year]
    return "FAIL", year, balance, balance - result["facility_limit"]


def tax_result(tax_rate):
    """Step-5-only tax scenario using the preserved Step 2 engine."""
    inputs = deepcopy(step2.INPUTS)
    inputs["tax_rate"] = float(tax_rate)
    model = step2.run_model(inputs)
    dcf = step2.dcf(model)
    facility = {year: model["balance"][year]["Liquidity facility"] for year in step2.YEARS}
    failures = {year: balance for year, balance in facility.items()
                if balance > inputs["facility_limit"] + step2.TOL}
    return {
        "inputs": model["inputs"], "annual_operating_income": {
            year: model["income"][year]["Operating income (EBIT)"] for year in step2.YEARS},
        "fcff": {year: model["cashflow"][year]["FCFF"] for year in step2.YEARS},
        "per_share_valuation": dcf["per_share"], "liquidity_facility_balances": facility,
        "facility_failures": failures, "facility_limit": inputs["facility_limit"],
        "validation_results": validation_results(model), "dcf": dcf, "raw_model": model,
    }


def run_case(driver, value, base):
    """Run one scenario, changing exactly one independent assumption."""
    if driver == "tax_rate":
        result = tax_result(value)
        passed_value = result["inputs"]["tax_rate"]
    else:
        result = run_workbench({driver: value})
        if driver == "wacc":
            passed_value = result["dcf"]["wacc"]
        elif driver == "terminal_growth":
            passed_value = result["inputs"][driver]
        else:
            passed_value = result["inputs"][driver][0]
    status, first_year, failure_balance, excess = facility_status(result)
    return {
        "driver": driver, "input": float(value), "passed_value": passed_value,
        "ebit": result["annual_operating_income"][2030], "fcff": result["fcff"][2030],
        "per_share": result["per_share_valuation"],
        "facility": result["liquidity_facility_balances"][2030], "status": status,
        "first_failure_year": first_year, "failure_balance": failure_balance, "excess": excess,
        "d_ebit": result["annual_operating_income"][2030] - base["annual_operating_income"][2030],
        "d_fcff": result["fcff"][2030] - base["fcff"][2030],
        "d_per_share": result["per_share_valuation"] - base["per_share_valuation"],
        "d_facility": result["liquidity_facility_balances"][2030] - base["liquidity_facility_balances"][2030],
        "validation": result["validation_results"], "inputs": result["inputs"],
        "raw_model": result["raw_model"], "wacc": result["dcf"]["wacc"],
    }


def assert_case_integrity(case, base, base_controls):
    """Verify the model received the requested value and all checks remain intact."""
    driver = case["driver"]
    expected = case["input"]
    assert abs(case["passed_value"] - expected) < 1e-10, (driver, case["passed_value"], expected)
    assert all(detail["pass"] for name, detail in case["validation"].items()
               if name != "Liquidity facility within limit"), driver
    if driver == "tax_rate":
        assert case["inputs"]["tax_rate"] == expected
        for key in ("revenue_growth", "gross_margin", "sga_pct_gross_profit", "inventory_days", "capex"):
            assert case["inputs"][key] == step2.INPUTS[key], (driver, key)
    elif driver == "wacc":
        for key in ("revenue_growth", "gross_margin", "sga_pct_gross_profit", "inventory_days", "capex"):
            assert case["inputs"][key] == step2.INPUTS[key], (driver, key)
        assert case["inputs"]["terminal_growth"] == step2.INPUTS["terminal_growth"]
    else:
        for key in ("revenue_growth", "gross_margin", "sga_pct_gross_profit", "inventory_days", "capex"):
            if key != driver:
                assert case["inputs"][key][0] == base_controls[key], (driver, key)
        if driver != "terminal_growth":
            assert case["inputs"]["terminal_growth"] == base_controls["terminal_growth"]


def money(value, decimals=1):
    return f"${value:,.{decimals}f}m"


def share(value):
    return f"-${abs(value):,.2f}" if value < 0 else f"${value:,.2f}"


def signed_money(value):
    return f"{value:+,.1f}m"


def signed_share(value):
    return f"-{abs(value):,.2f}" if value < 0 else f"+{value:,.2f}"


def input_text(driver, value):
    if driver in {"revenue_growth", "gross_margin", "sga_pct_gross_profit", "wacc", "terminal_growth", "tax_rate"}:
        return f"{value:.6%}" if driver == "wacc" else f"{value:.2%}"
    if driver == "capex":
        return f"${value:,.0f}m"
    return f"{value:.0f} days"


def case_row(case, label):
    failure = "—" if case["status"] == "PASS" else (
        f"{case['first_failure_year']}E; {money(case['failure_balance'])}; +{money(case['excess'])}")
    return (f"| {label} | {input_text(case['driver'], case['input'])} | {money(case['ebit'])} | "
            f"{money(case['fcff'])} | {share(case['per_share'])} | {money(case['facility'])} | "
            f"{case['status']} | {failure} | {signed_money(case['d_ebit'])} | {signed_money(case['d_fcff'])} | "
            f"{signed_share(case['d_per_share'])} | {signed_money(case['d_facility'])} |")


def span_rows(results):
    rows = []
    for driver in DRIVER_ORDER:
        lower, base, higher = results[driver]
        raw = (higher["ebit"] - lower["ebit"], higher["fcff"] - lower["fcff"],
               higher["per_share"] - lower["per_share"])
        feasible = all(case["status"] == "PASS" for case in (lower, base, higher))
        valuation_use = "valid three-case span" if feasible else "diagnostic only; ≥1 endpoint fails"
        rows.append((DRIVERS[driver][0], *raw, valuation_use))
    return rows


def build_report(base, results):
    base_controls = base_assumptions()
    lines = [
        "# ADM Step 5 — Sensitivity and Assumption Challenge",
        "",
        "## Scope and reproducibility",
        "",
        "Run `python adm_step5_sensitivity.py` from this directory to regenerate this report. "
        "The script uses `adm_valuation_model.run_workbench()` for the seven adapter-supported drivers and the unmodified "
        "`adm_integrated_model` only for the Step-5 tax-rate extension. It does not alter any prior model or lab file. "
        "Amounts are USD millions except per-share values and percentages.",
        "",
        "Each operating control is applied uniformly to FY2026E–FY2030E, consistent with the existing adapter. "
        "Every sensitivity changes one independent driver only; statement outputs, FCFF, WACC for the tax cases, "
        "and facility borrowing are resulting dependent calculations.",
        "",
        "## Base-case verification",
        "",
        f"Exact adapter base controls: revenue growth {base_controls['revenue_growth']:.2%}; gross margin {base_controls['gross_margin']:.2%}; "
        f"SG&A/gross profit {base_controls['sga_pct_gross_profit']:.2%}; inventory {base_controls['inventory_days']:.0f} days; "
        f"CapEx ${base_controls['capex']:,.0f}m; WACC {base_controls['wacc']:.10%}; terminal growth {base_controls['terminal_growth']:.2%}. "
        f"The Step 2 tax rate is {step2.INPUTS['tax_rate']:.2%}.",
        "",
        "| Measure | Exact model output |",
        "|---|---:|",
        f"| 2030E operating income | {money(base['annual_operating_income'][2030], 6)} |",
        f"| 2030E FCFF | {money(base['fcff'][2030], 6)} |",
        f"| DCF equity value/share | {('-$' if base['per_share_valuation'] < 0 else '$')}{abs(base['per_share_valuation']):,.6f} |",
        f"| 2030E facility balance | {money(base['liquidity_facility_balances'][2030], 6)} |",
        "| Facility validation | PASS — $500m minimum-cash policy and $6,000m facility limit preserved |",
        "",
        "The reported base value is the current Step 2 residual equity value (about −$0.74/share), not the superseded Lab 11 $33.70/share result.",
        "",
        "## One-driver-at-a-time sensitivity results",
        "",
        "All differences are scenario minus the exact Step 2 base case. A failed facility result retains raw accounting and valuation outputs for diagnostics, but its valuation is not an investable or validated outcome.",
        "",
        "| Case | Independent input passed to model | 2030E EBIT | 2030E FCFF | DCF $/share | 2030E facility | Facility | First failure / diagnostic | Δ EBIT | Δ FCFF | Δ $/share | Δ facility |",
        "|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---:|",
    ]
    for driver in DRIVER_ORDER:
        name, low_label, base_label, high_label, _ = DRIVERS[driver]
        lines.append(f"| {name} |  |  |  |  |  |  |  |  |  |  |  |")
        for label, case in zip(("Lower", "Base", "Higher"), results[driver]):
            lines.append(case_row(case, label))
    lines += [
        "",
        "### Financing validation",
        "",
        "The model continues to enforce the Step 2 $500m minimum cash policy and $6,000m facility limit. "
        "No borrowing is capped or hidden. For every `FAIL` above, the displayed facility balance and excess are the raw linked-model diagnostic; the scenario is excluded from any valid valuation comparison.",
        "",
        "The Lab 11 file is retained as historical context only. It reported failure balances of $6,229.3m for 6.25% gross margin and $6,539.8m for $1,600m CapEx under the older model. "
        "This Step 5 analysis compares those results only qualitatively; it does not expect equality because the current Step 2 integrated model, FCFF framework, and valuation bridge were revised.",
        "",
        "### Tax-rate methodology",
        "",
        "The Step 5 tax cases change only `tax_rate` in a deep copy of the preserved Step 2 inputs. This is consistent with the model’s existing formulas: "
        "`FCFF = EBIT × (1 − tax rate) + depreciation − CapEx − change in operating NWC`, and "
        "`WACC = equity weight × cost of equity + debt weight × cost of debt × (1 − tax rate)`. Therefore, a tax-rate change affects both NOPAT/FCFF and WACC through the after-tax cost of debt. "
        "Cost of equity, capital weights, and all non-tax independent assumptions remain unchanged; the WACC movement is a dependent model calculation, not a separate methodology change.",
        "",
        "| Tax rate | 2030E NOPAT | 2030E FCFF | Model WACC | DCF $/share |",
        "|---:|---:|---:|---:|---:|",
    ]
    for case in results["tax_rate"]:
        ebit = case["raw_model"]["income"][2030]["Operating income (EBIT)"]
        tax_rate = case["inputs"]["tax_rate"]
        lines.append(f"| {tax_rate:.2%} | {money(ebit * (1 - tax_rate))} | {money(case['fcff'])} | {case['wacc']:.6%} | {share(case['per_share'])} |")
    revenue_cases = results["revenue_growth"]
    lines += [
        "",
        "### Revenue-growth mechanics",
        "",
        "The higher-growth result is not a data error. With gross margin, SG&A/gross profit, CapEx, days, and other ratios held constant, the model increases revenue in each forecast year. "
        "It also scales receivables, inventory, and other current assets with revenue (while trade payables scale with COGS and accrued payables scale with revenue). The resulting operating-NWC build can exceed the incremental NOPAT in the final year.",
        "",
        "| Revenue growth | 2030E revenue | 2030E EBIT | 2030E NOPAT | 2030E increase in operating NWC | 2030E CFO | 2030E FCFF | 2030E facility draw | 2030E facility | DCF $/share |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for case in revenue_cases:
        income = case["raw_model"]["income"][2030]
        cashflow = case["raw_model"]["cashflow"][2030]
        tax_rate = case["inputs"]["tax_rate"]
        lines.append(
            f"| {case['input']:.2%} | {money(income['Revenue'])} | {money(income['Operating income (EBIT)'])} | "
            f"{money(income['Operating income (EBIT)'] * (1 - tax_rate))} | {money(-cashflow['Change in operating NWC'])} | "
            f"{money(cashflow['Operating cash flow'])} | {money(case['fcff'])} | {money(cashflow['Borrowing (facility draw)'])} | "
            f"{money(case['facility'])} | {share(case['per_share'])} |")
    lines += [
        "",
        "From 2% to 4% growth, 2030E EBIT increases from $838.9m to $1,052.3m and NOPAT increases from $687.9m to $862.9m. "
        "However, the operating-NWC increase rises from $190.3m to $411.4m, a $221.1m additional cash use that exceeds the $175.1m NOPAT increase. "
        "With depreciation and CapEx unchanged in the growth-only test, FCFF falls from $352.4m to $306.4m. CFO falls from $1,288.9m to $1,227.7m, the 2030 facility draw rises from $1,113.7m to $1,174.9m, and the ending facility balance rises from $5,144.2m to $5,670.1m. "
        "Facility draws maintain the $500m cash floor but are financing cash flow; they are excluded from FCFF and the current-date DCF bridge. The lower FCFF also lowers terminal value, producing the lower DCF value/share. Both growth endpoints remain within the $6,000m facility limit.",
        "",
        "## Driver importance — endpoint spans",
        "",
        "A lower-to-higher span is `higher output − lower output`. It is sensitive to the chosen test range and units; it is not a probability-weighted forecast or a universal importance ranking. "
        "Where any endpoint fails financing, the value/share span is explicitly diagnostic only and is not used to rank investable outcomes.",
        "",
        "| Driver | EBIT span | FCFF span | $/share span | Valuation-use status |",
        "|---|---:|---:|---:|---|",
    ]
    spans = span_rows(results)
    for name, ebit_span, fcff_span, share_span, use in spans:
        lines.append(f"| {name} | {signed_money(ebit_span)} | {signed_money(fcff_span)} | {signed_share(share_span)} | {use} |")
    feasible_spans = [row for row in spans if row[-1] == "valid three-case span"]
    if feasible_spans:
        ebit_top = max(feasible_spans, key=lambda row: abs(row[1]))
        fcff_top = max(feasible_spans, key=lambda row: abs(row[2]))
        share_top = max(feasible_spans, key=lambda row: abs(row[3]))
        lines += ["", f"Among the fully funded three-case tests, the largest endpoint span is {ebit_top[0]} for EBIT, {fcff_top[0]} for FCFF, and {share_top[0]} for value/share. "
                  "That finding is conditional on these test widths, not a claim that the same driver is always most economically important."]
    lines += [
        "",
        "Mechanically, margin and SG&A change operating profit; revenue growth changes the revenue base; inventory days change operating working capital; CapEx changes reinvestment and later depreciation; "
        "tax changes NOPAT and the debt tax shield in WACC; and WACC/terminal growth affect DCF discounting and terminal value. Financing stress is a separate feasibility constraint, not a reason to treat the raw failed valuation as valid.",
        "",
        "## Assumption-challenge table",
        "",
        "| Driver | Exact base assumption | Source or basis | Specific challenge / uncertainty | Evidence that would cause revision | Decision | Implication for recommendation |",
        "|---|---:|---|---|---|---|---|",
        "| Revenue growth | 2.00% | Analyst assumption in Step 2; FY2025 revenue is $80,269m in the ADM FY2025 10-K as documented in `adm_model_documentation.md`. | Uniform 2% growth may miss commodity-cycle and volume/price mix changes. | Updated ADM guidance, segment volume/pricing evidence, and subsequent filings. | Investigate | Higher durable growth can improve operating outputs, but does not itself prove the DCF supports market price. |",
        "| Gross margin | 6.75% | Analyst assumption; Lab 11 cites approximately 8.00% (2023), 6.76% (2024), and 6.27% (2025). | Sustainability through commodity cycles is not established by the model. | Reconcile additional 10-K/quarterly gross-profit evidence and management/industry margin evidence; no guidance is asserted here. | Investigate | Primary research priority; lower-margin cases can impair funding feasibility. |",
        "| SG&A / gross profit | 65.00% | Step 2 analyst operating assumption. | Ratio-based forecast may not reflect fixed-cost behavior or cost actions. | Segment/expense disclosures and management cost commentary, if verified. | Investigate | Can materially change EBIT and FCFF; avoid treating a tested range as a probability. |",
        "| Inventory days | 51 days | Step 2 analyst working-capital assumption; business rationale is commodity inventory intensity. | Days may move with commodity prices, volumes, and inventory mix. | Updated inventory, COGS, and working-capital disclosures. | Investigate | Slower conversion increases cash needs and facility draws. |",
        "| Annual CapEx | $1,400m | Step 2 analyst reinvestment assumption; Lab 11 selected it because ADM requires significant capital investment. | Required maintenance versus growth CapEx is not separated. | Company capital-spending plans and cash-flow disclosures, verified from filings. | Investigate | Higher CapEx reduces FCFF and can create financing stress. |",
        "| Effective tax rate | 18.00% | Step 2 analyst assumption (`INPUTS['tax_rate']`); Step 5 direct-model extension. | Jurisdictional mix, discrete items, and loss utilization could differ. | Effective-tax-rate reconciliation and updated tax disclosures. | Investigate | Changes NOPAT and the after-tax debt component of WACC. |",
        "| WACC | 6.6894040788% | Step 2 calculation: 9/24/2026 price, 482m June-2026 shares, 0.61 beta, 4.75% risk-free rate, 4.14% ERP, and 4.80% pre-tax debt cost; sources documented in `adm_model_documentation.md`. | Market inputs are dated and beta/ERP provider choices are judgmental. | Updated price, shares, rates, beta/ERP policy, and debt-cost evidence. | Revise when evidence updates | Discount-rate changes can materially change DCF value; not an operating forecast. |",
        "| Terminal growth | 2.50% | Step 2 analyst perpetual-growth assumption. | Long-run growth is inherently judgmental and terminal value is a large share of EV. | Long-run nominal growth/inflation evidence and a documented terminal-value policy. | Investigate | A higher terminal rate can increase DCF value but must remain below WACC and be economically supportable. |",
        "",
        "Sourced historical facts and dated market observations are identified above; all other forward values are analyst assumptions or model calculations. No unverified management guidance, quote, or date is presented as evidence.",
        "",
        "## Lab 12 partner feedback and response",
        "",
        "`Lab12-notes.md` documents the exchange with an **Ulta Beauty analyst partner**; the materials do not provide the partner’s name, so this report does not invent one. The documented questions were why gross margin and CapEx were chosen, whether the ranking changes when test ranges change, and why the prior model value differed from market price. The partner also identified stronger support for the gross-margin assumption as an improvement.",
        "",
        "**Kept:** the $6,000m facility constraint and the practice of marking over-limit cases as unavailable for investment interpretation. **Revised:** the valuation discussion now uses the current Step 2 base of about −$0.74/share, not Lab 11’s superseded $33.70/share, and explains that DCF/peer/market differences reflect different assumptions rather than an automatic error by any one method. **Investigate:** sustainable gross margin, CapEx requirements, working-capital conversion, and the financing/refinancing policy. The broader eight-driver analysis also implements the partner’s range-ranking caution: a span changes when the test range or units change.",
        "",
        "Additional analyst challenges (not attributed to the partner) are whether the $500m cash floor and facility stress-test policy are suitable for a terminal valuation framework, whether leases/affiliates require a bridge-policy adjustment, and whether forecast DSO/DPO assumptions remain appropriate. These are documented model limitations, not new facts.",
        "",
        "## Recommendation",
        "",
        "Maintain the provisional **watch/defer** recommendation. The current Step 2 DCF base has negative residual equity value while the peer documentation reports a wide, method-dependent range and a September 24, 2026 ADM market price of $81.88. These methods should not be mechanically averaged. A change in recommendation would require evidence that supports sustainably stronger margins, cash conversion, growth, or a defensible capital/terminal-value policy while retaining a feasible funding path; conversely, weaker margins, slower inventory conversion, higher CapEx, or tighter financing evidence would reinforce deferral.",
        "",
        "## Verification performed by the script",
        "",
        "- Reproduces the adapter base case and checks the exact Step 2 base controls before sensitivity runs.",
        "- Runs lower/base/higher cases for all eight requested drivers and verifies the requested value reaches the model.",
        "- Verifies that all non-facility accounting validations pass; facility `PASS`/`FAIL`, first failure year, balance, and excess are recorded separately.",
        "- Verifies only one independent driver changes in each case. For WACC, cost of equity is the adapter’s dependent translation; for tax, the model’s WACC is a dependent calculation.",
        "- Keeps raw failed-case outputs only as diagnostics and labels failed valuation spans as non-investable.",
        "- Creates only this script and this report; it does not write to prior project files.",
        "",
        "## AI-use disclosure",
        "",
        "Codex assisted with structuring this reproducible Step 5 script and report, reading the existing project documentation and Lab 11/12 materials, and running the model checks. The student remains responsible for verifying all source evidence, selecting assumptions, and making the investment recommendation.",
        "",
    ]
    return "\n".join(lines)


def main():
    base_controls = base_assumptions()
    base = run_workbench()
    base_from_controls = run_workbench(base_controls)
    assert base["per_share_valuation"] == base_from_controls["per_share_valuation"]
    assert base["annual_operating_income"] == base_from_controls["annual_operating_income"]
    assert base["fcff"] == base_from_controls["fcff"]
    assert not base["facility_failures"]

    results = {}
    for driver in DRIVER_ORDER:
        name, _, _, _, levels = DRIVERS[driver]
        if driver == "wacc":
            levels = (base_controls["wacc"] - 0.005, base_controls["wacc"], base_controls["wacc"] + 0.005)
        cases = [run_case(driver, level, base) for level in levels]
        for case in cases:
            assert_case_integrity(case, base, base_controls)
        results[driver] = cases

    OUTPUT_FILE.write_text(build_report(base, results), encoding="utf-8")
    failures = [case for cases in results.values() for case in cases if case["status"] == "FAIL"]
    print(f"Wrote {OUTPUT_FILE.name}")
    print(f"Base reproduced: ${base['per_share_valuation']:.6f}/share; 2030 facility ${base['liquidity_facility_balances'][2030]:,.6f}m")
    print(f"Ran {sum(len(cases) for cases in results.values())} scenarios; {len(failures)} facility failures.")
    for case in failures:
        print(f"FAIL {DRIVERS[case['driver']][0]} {input_text(case['driver'], case['input'])}: "
              f"{case['first_failure_year']}E facility ${case['failure_balance']:,.1f}m, excess ${case['excess']:,.1f}m")


if __name__ == "__main__":
    main()
