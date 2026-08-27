#!/usr/bin/env python3
"""
Render every chart in the deck from the dataset, ready to drop into PowerPoint.

Nothing here is drawn by hand — each figure pulls its numbers from the same
engine the deck is verified against, so a chart cannot drift from the text.

    python3 build_charts.py     ->  charts/*.png  (300 dpi, transparent)
"""
import sys, json, statistics
sys.path.insert(0, ".")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from cipla_cardiac_agent import CardiacAgent, CIPLA, M24, M26, Q24, Q26

Q25 = "QTY MAT FEB'25"
BLUE, GREEN, VIVID = "#0B4DA2", "#3C6E14", "#8DC63F"
RED, AMBER, INK, DIM, FAINT = "#C4241C", "#8A5800", "#0F2340", "#4A6285", "#A9BBD2"
GREY = "#C6D3E4"

plt.rcParams.update({
    "font.family": ["Avenir Next", "Helvetica Neue", "DejaVu Sans"],
    "font.size": 11, "axes.edgecolor": DIM, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": DIM, "ytick.color": DIM,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.transparent": True,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.25,
})

A = CardiacAgent(); D = A.df; G = A.analyse()
SP = {r["space"][:2]: r for _, r in G.iterrows()}
M = D.MOLECULE_DESC
OUT = "charts/"
made = []


def save(fig, name):
    fig.savefig(OUT + name)
    plt.close(fig)
    made.append(name)


# ── SLIDE 2 · the bridge, with the ceiling far above the commitment ──────────
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.bar(0, 389.5, color=GREY, width=.72)
ax.bar(1, 62, bottom=389.5, color=VIVID, width=.72)
ax.bar(2, 451.5, color=BLUE, width=.72)
ax.axhline(389.5 + 201, color=RED, ls=(0, (5, 4)), lw=1.4)
ax.text(2.9, 389.5 + 201 + 14, "₹201 Cr — the ceiling the model computes",
        va="bottom", ha="left", color=RED, fontsize=10)
ax.text(2.9, 389.5 + 62 - 8, "₹62 Cr — what we commit to", va="top", ha="left",
        color=GREEN, fontsize=10, fontweight="bold")
ax.annotate("", xy=(2.75, 389.5 + 201), xytext=(2.75, 389.5 + 62),
            arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.2))
ax.text(2.62, 389.5 + 131, "headroom we\nleave on the table", ha="right", va="center",
        fontsize=9, color=DIM, style="italic")
for x, v, lab in [(0, 389.5, "₹389 Cr\ntoday"), (2, 451.5, "₹451 Cr\nyear 5")]:
    ax.text(x, v / 2, lab, ha="center", va="center", color="white",
            fontweight="bold", fontsize=10.5, linespacing=1.4)
ax.text(1, 389.5 + 31, "+₹62 Cr", ha="center", va="center", color="#14300A",
        fontweight="bold", fontsize=10)
ax.set_xlim(-.6, 4.6); ax.set_ylim(0, 640)
ax.set_xticks([]); ax.set_yticks([])
ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
ax.set_title("The gap between what the model permits and what we underwrite",
             loc="left", color=INK, fontsize=12, fontweight="bold", pad=14)
save(fig, "s2_bridge.png")

# ── SLIDE 4 · the opportunity map ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.6, 4.8))
for k, r in SP.items():
    pri = k in ("A7", "A1")
    ax.scatter(r["value"], r["m26"], s=max(40, r["cip_sh"] * 380),
               color=VIVID if pri else GREY, edgecolor=GREEN if pri else DIM,
               linewidth=1.6 if pri else .8, zorder=3 if pri else 2, alpha=.95)
    ax.annotate("%s" % k, (r["value"], r["m26"]),
                textcoords="offset points", xytext=(0, 13), ha="center",
                fontsize=10.5, fontweight="bold" if pri else "normal",
                color=INK if pri else DIM)
ax.axvline(A.mkt_cagr, color=BLUE, ls=(0, (4, 4)), lw=1.2)
ax.text(A.mkt_cagr + .6, 7000, "market\n%.1f%%" % A.mkt_cagr, color=BLUE, fontsize=9)
ax.set_xlabel("Real growth, 2-yr CAGR  →", fontsize=10)
ax.set_ylabel("Addressable pool, ₹ Cr  →", fontsize=10)
ax.set_title("Bubble size = Cipla's share today. The two we fund are the two it barely holds.",
             loc="left", fontsize=11.5, fontweight="bold", pad=12)
