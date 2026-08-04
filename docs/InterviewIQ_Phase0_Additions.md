# InterviewIQ — Phase 1 Additions

Two fixes carried over from Phase 0 review: the missing resume link on interviews, and a proper design for sandboxed code execution.

---

## 1. Revised Database Schema

### Interviews Table (updated)

| Field Name   | Data Type            | Notes |
|--------------|-----------------------|-------|
| id           | UUID (Primary Key)   | |
| user_id      | UUID (Foreign Key)   | references Users(id) |
| resume_id    | UUID (Foreign Key)   | **new** — references Resumes(id) |
| role         | VARCHAR              | |
| difficulty   | VARCHAR              | |
| created_at   | TIMESTAMP            | |

**Why this matters:** your own flow says questions are generated *from* a specific resume. Without `resume_id`, you can't answer "why did the AI ask this question" or regenerate/audit a session later, and if a user uploads a new resume version, old interviews silently lose their source-of-truth link.

**Relationship added:**
`Resume (1) → Interview (N)` — one resume can be the basis for multiple interviews (different roles/difficulty), one interview always traces back to exactly one resume version.

### Small related additions worth making now while you're in the schema

- **Users table:** add `reset_token` and `reset_token_expires` (nullable) to support forgot-password, or a separate `password_resets` table if you'd rather keep Users clean. Separate table is cleaner — recommend that.
- **Coding_Assessments table:** add `status` (`pending | running | completed | failed | timeout`) and `execution_time_ms` — you'll need these once real code execution is involved (see below).

```
password_resets
----------------
id            UUID (PK)
user_id       UUID (FK -> Users.id)
token_hash    VARCHAR
expires_at    TIMESTAMP
used          BOOLEAN default false
created_at    TIMESTAMP
```

Store a hash of the token, not the raw token — same principle as password_hash.

---

## 2. Sandboxed Code Execution Design

This is the highest-risk component in the whole system: you're running arbitrary, user-submitted code on your server. Treat it as its own subsystem, not a line item inside the Coding Assessment module.

### Threat model (what you're defending against)

- **Malicious code** — reading env vars, hitting internal network, deleting files, spawning processes
- **Resource exhaustion** — infinite loops, fork bombs, memory bombs, huge output (`print("x"*10**9)`)
- **Data exfiltration** — trying to reach the internet or your DB from inside the sandbox
- **Timing/DoS** — many submissions at once starving the host

### Design: Isolated execution service

Do **not** run submitted code inside your FastAPI process or its container. Split it into its own service.

```
Coding API (FastAPI)
     │
     ▼
Execution Queue (Redis / simple job table)
     │
     ▼
Execution Worker
     │
     ▼
Ephemeral Docker Container (per submission)
     │
     ▼
Result written back → Coding_Assessments row
```

**Flow:**
1. User submits code → API validates language/size, writes a `pending` row, pushes a job to the queue.
2. A worker process picks up the job and spins up a **fresh, single-use Docker container** for that submission only.
3. Container runs with hard limits (below), executes against the test cases, captures stdout/stderr/exit code.
4. Container is destroyed immediately after — never reused across submissions.
5. Worker writes score/feedback back to Postgres; API polls or the frontend gets notified.

### Container hardening (non-negotiable, in order of importance)

| Control | Setting | Why |
|---|---|---|
| Network | `--network none` | No exfiltration, no calling out |
| Memory | `--memory 256m` (tune per language) | Kills memory bombs |
| CPU | `--cpus 0.5` | Prevents one submission starving others |
| Time | wall-clock timeout, e.g. 10s, enforced *outside* the container (worker kills it) | Kills infinite loops |
| Filesystem | read-only root, tmpfs for scratch, no volume mounts to host | No file tampering, no reading host files |
| User | run as non-root unprivileged user inside container | Limits blast radius of a container escape |
| Process limit | `--pids-limit 64` | Kills fork bombs |
| Output size | cap captured stdout/stderr (e.g. 100KB), truncate beyond that | Kills output-flood DoS |
| Image | minimal, language-specific base image, rebuilt regularly, no unnecessary tools (no curl, no compilers beyond what's needed) | Smaller attack surface |

### Why not just `exec()` / `subprocess` in-process

It's tempting to just run submitted Python with `subprocess.run()` inside your FastAPI backend. Don't — that gives submitted code the same privileges, filesystem access, and network reachability as your entire application, including access to `GEMINI_API_KEY` and `DATABASE_URL` from the environment. One container per submission with no network and read-only FS is the actual isolation boundary.

### Updated Coding_Assessments status flow

```
submitted → pending → running → completed
                              → failed (runtime error)
                              → timeout (exceeded wall clock)
```

Store `status`, `execution_time_ms`, and truncated stdout/stderr per test case so the frontend can show *why* a submission failed, not just a score.

### Practical note for a student project timeline

Full custom sandboxing (Docker-per-submission + queue + worker) is real infra work. If timeline is tight, a reasonable fallback for MVP is a hosted code-execution API (e.g. Judge0, Piston) that already implements this isolation, and swap to self-hosted Docker workers later if you want the "built it myself" story for your report. Worth deciding now since it affects Module 8's folder structure (a `coding_execution_service.py` that either calls Judge0's API or talks to your own worker queue).

---

## Suggested Phase 1 order

1. Apply schema fix (`resume_id` on Interviews, `password_resets` table)
2. Decide: self-hosted sandbox vs. Judge0/Piston for coding execution
3. Build Auth (including reset flow) + Resume Upload — these unblock everything else
4. Then Interview Generation, since it now correctly depends on a stored resume
