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
    if any(w in ql for w in ("wrong", "sensitiv", "robust", "assumption")):
        out["run_sensitivity"] = t["run_sensitivity"]
    if any(w in ql for w in ("signal", "guideline", "regulat", "external", "cdsco", "nlem")):
        out["external_signals"] = t["external_signals"]
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
not there, you do not have it, and you say so. Keep the answer tight: a judge is
listening, not reading.

EVIDENCE — computed tool responses (reproducible from the dataset):
%s

EVIDENCE — knowledge base entries (kind=team is our analysis; kind=public is
cited external evidence; an entry marked retracted:true must have its correction
stated FIRST):
%s

QUESTION: %s"""


def gemini(prompt, key):
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-2.0-flash:generateContent?key=" + key)
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0.2, "maxOutputTokens": 900}}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        d = json.loads(r.read())
    return d["candidates"][0]["content"]["parts"][0]["text"]


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

        tools, kb = pick_tools(q), kb_search(q)
        prompt = PROMPT % (load("tools.json")["system"],
                           json.dumps(tools, separators=(",", ":"))[:60000],
                           json.dumps(kb, separators=(",", ":"))[:40000], q)
        try:
            answer = gemini(prompt, key)
        except Exception as e:
            return self._send(502, {"error": "The model did not respond (%s). "
                                             "Try again, or run the agent locally." % type(e).__name__})

        self._send(200, {"answer": answer,
                         "grounded": sorted(tools.keys()),
                         "entries": [e["entry_id"] for e in kb]})

    def do_GET(self):
        self._send(405, {"error": "POST a JSON body: {\"q\": \"...\"}"})
