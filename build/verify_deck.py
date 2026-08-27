#!/usr/bin/env python3
"""
Recompute every load-bearing figure in Finale_Deck_Content.md from the dataset.

The deck is the master context document, so a stale number in it propagates into
the PPT, the knowledge base and the agent's mouth. This asserts each claim
against a fresh computation and prints what does not match.

    python3 verify_deck.py
"""
import sys, re, io, json
import numpy as np
sys.path.insert(0, ".")
from cipla_cardiac_agent import (CardiacAgent, CIPLA, M24, M25, M26, Q24, Q26)

Q25 = "QTY MAT FEB'25"
DECK = io.open("Finale_Deck_Content.md", encoding="utf-8").read()

A = CardiacAgent(); D = A.df; G = A.analyse()
SP = {r["space"][:2]: r for _, r in G.iterrows()}

FAILS, CHECKS = [], 0


def ck(label, computed, claimed, tol=0.02, unit="", abstol=None):
    """Relative tolerance by default. A wrong conversion median (0.27 vs a claimed
    0.29) slipped through an earlier 0.05 floor, so there is no floor now: pass
    abstol explicitly where a small absolute band is genuinely appropriate."""
    global CHECKS
    CHECKS += 1
    band = abstol if abstol is not None else abs(claimed) * tol
    ok = abs(computed - claimed) <= band
    status = "ok " if ok else "FAIL"
    if not ok:
        FAILS.append((label, claimed, computed))
    print("  %s  %-52s deck %10.2f%s | computed %10.2f%s" %
          (status, label[:52], claimed, unit, computed, unit))


def indeck(txt):
    """Is this exact string present in the deck?"""
    global CHECKS
    CHECKS += 1
    ok = txt in DECK
    if not ok:
        FAILS.append((txt[:60], "in deck", "NOT FOUND"))
    print("  %s  deck contains: %s" % ("ok " if ok else "FAIL", txt[:66]))


print("=" * 96)
print("1 · MARKET AND PORTFOLIO")
print("=" * 96)
ck("whole market Rs Cr", D[M26].sum(), 23244)
ck("Cipla cardiac Rs Cr", D[D.COMPANY == CIPLA][M26].sum(), 389)
ck("Cipla share %", D[D.COMPANY == CIPLA][M26].sum() / D[M26].sum() * 100, 1.68, tol=0.02)
ck("SKU count", len(D), 7452, tol=0)
ck("company count", D.COMPANY.nunique(), 279, tol=0)
ck("molecule count", D.MOLECULE_DESC.nunique(), 285, tol=0)
ck("brand count", D.BRANDS.nunique(), 3788, tol=0)
ck("Cipla rank", D.groupby("COMPANY")[M26].sum().rank(ascending=False)[CIPLA], 19, tol=0)
cv = (np.sqrt(D[D.COMPANY == CIPLA][Q26].sum() / D[D.COMPANY == CIPLA][Q24].sum()) - 1) * 100
mv = (np.sqrt(D[Q26].sum() / D[Q24].sum()) - 1) * 100
ck("Cipla book volume CAGR %", cv, -4.0, tol=0.15)
ck("market volume CAGR %", mv, 3.7, tol=0.15)

print()
print("=" * 96)
print("2 · ARCHETYPE TABLE (Slide 4 shortlist)")
print("=" * 96)
CLAIM = {  # key: (pool, cagr, volume, leader, cipla_sh, prize)
    "A7": (1249, 16.8, 11.2, 10.3, 0.71, 69),
    "A1": (2166, 12.9, 5.4, 19.2, 0.79, 133),
    "A4": (353, 55.8, 40.7, 15.3, 0.28, 19),
    "A3": (998, 14.8, 7.1, 30.1, 6.63, 8),
    "A8": (7318, 10.3, 2.2, 15.6, 2.52, None),
}
for k, (pool, cagr, vol, lead, cip, prize) in CLAIM.items():
    r = SP[k]
    ck("%s pool Rs Cr" % k, r["m26"], pool, tol=0.01)
    ck("%s CAGR %%" % k, r["value"], cagr, tol=0.02)
    ck("%s volume %%" % k, r["volume"], vol, tol=0.05)
    ck("%s leader %%" % k, r["leader"], lead, tol=0.02)
    ck("%s Cipla share %%" % k, r["cip_sh"], cip, tol=0.02)
    if prize is not None:
        ck("%s prize Rs Cr" % k, r["prize"], prize, tol=0.02)

print()
print("=" * 96)
print("3 · GROWTH DECOMPOSITION (the class of error we just found)")
print("=" * 96)
for k, (val, vol, mix) in {"A8": (10.3, 2.2, 7.9), "A1": (12.9, 5.4, 7.9)}.items():
    r = SP[k]
    ck("%s value %%" % k, r["value"], val, tol=0.02)
    ck("%s volume %%" % k, r["volume"], vol, tol=0.05)
    ck("%s mix %%" % k, r["mix"], mix, tol=0.05)
    ck("%s parts sum to value" % k, r["volume"] + r["mix"] + r["price"], r["value"], tol=0.02)

