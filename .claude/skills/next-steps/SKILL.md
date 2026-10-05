---
name: next-steps
description: Rank what to work on next from the risk register, the roadmap and the decision log. Use when someone asks "what should we do next?", at the start of a planning session, or before the start of a term. Reads only; never edits the register or the roadmap.
---

# Next steps

Produce a short, ranked list of what to work on next, with the reasoning a person needs to agree or
disagree. **You recommend; a person decides.** This skill reads files and writes nothing.

## Inputs

Read these, in this order. If one does not exist, say so in the output and carry on.

1. `templates/risk-register.md` (or wherever this repository keeps its register): every open risk,
   its likelihood, severity and mitigation status.
2. `templates/roadmap.md` (or this repository's roadmap): every item not yet shipped, with its
   status, value and effort.
3. `DECISIONS.md`: **search it, do not read it end to end.** For each candidate item, grep its id
   and its subject, and read only the entries that match.
4. `templates/parking-lot.md`: read it, but **never rank from it.** Parked ideas are not work until
   a person says so. You may mention one if it bears on a ranked item.

## How to rank

1. **Risk first.** Any open risk scored High or above whose mitigation is not in place goes above
   everything else, highest score first. Student data exposure outranks everything at the same
   score.
2. **Then value per effort.** Among the rest, rank by the value and effort columns on the roadmap.
   When two items tie, prefer the one that unblocks others.
3. **Blocked items are not candidates.** List them separately with what they wait on.
4. **Work waiting on a person goes in its own list**, not the ranking. These are the items people
   forget: a permission to grant, a credential to rotate, a sensor to switch on.
5. **Check for stale cells.** If a decision entry or a recent commit shows an item is done, or a
   step listed as pending has happened, say so: "RM-12's status still says X, but the 2026-02-03
   entry shows it was done." Do not fix it yourself.

## Output

```
## Recommended next (top 5)
1. <id> <title>: <one line on why it ranks here, citing the risk score or value/effort>
...

## Waiting on a person
- <id>: <what the person must do>

## Blocked
- <id>: <what it waits on>

## Possibly stale
- <file, row>: <what looks out of date and the evidence>
```

Keep it to one screen. Cite ids and decision dates so a person can check your reasoning.

## Never

- Never edit the register, the roadmap or the parking lot. Ranking and editing are separate jobs,
  so a ranking never quietly changes the thing it ranks.
- Never create a roadmap item. Suggest one in the output, under a heading "Ideas for the parking
  lot", and let a person decide.
- Never query a database to check a status. If a fact needs data, say what query a person should
  run.
