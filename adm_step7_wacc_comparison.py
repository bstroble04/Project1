"""Read-only WACC/DCF comparison for the Step 7 October 16 price.

Run: ``py adm_step7_wacc_comparison.py``. The script changes the market-
capitalization input only in an in-memory copy of the existing base inputs.
"""
from __future__ import annotations

import json
from copy import deepcopy

import adm_integrated_model as model

SEPTEMBER_24_CLOSE = 81.88
OCTOBER_16_CLOSE = 82.61


def valuation_at_price(price: float) -> dict:
    inputs = deepcopy(model.INPUTS)
    inputs["market_price"] = price
    inputs["market_capitalization"] = price * inputs["share_count"]
    statements = model.run_model(inputs)
    value = model.dcf(statements)
    return {
        "price": price,
        "share_count_millions": inputs["share_count"],
        "market_capitalization_millions": inputs["market_capitalization"],
        "cost_of_equity": inputs["cost_of_equity"],
        "cost_of_debt": inputs["cost_of_debt"],
        "tax_rate": inputs["tax_rate"],
        "wacc": value["wacc"],
        "enterprise_value": value["enterprise_value"],
        "equity_value": value["equity_value"],
        "per_share": value["per_share"],
        "facility_2030": statements["balance"][2030]["Liquidity facility"],
    }


def main() -> None:
    old = valuation_at_price(SEPTEMBER_24_CLOSE)
    new = valuation_at_price(OCTOBER_16_CLOSE)
    result = {
        "assumption": "Only market capitalization is updated: closing price x existing 482m share count. All operating inputs, debt, risk-free rate, beta, ERP, cost of debt, tax rate, and terminal growth remain unchanged.",
        "september_24": old,
        "october_16": new,
        "change": {
            "market_capitalization_millions": new["market_capitalization_millions"] - old["market_capitalization_millions"],
            "wacc_percentage_points": (new["wacc"] - old["wacc"]) * 100,
            "enterprise_value": new["enterprise_value"] - old["enterprise_value"],
            "equity_value": new["equity_value"] - old["equity_value"],
            "per_share": new["per_share"] - old["per_share"],
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
