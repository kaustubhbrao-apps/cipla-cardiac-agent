#!/usr/bin/env python3
"""
Turn the licensed case workbook into the aggregated JSON the web app ships.

Run this LOCALLY, where the workbook lives. It writes only archetype- and
molecule-level aggregates into public/data/ — never SKU rows — so the deployed
app never touches, and the repo never contains, the licensed dataset.

    python3 build/build_data.py

Everything downstream of these aggregates is arithmetic, so neither the browser
nor the serverless function needs pandas.
"""
import json, os, sys, numpy as np, pandas as pd

CASE = os.environ.get("CIPLA_CASE_DIR", "../cipla")
sys.path.insert(0, CASE)
os.chdir(CASE)                       # the agent resolves the workbook relative to cwd

from cipla_cardiac_agent import (CardiacAgent, SIGNALS, ARCH_LABEL, CIPLA, cagr,
                                 M24, M26, Q24, Q26)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.normpath(os.path.join(HERE, "..", "public", "data"))
LOCKS  = [0.50, 0.60, 0.70, 0.80, 0.90, 1.01]
FIELDS = ["space", "m26", "value", "real", "volume", "mix", "price", "momentum",
          "hhi", "leader", "top3", "n_co", "cip", "cip_sh", "cip_vol", "n_mol",
          "n_cbrand", "shmom", "signal", "P_attract", "P_future", "P_compete", "P_fit"]


def jnum(x):
    if x is None:
        return None
    try:
        f = float(x)
        return None if (np.isnan(f) or np.isinf(f)) else round(f, 4)
    except Exception:
        return None


