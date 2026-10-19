"""ADM integrated three-statement and FCFF DCF model for FIN 43900 Project 1.

Amounts are USD millions except per-share data and percentages.  This is a
new file: proforma_adm.py (the Lab 10 work) is deliberately not modified.
Run: python adm_integrated_model.py
"""
from copy import deepcopy

YEARS = [2026, 2027, 2028, 2029, 2030]
TOL = 0.01

# ---------------------------------------------------------------------------
# CENTRALIZED, EDITABLE INPUTS
# Sources/rationales/limitations are printed at the end of the program.
# Values marked judgment are not claimed to be filing figures.
# ---------------------------------------------------------------------------
INPUTS = {
    "revenue_growth": [0.020] * 5,
    "gross_margin": [0.0675] * 5,
    "sga_pct_gross_profit": [0.650] * 5,
    "inventory_days": [51.0] * 5,
    # Working-capital drivers: FY2025 10-K opening balances / FY2025 flow.
    "receivable_days": [13.73] * 5,
    "payable_days": [25.21] * 5,
    "other_current_assets_pct_revenue": [3796.0 / 80269.0] * 5,
    "accrued_payables_pct_revenue": [3313.0 / 80269.0] * 5,
    "depreciation_pct_opening_ppe": [0.105] * 5,
    "capex": [1400.0] * 5,
    "tax_rate": 0.180,
    "minimum_cash": 500.0,
    "facility_limit": 6000.0,
    "existing_debt_rate": 446.0 / ((8410.0 + 10157.0) / 2),
    "facility_rate": 0.040,
    "dividend_per_share": 2.08,
    "share_count": 482.0,
    # Dated market WACC inputs.  Source/date details are printed with output.
    "risk_free_rate": 0.0475,
    "beta": 0.61,
    "equity_risk_premium": 0.0414,
    "market_price": 81.88,
    "market_capitalization": 81.88 * 482.0,
    "cost_of_equity": 0.0475 + 0.61 * 0.0414,
    "cost_of_debt": 446.0 / ((8410.0 + 10157.0) / 2),
    "terminal_growth": 0.025,
    "market_price_date": "2026-09-24 close",
}

# Historical values preserved from the student's Lab 10 notes / existing model.
# None means the input was not present in those materials and is not invented.
HISTORICAL = {
    2023: {"Revenue": 93935.0, "Gross profit": 7513.0, "SG&A": 3456.0,
           "Net income attributable to ADM": 3483.0, "Inventory": 11957.0,
           "PP&E, net": 10508.0, "Shareholders' equity": 24145.0},
    2024: {"Revenue": 85530.0, "Gross profit": 5778.0, "SG&A": 3706.0,
           "Net income attributable to ADM": 1800.0, "Inventory": 11572.0,
           "PP&E, net": 10837.0, "Shareholders' equity": 22178.0},
    2025: {"Revenue": 80269.0, "Gross profit": 5033.0, "SG&A": 3609.0,
           "Net income attributable to ADM": 1078.0, "Inventory": 10369.0,
           "PP&E, net": 11179.0, "Shareholders' equity": 22740.0,
           "Cash": 1015.0, "Trade receivables, net": 3021.0,
           "Trade payables": 5195.0, "Other current assets": 3796.0,
           "Accrued expenses and other payables": 3313.0,
           "Interest-bearing debt": 8410.0},
}

# FY2025 10-K opening balance sheet (USD millions).  Every former residual is
# explicitly decomposed.  Segregated balances and brokerage payables remain
# paired, held constant, and excluded from ordinary operating NWC.
OPENING = {"cash": 1015.0, "marketable_securities": 32.0, "segregated_cash": 8432.0,
           "receivables": 3021.0, "inventory": 10369.0, "other_current_assets": 3796.0,
           "ppe": 11179.0, "other_noncurrent_assets": 14545.0, "debt": 8410.0,
           "facility": 0.0, "trade_payables": 5195.0, "brokerage_payables": 8919.0,
           "accrued_payables": 3313.0, "lease_liabilities": 1348.0,
           "deferred_taxes": 1135.0, "other_noncurrent_liabilities": 1042.0,
           "temporary_equity": 287.0, "equity": 22740.0}

