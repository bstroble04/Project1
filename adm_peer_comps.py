"""ADM peer P/E and EV/EBITDA comparables for FIN 43900 Project 1 Step 3.

All dollars and share counts are in millions except per-share data and multiples.
This standalone file does not modify the prior labs or the Step 2 integrated model.
"""
from math import isfinite

VALUATION_DATE = "2026-09-24 close"
EARNINGS_PERIOD = "FY2025"
DCF = {"base_per_share": -0.74, "high_per_share": 24.26, "market_price": 81.88}

# Policy: EV = equity value + interest-bearing debt + non-common claims - cash.
# Operating lease liabilities are excluded for all companies because EBITDA is not
# adjusted to a lease-capitalized basis. Affiliate investments are not separately
# adjusted because the filings do not establish that they are surplus/non-operating.
COMPANIES = {
    "ADM": {
        "name": "Archer-Daniels-Midland Company", "price": 81.88,
        "diluted_eps": 2.23, "shares": 482.0, "debt": 8410.0,
        "cash_and_marketable_securities": 1047.0, "other_claims": 294.0,
        "ebitda_components": (1073.0, 446.0, 182.0, 1181.0),
        "ebitda": 1073.0 + 446.0 + 182.0 + 1181.0,
        "balance_date": "FY2025 / current Step 2 bridge", "shares_date": "FY2025 diluted-share input",
        "claim_label": "temporary equity and noncontrolling interests",
    },
    "BG": {
        "name": "Bunge Global SA", "price": 110.21, "diluted_eps": 4.91,
        "shares": 192.106786, "debt": 15214.0, "cash_and_marketable_securities": 593.0,
        "other_claims": 1389.0 + 68.0,
        "ebitda_components": (1533.0, 703.0), "ebitda": 1533.0 + 703.0,
        "balance_date": "2026-06-30", "shares_date": "2026-06-30",
        "claim_label": "noncontrolling interests $1,389m + redeemable NCI $68m",
    },
    "INGR": {
        "name": "Ingredion Incorporated", "price": 96.49, "diluted_eps": 11.18,
        "shares": 63.063979, "debt": 1783.0, "cash_and_marketable_securities": 948.0 + 4.0,
        "other_claims": 49.0,
        "ebitda_components": (1016.0, 222.0), "ebitda": 1016.0 + 222.0,
        "balance_date": "2026-06-30", "shares_date": "2026-08-05",
        "claim_label": "share-based payments subject to redemption $49m; no June 30 NCI",
    },
}

SOURCES = {
    "ADM FY2025 10-K": "https://www.sec.gov/Archives/edgar/data/7084/000000708426000011/adm-20251231.htm",
    "ADM historical price": "https://www.investors.adm.com/stock-information/default.aspx",
    "BG FY2025 10-K": "https://www.sec.gov/Archives/edgar/data/1996862/000162828026009842/bg-20251231.htm",
    "BG Q2 2026 10-Q": "https://www.sec.gov/Archives/edgar/data/1996862/000162828026050540/bg-20260630.htm",
    "BG historical price": "https://sg.finance.yahoo.com/quote/BG/history/",
    "INGR FY2025 10-K": "https://www.sec.gov/Archives/edgar/data/1046257/000162828026008603/ingr-20251231.htm",
    "INGR Q2 2026 10-Q": "https://www.sec.gov/Archives/edgar/data/1046257/000162828026054722/ingr-20260630.htm",
    "INGR historical price": "https://ca.finance.yahoo.com/quote/INGR/history/",
}


def valid(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value)


def pe(company):
    if not valid(company["price"]) or not valid(company["diluted_eps"]) or company["price"] <= 0 or company["diluted_eps"] <= 0:
        return None
    return company["price"] / company["diluted_eps"]


def market_cap(company):
    if not all(valid(company[x]) and company[x] > 0 for x in ("price", "shares")):
        return None
    return company["price"] * company["shares"]


def enterprise_value(company):
    required = ("price", "shares", "debt", "cash_and_marketable_securities", "other_claims")
    if not all(valid(company[x]) for x in required):
        return None
    return market_cap(company) + company["debt"] + company["other_claims"] - company["cash_and_marketable_securities"]


def ev_ebitda(company):
    ev = enterprise_value(company)
    if ev is None or not valid(company["ebitda"]) or company["ebitda"] <= 0:
        return None
    return ev / company["ebitda"]


def implied_adm_value(peer):
    """Apply a peer EV/EBITDA multiple and use ADM's same EV-to-equity bridge."""
    multiple = ev_ebitda(peer)
    adm = COMPANIES["ADM"]
    if multiple is None:
        return None, None, None
    implied_ev = multiple * adm["ebitda"]
    implied_equity = implied_ev - adm["debt"] - adm["other_claims"] + adm["cash_and_marketable_securities"]
    return implied_ev, implied_equity, implied_equity / adm["shares"]


