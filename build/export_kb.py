#!/usr/bin/env python3
"""
Export the knowledge base to JSON for seeding Supabase.

The KB is our own analysis and cited public evidence — no licensed SKU data —
so it is safe to store remotely. Each row keeps its provenance (`kind`) and a
`retracted` flag, because the agent's hard rules require a retraction to be
stated before the entry is used for anything else.

    python3 build/export_kb.py     ->  build/kb.json
"""
import json, os, sys

CASE = os.environ.get("CIPLA_CASE_DIR", "../cipla")
sys.path.insert(0, CASE)
import cipla_knowledge as K
import cipla_external as X

HERE = os.path.dirname(os.path.abspath(__file__))

RETRACTION_MARKERS = ("RETRACTION", "CORRECTION", "That is wrong")


def rows():
    out = []
    for e in K.KB:
        out.append(dict(entry_id=e["id"], kind="team", title=e["title"], tags=e["tags"],
                        body=e["body"], source=e["src"],
                        retracted=any(m in e["body"] for m in RETRACTION_MARKERS)))
    for i, e in enumerate(X.EXTERNAL):
        out.append(dict(entry_id=e.get("id", "public-%02d" % i), kind="public",
                        title=e["title"], tags=e["tags"], body=e["body"],
                        source=e["src"],
                        retracted=any(m in e["body"] for m in RETRACTION_MARKERS)))
    return out


if __name__ == "__main__":
    r = rows()
    path = os.path.join(HERE, "kb.json")
    with open(path, "w") as fh:
        json.dump(r, fh, indent=1)
    team = sum(1 for x in r if x["kind"] == "team")
    print("wrote %s — %d entries (%d team, %d public), %d carrying retractions"
          % (path, len(r), team, len(r) - team, sum(x["retracted"] for x in r)))
