"""Callable workbench adapter for the unmodified ADM Step 2 integrated model.

This module deliberately imports, rather than duplicates or changes,
``adm_integrated_model.py``.  All statement and valuation calculations remain
in that Step 2 model; this file only translates the seven UI assumptions.
Amounts are USD millions except per-share data and percentages.
"""
from copy import deepcopy

import adm_integrated_model as step2


ADJUSTABLE_KEYS = (
    "revenue_growth", "gross_margin", "sga_pct_gross_profit", "inventory_days",
    "capex", "wacc", "terminal_growth",
)


def base_assumptions():
    """Return the exact, unrounded Step 2 base values used by the workbench."""
    base = deepcopy(step2.INPUTS)
    return {
        "revenue_growth": base["revenue_growth"][0],
        "gross_margin": base["gross_margin"][0],
        "sga_pct_gross_profit": base["sga_pct_gross_profit"][0],
        "inventory_days": base["inventory_days"][0],
        "capex": base["capex"][0],
        "wacc": step2.wacc(base),
        "terminal_growth": base["terminal_growth"],
    }


def _cost_of_equity_for_wacc(inputs, target_wacc):
    """Solve the Step 2 capital-weight equation for the requested WACC."""
    debt_weight, equity_weight = step2.capital_weights(inputs)
    return ((target_wacc - debt_weight * inputs["cost_of_debt"] * (1 - inputs["tax_rate"]))
            / equity_weight)


def _apply_assumptions(assumptions):
    """Apply scalar widget inputs uniformly across the five Step 2 forecast years."""
    adjusted = deepcopy(step2.INPUTS)
    supplied = assumptions or {}
    unknown = set(supplied) - set(ADJUSTABLE_KEYS)
    if unknown:
        raise KeyError(f"Unsupported workbench assumption(s): {sorted(unknown)}")
    values = base_assumptions()
    values.update(supplied)
    if values["terminal_growth"] >= values["wacc"]:
        raise ValueError("Terminal growth must be below WACC.")
    for key in ("revenue_growth", "gross_margin", "sga_pct_gross_profit", "inventory_days", "capex"):
        adjusted[key] = [float(values[key])] * len(step2.YEARS)
    adjusted["cost_of_equity"] = _cost_of_equity_for_wacc(adjusted, float(values["wacc"]))
    adjusted["terminal_growth"] = float(values["terminal_growth"])
    return adjusted


def validation_results(model):
    """Return explicit pass/fail results for every linked-statement control."""
    rules = {
        "Balance sheet balances": ("BS gap", lambda value: abs(value) <= step2.TOL),
        "Cash reconciles to balance sheet": ("CF-to-BS cash difference", lambda value: abs(value) <= step2.TOL),
        "Minimum cash maintained": ("cash minimum difference", lambda value: value >= -step2.TOL),
        "Liquidity facility within limit": ("facility limit difference", lambda value: value >= -step2.TOL),
        "Retained earnings roll-forward": ("RE roll-forward difference", lambda value: abs(value) <= step2.TOL),
        "Debt roll-forward": ("debt roll-forward difference", lambda value: abs(value) <= step2.TOL),
    }
    results = {}
    for label, (check_key, predicate) in rules.items():
        by_year = {year: model["checks"][year][check_key] for year in step2.YEARS}
        results[label] = {"check_key": check_key, "values": by_year,
                          "pass": all(predicate(value) for value in by_year.values())}
    return results


def run_workbench(assumptions=None):
    """Run the actual Step 2 model and return workbench-ready linked outputs.

    ``assumptions`` may contain any key in ``ADJUSTABLE_KEYS``.  Operating
    controls apply the same selected value to each of 2026--2030, matching the
    Step 2 base-case convention.  WACC is translated to Step 2 cost of equity
    using its original capital weights; it is not a separate valuation engine.
    """
    inputs = _apply_assumptions(assumptions)
    model = step2.run_model(inputs)
    valuation = step2.dcf(model)
    validations = validation_results(model)
    facility = {year: model["balance"][year]["Liquidity facility"] for year in step2.YEARS}
    failures = {year: balance for year, balance in facility.items()
                if balance > model["inputs"]["facility_limit"] + step2.TOL}
    return {
        "inputs": model["inputs"], "income_statement": model["income"],
        "balance_sheet": model["balance"], "cash_flow_statement": model["cashflow"],
        "fcff": {year: model["cashflow"][year]["FCFF"] for year in step2.YEARS},
        "annual_operating_income": {year: model["income"][year]["Operating income (EBIT)"] for year in step2.YEARS},
        "dcf": valuation, "per_share_valuation": valuation["per_share"],
        "liquidity_facility_balances": facility, "validation_results": validations,
        "facility_failures": failures, "facility_limit": model["inputs"]["facility_limit"],
        "raw_model": model,
    }


def failure_test_assumptions():
    """Documented operating stress derived from the existing Step 2 Low case."""
    base = base_assumptions()
    base.update({"revenue_growth": 0.0, "gross_margin": 0.0625,
                 "inventory_days": 53.0, "capex": 1600.0,
                 "wacc": step2.wacc({**deepcopy(step2.INPUTS),
                                      "cost_of_equity": step2.INPUTS["cost_of_equity"] + 0.010}),
                 "terminal_growth": 0.020})
    return base