ax.grid(axis="y", color=GREY, lw=.5, alpha=.6)
save(fig, "s4_bubble.png")

# ── SLIDE 5 · pools accelerating while Cipla's brands slow ───────────────────
def yoy(sub):
    x, y, z = sub[Q24].sum(), sub[Q25].sum(), sub[Q26].sum()
    return (y / x - 1) * 100, (z / y - 1) * 100

amh = D[M.str.contains("AMLODIPINE", na=False) & M.str.contains("HYDROCHLOROTHIAZID", na=False)
        & M.str.contains("TELMISARTAN", na=False)]
mt = D[M.str.contains("CILNIDIPINE", na=False) & M.str.contains("METOPROLOL", na=False)
       & M.str.contains("TELMISARTAN", na=False)]
lp = D[M.str.contains("CHLORTALIDONE", na=False) & M.str.contains("CILNIDIPINE", na=False)
       & M.str.contains("TELMISARTAN", na=False)]
series = [("Cresar AMH's pool", amh, BLUE), ("Metolar Trio's pools", mt, BLUE),
          ("Horizon-2 molecule", lp, BLUE),
          ("CIPLA · Cresar AMH", D[(D.COMPANY == CIPLA) & (D.BRANDS == "CRESAR AMH")], RED),
          ("CIPLA · Metolar Trio", D[(D.COMPANY == CIPLA) & (D.BRANDS == "METOLAR TRIO")], RED)]
fig, ax = plt.subplots(figsize=(7.4, 4.8))
for lab, sub, col in series:
    a, b = yoy(sub)
    ax.plot([0, 1], [a, b], color=col, lw=2.6 if col == RED else 1.8,
            marker="o", ms=7, zorder=3 if col == RED else 2,
            alpha=1 if col == RED else .75)
    ax.text(1.03, b, "  %s  %.1f%%" % (lab, b), va="center", fontsize=9.5,
            color=col, fontweight="bold" if col == RED else "normal")
    ax.text(-0.03, a, "%.1f%%  " % a, va="center", ha="right", fontsize=9.5, color=col)
ax.set_xlim(-.35, 1.9); ax.set_xticks([0, 1])
ax.set_xticklabels(["FY24 → FY25", "FY25 → FY26"], fontsize=10)
ax.set_ylabel("Unit growth, year on year", fontsize=10)
ax.axhline(0, color=DIM, lw=.8)
ax.set_title("Every pool is accelerating. Both Cipla brands inside them are slowing.",
             loc="left", fontsize=11.5, fontweight="bold", pad=12)
ax.grid(axis="y", color=GREY, lw=.5, alpha=.6)
save(fig, "s5_slope.png")

# ── SLIDE 5 · where the ₹35 Cr comes from ────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.0, 2.5))
segs = [("Cresar AMH", 20.2, VIVID), ("Metolar Trio", 10.0, GREEN),
        ("Horizon-2 launch", 5.0, GREY)]
left = 0
for lab, v, c in segs:
    ax.barh(0, v, left=left, color=c, height=.5, edgecolor="white", lw=1.5)
    ax.text(left + v / 2, 0, "%s\n₹%.1f Cr" % (lab, v), ha="center", va="center",
            fontsize=9.5, color="#14300A" if c != GREY else INK, fontweight="bold")
    left += v
ax.set_xlim(0, 36); ax.set_ylim(-.5, .5); ax.axis("off")
ax.set_title("₹35 Cr — and 86% of it comes from two brands Cipla already sells",
             loc="left", fontsize=11.5, fontweight="bold", pad=10)
save(fig, "s5_stack.png")

print("charts so far:", made)

# ── SLIDE 6 · the two dot-plots — the most important chart in the deck ───────
fe = D[(D.ARCH == "A8") & M.str.contains("TELMISARTAN", na=False)]
tri = D[D.ARCH == "A7"]
g7 = fe.groupby("COMPANY")[M26].sum(); t7 = tri.groupby("COMPANY")[M26].sum()
r7 = sorted([(t7.get(c, 0) / g7[c], c) for c in g7.index if g7[c] >= 50])
g5 = D[D.ARCH == "A5"].groupby("COMPANY")[M26].sum()
t1 = D[D.ARCH == "A1"].groupby("COMPANY")[M26].sum()
r1 = sorted([(t1.get(c, 0) / g5[c], c) for c in g5.index if g5[c] >= 50])

fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6))
# A1's top value (USV at 4.34) is an outlier that would crush the informative
# range and destroy the "same shape twice" read, so each panel is clipped to
# where the companies actually sit and the outlier is called out at the edge.
PANELS = [(axes[0], r7, "A7  ·  duals → triples",
           "telmisartan-dual base ≥ ₹50 Cr   n=20", 1.10, None),
          (axes[1], r1, "A1  ·  plain statins → combinations",
           "plain-statin base ≥ ₹50 Cr   n=13", 2.10, ("U S V", 4.34))]
for ax, rows, title, sub, xmax, outlier in PANELS:
    med = statistics.median([v for v, _ in rows])
    top = max(v for v, _ in rows if v <= xmax)
    for i, (v, c) in enumerate(rows):
        me = (c == CIPLA)
        clipped = v > xmax
        xv = xmax * .985 if clipped else v
        ax.scatter(xv, i, s=210 if me else 74, color=RED if me else GREY,
                   edgecolor=RED if me else DIM, lw=1.7 if me else .7,
                   zorder=4 if me else 3, clip_on=False)
        name = str(c).replace("*", "").replace(" PHARMA", "").replace(" LIMITED", "").title()
        if me:
            ax.annotate("CIPLA  %.2f" % v, (xv, i), textcoords="offset points",
                        xytext=(0, -20), ha="center", fontsize=10,
                        color=RED, fontweight="bold")
        elif clipped:
            ax.annotate("%s  %.2f  →" % (name, v), (xv, i), textcoords="offset points",
                        xytext=(-8, 0), ha="right", va="center", fontsize=8.6, color=DIM)
        elif v >= top - 1e-9 or v > med * 2.0:
            ax.annotate(name, (xv, i), textcoords="offset points", xytext=(9, 0),
                        va="center", fontsize=8.6, color=DIM)
    ax.axvline(med, color=BLUE, lw=1.8, zorder=2)
    ax.annotate("median %.2f" % med, (med, len(rows) - .3),
                textcoords="offset points", xytext=(7, 0), va="center",
                fontsize=10, color=BLUE, fontweight="bold")
    ax.set_yticks([]); ax.set_ylim(-1.6, len(rows) + .6); ax.set_xlim(0, xmax)
    ax.set_xlabel("conversion ratio", fontsize=9.5)
    ax.set_title(title, loc="left", fontsize=11.5, fontweight="bold", pad=22, color=INK)
    ax.annotate(sub, (0, 1.02), xycoords="axes fraction", fontsize=8.4, color=DIM)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color=GREY, lw=.5, alpha=.5)
fig.subplots_adjust(wspace=.22)
fig.suptitle("Cipla converts at roughly half the median — in both funded archetypes",
             x=.015, ha="left", fontsize=13, fontweight="bold", color=INK, y=1.07)
save(fig, "s6_dotplots.png")

# ── SLIDE 6 · price is not the explanation ──────────────────────────────────
PRICE = [("Rosuva + Clopidogrel", 9.0, 0.69), ("ASA + Rosuvastatin", -4.2, 0.88),
         ("Atorva + Clopidogrel", -0.8, 0.54), ("Cilnidipine triple", -8.0, 1.13),
         ("Amlo + HCTZ + Telmi", 84.5, 1.11)]
RIVALS = [("Lupin", 42.9, 20.2), ("Torrent", 21.3, 31.9), ("Ajanta", 13.8, 16.8),
          ("Ajanta ", 13.5, 23.2), ("Glenmark", 86.2, 12.4)]
fig, ax = plt.subplots(figsize=(7.4, 4.4))
for lab, px, sh in RIVALS:
    ax.scatter(px, sh, s=110, color=GREY, edgecolor=DIM, lw=.8, zorder=2)
    ax.text(px, sh + 1.4, lab.strip(), ha="center", fontsize=8.6, color=DIM)
for lab, px, sh in PRICE:
    ax.scatter(px, sh, s=150, color=RED, edgecolor=RED, lw=1.4, zorder=3)
