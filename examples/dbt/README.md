# dbt examples: written rules that fail when broken

Three files that turn rules from `AGENTS.md` into checks. Copy them into your own dbt project and
rename the source to match yours. They are written for BigQuery; the comments say what to change
for Postgres or Snowflake.

| File | Rule it enforces | What happens when it breaks |
|---|---|---|
| `models/staging/stg_sis__students.sql` | Cast every id to text in staging; a measured exclusion names its re-count test | Nothing fails here; this is the pattern to copy |
| `tests/assert_no_name_columns_in_reporting.sql` | Reporting tables never carry names, emails or birth dates | `dbt build` fails |
| `tests/assert_excluded_applicants_have_no_records.sql` | "We checked, there are none" is re-checked every night | `dbt build` warns |

The progression is the point. A rule starts as a sentence in `AGENTS.md`, which works when it is
read (a sign). It becomes a test, which works whether or not anyone reads it (a lock). See
`docs/guide.md` for when each is worth the effort.

`sis` stands for "student information system". The columns are made up; read your own source
before you reference anything (`AGENTS.md`: never assume a column exists).
