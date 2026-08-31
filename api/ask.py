"""
/api/ask — the one piece that genuinely needs a server, because it holds the
model API key.

Design note: locally the agent runs a multi-turn tool loop. Here it does
retrieval-then-answer in a single round trip — the question is routed to the
relevant precomputed tool responses, those are supplied as the only permitted
evidence, and the model writes the answer. One call instead of a loop, because
serverless functions time out and a stalled loop is worse than a narrower one.
Grounding is unchanged: the model still may not state a figure that is not in
the context it was handed.
"""
import json, os, re, urllib.request
from http.server import BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))

# Vercel serves public/ from the CDN but does not bundle it into the function,
# so public/data is unreadable at runtime (/var/task/public/... does not exist).
# Files beside the function ARE bundled, so api/_data is the deployed copy;
# public/data is the fallback for running this handler locally.
_CANDIDATES = [os.path.join(HERE, "_data"),
               os.path.normpath(os.path.join(HERE, "..", "public", "data"))]
DATA = next((p for p in _CANDIDATES if os.path.isdir(p)), _CANDIDATES[0])

_cache = {}


def load(name):
    if name not in _cache:
        with open(os.path.join(DATA, name), encoding="utf-8") as fh:
            _cache[name] = json.load(fh)
    return _cache[name]


# ── scope guard: mirrors t_lookup_context in cipla_ai_agent.py ───────────────
OUT_OF_SCOPE = {
    "another therapy area": ("oncology", "cancer", "respiratory", "inhaler", "copd", "asthma",
                             "hiv", "antiretroviral", "urology", "cns", "neuro", "dermatology",
                             "antibiotic", "vaccine", "fertility"),
    "another geography": (r"\bu\.?s\.?\s+(market|business|generics|sales|revenue|portfolio)\b",
                          "usa", "america", "europe", "africa", "china", "export", "overseas"),
    "another business": ("diagnostics", "consumer health", "biosimilar", "medical devices"),
    "outside the case dataset": ("sglt2", "arni", "sacubitril", "anticoagulant",
                                 "apixaban", "rivaroxaban", "warfarin"),
}


def out_of_scope(q):
    ql = " " + q.lower() + " "
    for reason, terms in OUT_OF_SCOPE.items():
        for t in terms:
            if (re.search(t, ql) if t.startswith("\\") else t in ql):
                return reason
    return None


def kb_search(q, limit=4):
    words = {w for w in re.sub(r"[^a-z0-9]+", " ", q.lower()).split()
             if len(w) > 2 or re.fullmatch(r"a\d", w)}
    if not words:
        return []
    scored = []
    for e in load("kb.json"):
        tags = set(e["tags"].split())
        sc = 3 * len(words & tags)
        sc += sum(1 for w in words if w in e["title"].lower())
        sc += sum(0.4 for w in words if w in e["body"].lower())
        if sc >= 2.0:
            scored.append((sc, e))
    scored.sort(key=lambda x: -x[0])
    return [e for _, e in scored[:limit]]


def pick_tools(q):
    """Rule-based routing — the same intent map the local planner uses."""
    t, ql, out = load("tools.json"), q.lower(), {}
    out["rank_opportunities"] = t["rank_opportunities"]
    for key in re.findall(r"\ba([1-9])\b", ql):
        k = "A" + key
        if k in t["analyze_space"]:
            out.setdefault("analyze_space", {})[k] = t["analyze_space"][k]
            out.setdefault("competitor_profile", {})[k] = t["competitor_profile"][k]
    if any(w in ql for w in ("grow", "volume", "mix", "price", "durable")):
        out["decompose_growth"] = t["decompose_growth"]
    if any(w in ql for w in ("future", "project", "3-5", "five year", "outperform")):
        out["project_forward"] = t["project_forward"]
    # The prize question must never come back as the ceiling alone, so the
    # ladder rides along with anything asking how big, how long or how sure.
    if any(w in ql for w in ("prize", "headroom", "5-year", "5 year", "five year",
                             "yr 5", "year 5", "how much", "how big", "upside",
                             "underwrit", "commit", "conservat", "floor", "ceiling",
                             "nothing", "baseline", "worst case", "downside",
                             "book", "target", "ladder", "cannibal", "201",
                             "tier", "reserve", "realistic", "deliver", "promise",
                             # the four-verb strategy question quotes a build
                             # figure, so it must quote the committed one
                             "double down", "build capabilit", "selective", "avoid")):
        out["underwrite"] = t["underwrite"]
    if any(w in ql for w in ("wrong", "sensitiv", "robust", "assumption")):
        out["run_sensitivity"] = t["run_sensitivity"]
    if any(w in ql for w in ("signal", "guideline", "regulat", "external", "cdsco", "nlem")):
        out["external_signals"] = t["external_signals"]
    # a "what's the answer" question needs the whole picture, not one archetype
    if any(w in ql for w in ("recommend", "final", "solution", "summar", "overall",
                             "bottom line", "conclusion", "what should cipla", "the plan")):
        out["decompose_growth"] = t["decompose_growth"]
        out["project_forward"] = t["project_forward"]
        out["underwrite"] = t["underwrite"]
    if any(w in ql for w in ("brand", "cresar", "rosulip", "amlopres", "metolar", "atorlip")):
        out["brand_profile"] = t["brand_profile"]
    if any(w in ql for w in ("molecule", "telmisartan", "statin", "rosuva", "atorva", "amlodipine")):
        pat = [w for w in re.sub(r"[^a-z]+", " ", ql).split() if len(w) > 5]
        mols = [m for m in t.get("molecules", [])
                if any(p.upper() in m["molecule"] for p in pat)][:15]
        if mols:
            out["molecules"] = mols
    return out


