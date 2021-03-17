# DJH Screener

Overview
-
The screener filters option-stock pair based on four tests:
1. Option profitability : Covered call profitability 
2. Momentum test : Price objective in Point & Figure chart
3. Analyst recommendations : marketwatch.com 
4. Stock fundamentals : P/E ratio

The stock-option pair has to pass all the above test inorder to be screened.

Project Structure
-
- <main.py> does the above tests and stores the result in reports folder and also sends email to the user
- <config.py> has configurations of the test 
- step_1_xxx to step_4_xxx folders have for codes respect to each step
- yahoo_finance_api : Yahoo finance API connectors
- email_alerts: Email sending util
- unused: Experimental codes that doesn't affect the project flow

Detailed Specification
-
Refer to /project_spec/DJH_spec.docx for more details on each step