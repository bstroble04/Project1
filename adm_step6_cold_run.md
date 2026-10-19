# ADM Step 6 — Cold-Run Record

Status: **PASS**. A genuine isolated Windows cold run completed on October 17, 2026, beginning at 3:03:15 PM EDT (UTC-04:00).

Use a fresh Windows PowerShell session in a copy of the project directory. Do not use the existing `__pycache__` folder as evidence of a cold run.

```powershell
py -3.13 -m venv .venv-step6
.\.venv-step6\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
python -m pip list --format=freeze
python adm_integrated_model.py
python adm_peer_comps.py
python adm_step6_validation.py
```

If your Windows Python launcher does not expose 3.13, replace `py -3.13` with the exact installed Python executable and record that version. No third-party package installation is expected; if an import error occurs, record the full error before any repair. Do not run the `--post-lock-capex` command until the prediction has been independently locked and you have authorized the test.

Fill this with observed facts after completion:

| Field | Record |
|---|---|
| Date/time and time zone | October 17, 2026, 3:03:15 PM EDT (UTC-04:00) |
| Fresh directory / environment path | `.venv-step6-cold`; `include-system-site-packages = false` |
| Python version | Python 3.13.15 |
| Package versions (`pip freeze`) | `pip==26.2.1`; no project third-party dependencies |
| Commands run | `Proforma.py`, `adm_integrated_model.py`, `adm_peer_comps.py`, `adm_step5_sensitivity.py`, and `adm_step6_validation.py`, all with the fresh interpreter |
| Outputs created | Temporary console logs in `C:\Users\brian\AppData\Local\Temp\adm-step6-cold-run-20261017` |
| Errors and exact repair commands | No execution errors or code repairs. Added previously missing `README.md` and `requirements.txt`. |
| Final result | PASS; all five scripts exited successfully and reproduced documented base and expected-failure results. |

## Actual cold-run evidence

The project initially had no README or dependency manifest. Import inspection of required scripts found only Python standard-library modules (`argparse`, `copy`, `json`, `math`, and `pathlib`) and local project modules. `README.md` and `requirements.txt` now document that no third-party packages are required; no model calculation was changed.

The isolated environment was created and populated with:

```powershell
py -3.13 -m venv .venv-step6-cold
.\.venv-step6-cold\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-step6-cold\Scripts\python.exe -m pip list --format=freeze
```

`requirements.txt` contains comments only, so installation succeeded without packages. The fresh environment reports Python 3.13.15, `pip==26.2.1`, and `include-system-site-packages = false`.

To preserve the original Step 5 report, the project was copied to `C:\Users\brian\AppData\Local\Temp\adm-step6-cold-run-20261017`; all five scripts ran from that copy with `C:\Users\brian\ai-finance-class\.venv-step6-cold\Scripts\python.exe`. The copied `Proforma.py`, `adm_integrated_model.py`, `adm_peer_comps.py`, `adm_step5_sensitivity.py`, and `adm_step6_validation.py` SHA-256 hashes matched their originals before and after execution.

| Script | Actual observed result | Status |
|---|---|---|
| `Proforma.py` | ABG value/share $291.75 (unrounded $291.751666); statement checks pass | PASS |
| `adm_integrated_model.py` | Base DCF displayed $(0.74)/share; all base accounting/facility checks pass | PASS |
| `adm_peer_comps.py` | All displayed validation checks pass | PASS |
| `adm_step5_sensitivity.py` | Base $(0.740876)/share; 70% SG&A fails in 2030 at $6,418.6m and $1,600m CapEx fails at $6,176.8m | PASS: expected failures reproduced |
| `adm_step6_validation.py` | Base financing PASS; compound stress and the two documented endpoint cases fail financing in 2030; WACC and terminal-growth monotonic tests pass | PASS: expected failures reproduced |

Logs were preserved in the temporary copy as `cold_run_proforma.log`, `cold_run_integrated.log`, `cold_run_peer.log`, `cold_run_step5.log`, and `cold_run_step6.log`. The separately authorized Step 6.3 changed-input command was excluded because its post-test evidence already exists.