PROMPT = """%s

You are answering ONE question in a single pass. The EVIDENCE below is the only
material you may use. Every figure must appear in it verbatim — if a number is
not there, you do not have it, and you say so.

LENGTH: aim for 120-200 words. Lead with the answer in one sentence, then the
evidence for it. Finish the thought — a complete short answer always beats a
detailed one that stops mid-sentence. No preamble, no restating the question.

VOICE: never build a sentence on the "not X, but Y" seesaw. It is the clearest
tell that a machine wrote the answer, and it is banned in every variant — "not
because the pool is large, but because it is contestable" / "Cipla does not drop
A8, our strategy converts it" / "it is not a harvest, it is a leak" / "this is
not a portfolio problem, it is a push problem" / "the question is not whether
Cipla can, but whether it will" / "less about price, more about detailing" /
"price is not the issue, coverage is". Each of those walks the reader past a
false statement to reach a true one. State the true one on its own and attach
its reason: "A7 is contestable. The leader holds 10.3%%." · "Cipla keeps A8 and
converts its patients into A7." · "A8 leaks 4.3%% of its units a year, so it
funds the plan." Open on the claim, never on the correction. Where the question
carries a premise that is wrong, the FIRST sentence still says what is the case
— "Cipla keeps A8 and converts its patients into A7" — and any explicit
correction follows in its own sentence. "Cipla does not drop A8. Our strategy
converts it" still fails this rule: it spends the opening sentence on the denial.
A direct "no" to a yes-or-no question is the one exception, with the positive
statement as its own sentence after it.

THE PRIZE: when the underwrite tool is in the evidence, the headroom figure in
rank_opportunities is the STRUCTURAL CEILING and is never the answer on its own.
Give the whole ladder in one line, in this order and using that tool's own
numbers: do-nothing, floor, plan, reserve, ceiling. Name the PLAN tier as what
the team commits to, with its incremental figure. Then close on the tool's
headline_line verbatim. Never quote a ladder number that the underwrite tool
does not state.

ATTRIBUTION: say where a fact came from in plain English — "from the dataset",
"our own analysis", or name the published source for external evidence. Never
print the internal field names of the evidence: no entry_id, no kind="team", no
JSON keys, no backticked slugs. A judge is reading the answer, not the
plumbing.

CONVERSATION SO FAR (earlier turns in this thread; the question below may lean
on them for its subject, so read pronouns and words like "it", "that one" and
"why" against this. The evidence rules apply unchanged: a figure you stated
earlier still has to appear in the EVIDENCE below to be repeated):
%s

EVIDENCE — computed tool responses (reproducible from the dataset):
%s

EVIDENCE — knowledge base entries (kind=team is our analysis; kind=public is
cited external evidence; an entry marked retracted:true must have its correction
stated FIRST):
%s

QUESTION: %s"""

# This template is filled with %-formatting, so a literal percent sign in the
# prose becomes an invalid format spec and every question returns a 500. That
# is exactly how it broke once: a VOICE example quoting "10.3%" took the whole
# endpoint down, and nothing caught it until a live request did. Render it with
# dummies at import, so a stray percent fails here and in the build instead of
# in front of a judge. Literal percents belong in the template as %%.
try:
    PROMPT % ("", "", "", "", "")
except (TypeError, ValueError) as _err:
    raise RuntimeError("PROMPT is malformed; escape any literal percent sign as "
                       "a double percent. Formatting error: %s" % _err)


