"""Read-only October 16, 2026 Step 7 scenario and CapEx comparison.

Run: ``py adm_step7_oct16_scenarios.py``. Existing model files and inputs are
never changed; each case uses an in-memory copy.
"""
from __future__ import annotations

import json
from copy import deepcopy

import adm_integrated_model as model

AS_OF_PRICE = 82.61


def dated_inputs(overrides: dict | None = None) -> dict:
    inputs = deepcopy(model.INPUTS)
    inputs["market_price"] = AS_OF_PRICE
    inputs["market_capitalization"] = AS_OF_PRICE * inputs["share_count"]
    if overrides:
        inputs.update(deepcopy(overrides))
    return inputs


def summarize(inputs: dict) -> dict:
    statements = model.run_model(inputs)
    value = model.dcf(statements)
    facility = statements["balance"][2030]["Liquidity facility"]
    limit = statements["inputs"]["facility_limit"]
    return {
        "wacc": value["wacc"],
        "enterprise_value": value["enterprise_value"],
        "equity_value": value["equity_value"],
        "per_share": value["per_share"],
        "fcff_2030": statements["cashflow"][2030]["FCFF"],
        "facility_2030": facility,
        "facility_headroom": limit - facility,
        "funding_status": "PASS" if facility <= limit + model.TOL else "FAIL",
    }


def reverse_margin() -> dict:
    low, high = 0.04, 0.25

    def price_at(margin: float) -> tuple[float, dict]:
        inputs = dated_inputs({"gross_margin": [margin] * len(model.YEARS)})
        statements = model.run_model(inputs)
        return model.dcf(statements)["per_share"], statements

    for _ in range(100):
        mid = (low + high) / 2
        if price_at(mid)[0] < AS_OF_PRICE:
            low = mid
        else:
            high = mid
    per_share, statements = price_at(mid)
    return {
        "gross_margin": mid,
        "percentage_points_above_base": (mid - model.INPUTS["gross_margin"][0]) * 100,
        "per_share": per_share,
        "facility_2030": statements["balance"][2030]["Liquidity facility"],
    }


def main() -> None:
    scenarios = {}
    for name in ("Low", "Base", "High"):
        scenarios[name] = summarize(dated_inputs(model.SCENARIOS[name]))
    capex = {}
    for amount in (1300.0, 1400.0, 1500.0):
        capex[str(int(amount))] = summarize(dated_inputs({"capex": [amount] * len(model.YEARS)}))
    print(json.dumps({
        "as_of_price": AS_OF_PRICE,
        "market_capitalization": AS_OF_PRICE * model.INPUTS["share_count"],
        "scenarios": scenarios,
        "capex_guidance_cases": capex,
        "reverse_dcf": reverse_margin(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
