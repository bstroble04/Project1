FIN 439 – Project 1: Video 2 Transcript

Company: Archer-Daniels-Midland (ADM)
Topic: Financial Model, Valuation, and Validation

Introduction

For my second video, I'm going to explain how my ADM financial model works, how I used Python to complete my valuation, and how I tested my results.

I used Python and VS Code to connect the financial statements, calculate free cash flow, and estimate ADM's value.

My main goal was to make a model where changing an assumption would automatically update the results.

Financial Model and Assumptions

I started with ADM's historical financial information and used it to forecast the company's performance from 2026 through 2030.

My base assumptions included 2% annual revenue growth, a 6.75% gross profit margin, and 51 inventory days.

I also assumed $1.4 billion in annual capital expenditures, a $500 million minimum cash balance, and a $6 billion financing limit.

I also included the inputs needed to calculate my discount rate and complete the valuation.

The historical financial information provided the starting point for my projections.

Integrated Financial Statements

The next part of my code connects the income statement, balance sheet, and cash flow statement.

I used these statements to forecast ADM's financial performance.

This section calculates working capital, including inventory, receivables, and payables.

It then calculates cash flow and determines whether ADM needs additional financing.

My free cash flow calculation starts with operating income after taxes, adds depreciation, and subtracts capital expenditures and changes in working capital.

The results are then organized into the three financial statements for each forecast year.

Discounted Cash Flow Valuation

I then used a discounted cash flow model to calculate ADM's enterprise value.

After that, I adjusted for cash, debt, and other claims to estimate equity value per share.

One thing I learned was that changing one assumption could affect several parts of the model, so everything needed to stay connected.

Comparable Company Analysis

Moving on to the ADM peer comps PY.

I also completed a comparable company analysis using Bunge and Ingredion.

I used their stock prices, earnings, debt, cash, and EBITDA to compare the companies.

I calculated P/E multiples to compare ADM with other companies.

I also calculated EV/EBITDA multiples using the companies' enterprise values.

The results varied depending on the company and valuation method, which showed me why it was important to use more than one valuation approach.

Sensitivity Analysis

I also completed sensitivity analysis to see how different assumptions affected my model.

Gross margin, inventory days, and capital expenditures were especially important because they affected cash flow and financing needs.

This helped me identify which assumptions had the biggest impact on my valuation.

Model Validation and Testing

After building my model, I completed several validation tests to make sure it worked correctly.

This section collects the model's results, including free cash flow, valuation per share, financing needs, and accounting validation results.

I tested my base model and different assumptions to see whether the calculations responded correctly.

I also checked that increasing the discount rate decreased the valuation and that increasing terminal growth increased the valuation.

Changed-Input Test

For my changed-input test, I reduced annual capital expenditures from $1.4 billion to $1.3 billion.

Before running the test, I expected free cash flow to improve and financing needs to decrease.

This function allowed me to run that specific change after my prediction was locked.

The results supported my prediction.

By 2030, free cash flow increased by approximately $93.55 million, and the financing facility balance decreased by approximately $516 million.

Known-Answer Test

I also reproduced a known-answer example from an earlier Asbury Automotive Group lab, which matched an expected result of approximately $291.75 per share.

Financing Limit and Failure Testing

Another important test was checking whether the model could identify scenarios that were not financially feasible.

The code checks whether the financing facility exceeds the model's limits and identifies the first year of failure.

In my downside scenario, ADM needed approximately $6.87 billion in financing, which exceeded my $6 billion limit.

The model identified this as a failure, so I did not treat that scenario as a valid investment valuation.

Reproducibility Testing

I also completed a cold-run test in a separate Python environment to make sure the project could reproduce the same results.

This was important because I wanted someone else to be able to run my model and understand where the numbers came from.

Final Reflection

Overall, this project helped me become more comfortable using Python for financial modeling.

I learned how to connect financial statements, calculate valuations, and test assumptions rather than just accepting the first result.

AI helped me develop and troubleshoot the code, but I still needed to verify the results and make my own investment decision.

Thank you.