"""Read-only Step 6 validation runner for the existing ADM project.

Run ``py adm_step6_validation.py`` for the permitted validation record.
The 6.3 test is deliberately not part of the default run.  After the student
has independently locked a prediction, run the explicitly gated command in
adm_step6_locked_prediction.md.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

import adm_integrated_model as step2
from adm_valuation_model import failure_test_assumptions, run_workbench

TOLERANCE_MILLIONS = step2.TOL


def status(value: bool) -> str:
    return "PASS" if value else "FAIL"


def result_summary(result: dict) -> dict:
    """Return actual linked-model results needed for a post-lock audit trail."""
    model = result["raw_model"]
    facility = result["liquidity_facility_balances"]
    failures = result["facility_failures"]
    first_year = min(failures) if failures else None
    return {
        "input_capex_millions": result["inputs"]["capex"][0],
        "annual_ebit_millions": result["annual_operating_income"],
        "annual_fcff_millions": result["fcff"],
        "per_share_valuation": result["per_share_valuation"],
        "facility_balances_millions": facility,
        "facility_limit_millions": result["facility_limit"],
        "financing_validation": status(not failures),
        "first_facility_failure_year": first_year,
        "first_failure_balance_millions": failures.get(first_year) if first_year else None,
        "amount_over_limit_millions": (
            failures[first_year] - result["facility_limit"] if first_year else 0.0
        ),
        "accounting_validations": result["validation_results"],
        "recommendation_implication": (
            "Do not treat the DCF result as investable: the facility limit fails."
            if failures else
            "Funding validation passes; interpret the valuation with the documented model limitations."
        ),
        "ending_cash_millions": {year: model["balance"][year]["Cash"] for year in step2.YEARS},
    }


def permitted_validation() -> dict:
    """Run only the base model, existing Step-5 endpoints, and stress scenario."""
    base = run_workbench()
    stress = run_workbench(failure_test_assumptions())
    wacc_low = run_workbench({"wacc": base["dcf"]["wacc"] - 0.005})
    wacc_high = run_workbench({"wacc": base["dcf"]["wacc"] + 0.005})
    growth_low = run_workbench({"terminal_growth": 0.020})
    growth_high = run_workbench({"terminal_growth": 0.030})
    sga_70 = run_workbench({"sga_pct_gross_profit": 0.70})
    capex_1600 = run_workbench({"capex": 1600.0})
    return {
        "tolerance_millions": TOLERANCE_MILLIONS,
        "base": result_summary(base),
        "stress": result_summary(stress),
        "sga_70_percent": result_summary(sga_70),
        "capex_1600_millions": result_summary(capex_1600),
        "wacc_monotonic": {
            "lower_wacc_per_share": wacc_low["per_share_valuation"],
            "base_wacc_per_share": base["per_share_valuation"],
            "higher_wacc_per_share": wacc_high["per_share_valuation"],
            "result": status(wacc_high["per_share_valuation"] < base["per_share_valuation"] < wacc_low["per_share_valuation"]),
        },
        "terminal_growth_monotonic": {
            "lower_growth_per_share": growth_low["per_share_valuation"],
            "base_growth_per_share": base["per_share_valuation"],
            "higher_growth_per_share": growth_high["per_share_valuation"],
            "result": status(growth_low["per_share_valuation"] < base["per_share_valuation"] < growth_high["per_share_valuation"]),
        },
    }


def post_lock_capex(capex: float) -> dict:
    """Execute a single CapEx input only after an independently locked prediction."""
    if capex <= 0:
        raise ValueError("CapEx must be a positive USD-millions amount.")
    return result_summary(run_workbench({"capex": capex}))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-lock-capex", type=float, metavar="USD_MILLIONS")
    parser.add_argument("--confirm-independent-lock", action="store_true")
    parser.add_argument("--output", type=Path, help="Optional JSON result path for an authorized post-lock test.")
    args = parser.parse_args()
    if args.post_lock_capex is None:
        if args.confirm_independent_lock or args.output:
            parser.error("--confirm-independent-lock and --output require --post-lock-capex.")
        payload = permitted_validation()
    else:
        if not args.confirm_independent_lock:
            parser.error("Refusing to run 6.3: independently lock the prediction first, then add --confirm-independent-lock.")
        payload = post_lock_capex(args.post_lock_capex)
        if args.output:
            args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