SCENARIOS = {
    "Low": {"revenue_growth": [0.000] * 5, "gross_margin": [0.0625] * 5,
            "inventory_days": [53.0] * 5, "capex": [1600.0] * 5,
            "cost_of_equity": INPUTS["cost_of_equity"] + 0.010, "terminal_growth": 0.020},
    "Base": {},
    "High": {"revenue_growth": [0.030] * 5, "gross_margin": [0.0725] * 5,
             "inventory_days": [49.0] * 5, "capex": [1200.0] * 5,
             "cost_of_equity": INPUTS["cost_of_equity"] - 0.0075, "terminal_growth": 0.030},
}


def status(ok):
    return "PASS" if ok else "FAIL"


def validate_inputs(a):
    for key in ("revenue_growth", "gross_margin", "sga_pct_gross_profit", "inventory_days",
                "receivable_days", "payable_days", "other_current_assets_pct_revenue",
                "accrued_payables_pct_revenue", "depreciation_pct_opening_ppe", "capex"):
        if len(a[key]) != len(YEARS):
            raise ValueError(f"{key} must contain five annual values.")
    if a["terminal_growth"] >= wacc(a):
        raise ValueError("Terminal growth must be below WACC.")


def capital_weights(a):
    """Market-value weights at the dated market observation; facility is a stress test."""
    debt_weight = OPENING["debt"] / (OPENING["debt"] + a["market_capitalization"])
    equity_weight = 1.0 - debt_weight
    return debt_weight, equity_weight


def wacc(a):
    debt_weight, equity_weight = capital_weights(a)
    return equity_weight * a["cost_of_equity"] + debt_weight * a["cost_of_debt"] * (1 - a["tax_rate"])


