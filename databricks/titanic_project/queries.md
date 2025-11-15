# SQL and Dashboard

With the gold tables created for the titanic dataset, I move to the SQL Editor
to ultimately connect insights from these tables into a dashboard.

I intend to communicate a couple key findings in this dashboard:

- Passenger sex and class have a profound impact on survival probability
- Port of departure predicted fare price and more weakly, survival probability

## SQL Queries

To construct tables used in the dashboard, I run some SQL queries, add
visualizations attached to the resulting tables, and add those visualizations
as components in the dashboard.

## Survival vs. sex and passenger class

First, the query relating survival to sex and passenger class-- this was simple
because we already had a gold table pre-computed with the relevant metrics.

```sql
SELECT
  CONCAT(Sex, '- class ', Pclass) AS SexClass,
  Sex,
  SurvivalRate
FROM gold.titanic_sex_class;
```

## Stats related to port of departure

First, I explore the distribution of ticket price against port of departure.
The silver table is sufficient here to access cleaned passenger-level data.

```sql
SELECT Embarked, Fare
FROM silver.titanic
WHERE Embarked IS NOT NULL;
```

The simplest query of all was simply pulling one of the gold tables, which
already had info about survival rate by port.

```sql
SELECT * FROM gold.titanic_port;
```

## Dashboard

I simply added the visualizations associated with each query to a new dashboard,
tweaked some things visually, added some descriptive text, and had a complete
dashboard:

![The complete dashboard](images/dashboard.png)