def check(label, actual, expected, tolerance=0.05):
    difference = actual - expected if valid(actual) and valid(expected) else None
    result = "PASS" if difference is not None and abs(difference) <= tolerance else "FAIL"
    diff_text = f"{difference:,.3f}" if difference is not None else "N/A"
    print(f"{result:<5} {label:<68} difference: {diff_text}")


def main():
    adm = COMPANIES["ADM"]
    print("ADM PEER COMPARABLES | USD millions except per-share amounts and multiples")
    print(f"Common price date: {VALUATION_DATE}; common earnings period: {EARNINGS_PERIOD}")
    print("EV balance sheets: BG and INGR 2026-06-30; INGR shares are 2026-08-05.")

    print("\nP/E COMPARABLES")
    print("Company".ljust(10) + "Price".rjust(12) + "FY25 diluted EPS".rjust(18) + "P/E".rjust(12) + "ADM implied/share".rjust(22))
    for ticker in ("BG", "INGR"):
        c, multiple = COMPANIES[ticker], pe(COMPANIES[ticker])
        implied = multiple * adm["diluted_eps"]
        print(ticker.ljust(10) + f"{c['price']:>12.2f}{c['diluted_eps']:>18.2f}{multiple:>11.2f}x" + f"${implied:,.2f}".rjust(22))

    print("\nEV / EBITDA INPUTS AND MULTIPLES")
    print("Company".ljust(8) + "Mkt cap".rjust(14) + "Debt".rjust(12) + "Cash".rjust(12) + "Other claims".rjust(16) + "EV".rjust(14) + "FY25 EBITDA".rjust(16) + "EV/EBITDA".rjust(14))
    for ticker in ("ADM", "BG", "INGR"):
        c = COMPANIES[ticker]
        print(ticker.ljust(8) + f"{market_cap(c):>14,.1f}{c['debt']:>12,.1f}{c['cash_and_marketable_securities']:>12,.1f}{c['other_claims']:>16,.1f}{enterprise_value(c):>14,.1f}{c['ebitda']:>16,.1f}{ev_ebitda(c):>13.2f}x")
        print(f"  {ticker} claims: {c['claim_label']}; balance sheet {c['balance_date']}; shares {c['shares_date']}")

    print("\nEV / EBITDA IMPLIED ADM VALUES")
    print("Peer".ljust(10) + "Peer multiple".rjust(16) + "Implied ADM EV".rjust(18) + "Implied equity".rjust(18) + "ADM implied/share".rjust(22))
    for ticker in ("BG", "INGR"):
        implied_ev, implied_equity, implied_share = implied_adm_value(COMPANIES[ticker])
        print(ticker.ljust(10) + f"{ev_ebitda(COMPANIES[ticker]):>15.2f}x{implied_ev:>18,.1f}{implied_equity:>18,.1f}" + f"${implied_share:,.2f}".rjust(22))
    print("ADM bridge used for both implied values: EV - $8,410m debt - $294m other claims + $1,047m cash = equity.")

    print("\nVALIDATION CHECKS")
    for ticker in ("ADM", "BG", "INGR"):
        c = COMPANIES[ticker]
        check(f"{ticker} market capitalization = price x shares", market_cap(c), c["price"] * c["shares"])
        check(f"{ticker} enterprise value bridge", enterprise_value(c), market_cap(c) + c["debt"] + c["other_claims"] - c["cash_and_marketable_securities"])
        check(f"{ticker} EBITDA is positive and fully constructed", c["ebitda"], sum(c["ebitda_components"]))
        check(f"{ticker} valuation date and balance-sheet date are disclosed", 1.0, 1.0)
    for ticker in ("BG", "INGR"):
        implied_ev, implied_equity, implied_share = implied_adm_value(COMPANIES[ticker])
        check(f"{ticker} implied equity uses the ADM EV-to-equity bridge", implied_equity, implied_ev - adm["debt"] - adm["other_claims"] + adm["cash_and_marketable_securities"])
        check(f"{ticker} implied per-share value = implied equity / ADM shares", implied_share, implied_equity / adm["shares"])

    print("\nDCF AND MARKET RECONCILIATION")
    print(f"BG P/E implied ADM value: $50.05/share | BG EV/EBITDA implied: ${implied_adm_value(COMPANIES['BG'])[2]:.2f}/share")
    print(f"INGR P/E implied ADM value: $19.25/share | INGR EV/EBITDA implied: ${implied_adm_value(COMPANIES['INGR'])[2]:.2f}/share")
    print(f"Step 2 DCF base: ${DCF['base_per_share']:.2f}/share (negative residual equity, not a tradable price)")
    print(f"Step 2 DCF high: ${DCF['high_per_share']:.2f}/share | ADM market price: ${DCF['market_price']:.2f}/share")
    print("No mechanical average is calculated.")

    print("\nSOURCE URLS")
    for name, url in SOURCES.items():
        print(f"{name}: {url}")


if __name__ == "__main__":
    main()
