# Grand Finale deck — content
**Team JK · XLRI Jamshedpur · Jenny Panchmatia (H26154) · Kaustubh Bhalerao (H26084)**
Cipla House, Mumbai · 4 September 2026 · 10 min + 5 min Q&A · submission 29 Aug, 7pm

Every market figure below is computed from `Data Set_Ascend Season 4_2026.xlsx` (7,452 SKUs,
MAT Feb'24 → Feb'26) through our agent. Patient epidemiology is cited to named published sources
(Annexure F). **Exactly three inputs are neither computed nor cited — field-force cost per rep,
contribution margin, and the size of the physician universe — and all three sit inside the task-force
sizing on Slide 8, where we show how wrong they can be before the conclusion changes.** We make no
forecast of regulatory action, no claim about therapies outside this dataset, and no assertion about
Cipla's internal operations that the data cannot support.

**Format rules from the invite:** 10 slides max in the core deck · min 10–12pt · a visual on every
slide · no text walls · plain language, no jargon · personas and named brands, not generic advice ·
annexures after Thank You · file named `Team JK_Jenny Panchmatia Kaustubh Bhalerao_XLRI Jamshedpur`.

---

# SLIDE 1 · Team Introduction

**Headline:** Team JK · XLRI Jamshedpur

Two photos, names, roll numbers. One line each — keep it human, not a CV:
- **Jenny Panchmatia** (H26154)
- **Kaustubh Bhalerao** (H26084)

**One line under the names, and this is the line that sets up the whole deck:**
> We built a working agent, pointed it at 7,452 SKUs, and let it tell us where Cipla should go.
> It changed our answer three times — the archetype, the molecule, and the size of the prize.

*Visual:* photos + the Ascend/Cipla lockup. Keep it to 10 seconds of airtime.

---

# SLIDE 2 · Executive Summary

**Headline:** Cipla has the cardiac portfolio. It does not have the push.

Four blocks across the page:

**1 · The problem**
Rank 19 of 279 in cardiac. 1.68% share. In resistant hypertension Cipla sells **nine brands and holds
0.71%**, and its cardiac book is losing patients at 4.0% a year while the market gains them at 3.7%.
**The sharpest version: Cipla converts 0.14 of its own two-drug patients onto a three-drug pill. The
median company converts 0.27. Macleods converts 0.96.** That is a scale problem, not a portfolio one.

**2 · Where to go**
Two archetypes out of nine: **A7 Resistant Hypertension** (₹1,249 Cr, +16.8%) and
**A1 Secondary Prevention** (₹2,166 Cr, +12.9%). Both grow on patients, not price. Neither has a
leader above 20%.

**3 · What to do**
**93% market penetration, 7% product development, no diversification** — Ansoff's safest box, chosen
because Cipla's own seven launches in this window earned ₹1.94 Cr between them. Not a launch. **Detail four brands Cipla already sells** — Cresar AMH and Metolar Trio in A7,
Rosulip-CV and Rosulip-ASP in A1 — to patients Cipla is already losing. Atorlip-CV is funded, deliberately, at a third of their weight. Add
**Telmisartan + Cilnidipine + Chlorthalidone** in Horizon 2, built from two duals Cipla makes today.
Funded from A8's budget, not A8's reps.

**4 · What it's worth**
**₹201 Cr of headroom** — the ceiling the model computes. **We underwrite ₹62 Cr net over five
years**, the rate at which the best-performing challenger in this dataset actually gained share
from Cipla's starting position. Against a task force costing **₹15–19 Cr a year**, that is
**~2× contribution to cost at run-rate, cumulative positive in year 4.**

*Visual:* the four blocks as a left-to-right band, with the ₹389 Cr → ₹451 Cr bridge on the right.
Show the ₹201 Cr ceiling as a faint upper bound above the ₹62 Cr bar — the gap is the point.

---

# SLIDE 3 · The agent, and the agent deciding *(deliverable a — objective, inputs, framework, metrics, trade-offs)*

**Headline:** We didn't score a spreadsheet. We built something that can be questioned.

**Objective** — find the opportunity spaces in Indian cardiac most likely to beat the market over
3–5 years, and size what Cipla can realistically win in each.

