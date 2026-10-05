# Rules for agents working in this repository

Each rule is one line, a one-line why, and the decision behind it. The reasoning lives in
`DECISIONS.md`: **search it for the area you are touching; never read it end to end.**
This file is a contract, not a manual. Keep it short (`DECISIONS.md` 2026-01-12 (b)).

## Before you start

- Read `README.md`, then only the section for what you are touching.
- Search `DECISIONS.md` before changing anything in an area. Why: most "obvious fixes" were tried
  once and undone, and the entry says why.

## Student data

- **You never connect to, query or export production data.** Write the query; a person runs it,
  checks the result for anything identifying, and pastes back what you may see. Why: the safest
  student record is one you never touch (`DECISIONS.md` 2026-01-05).
- Never put real names, ids or other identifying values in code, tests, examples or commit
  messages. Use made-up values.

## Writing SQL

- **Never assume a column exists.** Read the upstream model before you reference it. Why: a guessed
  column name compiles in your head and fails in the warehouse.
- **Cast every id to text in staging.** Why: a number joined to text drops rows without an error.
- **Build on the model under a report, never on the report itself.** Why: reports are the end of
  the line; anything built on them breaks when the report changes.
- **A record that looks missing may have been deleted at the source.** Check how long the source
  keeps that record type before calling it a bug (`DECISIONS.md` 2026-02-03).
- **An exclusion justified by a count names the test that re-counts it.** Why: "we checked, there
  are none" is true only of the data you checked (`DECISIONS.md` 2026-02-17).

## Documentation

- A change someone could plausibly undo gets a `DECISIONS.md` entry, and any rule it creates cites
  that entry. Allocate the entry's id **last**, at the write-up, with `python3 scripts/check_docs.py --next`
  (`DECISIONS.md` 2026-01-20).
- Fix any `README.md` sentence your change makes false, in the same change.
- Never edit an old decision. Add a correction line under its heading and write a new entry.
- Anything that writes to production records its first real run as **FIRST RUN PASSED** or
  **FIRST RUN FAILED** in its entry (`DECISIONS.md` 2026-03-02).

## Who decides

- A new idea goes in the parking lot (see `templates/parking-lot.md`), not the roadmap, until a
  person says yes (`DECISIONS.md` 2026-02-24).
- Never push to `main`, change permissions, or touch credentials. Propose; a person does it.
