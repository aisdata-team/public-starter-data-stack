# Roadmap

_Last updated 2026-03-02: one note only. Move the previous note to a history file when you replace it._

One backlog, ranked: **risk first, then value per effort.** An item reaches this file only when a
person decides it should (DECISIONS.md 2026-02-24). Ideas go to `parking-lot.md` first.

## How this file works

- Ids (`RM-NN`) are permanent and never reused. Decision entries cite them.
- **Status** starts with one of `Proposed`, `Next`, `In progress`, `Blocked`. When an item is done,
  move its row to Shipped with the date and the decision entry that closed it.
- **Value** and **Effort** are S, M or L. **Risk** names the register row the item reduces, if any.
- Work waiting on a person ends its Status cell with `WAITING ON <role>: <what they must do>`.

## Backlog

| Id | Item | Risk | Value | Effort | Status |
|---|---|---|---|---|---|
| RM-03 | Extend the no-names check to exports built outside the warehouse | R-01 | M | M | Next |
| RM-04 | Row-count check after each load, warn on a large drop | R-03 | M | S | Proposed |
| RM-05 | Attendance dashboard for heads of grade | (none) | L | M | Blocked: needs RM-04 first |

## Shipped

| Id | Item | Shipped | Decision |
|---|---|---|---|
| RM-01 | README section "Things that look wrong but are right" | 2026-02-03 | 2026-02-03 |
| RM-02 | Documentation checks on every pull request and push to `main` | 2026-01-20 | 2026-01-20 |