**Data in** — 7,452 SKU records · 279 companies · 285 molecules · 3,788 brands · both sheets.
**Three time points, not two** (MAT Feb'24, '25, '26 · value, constant-price value, units) — the
midpoint is what separates a brand that is accelerating from one that is coasting, and we use it on
Slides 5 and 7 even where it cuts against us. Archetypes reconciled back to the file's own 15 cardiac
sub-segments *(Annexure D)*. **External signals:** CSI 2024 · IHCI protocol · CDSCO FDC bans (Aug'24,
Jun'26) · NLEM 2022 · ESC 2024 · patent expiries · the patient epidemiology on Slide 8 · and
**air quality** — Indian hypertension prevalence rises **5.2% per 10 µg/m³ of PM2.5**, and meeting
the National Clean Air Programme target would cut it by only 2.42%, so the exposure persists across
our whole window.

**How it is built** — three layers, and the split is the point:

| Layer | What it does | Why it matters |
|---|---|---|
| Reasoning | Chooses which analyses to run | Judgement |
| Tools | 10 typed analyses | The interface |
| Engine | Deterministic Python over 7,452 SKUs | **Every number is computed, never generated** |

**Metrics it computes:** addressable pool (net of locked molecules) · growth decomposed into
volume / mix / price · leader share and HHI · portfolio breadth and volume momentum · achievable
share · prize in rupees.

**And here it is resolving the four trade-offs the case asks about:**

| Trade-off | What the data said | How it resolved |
|---|---|---|
| **Size vs growth** | A8 is ₹7,318 Cr but only 2.2 of its 10.3 growth points are volume — 7.9 are mix, the same patients paying more | Only volume persists 3–5 years. **A8 became the funding source, not the destination** |
| **Growth vs competition** | A3 showed 27% headline growth | 58% of it was Saroglitazar, which Zydus owns 79.5% of. Any molecule >70% single-owner is stripped. **A3 fell from first to defend** |
| **Attractiveness vs right to win** | A4 grows 55.8%, fastest on the board | Cipla holds 0.28% and starts from nothing. Horizon 3, outside the priority prize |
| **Prize vs score** | A3 scored well on attractiveness | Ranked on rupees Cipla can win, not on score. **A7 offers 8× the prize** |
| **Ceiling vs precedent** | Model said Cipla could reach 8% of A1 — ₹201 Cr | We asked whether anyone ever had. **Nobody starting where Cipla starts has doubled share in two years.** So we underwrite ₹62 Cr |

**The one that changed our answer:** the locked-molecule filter. ₹3,001 Cr — 12.9% of the market —
sits in molecules a single rival owns more than 70% of. Before we stripped it, A3 looked like the
winner. After, the order flips.

*Visual:* the three-layer diagram on the left; on the right, a before/after bar showing A3 and A7
swapping rank once locked molecules are removed. **Then open the laptop and ask it something.**

---

# SLIDE 4 · The shortlist *(deliverable b — top 3–5, prioritise 2–3)*

**Headline:** Nine archetypes in. Five worth naming. Two worth funding.

| # | Archetype | Addressable | Real growth | Volume | Leader | Cipla | Headroom | Underwritten | Call |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | **A7 Resistant Hypertension** | ₹1,249 Cr | +16.8% | 11.2 | 10.3% | 0.71% | ₹69 Cr | **₹35 Cr** | **BUILD** |
| 2 | **A1 Secondary Prevention** | ₹2,166 Cr | +12.9% | 5.4 | 19.2% | 0.79% | ₹133 Cr | **₹38 Cr** | **ATTACK** |
| 3 | A4 Intensive Lipid | ₹353 Cr | +55.8% | 40.7 | 15.3% | 0.28% | ₹19 Cr | — | Horizon 3 |
| 4 | A3 Cardiometabolic | ₹998 Cr | +14.8% | 7.1 | 30.1% | 6.63% | ₹9 Cr | — | DEFEND |
| 5 | A8 Step-up Dual | ₹7,318 Cr | +10.3% | 2.2 | 15.6% | 2.52% | — | — | CONVERT |

**Read the last two columns together.** Headroom is what the pool structure permits. Underwritten is
what we will commit to — anchored to the fastest share gain any company in this dataset actually made
from Cipla's position. The gap between them is not conservatism for its own sake; it is the
difference between a market that *allows* a move and a company that *makes* one.

*Footnote on the slide:* ₹35 Cr + ₹38 Cr = ₹73 Cr gross. **₹62 Cr net**, after deducting ~₹11 Cr of
Cipla's own leaking telmisartan-dual patients converting into the focus triples (Slide 9). ₹62 Cr is the number we
carry through the rest of the deck.

**A forward-looking signal that favours A7 specifically.** PM2.5 raises both blood pressure and
hypertension incidence in India — **+5.2% prevalence per 10 µg/m³**, with a Delhi cohort showing
higher systolic BP and incident hypertension on long-term exposure. It enlarges the treated pool and,
more usefully for us, the share of patients **not controlled on two drugs** — which is the definition
of A7. This is the only external signal in our register that acts on a specific archetype rather than
the category, and it points at the one we are funding.

**One structural fact behind all five rows:** multinationals hold ₹1,110 Cr of this ₹23,244 Cr
market — **4.8%**. Every company Cipla has to beat here is an Indian company competing on field
force and price, not on originator brand. That is a fight Cipla is built for.

**Prioritise A7 and A1.** Both beat the market, both have leaders under 20%, and Cipla already
sells the brands in each.

**Why not the others — and A4 is the one we argue with our own model about.** Our agent scores A4
**second highest on the board (69.1)** because it grows 55.8%. Its prize is only **₹19 Cr** because
our method holds every pool flat at MAT Feb'26 and treats pool growth as uncounted upside — a
convention that penalises the fastest-growing space hardest. **Grow the pool at even 20% a year,
under half its current rate, and A4 is ₹49 Cr.** We still exclude it from the underwritten ₹62 Cr,
deliberately, to keep that number conservative — and Cipla already holds Rosulip EZ in it. **A4 is
an exclusion we chose, not one the data forced.** A3 is Cipla's strongest position and its worst opportunity: 6.63%
share, ₹8 Cr of headroom, a 30.1% leader, and 36% of the pool locked. A8 is the largest position
Cipla holds and grows on price — a cash source.

*Visual:* bubble chart — real growth on X, addressable pool on Y, bubble = Cipla's current share.
A7 and A1 highlighted; everything else in grey.

---

# SLIDE 5 · A7 — right to win, and the exact molecule *(deliverable b — right to win)*

**Headline:** Cipla already sells nine triples in this market. It details none of them.

**What Cipla has** — nine brands, **₹8.9 Cr, 0.71%** of a ₹1,249 Cr addressable pool. It is the
**only** archetype where Cipla is winning patients: volume **+13.2%** against a market at +11.2%.
Everywhere else in Cipla's ₹389 Cr cardiac book, units are falling. Underneath it sits a
**₹90.7 Cr telmisartan franchise across 15 molecules** — the backbone of every triple here.

**Cipla's right to win against the people actually winning here** — 107 companies, no fortress:

| | Their strength | Cipla against it |
|---|---|---|
| **Mankind** 10.3%, +7.1 momentum | Tier-2/3 reach and price aggression | Cipla does not win a price war in Tier-2/3 and we do not propose one. **₹69.4 Cr of the step-up patients are already on Cipla's duals** — that list is the asset Mankind cannot buy |
| **Torrent** +5.4 momentum | Dedicated cardio division, decades of CV detailing | This is the gap we are asking Cipla to close — hence the task force, not a launch |
| **IPCA** ×1.90 in two years | Ran **two** molecules, hard | We copy the method, not the molecules — theirs are 71.7% locked and excluded |
| **Cipla** 0.71%, −3.0 | 9 brands, ₹90.7 Cr telmisartan base, makes every SKU itself | Widest triple portfolio in the segment and no field force pointed at it. *(In-house manufacturing is table stakes here — Mankind, Aristo, Macleods and IPCA are all 100% self-made. **Sun, the largest A7 player at ₹139 Cr, makes none of its own.**)* |

**Our own rule killed our Round 1 answer.** We recommended Amlopres-3D. **IPCA holds 71.7% of that
molecule** — above the 70% threshold our method calls uncontestable. Metolar 3D fails it too, at
70.5%. Two of the nine are excluded by our own filter.

**So the ₹35 Cr comes from brands Cipla already sells, not from a launch.** Cipla ran seven cardiac
launches in this window and made **₹1.94 Cr between them** *(Annexure C)*. The new molecule moves to
Horizon 2 and carries ₹5 Cr, not ₹15 Cr.

| Brand | Molecule | Pool | Today | Year 5 | Gain |
|---|---|---:|---:|---:|---:|
| **CRESAR AMH** | Amlodipine + HCTZ + Telmisartan | ₹466 Cr | ₹5.2 Cr | ₹25.4 Cr | **+₹20.2 Cr** |
| **METOLAR TRIO** | the two Cilnidipine triples | ₹232 Cr | ₹2.6 Cr | ₹12.6 Cr | **+₹10.0 Cr** |
| *New triple — Horizon 2* | Chlortalidone + Cilnidipine + Telmisartan | ₹249 Cr | — | ₹5.0 Cr | +₹5.0 Cr |
| Four others | maintained, not pushed | ₹302 Cr | ₹1.1 Cr | ₹1.1 Cr | — |
| | | **₹1,249 Cr** | **₹8.9 Cr** | **₹44.1 Cr** | **+₹35 Cr** |

**One caveat, and we will put it up before you find it.** Every figure above is a two-year average.
Split on the Feb'25 midpoint and the picture sharpens against us:

| Units, year on year | Feb'24→'25 | Feb'25→'26 |
|---|---:|---:|
| Cresar AMH's pool | +7.0% | **+9.2%** |
| Metolar Trio's pools | +29.4% | **+30.8%** |
| Horizon-2 molecule | +13.3% | **+17.7%** |
| **Cipla — Cresar AMH** | +38.5% | **+4.0%** |
| **Cipla — Metolar Trio** | +129.7% | **+38.9%** |

**Every pool is accelerating. Both Cipla brands inside them are slowing.** A burst then a flatline is
what a brand does when nobody details it in year two. That is the case for the task force, stated
against us.

**Why two brands and not nine.** IPCA started this window ₹0.08 Cr from Cipla — ₹6.93 Cr against
₹6.85 Cr. IPCA ran **two** molecules and reached ₹17.9 Cr (×1.90). Cipla ran **seven** and went
backwards (×0.95). Of 18 companies starting where Cipla started, **every one that beat ×1.4 ran
three molecules or fewer.** Our two focus brands run to 5.44% of their pools — ×4.9 on today's base,
against IPCA's ×4.98. We underwrite at the benchmark, not past it.

**Two things that make this executable today:**
1. **Cresar AMH is one triple sold under three Cipla brands.** Amlopres Trio, Cresar Plus and Cresar
   AMH all sit on amlodipine + HCTZ + telmisartan; Cipla holds 1.11% of ₹466 Cr while competing with
   itself. Consolidate onto Cresar AMH — the one growing. Costs nothing, doubles detailing weight.
2. **Cipla can already make the Horizon 2 triple.** It sells Cilnidipine + Telmisartan (Cilogard T)
   and Chlorthalidone + Telmisartan (Cresar CT) — the new molecule is those two duals merged, not new
   chemistry, and Cipla makes **137 of its 137 cardiac SKUs itself**. No partner needed.

*Why a doctor writes Cipla's version rather than Mankind's identical one — Slide 6.*

*Visual:* one stacked bar for the ₹35 Cr — ₹20.2 Cr / ₹10.0 Cr / ₹5.0 Cr — with the old launch-led
split ghosted behind it. Beneath, the feeder map: four Cipla dual brands arrowed into two triples.

---

# SLIDE 6 · The differentiation — why Cipla, and not Mankind *(deliverable b — right to win)*

**Headline:** Cipla builds feeder franchises and then doesn't climb them. That is the opportunity.

We assumed Cipla's edge was owning the patients who need the next drug. **It isn't.** Cipla ranks
**18th of 175** in telmisartan duals at ₹71 Cr. Mankind holds ₹518 Cr. Glenmark holds ₹1,140 Cr. On
base size Cipla loses — so base size cannot be the argument. We measured what each company actually
*does* with the base it has.

**A7 — how much of your two-drug base becomes a three-drug pill**

| Company | Dual base | A7 triples | **Converted** |
|---|---:|---:|---:|
| Micro Labs · Macleods | ₹85 / ₹115 Cr | ₹82 / ₹111 Cr | **0.96** |
| Sun | ₹202 Cr | ₹139 Cr | 0.69 |
| IPCA | ₹162 Cr | ₹77 Cr | 0.48 |
| *Median, 20 companies with a ₹50 Cr+ base* | | | *0.27* |
| Mankind | ₹518 Cr | ₹131 Cr | 0.25 |
| Torrent | ₹447 Cr | ₹100 Cr | 0.22 |
| **CIPLA** | **₹71 Cr** | **₹9.9 Cr** | **0.14** |
| Glenmark | ₹1,140 Cr | ₹74 Cr | 0.07 |

**Then we tested whether it was a fluke. It is the same company-wide.**

**A1 — how much of your plain-statin base becomes a combination**

| Company | Statin base | A1 combinations | **Converted** |
|---|---:|---:|---:|
| USV | ₹211 Cr | ₹914 Cr | 4.34 *(Ecosprin — which our sizing strips out)* |
| Macleods | ₹80 Cr | ₹151 Cr | 1.88 |
| Torrent | ₹153 Cr | ₹265 Cr | 1.74 |
| Mankind | ₹63 Cr | ₹72 Cr | 1.14 |
| *Median, 13 companies with a ₹50 Cr+ base* | | | *0.59* |
| **CIPLA** | **₹64 Cr** | **₹18.5 Cr** | **0.29** |

**In both archetypes Cipla converts at roughly half the median.** Not because the products are
missing — they are on the shelf. Because nobody is asking the doctor for the next step.

> **The differentiation, in one line:** Cipla's advantage is not that it has the most patients.
> It is that it converts the fewest of the ones it already has. **Every rupee in this plan needs no
> new patient and no competitive win** — only that Cipla convert its own base at a rate its peers
> already reach.

**And it is already happening, unaided.** Inside the Cresar family the duals lost **11.1%** of units
last year while the Cresar triples gained **17.9%**. Inside Metolar: duals **−7.7%**, triples
**+41.7%**. Same reps, same doctors, same brand name. Patients are walking up the ladder alone.

**We tested the obvious alternative explanation, and it fails.** If Cipla converts less, maybe
Cipla is simply priced out. So we computed realised price per tablet in all five focus molecules:

| Molecule | Cipla vs market | Cipla share | The company that beats it |
|---|---:|---:|---|
| Rosuvastatin + Clopidogrel | **+9.0%** | 0.69% | Lupin at **+42.9%** holds 20.2% |
| ASA + Rosuvastatin | **−4.2%** | 0.88% | Torrent at **+21.3%** holds 31.9% |
| Atorvastatin + Clopidogrel | **−0.8%** | 0.54% | Ajanta at +13.8% holds 16.8% |
| Cilnidipine + Metoprolol + Telmisartan | **−8.0%** | 1.13% | Ajanta at +13.5% holds 23.2% |
| Amlodipine + HCTZ + Telmisartan | **+84.5%** | 1.11% | **Glenmark, priced within 1% of Cipla, holds 11× more** |

**In four of five, Cipla is at or below market price and still holds under 1.2%. Cheaper products are
losing to dearer ones by up to 36×.** In the fifth — the one molecule where Cipla really is expensive
— its closest price twin in the market sells eleven times as much at the same price. **Price does not
explain this. Nothing is being asked of the doctor.**

*(Caveat: price per tablet does not adjust for strength mix, so read it as a range, not a decimal.
The Glenmark comparison is same-molecule and same-price, which is why we lead with it.)*

**Three checks a judge should run on us:**
1. **Is the target credible?** ₹35 Cr in A7 implies a ratio of **0.62** — above the median, below
   Sun. ₹38 Cr in A1 implies **0.85** — above the median, below Torrent. **These were computed
   independently of the IPCA share-multiple anchor on Slide 5 and land in the same place.**
2. **Why hasn't someone already done it?** Glenmark. The largest dual base in the market converts
   **7%** of it. A feeder base converts nothing on its own — it takes a team pointed at it, which is
   what Slide 8 buys.
3. **Isn't in-house manufacturing your moat?** No. Cipla makes 137 of 137 cardiac SKUs itself — but
   so do Mankind, Aristo, Macleods and IPCA, all at 100%. It is table stakes, and we won't claim it.
   *(It is only notable in reverse: **Sun, the largest A7 player at ₹139 Cr, self-manufactures none
   of it.**)*

**We propagated the shrinking base through the model rather than just flagging it.** Cipla's dual
base is falling **10.6% of units a year**, so the ₹35 Cr cannot rest on today's ₹71 Cr forever.

**First, the reason matters. The category is not shrinking — Cipla's slice of it is.**

| Telmisartan duals, units | Feb'24→'25 | Feb'25→'26 |
|---|---:|---:|
| The market | +6.4% | **+7.4%** |
| Mankind | +8.8% | **+8.2%** |
| **Cipla** | +0.3% | **−10.6%** |

**This is share loss, not category decline.** Every year of delay does not merely shrink the prize —
it hands the feeder patients to Mankind permanently.

**Second, does the target survive a smaller base?** The ₹44.1 Cr year-5 A7 figure implies a
conversion ratio of 0.62 on today's base. On a shrinking one it implies more:

| If Cipla's dual base… | Year-5 base | Implied ratio | Where that sits |
|---|---:|---:|---|
| repeats last year's decline | ₹59 Cr | **0.74** | between Sun (0.69) and Macleods (0.96) |
| follows its 2-year trend | ₹82 Cr | **0.54** | between IPCA (0.48) and Sun (0.69) |
| merely stops losing share | ₹71 Cr | **0.62** | between IPCA and Sun |

**Even on the worst case the target stays inside what companies in this dataset already do** — it asks
Cipla to convert slightly better than Sun, third best of twenty. It is demanding. It is not
unprecedented. **We would rather show you the worst case than the flattering one.**

*Two honest notes on this metric.* Converting a patient shrinks the base it is measured against, so
the ratio partly inflates itself — the rupee figure is the commitment, the ratio is the diagnostic.
And the same shrinkage is self-limiting under the plan: the patients leaving are the ones it retains.

*Visual:* two dot-plots side by side — A7 and A1 — each company a dot on a 0-to-1 conversion scale,
median marked, Cipla shaded red and sitting left of it in both. Same shape twice is the argument.

---

# SLIDE 7 · A1 — the largest prize, entered from strength *(deliverable b — right to win)*

**Headline:** Don't attack USV. Cipla is already registered in ₹1,063 Cr of A1 and holds ₹8 Cr of it.

**What Cipla has**
- **51.2% of ASA + Clopidogrel + Rosuvastatin. That molecule is ₹14.4 Cr; Cipla's share of it is
  ₹7.4 Cr.** It is not a base to extend from. It is **proof of formulation and proof of demand** —
  Cipla can make a triple-combination secondary-prevention pill and doctors already write it.
- The real base is **₹17.1 Cr across five molecules**, three of which sit under 1% share in pools of
  ₹307 Cr, ₹323 Cr and ₹432 Cr. Those three are the opportunity — Cipla is *already registered and
  selling* in **₹1,063 Cr of pool** and holding ₹8.0 Cr of it.
- In-house statin API manufacturing

**Cipla's right to win against the leaders**

| | Their strength | Cipla against it |
|---|---|---|
| **USV** 19.2% | Ecosprin — a 60-year prescriber habit | It is one molecule USV owns 87.5% of, which our sizing strips out. **A brand moat, not a category moat** — the three pools we target are open |
| **USV 21.1% / Emcure 19.6%** in rosuva+ezetimibe | First movers on the fastest-growing molecule in the dataset | Cipla is *already there* with Rosulip EZ at 0.54%. Registration is not the gap; detailing is |
| **Cipla** 0.79% | In-house statin API, registered in ₹1,063 Cr of pool, proven triple-combination formulation | Everything needed except the calls |

**Half of Cipla's A1 base cannot grow.** ₹9.1 Cr of the ₹17.1 Cr sits
in Rosulip Gold and Atorlip Gold — 51.2% and 9.5% shares of pools worth only ₹14 Cr and ₹18 Cr.
Under our own 8% ceiling those two are already *above* their headroom. **All of A1's growth has to
come from three molecules where Cipla holds under 1%.**

Cipla is registered and stocked in all three today:

| Brand | Molecule | Pool | Pool volume | Cipla | **Cipla volume** | Year 5 | Gain |
|---|---|---:|---:|---:|---:|---:|---:|
| **ROSULIP-CV** | Rosuvastatin + Clopidogrel | ₹323 Cr | **+16.8%** | 0.89% | **+12.3%** | 5.9% | **+₹16.2 Cr** |
| **ROSULIP-ASP** | ASA + Rosuvastatin | ₹307 Cr | +5.2% | 0.89% | **+11.7%** | 5.9% | **+₹15.4 Cr** |
| ATORLIP-CV | Atorvastatin + Clopidogrel | ₹432 Cr | +3.6% | 0.55% | **−14.8%** | 2.0% | +₹6.3 Cr |
| Rosulip Gold, Atorlip Gold | at ceiling | ₹32 Cr | — | — | — | held | — |
| | | | | **₹17.1 Cr** | | **₹54.9 Cr** | **+₹38 Cr** |

**The weighting is the decision.** Two of these are rosuvastatin and their units are already growing
double digits under Cipla — and **Rosulip-CV is the one brand in this plan that is speeding up on
its own: units +7.8% in the first year, +17.0% in the second.** It is the only place we are adding
weight to something already moving. The third is atorvastatin, in the slowest pool, and **Cipla is losing
14.8% of its units there every year** — our own signal register says rosuvastatin is displacing
atorvastatin, so we fund it at 2%, not 5.9%. Same discipline as A7: weight follows units.

**Then scale Rosulip EZ — because Cipla already launched it, and that is the whole argument.**
The deck's earlier draft said "launch a Rosuvastatin + Ezetimibe FDC." Cipla launched it. **Rosulip
EZ holds 0.54% of a ₹183 Cr pool growing +91.5% in value on +77.4% volume** — the fastest-growing
molecule in this dataset, with USV at 21.1% and Emcure at 19.6%. Cipla launched into the best market
in Indian cardiac and two years later holds half a percent. Ezetimibe is also non-scheduled — the
one place in this plan with real pricing headroom.

> **The line to say:** Cipla launched into the best market in Indian cardiac and two years later
> holds half a percent of it. The portfolio is not the problem. The push is.

**Why now:** 7.9 of A1's 12.9 growth points come from mix — patients upgraded to combinations at
discharge, not new patients arriving. Each switched patient is worth more per script. But note
**Cipla's own A1 units are −6.7%** while the market's are +5.4%. These products are losing patients
today. That is not an argument against detailing them. It is the evidence that nobody is.

*Visual:* five bars, one per Cipla A1 molecule, each showing pool size with Cipla's sliver shaded.
The 51.2% bar is tiny and the three ~0.9% bars are huge — that contrast *is* the argument. Do not
draw a ladder; a ladder implies the base carries weight, and ₹7.4 Cr does not. Inset: Rosulip EZ's
0.54% against a pool growing 91.5%.

---

# SLIDE 8 · Who we are treating, who writes it, and what has to be built *(deliverable b)*

**Headline:** The doctor is the customer. The patient is the consumer. Cipla is losing both.

*In this market the two are not the same person and never have been: the doctor decides, the patient
pays and swallows. A plan that only persuades one of them fails. Five personas, split by which role
they play.*

### THE CONSUMERS — two patients, both already on a Cipla prescription

| | **Ramesh Kulkarni · 54 · Nashik · shopkeeper** *(A7)* | **Sunita Menon · 56 · Kochi · school administrator** *(A1)* |
|---|---|---|
| Where he/she sits | One of **~315 million** Indian adults with hypertension — **35.5%** of everyone over 20 *(ICMR-INDIAB, Lancet 2023)* | Stented after a heart attack 14 months ago. **The mean age of a first MI in India is 53 — about a decade earlier than the West**, and **52% of India's CVD deaths occur under 50** |
| What went wrong | Diagnosed 6 years ago. He is in the **13.7%** actually on treatment — and not in the **7.8%** whose BP is controlled *(NFHS-5)*. On two drugs he is still 158/96: one of the **10–16%** of treated Indian hypertensives who resist dual therapy | Discharged on four drugs. She is on one. In **PURE**, only **23.6%** of Indians with established CVD were taking an antiplatelet and **15.5%** a statin — India's use peaked at 43% and fell back to **21.6%** |
| Why he/she stops | Three pills, three times a day. **32.7%** of rural south Indian NCD patients are non-adherent; **78.6%** say the medicines are hard to pay for | Rural statin use is **11.6%** against **19.9%** urban. Nobody re-detailed her regimen after discharge |
| What actually fixes it | **The third drug in the same pill.** Single-pill combinations roughly **double persistence** versus the same molecules taken separately *(meta-analysis, 27 studies, 346,030 patients)* | **Her discharge regimen collapsed into one tablet** — rosuvastatin + clopidogrel |
| **The Cipla brand that is that pill** | **Cresar AMH.** Ramesh is already on Amlopres-TL — a Cipla dual inside the **₹69.4 Cr that is leaking at 6% a year** | **Rosulip-CV.** Cipla already sells it, into a ₹323 Cr pool, and holds **0.89%** |

**And the consumer is the payer — which is the whole opening.** Under IHCI's public-channel
programme, patients' out-of-pocket medicine cost fell from **47% to 9%**. In the private channel,
where Cipla sells, nobody has solved it: **78.6%** of Indian patients on cardiovascular medicines
say they are hard to pay for. One pill instead of three is a cost argument and an adherence argument
in the same sentence — and it is the argument Cipla is currently not making to anyone.

> **The line to say:** we are not asking Cipla to find new patients. Ramesh and Sunita are already on
> a Cipla prescription, written by a doctor Cipla can already reach. The question is only whether
> their next prescription is also Cipla's.

### THE CUSTOMERS — three doctors, and they are not the same buyer

| | **Dr. Rao — interventional cardiologist** | **Dr. Iyer — consulting physician** | **Dr. Sharma — Tier-2/3 GP** |
|---|---|---|---|
| Sees | Sunita, at discharge | Ramesh, on his third visit this year | Both, on refill |
| Universe | ~5,000 in India | ~15,000 high-decile | The long tail |
| Decides | The post-ACS discharge regimen | Whether to add a third drug | Whether to substitute at refill |
| Moved by | CSI 2024 outcome data, KOL peers | **IHCI Step-3 protocol** — 141 districts, 303 m people, BP control **37% → 48%** | Availability and price on the shelf |
| Cipla's route | High-science detailing, investigator-led studies | Specialist reps against a protocol that already names the triple | **Existing 5,500-stockist network — no new headcount** |
| Reps we add | **50** | **60** | **0** |

**Dr. Sharma gets no reps and still matters.** He is where a written prescription either survives or
gets substituted, and Cipla's distribution already reaches him. Winning him is a supply-and-stocking
job, not a detailing job — which is exactly why the task force is 110 people and not 300.

**What to build: a Cardio-Metabolic Task Force — smaller than you would guess**

The point is the *shape*, not our arithmetic. India has thousands of cardiologists, not tens of
thousands, so a specialist force is small and affordable. Our working sizing — **flagged as ours,
not the data's** — is:

| Segment | Universe *(our planning figure)* | Per rep | Reps |
|---|---:|---:|---:|
| Cardiologists (Dr. Rao) | ~5,000 | 100 | **50** |
| High-decile physicians (Dr. Iyer) | ~15,000 | 250 | **60** |
| Tier-2/3 GPs | — | — | **0** |
| | | | **110** |

- Veeva CRM, so calls are measured on the archetype, not on gross volume.
- **Pay on 90-day repeat chemist offtake in the rep's own territory, not on gross adds.** We wanted to
  pay on month-4 patient persistence — no Indian data source resolves persistence to a rep. Secondary
  audits stop at chemist level; Rx audits are brand-level panels. So we pay on the closest thing
  measurable monthly: does the same chemist reorder.

**Cost, and the honest limits of it.** We estimate **₹4–5 Cr in the pilot year, ₹15–19 Cr a year at
full scale** — but rep cost, physician-universe size and contribution margin are the three numbers in
this deck the dataset cannot give us. Rather than defend them, we sized how wrong they can be:

| Contribution margin | Contribution on ₹62 Cr | **The plan clears its cost line at any spend below** |
|---|---:|---:|
| 60% *(our estimate)* | ₹37.2 Cr | **₹37 Cr a year** |
| 50% | ₹31.0 Cr | ₹31 Cr a year |
| 40% | ₹24.8 Cr | ₹25 Cr a year |
| 30% | ₹18.6 Cr | ₹19 Cr a year |

**Our cost estimate would have to be wrong by roughly 2× — or the margin wrong by half — before the
plan stops paying for itself.** Cipla's commercial team will size the force better than we can; the
conclusion does not depend on our version of it.

**The people design is the strategy, so we built it that way.** Three frameworks — Build–Buy–Borrow,
Sales Force Effectiveness, Total Rewards — quantified in **Annexure G**. The headline checks:

| | The HR call | Why it follows from the strategy |
|---|---|---|
| **Pay** | **80:20 fixed:variable in year 1, moving to 70:30 by year 3.** The variable is weighted to **territory conversion ratio**, not gross prescriptions | Pay on gross adds and reps chase new patients — the one motion the launch data says fails. Pay on conversion and the incentive enforces the plan. **The metric is already computable per territory from the same IQVIA data**, so nothing new has to be measured |
| **Hire** | **~60% lateral from cardio divisions** (Torrent, Mankind, USV, Sun), the rest internal transfer plus fresh | The missing capability is **prescriber relationships**, and those cannot be built quickly or in-licensed. They walk in with the hire. This is the one place Cipla genuinely *buys* rather than builds |
| **Keep** | Target **<15% annual attrition** against a first-year industry norm of **30–35%** | Every departure takes the prescriber relationship you paid a premium for. Torrent runs 16.6% and Sun 13.6%, so <15% is achievable, not aspirational |
| **Structure** | A dedicated cardio vertical with its own P&L, not a bolt-on to the respiratory force | Matches how Cipla has stood up new teams before, and stops the new force being scheduled around an existing one |

**Two numbers that make this more than an org chart.** The Indian field benchmark is **8–12 calls
per rep per day**; our panels work out at **9.1 for Dr. Rao's tier and 11.4 for Dr. Iyer's** — inside
the band, with no slack in the second. *That is an independent argument for concentration: the field
maths says the same thing the IPCA benchmark does.* And moving attrition from the industry's 30% to
**under 15%** returns **₹0.8 Cr a year and 4.4% of field capacity — about five reps Cipla then does
not have to hire.**

*Visual:* two rows, labelled. **CONSUMERS** on top — Ramesh and Sunita, one arrow each into a Cipla
brand. **CUSTOMERS** beneath — Rao, Iyer, Sharma, with their rep counts (50 / 60 / 0). The 110-rep
team as the base layer joining them. The arrow is the next prescription.
The arrow is the patient's next prescription — that is the whole deck in one picture.

---

# SLIDE 9 · Where the money goes, and where it stops *(deliverable b — strategic implications)*

**Headline:** Double down, build, be selective, avoid — and we are not asking anyone to give up revenue.

| | Archetypes | Why |
|---|---|---|
| **DOUBLE DOWN** | A7, A1 | ₹3,415 Cr combined, growing 12.9–16.8%, both leaders under 20%, Cipla already carries the brands. Both are combinations named in current treatment protocols (CSI 2024, IHCI Step-3) |
| **DEFEND** | A3 Cardiometabolic | Cipla's only over-indexed position (6.63% of the addressable pool against 1.68% of cardiac overall — **3.9×**) and the one it is losing fastest (−14.7 momentum). Ring-fence fenofibrate. Do not fund growth here — ₹8 Cr of headroom against a 30.1% leader |
| **CONVERT** | A8 Step-up Dual **and A5 Primary Lipid** | Cipla's two biggest positions — **₹249 Cr, 64% of its cardiac book — and both are leaking. A8 units −4.3% against a market at +2.2%; A5 units −1.6% against a market at +5.3%.** These are not harvests. They are the feeder base for A7 and A1 respectively, and the agent classifies them itself: *a position you hold but are losing patients in faster than the market is a leak, not a harvest* |
| **AVOID FURTHER INVESTMENT** | A6, A9 | Mature or moving against the guidelines. A9 is ₹4,219 Cr, but both IHCI and ESC 2024 now recommend initiating on combination rather than monotherapy. Existing revenue continues; zero incremental spend |

*Mapped to the four calls the case asks for: **double down** = A7 + A1 · **build capabilities** =
converting A8 and A5 (the task force is the capability) · **selective** = A3, defended not funded ·
**avoid further investment** = A6, A9.*

**The symmetry is the strategy.** A8 feeds A7; A5 feeds A1. Both feeders are large, both are leaking,
and Cipla under-converts both — 0.14 against a 0.27 median in A7, 0.29 against 0.59 in A1 *(Slide 6)*.
**Two-thirds of Cipla's cardiac book is a feeder base it is not climbing.** That is one problem with
one fix, not two initiatives.

**Two classical lenses, and they disagree about the past and agree about the plan.**

**BCG says Cipla has nothing to harvest in cardiac — and that is the finding, not a limitation.**
Plotting growth against *relative* share (Cipla ÷ leader), Cipla holds **no Star and no Cash Cow
anywhere in cardiac.** Its best relative share is 0.22 in A3; everything else is a Question Mark or a
Dog:

| | Growth vs market | Relative share | BCG | Our call |
|---|---:|---:|---|---|
| A4 | +55.8% | 0.018 | Question Mark | Option, not underwritten |
| **A7** | +16.8% | 0.069 | **Question Mark** | **DOUBLE DOWN** |
| A3 | +14.8% | 0.220 | Question Mark | DEFEND |
| **A1** | +12.9% | 0.041 | **Question Mark** | **DOUBLE DOWN** |
| A5 | +10.8% | 0.066 | **Dog** | CONVERT |
| A8 | +10.3% | 0.162 | **Dog** | CONVERT |
| A6 · A9 | +9.3% · +8.3% | 0.000 · 0.056 | Dog | AVOID |

**Two things follow.** First, **A8 is a Dog, not a Cash Cow** — which is precisely why "harvest" was
the wrong verb and CONVERT is the right one. BCG reaches that on relative share alone, independently
of our volume evidence. Second, with no cash cow in the book, **this plan cannot be funded by
harvesting something healthy. It has to be funded by fixing a behaviour** — which is exactly what the
conversion gap is. That is also the honest answer to why cardiac has been under-invested for years:
nothing in it ever self-funded.

**Ansoff says the plan is deliberately sitting in the safest box.**

| | Existing products | New products |
|---|---|---|
| **Existing markets** | **MARKET PENETRATION — ₹68.1 Cr, 93% of the plan.** Cresar AMH ₹20.2 Cr · Rosulip-CV ₹16.2 Cr · Rosulip-ASP ₹15.4 Cr · Metolar Trio ₹10.0 Cr · Atorlip-CV ₹6.3 Cr | **PRODUCT DEVELOPMENT — ₹5.0 Cr, 7%.** The Horizon 2 triple, sold to prescribers the reps have already called on for 18 months |
| **New markets** | **MARKET DEVELOPMENT — ₹0 incremental.** Tier-2/3 refill through the existing 5,500 stockists; no new headcount | **DIVERSIFICATION — deliberately empty.** A4 would be in-licensed, and sits outside the underwritten number |

**93% of this plan is market penetration — Ansoff's lowest-risk quadrant — and we did not choose that
for comfort.** Cipla ran seven launches into cardiac in this window and made ₹1.94 Cr between them.
**The risk gradient Ansoff describes in theory is measured in this dataset**, which is why the plan
is weighted the way it is.

**The A8 call is the one people get wrong, including us at first.** "Harvest" implies asking a
division to milk a healthy franchise. A8 is not healthy. Cipla is losing those patients **now**, to
Mankind and Torrent, at 4.3% a year. So the ask is not sacrifice — it is **giving Cipla's escaping
patients somewhere to go that is still Cipla.**

| Cipla dual, leaking | MAT26 | units | Steps up into |
|---|---:|---:|---|
| Amlopres-TL + Cresar-AM | ₹46.9 Cr | −6.0% | **Cresar AMH** |
| Cresar-H | ₹8.6 Cr | −12.4% | **Cresar AMH** |
| Metolar TL | ₹7.5 Cr | −10.7% | **Metolar Trio** |
| Cresar CT, Cilogard T | ₹6.4 Cr | −0.3% / +14.3% | the Horizon 2 triple |
| | **₹69.4 Cr** *(of Cipla's ₹71.0 Cr total telmisartan-dual base)* | | |

**So cannibalisation is the engine, not the cost.** Every patient converting was going to need a
third drug anyway; the only question is whose. **We have netted it out**: ~₹11 Cr of the A7 gain is
Cipla's own patients moving bucket, so the ₹35 Cr becomes **₹24 Cr genuinely new** — and the ₹62 Cr
headline for A1+A7 is stated *after* that deduction, not before it.

**Two honest notes, before a judge finds them.** A conversion-led plan cannibalises *more* than a
launch-led one by design — but the counterfactual is not that these patients stay on Cipla's dual.
They are leaving at 4.3% a year. And Amlopres-AT, at ₹96.2 Cr Cipla's largest cardiac brand, is
amlodipine + **atenolol** — it does not step up into a telmisartan triple, so it is not part of this
exposure.

*Visual:* the four calls as a 2×2, with the feeder map beneath — four leaking Cipla duals with
arrows converging on two triples. The arrow is patients, not budget.

---

# SLIDE 10 · The plan, the prize, and what could go wrong

**Headline:** ₹389 Cr to ₹451 Cr over five years — and here is the clock on it.

**Horizon 1 · months 0–18 — detail from day one, because the products already exist**
The ~50-rep cardiology team starts on **Cresar AMH, Metolar Trio, Rosulip-CV and Rosulip-ASP** —
all registered, stocked and shipping today — into the prescriber base already writing Cipla's
leaking duals. Consolidate Amlopres Trio and Cresar Plus onto Cresar AMH in month
one; it costs nothing and doubles detailing weight. Pilot in 4 metros, 500 cardiologists,
top-30-city stockist coverage. *In parallel:* file the new triple. The FDC holds **DCGI approval**
and is already marketed by 54 companies, so this is a manufacturing and filing exercise rather than
a new-drug approval. **We have not verified the exact licensing route and do not claim a timeline
from it** — what we do carry is formulation, stability and first commercial batch, **9–12 months**.

**Horizon 2 · months 18–36 — add the new triple to a door already open**
Launch Telmisartan + Cilnidipine + Chlorthalidone into prescribers the reps have called on for 18
months — not a cold launch into 54 competitors. Scale the physician team to 110. Push Rosulip EZ,
which is already on the shelf at 0.54%.

**Build, and we did check the alternative.** A7 has 54 companies and a 15% leader — the largest
asset buyable is roughly **₹37 Cr of revenue at leader share**, in molecules where nobody has a moat,
so buying share costs more than detailing it. **A1 is the one place buy is a real question**, because
USV's Ecosprin is exactly the kind of brand moat worth acquiring — we considered it and are not
recommending it. **A4 is where we would in-license rather than build**, since Cipla holds 0.28% and
starts from nothing in the fastest-growing tier on the board.

**Horizon 3 · months 36–60 — an option we are not underwriting**
A4 Intensive Lipid: ₹353 Cr growing 55.8%, leader at 15.3%. **₹19 Cr of headroom** — the model caps
Cipla at 5.7% here because the leader holds only 15.3%, so the ceiling is 60% of that. Deliberately
outside the ₹62 Cr we underwrite; do not add the two.

**Why five years and not three:** the achievable-share ceiling in our model is a five-year
parameter. Presenting it against a 36-month plan would be compressing our own assumption by two
years. We would rather show the real clock.

**How we will know it is working — 12 months**
A7 share 0.71% → **1.0%** — the year-1 step on our own ×4.98 five-year path, not a faster one ·
**Cipla's A7 conversion ratio 0.14 → 0.20**, the metric this whole plan is built on · 90-day chemist
reorder rate on the four focus brands · A3's −14.7 slide arrested. **All four are computable from the
same IQVIA data every quarter, so this plan can be marked right or wrong without waiting five years.**

**What could go wrong**
| Risk | Response |
|---|---|
| We capture less than underwritten | Break-even is **16% of headroom**; we underwrite **31%**. Roughly 2× margin of safety on the cost line |
| Cipla has never moved share this fast | True — nobody in this dataset has. We underwrite only the rate the **best** performer achieved, not the model ceiling |
| New team takes too long to stand up | Year 1 runs on ~50 reps against four products that already exist and are already stocked, so a hiring slip delays scale, not revenue. Nothing in Horizon 1 waits on a launch |
| Prescriber inertia | Lead with Indian adherence evidence on single-pill triples, not price |
| Another CDSCO FDC ban | Only guideline-backed combinations are in the plan — the triple is IHCI Step-3 |
| A3 erosion continues | Ring-fence fenofibrate from any detailing cut |

*Visual:* the ₹389 Cr → ₹451 Cr waterfall with the ₹201 Cr headroom ceiling drawn as a faint line
above it, and the five-year cost curve underneath so prize and cost sit on the same time axis.

---

# SLIDE 11 · Thank You
*(Per the invite's flow. Keep the Cipla lockup untouched.)*

---

# ANNEXURES *(after Thank You — keep them few)*

**A · Method in six decisions**
Archetype construction (7,452 records → 9 archetypes by how the patient is treated) · locked-pool
exclusion (>70% single-owner molecules, ₹3,001 Cr / 12.9% removed) · growth decomposition using
constant-price MAT · **headroom** sizing (achievable share capped at 8% or 60% of leader share,
modulated by portfolio breadth and volume momentum) · **underwriting** (headroom is a ceiling, not
a forecast — see below) · eight external signals · sensitivity across 108 parameter combinations.

**A2 · Headroom is not a forecast, and we do not present it as one**
Headroom asks *what does the pool structure permit.* It answers ₹201 Cr. It does not ask whether
anyone has ever moved that fast. So we tested that separately, in the same dataset:

| | Cipla today | Best 2-yr share multiple by any company starting in Cipla's 0.2–2.0% band | Compounded to 5 yrs | Underwritten yr-5 share |
|---|---:|---|---:|---:|
| A1 | 0.79% | ×1.60 (n=16) | ×3.24 | 2.55% |
| A7 | 0.71% | ×1.90 — IPCA, 0.76→1.43% (n=18) | ×4.98 | 3.53% |

Across 279 companies and two years, **the largest share gain anyone made was USV's +1.29pp in A1 and
Mankind's +1.16pp in A7 — both incumbents with existing scale. Nobody starting where Cipla starts
doubled.** Cipla itself went −0.01pp in A1 and −0.04pp in A7 over the same window. We therefore
underwrite Cipla matching the single best performer in the data, on pools held flat at MAT Feb'26
size, and treat pool growth as uncounted upside. That yields **₹73 Cr gross, ₹62 Cr net of
cannibalisation — 31% of headroom.** Break-even against a ₹19 Cr cost line is 16%.

*Earlier drafts of this deck applied a "30% take-rate haircut." It was in the caption, not in the
code. We removed the claim rather than the rigour, and replaced it with the table above.*

**B · Sensitivity — what it does and does not prove**
A7 holds top-3 in 108/108 parameter runs. A4 in 100/108. A1 in 84/108. **This is robustness of
*ranking*, not of the rupee figure** — it says the priority order does not depend on the weights we
chose. The rupee figure is defended by the underwriting table in A2, not by this.

**C · Launch precedent — why we stopped leading with one**

| | |
|---|---|
| Cipla's own launches into cardiac, 2024–26 | **7 products. ₹1.94 Cr between them. Best: ₹0.99 Cr** |
| Companies entering our Horizon-2 molecule from zero | **13 tried. All thirteen together: ₹1.9 Cr** |
| Best standing start into any open A7 molecule, 279 companies | ₹3.92 Cr — once, in 55 attempts |

The FDC itself is not the constraint — it holds DCGI approval and 54 companies market it. The
constraint is that a standing start earns ₹2–4 Cr while a detailed existing brand earns ₹20 Cr.
That is why the launch sits in Horizon 2 at ₹5 Cr rather than leading the plan.

**C2 · Dataset scope**
Covers Anti-Hypertensives, Lipid Regulators, Anti-Angina. Excludes SGLT2i, ARNI, anticoagulants,
beta-blockers, standalone diuretics — which the wider PharmaTrac cardiovascular figure
(₹33,115 Cr, MAT Dec'25) includes. Ours is ₹23,244 Cr on the case dataset.

**D · Reconciliation to the case file's own segmentation** *(why we built archetypes at all)*
The dataset ships a 15-value `CARDIAC SUB SEGMENTS` field. We did not ignore it — we tested against it:

| Case-file segment | Value | Our archetypes |
|---|---:|---|
| AHT Triple / Poly Comb. | ₹1,473 Cr | **A7, 100%** — our A7 totals ₹1,472 Cr. Identical. |
| Statins Comb. | ₹4,154 Cr | **A1 70% · A3 22% · A4 8%** — one segment, three different patients |
| CCB / ARBs / ACEi / Alfa blockers | ₹4,824 Cr | **A9** — four molecule classes, one clinical decision |
| Statins Plain | ₹2,821 Cr | A5, 100% |
| AHT Dual + AHT Diuretic Comb. | ₹7,751 Cr | A8, 100% |

**Where the file segments by how the patient is treated, we agree with it exactly.** Where it
segments by chemistry — statin combinations that serve post-ACS, diabetic and high-intensity
patients alike — we split it, because those patients are reached by different doctors. That split
is the whole reason A1 and A7 separate from A3 and A8 in our ranking.

**E · What we did not use**
Of 36 columns, 13 carry the analysis. Four are constant or near-empty (SUPERGROUP, ACUTE_CHRONIC,
FINAL NFC at 99.4% solids, PACK VOLUME blank on 7,412 of 7,452 rows). Price-to-retailer columns
were checked and not used — we size on MRP value and constant-price value, which is the pair that
separates volume from price.

**F · Sources** *(the invite asks for these explicitly)*
**Market:** IQVIA/PharmaTrac cardiac dataset (case study) · Cipla FY25 Annual Report and investor
disclosures · Torrent, Glenmark, USV, Mankind investor disclosures.

**Clinical and regulatory:** CSI Dyslipidaemia Guidelines 2024, *Indian Heart Journal* 2024;76(S1) ·
IHCI Standard Treatment Protocol, ihci.in · ESC 2024 Hypertension Guidelines · CDSCO FDC ban notices
Aug 2024 and Jun 2026 · NPPA / NLEM 2022 · TOPSPIN trial, *IJMR*.

**Patient epidemiology — every figure on Slide 8:**
- Prevalence (35.5%, ~315 m adults): ICMR-INDIAB-17, *Lancet Diabetes & Endocrinology*, Jul 2023
- Care cascade (70.5% screened / 34.3% aware / 13.7% treated / 7.8% controlled): NFHS-5 (2019–21)
  analyses, *Lancet Regional Health – SE Asia* 2023 and *J Human Hypertension* 2022/2025
- Resistant hypertension at 10–16% of treated hypertensives in India: published Indian series,
  summarised in *Approaches in Managing Resistant Hypertension: A Review* (2024)
- Non-adherence 32.7% (rural Puducherry, *J Family Med Prim Care* 2019); 78.6% report difficulty
  paying (Indian adherence literature, *Indian Heart Journal* 2021)
- Single-pill combination roughly doubles persistence: systematic review and meta-analysis,
  27 studies / 346,030 patients, *Expert Rev Pharmacoecon Outcomes Res* 2023
- Mean age of first MI ~53, ~10 years earlier than Western populations; 52% of Indian CVD deaths
  under 50: CREATE registry (*Lancet* 2008) and Indian premature-CAD literature
- Secondary prevention use (antiplatelet 23.6%, statin 15.5%; rural 11.6% vs urban 19.9%; India
  peaked 43% and fell to 21.6%): PURE study, *Lancet* 2011 and *JACC* 2024
- IHCI scale and results (141 districts, 25 states, 303 m people, 2 m+ on treatment, BP control
  37%→48%): *BMC Health Services Research* 2024; *Resolve to Save Lives* 2024 evaluation
- Air quality (+5.2% hypertension prevalence per 10 µg/m³ PM2.5; NCAP target would cut prevalence
  2.42%, WHO guideline 4.21%): *International Journal of Epidemiology* 2025 · Delhi cohort,
  *Hypertension* (AHA) 2020 · peri-urban Hyderabad cohort, *Epidemiology* 2019


---

**G · The HR architecture behind the 110** *(we are an HR team; this is the layer we own)*

Three frameworks carry this: **Build–Buy–Borrow** for where the people come from, **Sales Force
Effectiveness (SFE)** for whether 110 is the right number, and **Total Rewards** for making the
incentive carry the strategy rather than fight it.

**G1 · SFE: does 110 survive the benchmark?**
The Indian pharma field benchmark is **8–12 calls per rep per day**. Our panel sizes were set from
the physician universe; this tests them from the other end, and they hold — but only just, for
Dr. Iyer's tier.

| Segment | Panel/rep | Visits/month | Calls/month | **Calls/day (22 days)** | Verdict |
|---|---:|---:|---:|---:|---|
| Cardiologists (Dr. Rao) · 50 reps | 100 | 2 | 200 | **9.1** | Comfortably inside 8–12 |
| High-decile physicians (Dr. Iyer) · 60 reps | 250 | 1 | 250 | **11.4** | At the top of the band — no slack |
| Tier-2/3 GPs (Dr. Sharma) · 0 reps | — | — | — | — | Stockist network, not detailing |

**Read the second row as a constraint, not a comfort.** At 11.4 calls a day, Dr. Iyer's tier has no
capacity for a fourth brand. That is an independent argument for the concentration on Slide 5: the
field maths says the same thing the IPCA benchmark does.

**G2 · Total Rewards: the comp plan *is* the strategy**
A conventional pharma incentive pays on gross prescriptions, which pushes a rep toward new patients —
the exact motion the launch data says fails. So the variable is re-cut around conversion:

| Component | Yr 1 | Yr 3 | Why |
|---|---:|---:|---|
| **Fixed** | **80%** | 70% | A new division with unproven brands cannot recruit specialists on a thin fixed. Fixed buys the talent; variable steers it |
| Variable — **territory conversion ratio** | 12% | 20% | Cipla's A7 ratio is 0.14 against a 0.27 median; year-1 target 0.20. **Computable per territory from the same IQVIA data, monthly** — no new measurement system |
| Variable — 90-day repeat chemist offtake | 8% | 10% | Closest measurable proxy for persistence. We wanted month-4 patient persistence; no Indian source resolves it to a rep |

*Deliberately excluded: gross new-patient adds and any volume-only bonus. Both would pay people to
execute a different strategy from the one on Slide 6.*

**G3 · Build–Buy–Borrow: where 110 cardio reps come from**
The missing capability is not headcount, it is **prescriber relationships** — which cannot be built
quickly and cannot be in-licensed. They transfer with the person. **This is the one place the plan
buys rather than builds**, and it is the HR answer to the build-vs-buy question on Slide 10.

| | Share | Ramp to full productivity | Trade-off |
|---|---:|---|---|
| **BUY** — lateral from cardio divisions (Torrent, Mankind, USV, Sun) | ~60% | 3–4 months | Commands a premium; arrives with the prescriber list |
| **BUILD** — internal transfer from respiratory/GP | ~25% | 6–9 months + therapy certification | Knows Cipla's systems and stockists; must learn high-science detailing |
| **BORROW** — contract/fresh for the physician tier | ~15% | 12+ months | Cheapest, slowest; never used for cardiologists |

**G4 · Retention is asset protection, and it is worth ₹0.8 Cr a year plus capacity**
First-year attrition among Indian medical representatives runs **30–35%**; company-level attrition at
Torrent is 16.6% and Sun 13.6%, so **under 15% is achievable, not aspirational.**

| Attrition | Leavers/yr | Replacement cash | **Field capacity lost to re-ramp** |
|---:|---:|---:|---:|
| 35% | 38.5 | ₹1.88 Cr | **10.2%** |
| 30% | 33.0 | ₹1.61 Cr | 8.8% |
| **15% (target)** | **16.5** | **₹0.80 Cr** | **4.4%** |

*Replacement costed at 75% of fixed salary — the mid-band for a specialist role carrying
relationships; frontline roles sit nearer 40%, senior specialists above 100%.*

**Moving 30% → 15% returns ₹0.8 Cr of cash and 58 rep-months to selling — about 4.4% of field
capacity, which is roughly five reps you do not have to hire.** Levers in order of effect: the higher
year-1 fixed (G2); a 24-month retention bonus for the pilot cohort, who carry the relationships that
matter most; a career path into the vertical rather than out of it; manager span held at 8–10 so
coaching is real.

**G5 · Capability — a cardiologist call is not a GP call**
Dr. Rao is moved by outcome data and KOL peers, not by reach frequency; industry work suggests only
**one in three doctor interactions is rated valuable**, so at 9.1 calls a day the constraint is call
quality, not call count. Requires therapy certification before first call, clinical-data fluency on
CSI 2024 and IHCI Step-3, and KOL engagement skill. Budgeted inside the ₹3–5 Cr KOL and training
line, not on top of it.

**G6 · Org design, and the internal politics nobody puts on a slide**
A dedicated cardio vertical with **its own P&L**, matching how Cipla has stood up new teams before.
The harder problem is that Horizon 1 is funded from A8's budget, so an existing budget-holder is asked
to give something up. **The CONVERT framing is the answer to that conversation:** A8's patients are
leaving at 4.3% a year regardless, and this routes them to another Cipla brand rather than to
Mankind. Nobody is asked to sacrifice revenue; they are asked to stop losing it.

**G7 · What HR delivers, and the month-12 kill criterion**
Months 0–3: vertical stood up, 50 cardiologist-facing reps hired, comp signed off, Veeva configured
to report conversion ratio by territory. Months 4–9: certification complete, first conversion-ratio
readout. Months 10–18: scale to 110, first retention checkpoint against <15%. **If the conversion
ratio has not moved from 0.14 toward 0.20 by month 12, the incentive design is wrong before the
strategy is** — and that is the first thing to re-examine, not the last.
---

# Speaking notes — 10 minutes

| Slide | Time | The one thing to land |
|---|---|---|
| 1 Team | 0:15 | "It changed our answer three times." |
| 2 Exec summary | 1:00 | **Cipla converts 0.14 of its own two-drug patients onto a three-drug pill. The median is 0.27.** |
| 3 Agent + trade-offs | 1:45 | The model never writes a number — **demo it here.** The locked filter flipped A3 to A7 |
| 4 Shortlist | 0:45 | Two of nine, and why not the other seven |
| 5 A7 | 1:15 | We stopped leading with a launch. **Then volunteer the caveat: every pool accelerating, both Cipla brands slowing** |
| 6 Differentiation | 1:15 | **Same shape twice — Cipla converts at half the median in both funded archetypes.** Glenmark is the cautionary tale, not us |
| 7 A1 | 0:45 | Cipla already launched Rosulip EZ into the fastest pool on the board. It holds 0.54% |
| 8 Personas & build | 1:30 | **"The doctor is the customer, the patient is the consumer — Cipla is losing both."** Three doctors, two patients, 110 reps. **Then the HR point: we pay on conversion ratio, not prescriptions — the comp plan is the strategy** |
| 9 Implications | 1:00 | **"BCG says we have no cash cow in cardiac — so this is funded by fixing a behaviour, not by harvesting one. Ansoff says 93% of the plan is market penetration."** Then A8 leaking at −4.3% |
| 10 Plan | 0:45 | ₹201 Cr of headroom, ₹62 Cr underwritten, break-even at 16% |

**Hold in reserve for Q&A** — do not spend slide space on these:
- Cannibalisation maths, netted: ~₹11 Cr scaled to the underwritten A7 push, not the ₹18–24 Cr of
  the full-ceiling case
- Task force build-up: 50 + 60 reps × ₹10–12 L, plus ₹1 Cr Veeva and ₹3–5 Cr KOL
- On the same share targets applied to pools growing at their own CAGRs, the figure is ~₹171 Cr —
  we chose not to bank pool growth. Say this only if pushed on why ₹62 Cr and not ₹201 Cr
- Why ₹201 Cr and not the refined ₹221.9 Cr (`adj_prize` growth-premium refinement)
- Raw vs addressable USV share (31.6% vs 19.2%)
- Amlopres-3D is ₹0.05 Cr — a name, not a franchise
- Contribution margin of 60% is our assumption; the dataset has no margin data
- **"How do you know 110 is right?"** Two independent routes land on it: physician universe ÷ panel
  size, and the 8–12 calls/day field benchmark, which puts our panels at 9.1 and 11.4 calls/day
- **"Why did you pick those two frameworks?"** BCG is a diagnosis of the starting position and
  Ansoff is a description of the plan. BCG explains why cardiac was never funded — no Star, no Cash
  Cow, nothing that self-funds. Ansoff shows where we chose to play: 93% market penetration, 7%
  product development, diversification left deliberately empty
- **"Isn't A8 your cash cow?"** No — on relative share it is a Dog, 0.162 against the leader. That
  is exactly why we stopped calling it a harvest. A cash cow throws off cash while healthy; A8 is
  losing units at 4.3% a year
- **"What if attrition wrecks it?"** At the industry's 30% you lose 8.8% of field capacity to
  re-ramp every year. Our target is <15% — Torrent runs 16.6%, Sun 13.6%, so it is achievable.
  Levers and costs in Annexure G4
- **"Why build instead of buying in?"** A7's largest buyable asset is ~₹37 Cr of revenue at leader
  share across 54 competitors with no moat — an acquisition premium on a pool anyone can enter.
  Detailing brands Cipla already owns is cheaper than buying share it would then still have to
  detail. A1 is the one place we would look at a brand acquisition; A4 is where we would in-license
- If asked "isn't in-house manufacturing your edge?" — no. Mankind, Aristo, Macleods and IPCA are
  all 100% self-made. It is table stakes. Sun, the largest A7 player, makes none of its own
- If asked "doesn't Mankind have a bigger feeder base?" — yes, 7× bigger. That is why we measured
  conversion rate instead of base size, and why Glenmark at 0.07 on ₹1,140 Cr is the cautionary tale
- If asked "isn't Cresar AMH already stalling?" — yes, we said so on Slide 5. Its pool went from
  +7.0% to +9.2% while the brand went from +38.5% to +4.0%. The pool did not stop; the detailing did
- MNCs are 4.8% of this market — every competitor named in this deck is an Indian company
- Cipla manufactures 137 of 137 of its cardiac SKUs in-house, 100% of value — build, not buy

**If a judge asks the hardest question — "why should we believe you can 4× your share?"**
> We don't ask you to. We ask you to believe we can do what IPCA did — the best share gain anyone in
> this data made from where Cipla stands. That is ₹62 Cr, it breaks even at 16% of it, and the
> ₹201 Cr above it is headroom we have deliberately left on the table.