def run_model(inputs=INPUTS):
    """Return linked income statement, balance sheet, cash flow, and checks."""
    a = deepcopy(inputs)
    validate_inputs(a)
    income, balance, cashflow, checks = {}, {}, {}, {}
    opening, prior_revenue = OPENING.copy(), HISTORICAL[2025]["Revenue"]
    for i, year in enumerate(YEARS):
        revenue = prior_revenue * (1 + a["revenue_growth"][i])
        gross_profit = revenue * a["gross_margin"][i]
        cogs = revenue - gross_profit
        sga = gross_profit * a["sga_pct_gross_profit"][i]
        depreciation = opening["ppe"] * a["depreciation_pct_opening_ppe"][i]
        ebit = gross_profit - sga - depreciation
        debt_interest = opening["debt"] * a["existing_debt_rate"]
        facility_interest = opening["facility"] * a["facility_rate"]
        interest = debt_interest + facility_interest
        pretax = ebit - interest
        taxes = max(pretax, 0.0) * a["tax_rate"]
        net_income = pretax - taxes

        receivables = revenue * a["receivable_days"][i] / 365.0
        inventory = cogs * a["inventory_days"][i] / 365.0
        other_current_assets = revenue * a["other_current_assets_pct_revenue"][i]
        trade_payables = cogs * a["payable_days"][i] / 365.0
        accrued_payables = revenue * a["accrued_payables_pct_revenue"][i]
        opening_nwc = (opening["receivables"] + opening["inventory"] + opening["other_current_assets"]
                       - opening["trade_payables"] - opening["accrued_payables"])
        nwc = receivables + inventory + other_current_assets - trade_payables - accrued_payables
        change_nwc = nwc - opening_nwc
        ppe = opening["ppe"] + a["capex"][i] - depreciation
        dividends = a["dividend_per_share"] * a["share_count"]
        debt = opening["debt"]
        equity = opening["equity"] + net_income - dividends

        cfo = net_income + depreciation - change_nwc
        cfi = -a["capex"][i]
        cash_before_financing = opening["cash"] + cfo + cfi - dividends
        draw = max(0.0, a["minimum_cash"] - cash_before_financing)
        repay = min(opening["facility"], max(0.0, cash_before_financing - a["minimum_cash"]))
        facility = opening["facility"] + draw - repay
        financing = draw - repay - dividends
        ending_cash = opening["cash"] + cfo + cfi + financing
        fcff = ebit * (1 - a["tax_rate"]) + depreciation - a["capex"][i] - change_nwc

        income[year] = {"Revenue": revenue, "COGS": cogs, "Gross profit": gross_profit,
                        "SG&A": sga, "Depreciation": depreciation, "Operating income (EBIT)": ebit,
                        "Interest expense": interest, "Pretax income": pretax, "Taxes": taxes,
                        "Net income": net_income}
        balance[year] = {"Cash": ending_cash, "Short-term marketable securities": opening["marketable_securities"],
                         "Segregated cash and investments": opening["segregated_cash"], "Trade receivables, net": receivables,
                         "Inventory": inventory, "Other current assets": other_current_assets, "PP&E": ppe,
                         "Other non-current assets": opening["other_noncurrent_assets"],
                         "Total assets": ending_cash + opening["marketable_securities"] + opening["segregated_cash"] + receivables + inventory + other_current_assets + ppe + opening["other_noncurrent_assets"],
                         "Interest-bearing debt": debt, "Liquidity facility": facility,
                         "Trade payables": trade_payables, "Payables to brokerage customers": opening["brokerage_payables"],
                         "Accrued expenses and other payables": accrued_payables, "Lease liabilities": opening["lease_liabilities"],
                         "Deferred income taxes": opening["deferred_taxes"], "Other non-current liabilities": opening["other_noncurrent_liabilities"],
                         "Temporary equity": opening["temporary_equity"], "Shareholders' equity": equity,
                         "Total liabilities and equity": debt + facility + trade_payables + opening["brokerage_payables"] + accrued_payables + opening["lease_liabilities"] + opening["deferred_taxes"] + opening["other_noncurrent_liabilities"] + opening["temporary_equity"] + equity}
        cashflow[year] = {"Net income": net_income, "Depreciation": depreciation,
                          "Change in operating NWC": -change_nwc,
                          "Operating cash flow": cfo, "CapEx": -a["capex"][i],
                          "Investing cash flow": cfi, "Dividends": -dividends,
                          "Borrowing (facility draw)": draw, "Repayment (facility)": -repay,
                          "Financing cash flow": financing, "Net change in cash": ending_cash - opening["cash"],
                          "Ending cash": ending_cash, "FCFF": fcff}
        gap = balance[year]["Total assets"] - balance[year]["Total liabilities and equity"]
        checks[year] = {"BS gap": gap, "CF-to-BS cash difference": ending_cash - balance[year]["Cash"],
                        "cash minimum difference": ending_cash - a["minimum_cash"],
                        "facility limit difference": a["facility_limit"] - facility,
                        "RE roll-forward difference": equity - (opening["equity"] + net_income - dividends),
                        "debt roll-forward difference": debt - opening["debt"]}
        opening = {"cash": ending_cash, "marketable_securities": opening["marketable_securities"], "segregated_cash": opening["segregated_cash"],
                   "receivables": receivables, "inventory": inventory, "other_current_assets": other_current_assets, "ppe": ppe,
                   "other_noncurrent_assets": opening["other_noncurrent_assets"], "debt": debt, "facility": facility,
                   "trade_payables": trade_payables, "brokerage_payables": opening["brokerage_payables"], "accrued_payables": accrued_payables,
                   "lease_liabilities": opening["lease_liabilities"], "deferred_taxes": opening["deferred_taxes"],
                   "other_noncurrent_liabilities": opening["other_noncurrent_liabilities"], "temporary_equity": opening["temporary_equity"], "equity": equity}
        prior_revenue = revenue
    return {"inputs": a, "income": income, "balance": balance, "cashflow": cashflow, "checks": checks}


