"""Read-only Step 7 scenario summary using the existing ADM model.

Run from the project root with: ``py adm_step7_scenarios.py``.
It imports existing model logic and does not alter prior inputs, reports, or
calculations. Amounts are USD millions except per-share amounts and rates.
"""
from __future__ import annotations

import json
from copy import deepcopy

import adm_integrated_model as model
import adm_peer_comps as peers

AS_OF_PRICE = 82.61


def scenario_result(name: str) -> dict:
    statements = model.scenario_model(name)
    value = model.dcf(statements)
    facility = statements["balance"][2030]["Liquidity facility"]
    limit = statements["inputs"]["facility_limit"]
    return {
        "name": name,
        "assumptions": {
            "revenue_growth": statements["inputs"]["revenue_growth"][0],
            "gross_margin": statements["inputs"]["gross_margin"][0],
            "inventory_days": statements["inputs"]["inventory_days"][0],
            "capex": statements["inputs"]["capex"][0],
            "wacc": value["wacc"],
            "terminal_growth": statements["inputs"]["terminal_growth"],
        },
        "enterprise_value": value["enterprise_value"],
        "equity_value": value["equity_value"],
        "per_share": value["per_share"],
        "facility_2030": facility,
        "facility_headroom": limit - facility,
        "funding_status": "PASS" if facility <= limit + model.TOL else "FAIL",
    }


def reverse_margin_for_price(price: float) -> dict:
    """Solve the existing DCF for a uniform gross margin at the as-of price."""
    low, high = 0.04, 0.25

    def value_at(margin: float) -> tuple[float, dict]:
        inputs = deepcopy(model.INPUTS)
        inputs["gross_margin"] = [margin] * len(model.YEARS)
        statements = model.run_model(inputs)
        return model.dcf(statements)["per_share"], statements

    if not value_at(low)[0] <= price <= value_at(high)[0]:
        raise ValueError("As-of price is outside the 4%-25% gross-margin search range.")
    for _ in range(100):
        middle = (low + high) / 2
        if value_at(middle)[0] < price:
            low = middle
        else:
            high = middle
    per_share, statements = value_at(middle)
    facility = statements["balance"][2030]["Liquidity facility"]
    return {
        "as_of_price": price,
        "uniform_gross_margin_required": middle,
        "base_gross_margin": model.INPUTS["gross_margin"][0],
        "margin_increase_percentage_points": (middle - model.INPUTS["gross_margin"][0]) * 100,
        "per_share": per_share,
        "facility_2030": facility,
        "funding_status": "PASS" if facility <= statements["inputs"]["facility_limit"] + model.TOL else "FAIL",
    }


def peer_summary() -> dict:
    output = {}
    for ticker in ("BG", "INGR"):
        company = peers.COMPANIES[ticker]
        implied_ev, implied_equity, implied_share = peers.implied_adm_value(company)
        output[ticker] = {
            "pe": peers.pe(company),
            "pe_implied_adm_share": peers.pe(company) * peers.COMPANIES["ADM"]["diluted_eps"],
            "ev_ebitda": peers.ev_ebitda(company),
            "ev_ebitda_implied_adm_share": implied_share,
            "implied_enterprise_value": implied_ev,
            "implied_equity_value": implied_equity,
        }
    return output


def main() -> None:
    results = {
        "as_of_price": AS_OF_PRICE,
        "scenarios": {name: scenario_result(name) for name in ("Low", "Base", "High")},
        "reverse_dcf": reverse_margin_for_price(AS_OF_PRICE),
        "peer_summary": peer_summary(),
    }
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