def format_history(raw):
    """Normalise the client's thread into a compact transcript.

    Untrusted input: it arrives in the POST body, so the shape, the count and
    the length of every field are all capped here rather than trusted. Six
    turns is roughly the depth a judge's follow-ups reach before the subject
    changes, and it keeps the prompt inside the token budget.
    """
    first = "(this is the first question in the thread)"
    if not isinstance(raw, list):
        return first, []
    turns = []
    for item in raw[-6:]:
        if not isinstance(item, dict):
            continue
        q = str(item.get("q") or "").strip()[:500]
        a = str(item.get("a") or "").strip()[:1200]
        if q and a:
            turns.append((q, a))
    if not turns:
        return first, []
    return "\n\n".join("Q: %s\nA: %s" % (q, a) for q, a in turns), turns


# Same fallback chain the local agent uses: model availability on a given key
# changes over time, so try in order rather than pinning one name.
GEMINI_MODELS = ["gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash",
                 "gemini-flash-latest", "gemini-3.1-flash-lite", "gemini-2.5-flash"]


def gemini(prompt, key):
    # 900 was far too tight: the 3.x flash models spend tokens on reasoning
    # before they emit anything, so the visible answer was being cut off
    # mid-sentence. Budget generously and let the prompt enforce brevity.
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0.2,
                                            "maxOutputTokens": 4000}}).encode()
    problems = []
    for model in GEMINI_MODELS:
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               "%s:generateContent?key=%s" % (model, key))
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=50) as r:
                d = json.loads(r.read())
            cand = d["candidates"][0]
            parts = cand.get("content", {}).get("parts") or []
            text = "".join(p.get("text", "") for p in parts).strip()
            if not text:
                # thinking consumed the whole budget and nothing was emitted
                problems.append("%s: empty (%s)" % (model, cand.get("finishReason")))
                continue
            if cand.get("finishReason") == "MAX_TOKENS":
                text += ("\n\n_(cut off at the length limit — ask a narrower "
                         "question, or run the agent locally for the full answer.)_")
            return text, model
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = json.loads(e.read()).get("error", {}).get("message", "")[:200]
            except Exception:
                pass
            problems.append("%s: HTTP %s %s" % (model, e.code, detail))
            # 400/404 mean this model name is wrong for this key — try the next.
            # 401/403 mean the key itself is bad, so stop rather than loop.
            if e.code in (401, 403):
                break
        except Exception as e:
            problems.append("%s: %s" % (model, type(e).__name__))
    raise RuntimeError(" | ".join(problems))


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        b = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            req = json.loads(self.rfile.read(n) or "{}")
        except Exception:
            return self._send(400, {"error": "Send JSON: {\"q\": \"your question\"}"})

        gate = os.environ.get("ASK_PASSWORD")
        if gate and req.get("password") != gate:
            return self._send(401, {"error": "This agent is password-protected. "
                                             "Ask the team for the access phrase."})

        q = (req.get("q") or "").strip()
        if not q:
            return self._send(400, {"error": "No question supplied."})
        if len(q) > 500:
            return self._send(400, {"error": "Question too long — keep it under 500 characters."})

        reason = out_of_scope(q)
        if reason:
            return self._send(200, {"answer":
                "That is about %s. This analysis covers Indian cardiac only — anti-hypertensives, "
                "lipid regulators and anti-angina — so it is outside what the dataset can answer, "
                "and I will not reason by analogy from cardiac to get there." % reason,
                "grounded": [], "scope": reason})

        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            return self._send(503, {"error": "The reasoning layer is not configured on this "
                                             "deployment. Set GEMINI_API_KEY."})

        transcript, turns = format_history(req.get("history"))

        # Route on the question PLUS the previous question. A follow-up like
        # "why?" or "and A1?" carries no routing terms of its own, so retrieval
        # against it alone returns the wrong evidence and the thread loses its
        # subject at the second turn. The answer text is deliberately left out
        # of the routing string: it is long, and it would drag in every tool
        # the previous turn happened to mention.
        route_q = (turns[-1][0] + " " + q) if turns else q

        tools, kb = pick_tools(route_q), kb_search(route_q)
        prompt = PROMPT % (load("tools.json")["system"], transcript,
                           json.dumps(tools, separators=(",", ":"))[:60000],
                           json.dumps(kb, separators=(",", ":"))[:40000], q)
        try:
            answer, model = gemini(prompt, key)
        except Exception as e:
            # surface what actually failed — a silent 502 is undebuggable, and
            # the message never contains the key
            return self._send(502, {"error": "No Gemini model answered.",
                                    "detail": str(e)[:500]})

        self._send(200, {"answer": answer, "model": model,
                         "grounded": sorted(tools.keys()),
                         "entries": [e["entry_id"] for e in kb],
                         "turn": len(turns) + 1})

    def do_GET(self):
        self._send(405, {"error": "POST a JSON body: {\"q\": \"...\"}"})
