# Decisions

A dated log of decisions, newest first. Each entry says what was decided, why, and what would make
us revisit it.

**How this file works**

- A heading is a permanent id: `## YYYY-MM-DD — title`. A second entry on the same date is
  `## YYYY-MM-DD (b) — title`, then `(c)`, and so on. The bare date counts as `(a)`.
- Ids are never renumbered or reused, because rules elsewhere cite them.
  `python3 scripts/check_docs.py` fails on a duplicate; `--next` prints the next free id.
- A decision that turns out wrong is not edited. Add a correction line directly under its heading
  and write a new entry.
- Agents search this file for the area they are touching. Nobody, person or agent, reads it end
  to end.

> **These entries are examples.** They are generalized from a real school's decision log; dates
> and details are illustrative. Delete them and start your own, or keep the ones that apply.

---

## 2026-03-02 — Every first run that writes to production is declared: passed or failed

**Decision.** Work that writes to a production system records its first real run in its entry, on
its own line: `FIRST RUN PASSED`, or `FIRST RUN FAILED — <what it found>`.

**Why.** No automated test here calls a real system, so a green check means the code loads and its
logic holds against made-up data, nothing more. When we looked back at the problems that actually
reached us, most were wrong assumptions that surfaced on first contact with real data, with every
check green. Declaring the first run makes that visible, and the share of first runs that find
something becomes an honest measure of how well the checks work.

**Revisit if** the share that find something stays high for a term: the checks are not catching
what they should, and the fix is better checks, not more declarations.

---

## 2026-02-24 — A new idea is not a roadmap item until a person says yes

**Decision.** Ideas an agent or a person notices while doing other work go in a parking lot: one
line each, no number, deletable. A roadmap item is created only when a person decides it should be.

**Why.** Filing an idea is free for an agent and looks diligent, so the roadmap filled with
"proposed" items faster than work closed. A parking lot makes "not on the roadmap" a safe answer.

**Revisit if** the parking lot passes about forty lines (prune it), or an idea reaches the roadmap
without a person's decision.

---

## 2026-02-17 — An exclusion justified by a count names the test that re-counts it

**Decision.** When a model leaves something out because "we checked and there are none", the
comment beside it names a test that re-measures that set every night and warns when it is no
longer empty.

**Why.** We built a rule on a check that found no records of a certain kind. A month later a new
data source arrived and several existed, and their data was being dropped without an error. The
count was true the day it was taken. It was a fact about that month's data, not a law.

**Revisit if** the nightly warnings are routinely ignored; then they need an owner, not more tests.

---

## 2026-02-03 — Check the source's retention before calling records missing

**Decision.** Before treating rows as missing or a pipeline as broken, find out how long the source
system keeps that record type.

**Why.** A new feed returned far fewer attendance rows than the history we already held. The agent
first blamed the pipeline's paging, then a change in the vendor's API. Both were reasonable and
both were wrong: the source system deletes routine "present" records a few weeks after creating
them. The fuller history existed only because an older pull had kept them. No test would have found
this; someone who knew the system did.

**Revisit if** the source changes how long it keeps records, or we start archiving every pull.

---

## 2026-01-20 — Decision ids are allocated last, and duplicates fail the checks

**Decision.** A new entry takes its id at the write-up, not when the work starts, using
`check_docs.py --next`. The checks fail on a duplicate id, on the pull request and again on the
merge to `main`.

**Why.** Two pieces of work in progress at once each took "the next free id" from their own copy of
this file, and two different decisions ended up with the same id. Nothing broke, but a rule citing
that id now pointed at two decisions. A duplicate can only appear when two branches land, so the
merge to `main` is the first moment a check can see it.

**Revisit if** the repository gets branch protection that requires branches to be up to date
before merging; that closes the gap the merge-time check covers.

---

## 2026-01-12 (b) — The rules file is a contract: a rule, a one-line why, a citation

**Decision.** Each rule in `AGENTS.md` is one line, with a one-line reason and a citation to the
decision behind it. Reasoning, history and examples live in this file. The rules file stays under
a size budget that `check_docs.py` enforces.

**Why.** An agent reads the rules file on every turn, so every line costs attention before any
work starts. A rules file that grows into a manual crowds out the task. Short rules are also the
ones people actually read. And a rule without a citation gets "fixed back" by the next competent
person who cannot see why it exists.

**Revisit if** the budget forces out a rule that is genuinely needed on every turn; raise the
budget, don't split the file.

---

## 2026-01-12 — AGENTS.md holds the rules; CLAUDE.md imports it

**Decision.** The rules live in `AGENTS.md`. `CLAUDE.md` contains one line, `@AGENTS.md`, which
imports them.

**Why.** Claude Code reads `CLAUDE.md`; Codex reads `AGENTS.md`. One file with an import keeps both
tools on the same rules, so switching tools never means two rule sets drifting apart.

**Revisit if** either tool changes the file it reads.

---

## 2026-01-05 — The agent never touches production data; a person runs every query

**Decision.** The agent works on code, schemas and documentation only. Its environment holds no
warehouse credentials. When a question needs real data, the agent writes the query, a person runs
it, checks the result for anything identifying, and pastes back what the agent may see.

**Why.** An instruction not to query student data is a sign: it works on the days it is read. No
credentials is a cage: it works even when the agent is wrong, rushed or tricked by text it should
not have trusted. The cage is also what lets us give the agent real freedom over the code.

**Revisit if** a task genuinely needs automated read access; then give it a separate account that
can see only de-identified development data, and write a new entry.
