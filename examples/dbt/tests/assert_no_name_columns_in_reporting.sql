-- Fails if any table in the reporting schema has a column that looks like a name, an email
-- address or a birth date. Reporting tables are what dashboards and exports read, so this is the
-- last place identifying data can be stopped before it leaves the warehouse.
--
-- A sentence in AGENTS.md is a sign: it works when it is read. This test is a lock: `dbt build`
-- fails whoever wrote the model, person or agent.
--
-- Each returned row is one offending column. Zero rows is a pass.
--
-- BigQuery form below. For Postgres or Snowflake, read from `information_schema.columns` and filter
-- on `table_schema` instead.

{% set reporting_schema = var('reporting_schema', target.schema ~ '_reporting') %}

with columns as (

    select * from `{{ target.database }}`.`{{ reporting_schema }}`.INFORMATION_SCHEMA.COLUMNS

),

suspicious as (

    select
        table_name,
        column_name
    from columns
    where regexp_contains(
        lower(column_name),
        r'(first_name|last_name|full_name|preferred_name|email|birth|dob|phone|address)'
    )

)

select * from suspicious