print()
print("=" * 96)
print("4 · HEADROOM AND UNDERWRITING ARITHMETIC")
print("=" * 96)
head = SP["A7"]["prize"] + SP["A1"]["prize"]
ck("A7+A1 headroom Rs Cr (deck says 201)", head, 201, tol=0.01)
ck("35 + 38 gross", 35.2 + 37.9, 73, tol=0.02)
ck("73 gross less 11 cannibalisation = net", 73.1 - 11, 62, tol=0.03)
ck("389 + 62 = 451", 389.5 + 62, 451, tol=0.01)
ck("62 / 201 = 31%", 62 / head * 100, 31, tol=0.05)
ck("break-even 19/0.6 as % of headroom", (19 / 0.6) / head * 100, 16, tol=0.08)
for m, lim in ((0.60, 37), (0.50, 31), (0.40, 25), (0.30, 19)):
    ck("cost ceiling at %.0f%% contribution" % (m * 100), 62 * m, lim, tol=0.03)

print()
print("=" * 96)
print("5 · A7 BUILD-UP (Slide 5)")
print("=" * 96)
M = D.MOLECULE_DESC
amh_pool = D[M.str.contains("AMLODIPINE", na=False) & M.str.contains("HYDROCHLOROTHIAZID", na=False)
             & M.str.contains("TELMISARTAN", na=False)]
mt_pool  = D[M.str.contains("CILNIDIPINE", na=False) & M.str.contains("METOPROLOL", na=False)
             & M.str.contains("TELMISARTAN", na=False)]
lp_pool  = D[M.str.contains("CHLORTALIDONE", na=False) & M.str.contains("CILNIDIPINE", na=False)
             & M.str.contains("TELMISARTAN", na=False)]
ck("Cresar AMH pool Rs Cr", amh_pool[M26].sum(), 466, tol=0.01)
ck("Metolar Trio pools Rs Cr", mt_pool[M26].sum(), 232, tol=0.02)
ck("Horizon-2 molecule pool Rs Cr", lp_pool[M26].sum(), 249, tol=0.02)
cip_amh = amh_pool[amh_pool.COMPANY == CIPLA][M26].sum()
ck("Cipla share of the 466 Cr pool %", cip_amh / amh_pool[M26].sum() * 100, 1.11, tol=0.05)
a7c = D[(D.ARCH == "A7") & (D.COMPANY == CIPLA)]
ck("Cipla A7 today Rs Cr (addressable)", SP["A7"]["cip"], 8.9, tol=0.02)
ck("A7 brands Cipla sells", a7c.BRANDS.nunique(), 9, tol=0)
ck("A7 companies competing", D[(D.ARCH == "A7") & D.addressable].COMPANY.nunique(), 107, tol=0.02)
ck("Cipla A7 volume %", SP["A7"]["cip_vol"], 13.2, tol=0.05)

print()
print("=" * 96)
print("6 · CONVERSION RATIOS (the differentiation, Slide 6)")
print("=" * 96)
fe = D[(D.ARCH == "A8") & M.str.contains("TELMISARTAN", na=False)]
tri = D[D.ARCH == "A7"]
ck("Cipla telmisartan-dual base Rs Cr", fe[fe.COMPANY == CIPLA][M26].sum(), 71.0, tol=0.02)
ck("Mankind telmisartan-dual base Rs Cr", fe[fe.COMPANY == "MANKIND"][M26].sum(), 517.8, tol=0.01)
ck("Glenmark telmisartan-dual base Rs Cr", fe[fe.COMPANY == "GLENMARK PHARMA"][M26].sum(), 1140, tol=0.01)
ck("Cipla A7 conversion ratio",
   tri[tri.COMPANY == CIPLA][M26].sum() / fe[fe.COMPANY == CIPLA][M26].sum(), 0.14, abstol=0.005)
ck("Cipla rank among telmisartan-dual holders",
   fe.groupby("COMPANY")[M26].sum().rank(ascending=False)[CIPLA], 18, tol=0)
g = fe.groupby("COMPANY")[M26].sum(); t = tri.groupby("COMPANY")[M26].sum()
ratios = sorted([t.get(c, 0) / g[c] for c in g.index if g[c] >= 50])
import statistics
ck("median A7 conversion ratio (>=50 Cr base)", statistics.median(ratios), 0.27, abstol=0.005)
ck("A7 target ratio implied by 44.1 Cr", 44.1 / 71.0, 0.62, abstol=0.005)
a5 = D[D.ARCH == "A5"]; a1 = D[D.ARCH == "A1"]
g5 = a5.groupby("COMPANY")[M26].sum(); t1 = a1.groupby("COMPANY")[M26].sum()
r5 = sorted([t1.get(c, 0) / g5[c] for c in g5.index if g5[c] >= 50])
ck("Cipla A1 conversion ratio", t1.get(CIPLA, 0) / g5[CIPLA], 0.29, abstol=0.005)
ck("median A1 conversion ratio", statistics.median(r5), 0.59, abstol=0.005)

