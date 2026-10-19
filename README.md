# Project1
Project Overview
For Project 1, I analyzed Archer-Daniels-Midland (ADM) to determine whether an investment fund should initiate a position, place the company on watch, or decide not to invest.
I used Python and AI-assisted tools to develop a five-year financial model, calculate a discounted cash flow valuation, compare ADM with similar companies, and test how changes in assumptions affect the results.
Final Investment Recommendation
My final recommendation is WATCH/DEFER as of October 16, 2026, when ADM's closing stock price was $82.61.
My base DCF produced a negative mathematical residual equity value of approximately -$0.76 per share. My funded upside scenario produced approximately $24.22 per share.
Although one comparable-company valuation was close to the market price, my overall analysis did not provide enough evidence to recommend initiating a position.
The full analysis, supporting evidence, and conditions that could change my recommendation are documented in adm_investment_committee_memo.md.
Project Files
Research and Final Recommendation
- project-1-edition-a.md — Original Edition A baseline; preserved unchanged.
- adm-working-notes.md.txt — Early research and working notes.
- adm_investment_committee_memo.md — Final investment recommendation.
- adm_step7_decision_analysis.md — Final scenario analysis and investment decision.
Financial Models
- adm_integrated_model.py — Five-year financial statements, FCFF DCF, valuation bridge, and model checks.
- adm_model_documentation.md — Financial model assumptions, methodology, sources, and results.
- adm_valuation_model.py — Supporting valuation calculations.
- adm_peer_comps.py — Comparable-company valuation calculations.
- adm_peer_comps_documentation.md — Peer selection policy, assumptions, and sources.
- adm_step5_sensitivity.py — Sensitivity analysis.
- adm_step5_sensitivity_report.md — Sensitivity results and interpretation.
- adm_step7_scenarios.py — Additional scenario analysis.
- adm_step7_oct16_scenarios.py — Final October 16 valuation scenarios.
- adm_step7_wacc_comparison.py — Comparison of valuation-date WACC assumptions.
- adm_valuation_workbench.ipynb — Interactive Google Colab valuation model.
- adm_workbench_documentation.md — Interactive workbench documentation.
Validation and AI Use
- adm_step6_validation.py — Automated validation tests.
- adm_step6_validation_report.md — Validation results and supporting evidence.
- adm_step6_locked_prediction.md — Pre-run changed-input prediction.
- adm_step6_cold_run.md — Fresh-environment run results.
- adm_step6_ai_decision.md — AI-output evaluation and decision.
Video Transcripts
- video1transcript.md — Research Evolution video transcript.
- Video2transcript.md — Code and Validation video transcript.
- Video3transcript.md — Investment Committee video transcript.
The three recorded videos are submitted or linked separately according to the Brightspace instructions. The transcripts should reflect the actual recordings.
Reproducible Python Runs
The core valuation scripts require Python 3.13+ and use only the Python standard library plus local project modules. requirements.txt intentionally has no third-party package entries for these scripts. The interactive notebook may require additional packages in Colab.
From the project root, the validation sequence is:
python Proforma.py
python adm_integrated_model.py
python adm_peer_comps.py
python adm_step5_sensitivity.py
python adm_step6_validation.py
adm_step5_sensitivity.py regenerates adm_step5_sensitivity_report.md.
The $1,300 million Step 6.3 changed-input test is intentionally excluded from the default Step 6 validation command. It uses a separately documented, gated post-lock command to preserve the original prediction evidence.
Valuation Date and Model Results
The original integrated model uses September 24, 2026 market inputs, including an ADM closing price of $81.88.
The final investment committee recommendation uses October 16, 2026 market inputs, including an ADM closing price of $82.61.
The October 16 scenarios and updated WACC calculations are documented separately to preserve the original model's audit trail.
Final October 16 Scenario Results
Scenario	DCF Value per Share	2030 Facility Balance	Funding Status
Low	-$14.32	$6,873.55 million	FAIL
Base	-$0.76	$5,144.23 million	PASS
Funded High	$24.22	$3,126.30 million	PASS


The Low scenario exceeds the $6,000 million financing-facility limit and is treated as a diagnostic result rather than an investable valuation.
Negative DCF values represent mathematical residual equity values and are not negative stock-price targets.
Validation and Model Limitations
The project includes:
- A known-answer reconciliation using the ABG training case.
- An independent check of ADM's FY2025 reported revenue against its Form 10-K.
- A locked changed-input test comparing a prediction with actual model results.
- Five-year balance sheet and cash flow reconciliation checks.
- DCF and enterprise-to-equity bridge checks.
- WACC and terminal-growth directional tests.
- Financing-facility stress tests.
- A fresh-environment cold run.
- An AI-output evaluation and disclosure of remaining evidence limitations.
The model is sensitive to gross margin, working capital, capital expenditures, WACC, and terminal growth. The valuation also depends on assumptions about financing and the enterprise-to-equity bridge.
These limitations are discussed in the investment committee memo and supporting documentation.
AI Assistance
ChatGPT and Codex assisted with developing and troubleshooting Python code, organizing financial data, checking calculations, preparing sensitivity and validation reports, and improving written documentation.
I remained responsible for evaluating assumptions, verifying important financial information, interpreting results, and making the final investment recommendation.
The supporting validation and AI-use evidence is documented in adm_step6_validation_report.md and adm_step6_ai_decision.md.
