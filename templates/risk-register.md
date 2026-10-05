# Risk register

_Last updated 2026-03-02: one note only. Move the previous note to a history file when you replace it._

What could go wrong, how likely, how bad, and what is being done about it. Sorted by score, highest
first. **A new risk is a row here, not a roadmap item.** The roadmap holds the work that reduces it.

## How this file works

- **Likelihood** and **Severity** are 1 (low) to 3 (high). **Score** = likelihood × severity.
- **Status** is one of `Open`, `Mitigating`, `Mitigated`, `Accepted`. `Accepted` needs a decision
  entry saying who accepted it and why.
- Each row has a Detail entry below with the evidence. Update both together when a risk moves.
- Work waiting on a person ends the Detail entry with a line:
  `WAITING ON <role> since YYYY-MM-DD: <what they must do>`.

## Register

| Id | Risk | L | S | Score | Status | Roadmap |
|---|---|---|---|---|---|---|
| R-01 | Identifying student data reaches a report or export | 2 | 3 | 6 | Mitigating | RM-03 |
| R-02 | One person is the only one who knows how a pipeline works | 3 | 2 | 6 | Mitigating | RM-01 |
| R-03 | A source system changes its export and a pipeline drops rows silently | 2 | 2 | 4 | Open | RM-04 |
| R-04 | A credential in use is tied to a staff member's personal account | 1 | 3 | 3 | Mitigated | (none) |

## Detail

### R-01: Identifying student data reaches a report or export

Reporting tables feed dashboards that are shared beyond the data team. A column added for one
analysis could carry names into a shared view. **Mitigation:** the `assert_no_name_columns_in_reporting`
test fails the build (example in `examples/dbt/`). **Still open:** exports built outside the
warehouse are not covered.

### R-02: One person is the only one who knows how a pipeline works

The attendance pipeline's quirks live in one person's head. **Mitigation:** the README section
"Things that look wrong but are right" and a decision entry per quirk (DECISIONS.md 2026-02-03).

WAITING ON data lead since 2026-02-20: walk a colleague through the attendance pipeline and note
anything the README misses.

### R-03: A source system changes its export and a pipeline drops rows silently

**Mitigation planned:** a row-count check after each load that warns on a large drop (RM-04).

### R-04: A credential in use is tied to a staff member's personal account

**Mitigated 2026-01-15:** moved to a service account owned by the school, kept in the secret store.
