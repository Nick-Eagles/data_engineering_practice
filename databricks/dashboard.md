# Loan eligibility dashboard

## Overview

After getting a glimpse of the loan eligibility dataset and generating some
exploratory plots in a [Databricks notebook](notebooks/explore_data.ipynb),
I moved on to better understand the dataset through querying in the Databricks
SQL Editor. Afterwards, I built a dashboard to summarize and highlight some key
findings.

## SQL queries

To build the dashboard, I first constructed smaller tables by querying the main
loan eligibility dataset.

First, I wanted to summarize how loan amount was impacted by education level.
I subset to the `Education` and `LoanAmount` columns and took rows where the
load amount wasn't null.

```sql
SELECT Education, LoanAmount
FROM loan_eligibility
WHERE LoanAmount IS NOT NULL;
```

I then wanted to generate a scatterplot of loan amount vs. applicant income,
with additional coloring by property area (rural, semi-urban, urban). A couple
high outliers in applicant income made it difficult to visualize the majority of
the data, so I took the bottom 99% of rows by income. This was a slightly more
complex query to build:

```sql
-- Calculate 99th percentile of income
WITH income_limits AS (
  SELECT
    percentile_approx(ApplicantIncome, 0.99) AS p99_income
  FROM loan_eligibility
  WHERE ApplicantIncome IS NOT NULL
)
-- Subset to the relevant columns
SELECT
  LoanAmount,
  Property_Area,
  ApplicantIncome
FROM loan_eligibility l
-- Join with percentile info to filter rows
CROSS JOIN income_limits
WHERE
  l.ApplicantIncome < income_limits.p99_income
  AND LoanAmount IS NOT NULL
  AND Property_Area IS NOT NULL;
```

For the final component of the dashboard, I wanted to communicate how gender and
marital status affected loan amount on average. Since we had two variables to
include on the x-axis, I concatenated them in the query, then averaged loan
amount by group.

```sql
SELECT
  Gender,
  Married,
  CONCAT(Gender, ' - ', Married) AS gender_marital_group,
  ROUND(AVG(LoanAmount), 1) AS avg_loan_amount
FROM loan_eligibility
WHERE GENDER IS NOT NULL
GROUP BY gender_marital_group, Gender, Married
ORDER BY gender_marital_group;
```

## The dashboard

Obviously we lose interactivity with this screenshot, but this is what the
dashboard looked like with every component in place:

[](dashboard.png)
