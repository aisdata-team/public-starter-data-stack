# The technical guide

The workshop handout explains the ideas: the manual, signs, locks and cages, every rule has a scar,
and the growth path. This guide is the technical layer underneath. It covers how the pieces are
wired, what to set up, how to check it is still set up, and why each check in this kit exists.

It assumes you have a version-controlled data project (dbt, Python pipelines or both), a warehouse,
and an AI coding agent such as Claude Code or Codex. The examples use dbt on BigQuery, but the
patterns carry over to other tools.

**Contents**

1. [The architecture: where the agent sits](#1-the-architecture-where-the-agent-sits)
2. [The cage in practice](#2-the-cage-in-practice)
3. [Signs, locks and cages, with configuration](#3-signs-locks-and-cages-with-configuration)
4. [The manual as an engineering artifact](#4-the-manual-as-an-engineering-artifact)
5. [The machinery: each check and the scar behind it](#5-the-machinery-each-check-and-the-scar-behind-it)
6. [Skills](#6-skills)
7. [Closing out a change](#7-closing-out-a-change)
8. [Several agents at once](#8-several-agents-at-once)
9. [dbt and BigQuery traps we hit](#9-dbt-and-bigquery-traps-we-hit)

---

## 1. The architecture: where the agent sits

```
                        ┌──────────────────────── production ─────────────────────────┐
                        │                                                             │
  source systems ──▶ loader ──▶ raw tables ──▶ dbt: staging ─▶ models ─▶ reporting ──▶ dashboards
  (SIS, LMS, ...)       │           ▲                         ▲                         │
                        │           │ runs on a schedule as a service account,          │
                        │           │ secrets from a secret store                       │
                        └───────────┼─────────────────────────┼─────────────────────────┘
                                    │                         │
                              deploy (a person)          query (a person)
                                    │                         │
  ┌─────────── agent's workspace ───┼──────────┐              │
  │  a copy of the repository       │          │      ┌───────┴────────┐
  │  README, AGENTS.md, DECISIONS   │          │◀─────│ results the    │
  │  code, tests, checks            │          │      │ person chose   │
  │  NO credentials, NO .env        │          │      │ to paste back  │
  └──────────────┬─────────────────────────────┘      └────────────────┘
                 │ pull request
                 ▼
     automated checks (CI) ──▶ a person reviews and merges
```

Three properties make this safe enough to give the agent real freedom over the code:

- **The agent's workspace has no path to production.** It edits files and runs tests against
  made-up data. It cannot run a query, a model or a deploy, because nothing in its environment can
  authenticate to anything.
- **Every crossing into production goes through a person.** A person merges, a person deploys, and
  a person runs any query against real data.
- **The scheduler is a separate identity.** Production jobs run as a service account whose
  credentials live in a secret store and are injected at deploy time. They are never in the
  repository and never in the agent's workspace.

---

## 2. The cage in practice

### 2.1 Build it

| Piece | What to do | What it prevents |
|---|---|---|
| No warehouse credentials in the agent's environment | No `profiles.yml` with a key, no `gcloud auth login`, no `.env` with a password, no default application credentials on the machine or container the agent runs in | The agent querying or exporting real data, whatever it is told |
| Secrets outside the repository | Keep them in a secret manager (your cloud's, or a password manager's CLI). Render them into a gitignored `.env` on the production machine at deploy time | A secret committed once and living forever in git history |
| Production runs as a service account | A dedicated account owned by the school, with only the roles the pipelines need | Pipelines that stop working when a staff member leaves, and personal accounts with production power |
| A person deploys | One deploy command, run by a person, on the production machine | An agent change reaching production without a person choosing it |
| `.gitignore` covers credentials | See `.gitignore` in this kit | The most common accidental leak |

The simplest version of the cage is to **run the agent somewhere that has never had credentials**:
a cloud coding session, a dev container, or a separate user account on your laptop. That is easier
than removing credentials from a machine you also use for production work, and easier to trust.

### 2.2 Inspect it

A cage you believe is there and is not is worse than none, because you stop watching. Check it
when you set it up, after any change to the agent's environment, and once a term. Ask the agent to
run these and show you the output; every line should come back empty or with an error.

```bash
gcloud auth list 2>&1                         # expect: no credentialed accounts
ls ~/.config/gcloud/application_default_credentials.json 2>&1   # expect: no such file
ls ~/.dbt/profiles.yml 2>&1                   # expect: no such file (or one with no key)
env | grep -iE 'key|secret|token|password' | sed 's/=.*/=<set>/'   # expect: nothing you did not put there on purpose
git log --all -p | grep -iE 'BEGIN PRIVATE KEY|"private_key"' | head   # expect: nothing
```

Then try the real thing: ask the agent to run a trivial query (`select 1`) against the warehouse.
It should fail on authentication. **If it succeeds, the cage is not there**, whatever your rules
file says.

### 2.3 The query protocol

When a question needs real data, the agent writes the query and a person runs it.

1. **The agent writes a complete, runnable query**, with real table names and no placeholders, and
   says what it expects the result to show and what it will do with it.
2. **It asks for the least that answers the question.** Counts, distributions, min and max dates
   and lists of distinct codes are usually enough. Rows are the exception, and rows with names are
   never needed.
3. **A person reads the query before running it**, runs it with their own access, and checks the
   result for anything identifying.
4. **The person pastes back only what the agent may see.** For a row-level answer, that means ids
   replaced with made-up ones, or a count instead of the rows.
5. **The finding goes in the record.** If the result changes a decision, the decision entry cites
   the date and the count, and an exclusion based on a count names its re-count test (§5.3).

A useful shape for the agent's request:

```
QUESTION   Do any withdrawn students still have attendance after their exit date?
QUERY      select count(distinct a.student_id) as students, min(a.attendance_date), max(a.attendance_date)
           from `my-project.raw_sis.attendance` a
           join `my-project.raw_sis.students` s using (student_id)
           where s.enrollment_status = 'withdrawn' and a.attendance_date > s.exit_date
EXPECTED   0 students. If not 0, the exit-date filter in stg_attendance is wrong.
NEED BACK  The single row. No ids.
```

### 2.4 When the agent needs more than the protocol gives

Sometimes a task really does need the agent to run queries itself, such as profiling a new
source. Don't widen the cage. Build a second, smaller one:

- a **development dataset** holding de-identified data only (ids replaced by salted hashes; names,
  emails and birth dates dropped or replaced),
- a **separate service account** that can read only that dataset,
- a **decision entry** recording the change, who approved it and what would make you revoke it.

Salted hashing in dbt looks like this. The salt comes from an environment variable, so the
repository never holds it and the same student gets the same pseudonym in every model:

```sql
-- macros/pseudonym.sql
{% macro pseudonym(column) -%}
    to_hex(sha256(concat(cast({{ column }} as string), '{{ env_var("ANON_SALT") }}')))
{%- endmacro %}
```

An unsalted hash of a student id is not de-identification: anyone with the list of ids can
recompute it.

---

## 3. Signs, locks and cages, with configuration

The handout's test for each is **what happens if the sign is ignored?** Here is what each looks
like in files.

| Level | Example in this kit | File | Fails when |
|---|---|---|---|
| Sign | "You never connect to, query or export production data" | `AGENTS.md` | The agent does not read it, misreads it, or is talked out of it by text it should not trust |
| Sign | "Cast every id to text in staging" | `AGENTS.md` | Same |
| Lock | Database commands denied in the agent's tool permissions | `.claude/settings.json` | A person edits the file, or the agent reaches the database another way (a Python client library, say) |
| Lock | Reporting tables cannot carry name columns | `examples/dbt/tests/assert_no_name_columns_in_reporting.sql` | Someone skips the build, or names a column something the pattern misses |
| Lock | Duplicate decision ids fail CI | `.github/workflows/checks.yml` | Someone merges with red checks. Add branch protection so it takes an admin |
| Cage | No credentials in the agent's environment | §2.1 | It was never built, or credentials were added later for convenience. That is why §2.2 exists |

Two points people miss:

- **The permission deny list is a lock, not a cage.** It stops the obvious commands, and that is
  worth having: it catches the honest mistake and makes intent clear. But a determined or confused
  agent with credentials can still reach the data with a few lines of Python. Only the absence of
  credentials is a cage.
- **A check's dangerous failure is passing because it read nothing.** `check_docs.py` fails if it
  finds no decision headings at all, because a heading-format change would otherwise turn it into a
  check that passes forever. Do the same in any check you write: assert that it saw something
  before asserting that what it saw is clean.

---

## 4. The manual as an engineering artifact

### 4.1 The rules file is paid for on every turn

An agent loads `AGENTS.md` / `CLAUDE.md` into its context on every turn, before it starts on your
task. Ours grew to about 47 KB, roughly 12,000 tokens, because every lesson was written into it in
full. That is attention spent on every turn and not on the task. The fix was to treat it as a
contract:

- **One rule per line, a one-line why, a citation** to the decision entry that holds the reasoning.
- **A size budget**, enforced by `check_docs.py` (12 KB by default). Raising it is a decision, with
  an entry.
- **Reasoning, history and examples live in `DECISIONS.md`**, which the agent searches by keyword
  for the area it is touching. It never reads that file end to end.

`CLAUDE.md` in this kit is one line, `@AGENTS.md`. Claude Code expands `@path` imports, so both
tools read one file.

### 4.2 Decision entries

An entry is the decision, the why in about five lines, and a **Revisit if**. Before writing one,
ask: *would a competent future reader plausibly do the wrong thing without this?* If not, it is a
finding and belongs in the README or a status cell, not the log.

The heading is a permanent id because rules cite it. That is why ids are never renumbered, why a
wrong decision gets a correction line and a new entry instead of an edit, and why duplicate ids
fail the checks (§5.1).

### 4.3 The README section people skip

Every stack has things that look wrong and are right: a filter that looks too narrow, a table
that looks redundant, a join that looks backwards. These are exactly what a capable agent will
"fix". Give them their own README section, one line each, citing the decision entry. It is the
cheapest protection you will write.

---

## 5. The machinery: each check and the scar behind it

Every check here exists because something went wrong first. When you add one, write down the scar.

### 5.1 Unique decision ids (`scripts/check_docs.py`)

**Scar.** Two agent sessions, working on separate branches, each took "the next free id" from
their own copy of the log. Both entries were correct, and a rule citing that id now pointed at two
different decisions. It happened three times in two days before we stopped it.

**Climb.** We renumbered, changed the rule to allocate the id *last*, at the write-up, and wrote
`--next` to propose the free id. Then we made CI fail on a duplicate. The workflow runs on pull
requests **and on push to `main`**. The push trigger matters because two branches can each pass on
their own and only collide once both have merged.

### 5.2 Rules file budget (`scripts/check_docs.py`)

**Scar.** The 47 KB rules file in §4.1. Nobody decided to make it that big. Each addition was
reasonable on its own.

### 5.3 Measured exclusions (`examples/dbt/`)

**Scar.** A rule excluded a category of records because a check had found none. A month later a
new source arrived and several existed. Their data was dropped without an error.

**Pattern.** An exclusion justified by a count carries a marker in the SQL comment:

```sql
-- measured-exclusion: counted-by assert_excluded_applicants_have_no_records
where enrollment_status != 'applicant_placeholder'
```

The named test re-counts the excluded set every night with `severity = 'warn'`. A warning is a
question for a person, not a broken build. If you want the marker enforced, a short script can
check that every marker names a test file that exists. Write it when a marker first goes stale.

### 5.4 No identifying columns in reporting (`examples/dbt/`)

**Scar (common, not ours alone).** A column added for one analysis carries names into a table
that feeds a shared dashboard.

**Pattern.** A singular test reads the warehouse's column catalog for the reporting schema and
fails on anything that looks like a name, email, birth date, phone number or address. It is
deliberately crude. A false positive costs a rename; a false negative costs a disclosure.

### 5.5 What a green build does not tell you

None of these checks, and none of our unit tests, make a real call to a real system. A green build
means the code loads, lints and its logic holds against made-up data. Most problems that actually
reached us were wrong assumptions found on first contact with real data, with everything green.
So:

- every pull request ends with a **Verification status** block:

  ```
  ## Verification status
  - CI verified: lint, model compile, check_docs, unit tests
  - Tests cover: the exclusion logic, against made-up rows
  - Not verified until the first real run: the source's actual values for enrollment_status
  ```

- every change that writes to production records **FIRST RUN PASSED** or **FIRST RUN FAILED: what
  it found** in its decision entry. The share that fail is your honest measure of the checks.

---

## 6. Skills

A skill is a recurring task, written down once, that the agent loads only when the task comes up.
In Claude Code a skill is a folder under `.claude/skills/` with a `SKILL.md`. The `description` in
its front matter is what the agent reads to decide whether to use it. The rest is loaded only
then, so a skill costs nothing on the turns it is not used.

Anatomy, using `.claude/skills/next-steps/SKILL.md`:

| Part | What it says | Why |
|---|---|---|
| `description` | What it does and when to use it, including the phrases people actually say | This is the trigger. A vague description is a skill that never runs |
| Inputs | Which files, in which order, and what to do if one is missing | The agent stops guessing what to read |
| Method | The ranking rules: risk first, then value per effort | Two runs a week apart give the same answer for the same state |
| Output | A fixed template | People learn to read it quickly; changes stand out |
| Never | Never edit the register; never create a roadmap item; never query | **Reading and editing are separate skills**, so a ranking never quietly changes what it ranks |

**When to write one:** the second time you explain the same task to the agent. Copy what you
typed, turn it into the sections above, and the third time costs one line.

---

## 7. Closing out a change

The handout's tiers say what a change owes. Here is the close-out as a checklist the agent can
follow:

1. **Pick the tier.** Any single tier-three trigger (new source, secrets, access, student data, a
   change to the rules themselves) makes the whole change tier three.
2. **Fix what is now false.** Search the README for the thing you changed.
3. **Decision entry if it could be undone.** Allocate the id now, last, with `--next`.
4. **Sweep the neighbors.** Search the roadmap, register and log for the ids your change touches.
   Look for items that named yours as a blocker, status cells listing a step you just did, and
   risks your change moved. Work completed *indirectly*, and work whose last step is a person's
   action (a permission granted, a schedule switched on), is what goes stale, because nothing else
   will ever write it back.
5. **Mark what waits on a person.** If the next step is someone's action, write it as a marker
   (`WAITING ON <role> since <date>: <what>`) at the end of the status cell, where a skill or a
   script can find it.
6. **New ideas go to the parking lot,** not the roadmap.

---

## 8. Several agents at once

Running two or three agent sessions in parallel (one per branch) is where documentation pays most
and breaks most.

- **Anything numbered breaks first.** Decision ids, roadmap ids and migration numbers are all
  "next free number" problems. Allocate late, check against the main branch, and let a check catch
  what slips through.
- **One session, one branch, one pull request.** Two sessions on one branch overwrite each other's
  reasoning as well as each other's files.
- **Merge the main branch before waiting on checks.** Some CI systems run nothing on a pull request
  with a merge conflict. A session waiting for checks on a conflicted branch waits forever.
- **Batch review fixes.** Every push reruns the checks and any automated reviewer. Answer a whole
  review round in one push.

---

## 9. dbt and BigQuery traps we hit

Each of these failed a production build after review and CI had passed. They are generic, so you
can copy them into your own rules file if they apply.

- **`--` inside a Jinja tag is not a comment.** Anywhere between `{%` and `%}` it is a parse error.
  Use `{# … #}`, or put the comment on the line above.
- **And a Jinja tag inside a SQL comment is still a Jinja tag.** Jinja renders before SQL comments
  mean anything, so a tag written out in a comment runs. Name tags in prose instead.
- **A `ref()` used only inside `{% if execute %}` is invisible to dbt's dependency graph.** Add
  `-- depends_on: {{ ref('model') }}` near the top of the file.
- **`get_columns_in_relation` returns an empty list at parse time.** A loop over it is harmless; an
  assertion over it fails the whole build. Wrap only the assertion in `{% if execute %}`.
- **A new column on a model that another model `select *`s beside another `select *` can collide.**
  BigQuery raises "duplicate column name" at build time, not in review. Search for star-expansions
  downstream before you add a column.
- **With `persist_docs` on, BigQuery rejects a column description over 1,024 characters**, after
  the table is built, which fails the run. Keep descriptions short and put reasoning in the decision
  log.
- **External tables take their column types from whoever last ran the DDL.** Cast join keys
  explicitly in staging, even ones that are numbers today.
- **`rows` is a reserved word in BigQuery.** Alias counts as something else.
