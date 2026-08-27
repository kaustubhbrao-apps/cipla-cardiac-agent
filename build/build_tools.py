#!/usr/bin/env python3
"""
Precompute every tool response into one JSON bundle.

The dataset is static (MAT Feb'26), so there is no reason to run pandas at
request time. This bakes each tool's output locally; the serverless function
then answers by lookup plus light arithmetic, needs no scientific stack, and
never sees the licensed workbook.

    python3 build/build_tools.py   ->  public/data/tools.json
"""
import json, os, sys

CASE = os.environ.get("CIPLA_CASE_DIR", "../cipla")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.normpath(os.path.join(HERE, "..", "public", "data"))
sys.path.insert(0, os.path.abspath(CASE))
os.chdir(CASE)

import cipla_ai_agent as A

SPACES = ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]


def j(s):
    return json.loads(s)


def main():
    bundle = {
        "market_overview":   j(A.t_market_overview()),
        "rank_opportunities": j(A.t_rank_opportunities()),
        "decompose_growth":  j(A.t_decompose_growth()),
        "project_forward":   j(A.t_project_forward()),
        "run_sensitivity":   j(A.t_run_sensitivity()),
        "external_signals":  j(A.t_external_signals()),
        "brand_profile":     j(A.t_brand_profile("")),
        "analyze_space":     {k: j(A.t_analyze_space(k)) for k in SPACES},
        "competitor_profile": {k: j(A.t_competitor_profile(k)) for k in SPACES},
    }

    # search_molecules takes a free pattern, so ship the molecule table and let
    # the function filter it. Cardiac only, aggregated — no SKU rows.
    eng = A.ENGINE if hasattr(A, "ENGINE") else None
    if eng is not None:
        d = eng.df
        V26, V24 = "MAT FEB'26", "MAT FEB'24"
        rows = []
        for mol, g in d.groupby("MOLECULE_DESC"):
            cip = g[g["COMPANY"] == A.CIPLA][V26].sum() if hasattr(A, "CIPLA") else 0.0
            tot = float(g[V26].sum())
            if tot < 1.0:
                continue
            lead = g.groupby("COMPANY")[V26].sum()
            rows.append(dict(
                molecule=mol, arch=str(g["ARCH"].mode()[0]) if len(g["ARCH"].mode()) else "",
                cr=round(tot, 2), cr24=round(float(g[V24].sum()), 2),
                cipla_cr=round(float(cip), 2),
                cipla_pct=round(float(cip) / tot * 100, 2) if tot else 0.0,
                leader=str(lead.idxmax()), leader_pct=round(float(lead.max()) / tot * 100, 1),
                n_co=int(g["COMPANY"].nunique())))
        rows.sort(key=lambda r: -r["cr"])
        bundle["molecules"] = rows

    # the agent's system prompt travels with the bundle so the deployed
    # function enforces exactly the same grounding and hard rules as local
    bundle["system"] = A.SYSTEM

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "tools.json")
    with open(path, "w") as fh:
        json.dump(bundle, fh, separators=(",", ":"))
    print("wrote %s (%.0f KB) — %d tool responses, %d molecules"
          % (path, os.path.getsize(path) / 1024,
             len(bundle) - 1, len(bundle.get("molecules", []))))


if __name__ == "__main__":
    main()