def main():
    base = CardiacAgent()
    meta = dict(
        market=jnum(base.mkt), cagr=jnum(base.mkt_cagr), vol=jnum(base.mkt_vol),
        mix=jnum(base.mkt_real - base.mkt_vol), price=jnum(base.mkt_cagr - base.mkt_real),
        cipla=jnum(base.cip), ciplaShare=jnum(base.cip / base.mkt * 100),
        rank=int(base.df.groupby("COMPANY")[M26].sum().rank(ascending=False)[CIPLA]),
        nCompanies=int(base.df["COMPANY"].nunique()),
        nSkus=int(len(base.df)),
        nMolecules=int(base.df["MOLECULE_DESC"].nunique()),
        nBrands=int(base.df["BRANDS"].nunique()),
    )

    # Pillar scores are percentile ranks against the peer set, so they change
    # with the lock threshold and cannot be recomputed in the browser. Every
    # lock variant is precomputed; the sliders interpolate nothing.
    locks = {}
    for lk in LOCKS:
        ag = CardiacAgent(dict(lock=lk))
        g = ag.analyse()
        rows = []
        for _, r in g.iterrows():
            row = {f: (r[f] if f == "space" else jnum(r.get(f))) for f in FIELDS}
            row["key"] = r["space"][:2]
            rows.append(row)
        locked = ag.df.loc[~ag.df["addressable"], M26].sum()
        locks["%.2f" % lk] = dict(spaces=rows, locked=jnum(locked),
                                  lockedPct=jnum(locked / ag.df[M26].sum() * 100))

    # Per-archetype competitor and molecule detail for the workbench's row
    # drill-down. It reads DATA.comp[key] / DATA.mols[key]; without these the
    # panel threw on the first row click and took the whole render with it.
    # Computed at the base lock only — the drill-down is a description of the
    # pool, not a scored quantity, so it does not vary with the sliders.
    comp, mols = {}, {}
    for key in sorted({s[:2] for s in base.analyse()["space"]}):
        sub = base.df[(base.df["ARCH"] == key) & base.df["addressable"]]
        if not len(sub):
            continue
        tot = sub[M26].sum()
        tv = float(cagr([tot], [sub[M24].sum()])[0])
        co = sub.groupby("COMPANY").agg(m24=(M24, "sum"), m26=(M26, "sum"),
                                        q24=(Q24, "sum"), q26=(Q26, "sum"),
                                        mo=("MOLECULE_DESC", "nunique")).reset_index()
        co["sh"] = co["m26"] / tot * 100
        co["cg"] = cagr(co["m26"], co["m24"])
        co["vol"] = cagr(co["q26"], co["q24"])
        co["mom"] = co["cg"] - tv
        tb = sub.groupby(["COMPANY", "BRANDS"])[M26].sum().reset_index()
        dep = (tb.sort_values(M26, ascending=False).groupby("COMPANY").first()[M26]
               / tb.groupby("COMPANY")[M26].sum() * 100)
        co["dep"] = co["COMPANY"].map(dep)
        top = co.nlargest(6, "m26")
        if CIPLA in co["COMPANY"].values and CIPLA not in top["COMPANY"].values:
            top = pd.concat([top, co[co["COMPANY"] == CIPLA]])
        comp[key] = [dict(name=str(x["COMPANY"])[:22], sh=jnum(x["sh"]),
                          mom=jnum(x["mom"]), vol=jnum(x["vol"]), mo=int(x["mo"]),
                          dep=jnum(x["dep"]), isCipla=bool(x["COMPANY"] == CIPLA))
                     for _, x in top.iterrows()]
        mm = sub.groupby("MOLECULE_DESC").agg(v=(M26, "sum"), o=(M24, "sum")).nlargest(6, "v")
        mols[key] = [dict(name=str(n)[:44], v=jnum(x["v"]),
                          cagr=jnum(float(cagr([x["v"]], [x["o"]])[0])),
                          cip=jnum(sub[(sub["MOLECULE_DESC"] == n) &
                                       (sub["COMPANY"] == CIPLA)][M26].sum()
                                   / x["v"] * 100 if x["v"] else 0))
                     for n, x in mm.iterrows()]

    data = dict(meta=meta, locks=locks, labels=ARCH_LABEL, comp=comp, mols=mols,
                # `pat` is the regex that decides which archetypes a signal
                # applies to — it is the audit trail, so it has to ship. An
                # earlier version exported `space`, a key SIGNALS never had,
                # so every entry rendered as "applies to /undefined/".
                signals=[dict(name=s.get("name"), pat=s.get("pat"),
                              delta=s.get("delta"), src=s.get("src")) for s in SIGNALS]
                        if isinstance(SIGNALS, list) else SIGNALS,
                generated="MAT Feb'24 - Feb'26 case dataset; aggregates only")

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "model.json")
    with open(path, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))

    # The landing page's opportunity map and status strip are pure functions of
    # the base case, so they ship as static JSON rather than as extra serverless
    # functions. Only /api/ask genuinely needs a server (it holds the API key).
    g = base.analyse()
    amap = [dict(key=r["space"][:2], name=ARCH_LABEL[r["space"][:2]],
                 pool=round(r["m26"]), cagr=round(r["value"], 1),
                 volume=round(r["volume"], 1), leader=round(r["leader"], 1),
                 cipla=round(r["cip_sh"], 2), prize=round(r["prize"]),
                 prize_exact=round(r["prize"], 2), call=r["call"])
            for _, r in g.iterrows()]
    with open(os.path.join(OUT, "map.json"), "w") as fh:
        json.dump(amap, fh, separators=(",", ":"))

    status = dict(live=True, model="gemini-3.7-flash", n_tools=12,
                  skus=meta["nSkus"], market=round(base.mkt),
                  cipla=round(base.cip), cipla_share=round(base.cip / base.mkt * 100, 2))
    with open(os.path.join(OUT, "status.json"), "w") as fh:
        json.dump(status, fh, separators=(",", ":"))
    kb = os.path.getsize(path) / 1024
    print("wrote %s  (%.0f KB, %d lock variants, %d archetypes, 0 SKU rows)"
          % (path, kb, len(locks), len(locks["0.70"]["spaces"])))


if __name__ == "__main__":
    main()