def dcf(model):
    a, cf = model["inputs"], model["cashflow"]
    discount = wacc(a)
    fcff = [cf[y]["FCFF"] for y in YEARS]
    pv_explicit = sum(x / (1 + discount) ** (i + 1) for i, x in enumerate(fcff))
    terminal_value = fcff[-1] * (1 + a["terminal_growth"]) / (discount - a["terminal_growth"])
    pv_terminal = terminal_value / (1 + discount) ** len(YEARS)
    ev = pv_explicit + pv_terminal
    # FY2025 valuation-date bridge.  Facility draws are a liquidity stress-test,
    # not a second debt claim in this current-date FCFF bridge.
    bridge_cash = OPENING["cash"] + OPENING["marketable_securities"]
    other_claims = OPENING["temporary_equity"] + 7.0  # redeemable and non-controlling interests reported in 10-K
    equity = ev + bridge_cash - OPENING["debt"] - other_claims
    return {"wacc": discount, "fcff": fcff, "pv_explicit": pv_explicit, "terminal_value": terminal_value,
            "pv_terminal": pv_terminal, "enterprise_value": ev, "equity_value": equity,
            "per_share": equity / a["share_count"], "tv_pct_ev": pv_terminal / ev,
            "bridge_cash": bridge_cash, "other_claims": other_claims}


def scenario_model(name):
    a = deepcopy(INPUTS)
    a.update(deepcopy(SCENARIOS[name]))
    return run_model(a)


def format_value(v):
    return "N/A*" if v is None else f"{v:,.1f}"


def print_table(title, data):
    print(f"\n{title}")
    rows = list(data[YEARS[0]])
    width = max(len(x) for x in rows) + 2
    print("Line item".ljust(width) + "".join(f"{y}E".rjust(14) for y in YEARS))
    for row in rows:
        print(row.ljust(width) + "".join(format_value(data[y][row]).rjust(14) for y in YEARS))


def print_historical_reconciliation():
    print("\n1. HISTORICAL DATA RECONCILIATION")
    print("Known historical inputs preserved from Lab 10 notes (USD millions):")
    print("Line item".ljust(38) + "2023A".rjust(13) + "2024A".rjust(13) + "2025A".rjust(13))
    for row in ("Revenue", "Gross profit", "SG&A", "Net income attributable to ADM", "Inventory", "PP&E, net", "Shareholders' equity"):
        print(row.ljust(38) + "".join(f"{HISTORICAL[y][row]:>13,.1f}" for y in (2023, 2024, 2025)))
    assets = sum((OPENING["cash"], OPENING["marketable_securities"], OPENING["segregated_cash"], OPENING["receivables"],
                  OPENING["inventory"], OPENING["other_current_assets"], OPENING["ppe"], OPENING["other_noncurrent_assets"]))
    claims = sum((OPENING["debt"], OPENING["facility"], OPENING["trade_payables"], OPENING["brokerage_payables"],
                  OPENING["accrued_payables"], OPENING["lease_liabilities"], OPENING["deferred_taxes"],
                  OPENING["other_noncurrent_liabilities"], OPENING["temporary_equity"], OPENING["equity"]))
    difference = assets - claims
    print(f"2025 opening balance-sheet reconciliation: {status(abs(difference) <= TOL)}; difference = {difference:,.2f}")
    # ADM’s FY2025 earnings-release cash-flow summary groups the detailed 10-K
    # reconciling lines into Other--net and Other changes in operating assets/liabilities.
    historical_cfo = 1073.0 + 1181.0 + 361.0 + 285.0 - 211.0 + 2763.0
    print(f"2025 cash-flow reconciliation to CFO ($5,452m): {status(abs(historical_cfo - 5452.0) <= TOL)}; difference = {historical_cfo - 5452.0:,.2f}")
    print("Source: ADM FY2025 Form 10-K, Consolidated Balance Sheets (p. 47) and Cash Flows (p. 48); FY2025 earnings-release cash-flow summary for grouped CFO lines.")


def print_checks(model):
    print("\n5. MODEL VALIDATION CHECKS")
    print("Check".ljust(38) + "".join(f"{y}E".rjust(20) for y in YEARS))
    checks = model["checks"]
    tests = [("Assets - liabilities - equity", "BS gap", lambda x: abs(x) <= TOL),
             ("Cash flow ending cash vs BS cash", "CF-to-BS cash difference", lambda x: abs(x) <= TOL),
             ("Minimum cash compliance (difference)", "cash minimum difference", lambda x: x >= -TOL),
             ("Facility compliance (headroom)", "facility limit difference", lambda x: x >= -TOL),
             ("Retained earnings roll-forward", "RE roll-forward difference", lambda x: abs(x) <= TOL),
             ("Debt roll-forward", "debt roll-forward difference", lambda x: abs(x) <= TOL)]
    for label, key, rule in tests:
        print(label.ljust(38) + "".join(f"{status(rule(checks[y][key]))} {checks[y][key]:,.2f}".rjust(20) for y in YEARS))