print()
print("=" * 96)
print("7 · MOMENTUM, YEAR ON YEAR (Slide 5 caveat)")
print("=" * 96)
def yoy(sub):
    x, y, z = sub[Q24].sum(), sub[Q25].sum(), sub[Q26].sum()
    return (y / x - 1) * 100, (z / y - 1) * 100
a7a = D[(D.ARCH == "A7") & D.addressable]
for lbl, sub, c1, c2 in [
        ("addressable A7 market", a7a, 9.6, 12.9),
        ("Cresar AMH pool", amh_pool, 7.0, 9.2),
        ("Metolar Trio pools", mt_pool, 29.4, 30.8),
        ("Horizon-2 molecule", lp_pool, 13.3, 17.7),
        ("Cipla CRESAR AMH brand", D[(D.COMPANY == CIPLA) & (D.BRANDS == "CRESAR AMH")], 38.5, 4.0),
        ("Cipla METOLAR TRIO brand", D[(D.COMPANY == CIPLA) & (D.BRANDS == "METOLAR TRIO")], 129.7, 38.9)]:
    p1, p2 = yoy(sub)
    ck(lbl + " yr1 %", p1, c1, tol=0.03)
    ck(lbl + " yr2 %", p2, c2, tol=0.03)

print()
print("=" * 96)
print("8 · STRUCTURAL CLAIMS")
print("=" * 96)
import re as _re
norm = lambda x: _re.sub(r"[^A-Z]", "", str(x).upper())
cip = D[D.COMPANY == CIPLA].copy(); cip["self"] = cip["MANUFACT. DESC"].map(norm).eq("CIPLA")
ck("Cipla SKUs made in-house", cip["self"].sum(), 137, tol=0)
ck("Cipla total cardiac SKUs", len(cip), 137, tol=0)
mnc = D.groupby("INDIAN_MNC")[M26].sum()
ck("MNC share of market %", mnc.get("MNC", 0) / D[M26].sum() * 100, 4.8, tol=0.03)
sub = D.groupby("CARDIAC SUB SEGMENTS")[M26].sum()
ck("their AHT Triple/Poly segment Rs Cr", sub.get("AHT Triple / Poly Comb.", 0), 1473, tol=0.01)
ck("our A7 total Rs Cr", D[D.ARCH == "A7"][M26].sum(), 1472, tol=0.01)
ck("their Statins Comb. segment Rs Cr", sub.get("Statins Comb.", 0), 4154, tol=0.01)
locked = D.loc[~D["addressable"], M26].sum()
ck("locked-out pool Rs Cr", locked, 3001, tol=0.02)
ck("locked-out share of market %", locked / D[M26].sum() * 100, 12.9, tol=0.03)

print()
print("=" * 96)
print("9 · ANSOFF AND BCG (Slide 9)")
print("=" * 96)
pen = 20.2 + 16.2 + 15.4 + 10.0 + 6.3
ck("Ansoff market-penetration Rs Cr", pen, 68.1, tol=0.01)
ck("Ansoff penetration share of gross %", pen / (pen + 5.0) * 100, 93, tol=0.01)
for k, rel in [("A7", 0.069), ("A1", 0.041), ("A3", 0.220), ("A8", 0.162), ("A5", 0.066), ("A4", 0.018)]:
    ck("%s BCG relative share" % k, SP[k]["cip_sh"] / SP[k]["leader"], rel, tol=0.05)
best = max(SP[k]["cip_sh"] / SP[k]["leader"] for k in SP)
ck("best relative share anywhere (no cash cow)", best, 0.22, abstol=0.005)

print()
print("=" * 96)
print("10 · HR ARITHMETIC (Annexure G)")
print("=" * 96)
ck("Dr Rao tier calls/day", 100 * 2 / 22, 9.1, tol=0.02)
ck("Dr Iyer tier calls/day", 250 * 1 / 22, 11.4, tol=0.02)
ck("reps total", 50 + 60 + 0, 110, tol=0)
ck("replacement cash at 15% attrition Rs Cr", 110 * .15 * 6.5 * .75 / 100, 0.80, tol=0.05)
ck("replacement cash at 35% attrition Rs Cr", 110 * .35 * 6.5 * .75 / 100, 1.88, tol=0.05)
ck("capacity lost at 35% attrition %", 110 * .35 * 3.5 / 12 / 110 * 100, 10.2, tol=0.03)
ck("capacity lost at 15% attrition %", 110 * .15 * 3.5 / 12 / 110 * 100, 4.4, tol=0.03)
ck("cost line low Rs Cr", 110 * 10 / 100 + 4, 15, tol=0.02)
ck("cost line high Rs Cr", 110 * 12 / 100 + 6, 19, tol=0.02)

print()
print("=" * 96)
print("SUMMARY")
print("=" * 96)
print("checks run: %d | failures: %d" % (CHECKS, len(FAILS)))
for f in FAILS:
    print("   FAIL  %-50s deck=%s computed=%s" % f)
sys.exit(1 if FAILS else 0)