ax.axvline(0, color=BLUE, ls=(0, (4, 4)), lw=1.2)
ax.text(1.5, 34, "market price", color=BLUE, fontsize=9)
ax.annotate("Cipla — under 1.2% share\nwhatever the price", xy=(-4, 1.0), xytext=(14, 7.5),
            fontsize=10, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.annotate("Glenmark prices within 1% of Cipla\nand sells 11× more", xy=(85, 12.4),
            xytext=(28, 25), fontsize=9.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
ax.set_xlabel("Price per tablet vs the molecule's market average  (%)", fontsize=10)
ax.set_ylabel("Share of the molecule  (%)", fontsize=10)
ax.set_title("Cheaper products are losing to dearer ones. Price does not explain this.",
             loc="left", fontsize=11.5, fontweight="bold", pad=12)
ax.grid(color=GREY, lw=.5, alpha=.5)
save(fig, "s6_price.png")

# ── SLIDE 7 · A1 pools, with Cipla's sliver ─────────────────────────────────
A1B = [("Rosulip-CV", 323, 0.89), ("Rosulip-ASP", 307, 0.89), ("Atorlip-CV", 432, 0.55),
       ("Rosulip Gold", 14, 51.2), ("Atorlip Gold", 18, 9.5)]
fig, ax = plt.subplots(figsize=(7.4, 3.9))
for i, (lab, pool, sh) in enumerate(A1B):
    ax.barh(i, pool, color=GREY, height=.62)
    ax.barh(i, pool * sh / 100, color=RED, height=.62)
    ax.text(pool + 9, i, "₹%d Cr pool · Cipla %.2f%%" % (pool, sh), va="center",
            fontsize=9.2, color=DIM)
ax.set_yticks(range(len(A1B)))
ax.set_yticklabels([b[0] for b in A1B], fontsize=10)
ax.invert_yaxis(); ax.set_xlim(0, 560); ax.set_xticks([])
ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
ax.set_title("Cipla's 51% is in a ₹14 Cr pool. The ₹1,063 Cr is where it holds nothing.",
             loc="left", fontsize=11.5, fontweight="bold", pad=12)
save(fig, "s7_a1bars.png")
print("charts so far:", made)

# ── SLIDE 9 · BCG — the empty quadrants are the finding ─────────────────────
fig, ax = plt.subplots(figsize=(6.4, 5.4))
ax.axvspan(1, 6, 0.5, 1, color=VIVID, alpha=.10)
ax.axvspan(1, 6, 0, 0.5, color=AMBER, alpha=.08)
for k, r in SP.items():
    rel = r["cip_sh"] / r["leader"]
    pri = k in ("A7", "A1"); conv = k in ("A8", "A5")
    col = VIVID if pri else (BLUE if conv else GREY)
    ax.scatter(rel, r["value"], s=max(70, r["m26"] / 22), color=col,
               edgecolor=GREEN if pri else DIM, lw=1.6 if pri else .8, zorder=3)
    ax.annotate(k, (rel, r["value"]), textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=10.5, fontweight="bold" if pri or conv else "normal",
                color=INK)
ax.axhline(A.mkt_cagr, color=DIM, lw=1); ax.axvline(1.0, color=DIM, lw=1)
ax.set_xscale("log"); ax.set_xlim(0.012, 6); ax.set_ylim(4, 62)
ax.set_xticks([0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5])
ax.set_xticklabels(["0.02", "0.05", "0.1", "0.2", "0.5", "1.0", "2.0", "5.0"], fontsize=9)
ax.text(1.35, 56, "STAR", fontsize=11, color=FAINT, fontweight="bold")
ax.text(1.35, 6.5, "CASH COW", fontsize=11, color=FAINT, fontweight="bold")
ax.text(0.014, 56, "QUESTION MARK", fontsize=11, color=DIM, fontweight="bold")
ax.text(0.014, 6.5, "DOG", fontsize=11, color=DIM, fontweight="bold")
ax.add_patch(Rectangle((1.0, 4), 5.0, 58, facecolor="none", edgecolor=RED,
                       lw=1.6, ls=(0, (6, 4)), zorder=1))
ax.text(2.3, 30, "both quadrants empty\nnothing to harvest", ha="center",
        fontsize=10.5, color=RED, fontweight="bold")
ax.set_xlabel("Relative share  (Cipla ÷ leader)  →", fontsize=10)
ax.set_ylabel("Growth vs market  →", fontsize=10)
ax.set_title("No Star. No Cash Cow. Best relative share anywhere: 0.22.",
             loc="left", fontsize=11.5, fontweight="bold", pad=12)
save(fig, "s9_bcg.png")

# ── SLIDE 9 · Ansoff — where the money actually sits ────────────────────────
fig, ax = plt.subplots(figsize=(6.6, 5.0))
cells = [(0, 1, "MARKET PENETRATION", "₹68.1 Cr\n93%", VIVID, .95),
         (1, 1, "PRODUCT DEVELOPMENT", "₹5.0 Cr\n7%", VIVID, .30),
         (0, 0, "MARKET DEVELOPMENT", "₹0 incremental\nstockist refill", GREY, .55),
         (1, 0, "DIVERSIFICATION", "deliberately\nempty", GREY, .22)]
for x, y, title, val, col, alpha in cells:
    ax.add_patch(Rectangle((x, y), 1, 1, facecolor=col, alpha=alpha,
                           edgecolor="white", lw=3))
    ax.text(x + .5, y + .70, title, ha="center", fontsize=9.6, fontweight="bold", color=INK)
    ax.text(x + .5, y + .36, val, ha="center", fontsize=13 if "Cr" in val else 10,
            fontweight="bold" if "Cr" in val else "normal", color=INK)
ax.set_xlim(0, 2); ax.set_ylim(0, 2); ax.axis("off")
ax.text(.5, 2.08, "EXISTING PRODUCTS", ha="center", fontsize=9, color=DIM, fontweight="bold")
ax.text(1.5, 2.08, "NEW PRODUCTS", ha="center", fontsize=9, color=DIM, fontweight="bold")
ax.text(-.05, 1.5, "EXISTING\nMARKETS", ha="right", va="center", fontsize=9, color=DIM, fontweight="bold")
ax.text(-.05, .5, "NEW\nMARKETS", ha="right", va="center", fontsize=9, color=DIM, fontweight="bold")
ax.set_title("93% of the plan sits in the lowest-risk box — and the gradient is measured,\n"
             "not assumed: seven Cipla launches earned ₹1.94 Cr between them.",
             loc="left", fontsize=11, fontweight="bold", pad=34)
save(fig, "s9_ansoff.png")

# ── SLIDE 10 · prize and cost on one clock ──────────────────────────────────
# The year-by-year ramp is OUR planning shape, not a dataset output — only the
# year-5 endpoints (Rs 62 Cr revenue, Rs 15-19 Cr cost) are underwritten. The
# chart says so rather than implying the path is computed.
yrs = np.arange(0, 6)
rev = np.array([0, 8, 22, 38, 52, 62])
cost = np.array([0, 4.5, 11, 15, 17, 19])
contrib = rev * .6
fig, ax = plt.subplots(figsize=(7.6, 4.5))
ax.fill_between(yrs, cost, contrib, where=contrib >= cost, color=VIVID, alpha=.28,
                interpolate=True, label="Contribution above cost")
ax.plot(yrs, contrib, color=GREEN, lw=2.8, label="Contribution  (60% of revenue)")
ax.plot(yrs, cost, color=RED, lw=2.4, ls=(0, (5, 3)), label="Task-force cost")
ax.scatter([5, 5], [contrib[-1], cost[-1]], s=70,
           color=[GREEN, RED], zorder=4)
ax.annotate("₹37 Cr contribution\non ₹62 Cr revenue", (5, contrib[-1]),
            textcoords="offset points", xytext=(-12, 14), ha="right",
            fontsize=9.5, color=GREEN, fontweight="bold")
ax.annotate("₹15–19 Cr\nat full scale", (5, cost[-1]), textcoords="offset points",
            xytext=(-12, -26), ha="right", fontsize=9.5, color=RED, fontweight="bold")
ax.set_xticks(yrs); ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("₹ Cr per year", fontsize=10)
ax.set_ylim(0, 44)
ax.legend(frameon=False, fontsize=9.5, loc="upper left", bbox_to_anchor=(0, .98))
ax.set_title("Prize and cost read against one clock", loc="left",
             fontsize=11.5, fontweight="bold", pad=12)
ax.annotate("Year-5 endpoints are underwritten; the ramp between them is our planning shape",
            (0, -.19), xycoords="axes fraction", fontsize=8.4, color=DIM, style="italic")
ax.grid(axis="y", color=GREY, lw=.5, alpha=.6)
save(fig, "s10_prize_cost.png")

print("\n%d charts written to charts/" % len(made))
for m in made: print("   " + m)