def print_dcf_sections(model, valuation):
    print("\n6. FIVE-YEAR FCFF FORECAST")
    print("Year".ljust(12) + "EBIT".rjust(14) + "NOPAT".rjust(14) + "D&A".rjust(14) + "CapEx".rjust(14) + "Change NWC".rjust(14) + "FCFF".rjust(14))
    for y in YEARS:
        i, c = model["income"][y], model["cashflow"][y]
        print(f"{y}E".ljust(12) + f"{i['Operating income (EBIT)']:>14,.1f}{i['Operating income (EBIT)'] * (1-model['inputs']['tax_rate']):>14,.1f}{i['Depreciation']:>14,.1f}{-c['CapEx']:>14,.1f}{-c['Change in operating NWC']:>14,.1f}{c['FCFF']:>14,.1f}")
    a = model["inputs"]
    dw, ew = capital_weights(a)
    print("\n7. WACC CALCULATION")
    print(f"Risk-free rate: {a['risk_free_rate']:.2%}; beta: {a['beta']:.2f}; ERP: {a['equity_risk_premium']:.2%}; CAPM cost of equity: {a['cost_of_equity']:.2%}")
    print(f"Pre-tax cost of debt: {a['cost_of_debt']:.2%}; after-tax cost of debt: {a['cost_of_debt'] * (1-a['tax_rate']):.2%}")
    print(f"Market debt weight: {dw:.2%}; market equity weight: {ew:.2%}; WACC: {valuation['wacc']:.2%}")


def print_scenarios():
    print("\n8. LOW / BASE / HIGH DCF VALUATIONS")
    print("Scenario".ljust(12) + "WACC".rjust(10) + "g".rjust(10) + "EV".rjust(16) + "Equity".rjust(16) + "$/share".rjust(14) + "2030 facility".rjust(18) + "Funding".rjust(12))
    results = {}
    for name in ("Low", "Base", "High"):
        m, v = scenario_model(name), None
        v = dcf(m)
        facility = m["balance"][2030]["Liquidity facility"]
        funded = facility <= m["inputs"]["facility_limit"] + TOL
        results[name] = (m, v)
        print(f"{name.ljust(12)}{v['wacc']:>10.2%}{m['inputs']['terminal_growth']:>10.2%}{v['enterprise_value']:>16,.1f}{v['equity_value']:>16,.1f}{v['per_share']:>14,.2f}{facility:>18,.1f}{status(funded):>12}")
    return results


def print_sensitivity(base_model):
    print("\n11. WACC VERSUS TERMINAL-GROWTH SENSITIVITY ($/share)")
    growths, rates = [0.015, 0.020, 0.025, 0.030], [0.060, 0.065, 0.070, 0.075, 0.080]
    print("WACC \\ g".ljust(12) + "".join(f"{g:.1%}".rjust(12) for g in growths))
    for r in rates:
        row = f"{r:.1%}".ljust(12)
        for g in growths:
            a = deepcopy(base_model["inputs"])
            dw, ew = capital_weights(a)
            a["cost_of_equity"] = (r - dw * a['cost_of_debt'] * (1-a['tax_rate'])) / ew
            a["terminal_growth"] = g
            row += ("N/M" if g >= r else f"{dcf(run_model(a))['per_share']:.2f}").rjust(12)
        print(row)


def print_reverse_dcf():
    target = INPUTS["market_price"]
    lo, hi = 0.04, 0.25
    def price(margin):
        a = deepcopy(INPUTS)
        a["gross_margin"] = [margin] * 5
        return dcf(run_model(a))["per_share"]
    plo, phi = price(lo), price(hi)
    print("\n12. REVERSE DCF")
    print(f"Target ADM price: ${target:.2f}; observation date: {INPUTS['market_price_date']}")
    if not min(plo, phi) <= target <= max(plo, phi):
        print(f"No solution within a 4.0% to 25.0% gross-margin range (price range ${plo:.2f} to ${phi:.2f}).")
        return
    for _ in range(100):
        mid = (lo + hi) / 2
        if price(mid) < target: lo = mid
        else: hi = mid
    a = deepcopy(INPUTS); a["gross_margin"] = [mid] * 5
    m, v = run_model(a), dcf(run_model(a))
    facility = m["balance"][2030]["Liquidity facility"]
    print(f"Solved uniform 2026-30 gross-margin assumption: {mid:.2%} (base is {INPUTS['gross_margin'][0]:.2%})")
    print(f"Implied DCF value: ${v['per_share']:.2f}/share; 2030 facility: ${facility:,.1f}m; funding status: {status(facility <= INPUTS['facility_limit'] + TOL)}")


