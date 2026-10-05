# Teaching the machine: a starter kit

A small, copyable starting point for running a school data stack with an AI coding agent
(Claude Code, Codex or similar) **without ever giving the agent your student data**.

It accompanies the workshop *Teaching the Machine: How Documentation Makes AI Data Tools Actually
Work*. The idea in one sentence: **an AI agent only knows what you have written down, so the
documentation that makes it useful is the same documentation that makes your stack maintainable by
people.**

Nothing here is tied to one school, one student information system or one warehouse. Replace the
examples with your own.

## What is in the box

| Path | What it is | When you need it |
|---|---|---|
| `README.md` | This file. In your copy: what exists and where it lives | Day one |
| `AGENTS.md` | The rules file: about ten rules, each with a one-line why and a citation | Day one |
| `CLAUDE.md` | One line that imports `AGENTS.md`, so Claude Code and Codex read the same rules | Day one |
| `DECISIONS.md` | The decision log: one dated entry per decision, newest first | First month |
| `.claude/settings.json` | Permission rules that stop the agent running database commands (a lock, not a cage) | Day one |
| `.claude/skills/next-steps/` | One skill: a recurring task written down once | First repeated task |
| `scripts/check_docs.py` | Two checks: no duplicate decision ids, and a size budget for the rules file | First incident |
| `.github/workflows/checks.yml` | Runs those checks on every pull request and every push to `main` | First incident |
| `examples/dbt/` | A staging model and two tests that turn written rules into checks that fail | First incident |
| `templates/` | A risk register, a roadmap and a parking lot, for when a list in the README is not enough | Later |
| `docs/guide.md` | **The technical guide**: the cage in practice, the query protocol, how the pieces fit, and why each rule exists | Read this first |

## How to use it

1. **Copy, don't fork.** Use *Use this template* on GitHub, or copy the files into the repository
   that already holds your dbt project or pipeline code. The rules only help if they sit next to
   the code the agent edits.
2. **Rewrite the README** so it describes *your* stack: sources, pipelines, models, reports, and a
   section called "Things that look wrong but are right".
3. **Edit `AGENTS.md`.** Keep the rules that apply, delete the rest, and add the ones only you
   know. Keep it under a page: every line costs the agent attention on every turn.
4. **Start `DECISIONS.md`** the first time you decide something you might later be tempted to undo.
5. **Turn on the checks** when the first thing goes wrong twice. `python3 scripts/check_docs.py`
   runs locally; the workflow runs it on GitHub.
6. **Add the rest on a trigger, not a plan.** A skill when you do a task by hand twice; a check when
   something breaks; a register and roadmap when the backlog outgrows a list.

```bash
python3 scripts/check_docs.py          # both checks
python3 scripts/check_docs.py --next   # the next free decision id for today
python3 -m unittest discover tests     # the checks' own tests
```

## The three rules this kit is built on

- **You keep the authority.** The agent proposes; a person decides what reaches production, what
  goes on the roadmap and what a query is allowed to return.
- **The agent keeps the record.** Every decision is dated, every rule points at the decision behind
  it, and corrections are added, never edited away.
- **Your domain knowledge is the final check.** Tests catch broken code. Only someone who knows the
  school catches a confident answer that is wrong.

## Further reading

- The workshop handout, with the full blueprint and starter text for each file:
  [handout (PDF)](https://drive.google.com/file/d/18q8bAthU_drO1euMjP44No1xuQdJdnNZ/view?usp=sharing)
- The School Data Maturity Model (CC BY-NC-SA 4.0), for deciding where to go next:
  [read the model](https://docs.google.com/document/d/1r4e8YwzSf3hdcaYBxfb0hnoobNSWSbPIIEhuLjG7EIs/edit)

## License

MIT. See `LICENSE`. Copy it, change it, make it yours.
