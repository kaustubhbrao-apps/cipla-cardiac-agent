# Cipla Cardiac Opportunity Agent — web

Team JK · XLRI Jamshedpur · Cipla Ascend Season 4

An interactive prioritisation model for Cipla's Indian cardiac portfolio, plus a
question-answering agent grounded in the case dataset.

## What is deployed, and what is not

**The licensed IQVIA/PharmaTrac workbook is not in this repository and is never
deployed.** It stays on the team's machine. `build/` reads it locally and emits
aggregated archetype- and molecule-level results into `public/data/`; only those
aggregates ship. There are no SKU rows anywhere in this repo.

## Layout

    public/
      index.html          the agent — ask a question
      dashboard.html      the model — move the parameters, the ranking re-derives
      theme.css           shared design tokens (WCAG-checked, light and dark)
      data/model.json     archetype aggregates, all six lock variants   (21 KB)
      data/tools.json     precomputed tool responses + system prompt    (69 KB)
      data/kb.json        50 knowledge-base entries                     (66 KB)
      data/map.json       opportunity map for the landing page
      data/status.json    header counters
    api/ask.py            the only server-side code: holds the API key
    build/                run locally, where the workbook lives

## The master context document

`MASTER_CONTEXT.md` is the single source of truth for the analysis — every slide's
content, the annexures, the speaking notes and the Q&A cards. The PPT is built
from it; nothing is written directly into slides.

Every load-bearing figure in it is recomputed from the dataset by:

    python3 build/verify_deck.py     # 112 checks, exits non-zero on any mismatch

Run this after changing any number. It has already caught two live errors: a
stale growth-decomposition figure, and a conversion median misread off a sorted
list. Tolerances carry no floor — ratios are checked on absolute bands, because
a relative floor is wider than the errors that actually occur.

## Rebuilding the data

Requires the case folder alongside this one (`../cipla`), with the workbook in it.

    python3 build/build_data.py     # model.json, map.json, status.json
    python3 build/build_tools.py    # tools.json (every tool response + prompt)
    python3 build/export_kb.py      # kb.json

Set `CIPLA_CASE_DIR` if the case folder is elsewhere.

## Environment variables (set in Vercel, never committed)

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | The reasoning layer. Without it `/api/ask` returns 503 and the rest of the site still works. |
| `ASK_PASSWORD` | Shared phrase gating `/api/ask`. **Set this** — without it, anyone who finds the URL can spend your API quota. |

## Why the deployed agent is narrower than the local one

Locally the agent runs a multi-turn tool loop: it chooses a tool, reads the
result, and decides what to ask next. `/api/ask` does retrieval-then-answer in a
single round trip instead, because serverless functions time out and a stalled
loop is worse than a narrower one. The grounding rules are identical — the model
may not state a figure that is not in the evidence it was handed — but the local
agent is the one to demo.