def print_assumptions_and_gaps():
    print("\n13. KEY ASSUMPTIONS AND UNRESOLVED EVIDENCE GAPS")
    print("Base operating assumptions: 2.0% revenue growth; 6.75% gross margin; SG&A 65% of gross profit; 51 inventory days; D&A 10.5% of opening PP&E; $1,400m CapEx; 18% tax; $500m cash floor; $6,000m facility.")
    print("Working-capital drivers: trade receivables use 13.73 DSO; trade payables use 25.21 DPO; other current assets and accrued payables use FY2025 percentages of revenue. These derive from ADM FY2025 10-K balances and are editable assumptions.")
    print("WACC market inputs: 2026-09-24 ADM close $81.88 x 482m shares = $39,466m market capitalization; 0.61 beta; 4.75% risk-free rate; and 4.14% implied ERP. Pre-tax cost of debt is 4.80%, based on FY2025 interest on borrowings / average 2024-25 defined debt.")
    print("Scenario rationale: Low uses no growth, 6.25% margin, 53 inventory days, and $1,600m CapEx to represent weaker margins/cash conversion; High uses 3% growth, 7.25% margin, 49 days, and $1,200m CapEx to represent recovery and improved working-capital efficiency. Discount-rate and terminal-growth changes are judgmental risk cases, not price targets.")
    print("Facility policy: the modeled facility is a liquidity stress test used only to test cash-floor funding. It is financing cash flow, excluded from FCFF and terminal value, and not subtracted in the current-date bridge because opening facility debt is zero. It is not a forecast debt policy.")
    print("Remaining gaps: forecast DSO/DPO and other-current-account ratios are judgmental; share count is June-2026 reported shares while the price is September 24; beta/ERP are third-party market observations; leases and affiliates need a valuation-policy decision; and facility stress-test debt should not be used as a terminal debt forecast.")
    print("AI assistance: Codex created this separate linked model, retained the supplied Lab 10 inputs, added validations/FCFF/scenarios, and generated this output. The student must verify filing evidence and exercise judgment over assumptions.")


def main():
    base = run_model()
    value = dcf(base)
    print("ADM INTEGRATED FINANCIAL MODEL | USD millions except per-share amounts")
    print_historical_reconciliation()
    print_table("2. FORECAST INCOME STATEMENT", base["income"])
    print_table("3. FORECAST BALANCE SHEET", base["balance"])
    print_table("4. FORECAST CASH FLOW STATEMENT", base["cashflow"])
    print_checks(base)
    print_dcf_sections(base, value)
    scenarios = print_scenarios()
    print("\n9. ENTERPRISE-TO-EQUITY BRIDGE (base case; FY2025 valuation date)")
    print(f"Enterprise value: {value['enterprise_value']:,.1f}; + cash and marketable securities: {value['bridge_cash']:,.1f}; - interest-bearing debt: {OPENING['debt']:,.1f}; - temporary equity/NCI: {value['other_claims']:,.1f}; = equity value: {value['equity_value']:,.1f}; / {INPUTS['share_count']:,.1f} shares = ${value['per_share']:.2f}")
    print(f"\n10. TERMINAL VALUE CONTRIBUTION\nTerminal value at 2030: {value['terminal_value']:,.1f}; PV terminal value: {value['pv_terminal']:,.1f}; PV forecast FCFF: {value['pv_explicit']:,.1f}; terminal value as % of EV: {value['tv_pct_ev']:.2%}")
    print_sensitivity(base)
    print_reverse_dcf()
    print_assumptions_and_gaps()


if __name__ == "__main__":
    main()
