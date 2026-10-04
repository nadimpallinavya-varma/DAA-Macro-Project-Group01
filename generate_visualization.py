"""Generates the Greedy Job Sequencing visualizations.
  Visualization.png          - algorithm flowchart (decision logic)
  Visualization_Trace.png    - decision path for the sample input, step by step
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

BLUE, AMBER, GREEN, RED, GREY = "#dbe8fb", "#fff0c2", "#c9efd2", "#f8cdcd", "#444444"
EDGE = {BLUE: "#2f5fa8", AMBER: "#b8860b", GREEN: "#2e8b57", RED: "#c0392b"}

# ---------------------------------------------------------------- flowchart
fig, ax = plt.subplots(figsize=(11, 15))
ax.set_xlim(0, 11); ax.set_ylim(1.5, 16.4); ax.axis("off")

def box(x, y, text, color=BLUE, w=3.6, h=0.8, rounded=True):
    st = "round,pad=0.02,rounding_size=0.35" if rounded else "square,pad=0.02"
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle=st,
                 fc=color, ec=EDGE[color], lw=1.8))
    ax.text(x, y, text, ha="center", va="center", fontsize=10.5)

def diamond(x, y, text, w=3.6, h=1.5):
    ax.add_patch(Polygon([(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)],
                 fc=AMBER, ec=EDGE[AMBER], lw=1.8))
    ax.text(x, y, text, ha="center", va="center", fontsize=10.5)

def arrow(pts, label=None, lpos=None, head=True):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1], ys[:-1], color=GREY, lw=1.6, solid_capstyle="round")
    ax.annotate("", xy=pts[-1], xytext=pts[-2] if len(pts) > 1 else pts[0],
                arrowprops=dict(arrowstyle="-|>" if head else "-", color=GREY, lw=1.6))
    if label:
        ax.text(*lpos, label, fontsize=10, fontweight="bold", color=GREY,
                ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=1))

X = 4.0
ax.text(5.5, 16.0, "Greedy Job Sequencing - Flowchart", ha="center", fontsize=17, fontweight="bold")
box(X, 15.1, "START", GREEN, w=2.0, h=0.7)
box(X, 13.9, "Input jobs: (id, deadline, profit)")
box(X, 12.7, "Sort jobs by profit\n(highest first)")
box(X, 11.5, "Create slots 1..maxDeadline\n(all free)")
diamond(X, 9.9, "More jobs\nleft?")
box(X, 8.4, "Take next job J\nt = min(deadline, maxDeadline)")
diamond(X, 6.7, "Is slot t\nfree?")
box(X, 5.0, "t = t - 1")
diamond(X, 3.5, "t >= 1 ?", h=1.3)

ACC_X = 8.3
box(ACC_X, 6.7, "ACCEPT J in slot t\nprofit += J.profit", GREEN, w=3.2, h=0.9)
box(ACC_X, 3.5, "REJECT J\n(no free slot)", RED, w=3.2, h=0.9)
box(ACC_X, 9.9, "Print schedule\n& total profit", BLUE, w=3.0)
box(ACC_X, 11.5, "END", GREEN, w=2.0, h=0.7)

arrow([(X, 14.75), (X, 14.3)]); arrow([(X, 13.5), (X, 13.1)]); arrow([(X, 12.3), (X, 11.9)])
arrow([(X, 11.1), (X, 10.65)])
arrow([(X, 9.15), (X, 8.8)], "Yes", (X - 0.45, 9.0))
arrow([(X + 1.8, 9.9), (ACC_X - 1.5, 9.9)], "No", (X + 2.4, 10.15))
arrow([(ACC_X, 10.3), (ACC_X, 11.15)])
arrow([(X, 8.0), (X, 7.45)])
arrow([(X + 1.8, 6.7), (ACC_X - 1.6, 6.7)], "Yes", (X + 2.4, 6.95))
arrow([(X, 5.95), (X, 5.4)], "No", (X + 0.4, 5.7))
arrow([(X, 4.6), (X, 4.15)])
# t>=1 yes -> back up to slot-free test
arrow([(X - 1.8, 3.5), (1.0, 3.5), (1.0, 6.7), (X - 1.8, 6.7)])
ax.text(1.9, 3.75, "Yes", fontsize=10, fontweight="bold", color=GREY, ha="center",
        bbox=dict(fc="white", ec="none", pad=1))
# t>=1 no -> reject
arrow([(X + 1.8, 3.5), (ACC_X - 1.6, 3.5)], "No", (X + 2.4, 3.75))
# accept / reject return to loop test
arrow([(ACC_X, 7.15), (ACC_X, 9.0), (X, 9.0)], head=False)
arrow([(10.2, 3.5), (10.2, 9.0), (ACC_X, 9.0)], head=False)
ax.plot([ACC_X + 1.6, 10.2], [3.5, 3.5], color=GREY, lw=1.6)
ax.annotate("", xy=(X, 8.98), xytext=(X + 0.6, 8.98),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
ax.text(ACC_X + 0.3, 9.2, "next job", fontsize=9, style="italic", color=GREY)

# legend
for i, (c, lbl) in enumerate([(BLUE, "Process"), (AMBER, "Decision"),
                              (GREEN, "Accepted / start-end"), (RED, "Rejected")]):
    ax.add_patch(Rectangle((0.5 + i*2.6, 1.9), 0.35, 0.3, fc=c, ec=EDGE[c], lw=1.5))
    ax.text(0.95 + i*2.6, 2.05, lbl, fontsize=9, va="center")
fig.savefig("Visualization.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close(fig)

# --------------------------------------------------------- decision trace
jobs = [("J1", 2, 100), ("J3", 2, 27), ("J4", 1, 25), ("J2", 1, 19), ("J5", 3, 15)]
D = max(d for _, d, _ in jobs)
slots = [None] * (D + 1)
rows, total = [], 0
for jid, d, p in jobs:
    t, checks = d, []
    while t >= 1 and slots[t]:
        checks.append(f"slot {t} taken ({slots[t]})"); t -= 1
    if t >= 1:
        checks.append(f"slot {t} free")
        slots[t] = jid; total += p; res = ("ACCEPT in slot %d" % t, GREEN)
    else:
        res = ("REJECT", RED)
    rows.append((jid, d, p, "; ".join(checks), res, list(slots), total))

fig, ax = plt.subplots(figsize=(13, 8.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 9.2); ax.axis("off")
ax.text(6.5, 8.8, "Decision Path - Sample Run (5 jobs)", ha="center", fontsize=17, fontweight="bold")
heads = [(0.2, "Job"), (1.3, "d"), (2.0, "p"), (2.9, "Checks (latest free slot <= deadline)"),
         (7.4, "Decision"), (9.5, "Slots 1 | 2 | 3"), (12.2, "Profit")]
for x, h in heads:
    ax.text(x, 8.1, h, fontsize=10.5, fontweight="bold", va="center")
ax.plot([0.1, 12.9], [7.8, 7.8], color=GREY, lw=1.2)
for i, (jid, d, p, chk, (dec, col), sl, tot) in enumerate(rows):
    y = 7.0 - i * 1.25
    ax.add_patch(FancyBboxPatch((0.1, y - 0.5), 12.8, 1.0, boxstyle="round,pad=0.02,rounding_size=0.15",
                 fc=col, ec=EDGE[col], lw=1.4, alpha=0.55))
    ax.text(0.2, y, jid, fontsize=12, fontweight="bold", va="center")
    ax.text(1.3, y, str(d), fontsize=11, va="center"); ax.text(2.0, y, str(p), fontsize=11, va="center")
    ax.text(2.9, y, chk, fontsize=10, va="center")
    ax.text(7.4, y, dec, fontsize=11, fontweight="bold", va="center")
    for s in range(1, D + 1):
        x0 = 9.5 + (s - 1) * 0.85
        ax.add_patch(Rectangle((x0, y - 0.28), 0.75, 0.56, fc="white", ec=GREY, lw=1))
        ax.text(x0 + 0.375, y, sl[s] or "-", ha="center", va="center", fontsize=10)
    ax.text(12.2, y, str(tot), fontsize=11, fontweight="bold", va="center")
ax.text(6.5, 0.55, "Final schedule: %s   |   Total profit = %d" %
        (" -> ".join(s for s in slots[1:] if s), total),
        ha="center", fontsize=13, fontweight="bold",
        bbox=dict(fc="#eef3fb", ec=EDGE[BLUE], boxstyle="round,pad=0.4"))
ax.text(6.5, 0.0, "Jobs listed in descending-profit order (after sorting). Green = accepted, red = rejected.",
        ha="center", fontsize=9, style="italic", color=GREY)
fig.savefig("Visualization_Trace.png", dpi=170, bbox_inches="tight", facecolor="white")
