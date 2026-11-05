"""Chapter: 薄层色谱法 / Thin-Layer Chromatography."""
import math
import numpy as np
from common import *

CH = "tlc"
ORA, PUR = "#e8743b", "#a23d9e"


def spot(cv, x, y, w, h, col, alpha=1.0, z=5):
    cv.ax.add_patch(Ellipse((x, y), w, h, fc=col, ec="none", alpha=alpha, zorder=z))


# ------------------------------------------------------------------ 01
def development(cv, t):
    D = 13
    cv.title(L("薄层色谱的展开与比移值 Rf：Rf = 原点到斑点中心的距离 / 原点到溶剂前沿的距离",
               "TLC development and Rf: Rf = distance origin→spot centre / distance origin→solvent front"))
    # tank
    cv.rect(88, 74, 352, 12, fc="#d9d9d9", ec="#888", lw=1)
    cv.text(264, 80, L("盖", "lid"), size=8, color="#666", ha="center")
    cv.rect(92, 86, 346, 388, fc="#f5f8fb", ec="#777", lw=1.6)
    cv.rect(92, 440, 346, 34, fc="#cfe0ef", z=1)
    cv.text(432, 457, L("展开剂", "solvent"), size=9.5, color=C["teal"], ha="right")
    px0, px1, ptop, pbot = 144, 386, 114, 462
    y_or = 424
    cv.rect(px0, ptop, px1 - px0, pbot - ptop, fc="#fbfaf1", ec="#999", lw=1, z=2)
    dev = eseg(t, 2.4, 8.8)
    y_front = lerp(y_or + 8, 150, dev)
    if dev > 0:
        cv.rect(px0, y_front, px1 - px0, pbot - y_front, fc="#e6eef5", z=2)
        cv.line([px0, px1], [y_front, y_front], color=C["teal"], lw=1.5, z=3)
        cv.text(px0 + 4, y_front - 9, L("溶剂前沿", "solvent front"), size=9, color=C["teal"], zorder=4)
    cv.line([px0, px1], [y_or, y_or], color="#888", lw=1, ls=(0, (3, 3)), z=3)
    cv.text(px1 + 4, y_or, L("原点线", "origin"), size=9, color="#666")
    lanes = [(190, [(ORA, 0.30)], L("对照品 A", "Std A")),
             (265, [(ORA, 0.30), (PUR, 0.62)], L("样品", "Sample")),
             (340, [(PUR, 0.62)], L("对照品 B", "Std B"))]
    spot_a = fade(t, 0.3, 1.6)
    for x, sp, lab in lanes:
        cv.text(x, 492, lab, size=10, ha="center")
        for col, rf in sp:
            y = y_or - rf * (y_or - y_front)
            spot(cv, x, y, 22 + 6 * dev, 14 + 2 * dev, col, alpha=spot_a)
    steps = [L("① 点样：在原点线上点对照品和样品", "① Spot standards and sample on the origin line"),
             L("② 展开：放入饱和的展开缸，展开剂借毛细\n    作用沿薄层上升，带动各组分移动",
               "② Develop in a saturated tank: the solvent rises\n    by capillary action and carries the spots"),
             L("③ 取出、标记前沿，显色后计算 Rf", "③ Remove, mark the front, visualise, calculate Rf")]
    cur = 0 if t < 2.2 else (1 if t < 9.2 else 2)
    ys = [110, 172, 236]
    for i, s in enumerate(steps):
        on = i == cur
        cv.text(530, ys[i], s, size=10.5, color=C["green"] if on else "#888", weight="bold" if on else "normal",
                linespacing=1.4, va="top" if "\n" in s else "center")
    dist = (y_or - y_front) / 40
    if 0 < dev and t < 9.2:
        cv.text(530, 330, L(f"前沿已移动 {dist:.1f} cm", f"Front has moved {dist:.1f} cm"), size=12, color=C["teal"])
        cv.lines(530, 356, [L("同一条件下，各组分移动距离与前沿距离", "Under fixed conditions each spot keeps the same"),
                            L("之比（Rf）保持不变", "ratio to the front distance (Rf)")], size=10, gap=22)
    if t >= 9.2:
        a = fade(t, 9.3, 10.0)
        b_len = y_or - y_front
        # measurement arrows
        for x, yy, col in ((214, y_or - 0.30 * b_len, ORA), (364, y_or - 0.62 * b_len, PUR)):
            cv.arrow(x, y_or, x, yy + 2, color=col, lw=1.4, both=True, alpha=a, head=6)
        cv.arrow(404, y_or, 404, y_front, color=C["teal"], lw=1.4, both=True, alpha=a, head=6)
        cv.text(410, (y_or + y_front) / 2, "b", size=11, color=C["teal"], alpha=a, weight="bold")
        cv.text(205, y_or - 0.15 * b_len, "a", size=11, color=ORA, alpha=a, weight="bold", ha="right")
        cv.text(355, y_or - 0.31 * b_len, "a′", size=11, color=PUR, alpha=a, weight="bold", ha="right")
        cv.lines(530, 316, [(L("计算比移值：", "Calculate Rf:"), dict(weight="bold")),
                            (f"Rf(A) = a / b = {0.30 * dist:.1f} / {dist:.1f} = 0.30", dict(color=ORA)),
                            (f"Rf(B) = a′ / b = {0.62 * dist:.1f} / {dist:.1f} = 0.62", dict(color=PUR)),
                            L("样品中两斑点的 Rf 分别与 A、B 一致 →", "The sample spots match A and B in Rf →"),
                            L("初步判断样品含 A 和 B（定性）", "the sample likely contains A and B")],
                 size=10.5, gap=27, alpha=a)


# ------------------------------------------------------------------ 02
SYS = [("9 : 1", 0.20, 0.07), ("4 : 1", 0.52, 0.30), ("1 : 1", 0.88, 0.80)]


def polarity(cv, t):
    D = 11
    dev = eseg(t, 0.6, 8.0)
    cv.title(L("展开剂极性对 Rf 的影响（硅胶板，正相）：展开剂极性增大，各组分 Rf 都增大",
               "Developing-solvent polarity (silica, normal phase): more polar solvent → larger Rf for all"))
    for i, (ratio, rfo, rfb) in enumerate(SYS):
        x0 = 60 + i * 236
        x1 = x0 + 146
        cv.text((x0 + x1) / 2, 92, L("石油醚-乙酸乙酯", "Pet. ether–EtOAc"), size=10, ha="center")
        cv.text((x0 + x1) / 2, 112, ratio, size=10.5, ha="center")
        top, bot, yo = 138, 424, 392
        yf = lerp(yo, 170, dev)
        cv.rect(x0, top, x1 - x0, bot - top, fc="#fbfaf1", ec="#999", lw=1)
        cv.rect(x0, yf, x1 - x0, bot - yf, fc="#e6eef5", z=2)
        cv.line([x0, x1], [yf, yf], color=C["teal"], lw=1.4, z=3)
        cv.line([x0, x1], [yo, yo], color="#888", lw=1, ls=(0, (3, 3)), z=3)
        xc = (x0 + x1) / 2
        for rf, col in ((rfo, ORA), (rfb, C["teal"])):
            y = yo - rf * (yo - yf)
            spot(cv, xc, y, 38, 15, col)
            if t > 8.4:
                cv.text(xc + 26, y, f"{rf:.2f}", size=9, color=col, alpha=fade(t, 8.4, 9.0), weight="bold")
        if t > 8.4:
            good = 0.2 <= rfb and rfo <= 0.8
            tag = (L("Rf 太小，分不开", "Rf too small") if rfo < 0.25 else
                   L("Rf 太大，挤在前沿", "Rf too large") if rfb > 0.75 else L("Rf 适中 ✓", "Rf suitable ✓"))
            cv.text(xc, 446, tag, size=10.5, ha="center", weight="bold",
                    color=C["green"] if 0.25 <= rfo <= 0.8 and rfb >= 0.2 else C["red"], alpha=fade(t, 8.4, 9.0))
    for i, (col, lab) in enumerate(((ORA, L("极性较小的组分", "less polar solute")),
                                    (C["teal"], L("极性较大的组分", "more polar solute")))):
        spot(cv, 752, 190 + i * 40, 18, 12, col)
        cv.text(766, 190 + i * 40, lab, size=10)
    cv.text(744, 300, L("展开剂极性 ↑\n→ 与组分竞争吸附位点\n的能力 ↑\n→ 组分 Rf ↑",
                        "More polar solvent\n→ competes better for\nadsorption sites\n→ every Rf rises"),
            size=10, color=C["navy"], linespacing=1.4, va="top")
    cv.text(473, 482, L("一般使 Rf 落在 0.2～0.8 之间，各斑点分离最好", "Aim for Rf between 0.2 and 0.8 for the best separation"),
            size=10, color=C["green"], ha="center", alpha=fade(t, 9.0, 9.6))


# ------------------------------------------------------------------ 03
AMT = [1, 2, 4, 6]
SAMPLE = 3.2


def _area(m):
    return 10 * m ** 0.88


def densitometry(cv, t):
    D = 14
    cv.title(L("薄层扫描法定量：用光束沿展开方向扫描斑点，斑点吸光度积分（峰面积）与点样量相关",
               "TLC densitometry: a light beam scans each spot; the peak area tracks the amount spotted"))
    px0, px1, ptop, pbot = 34, 344, 76, 440
    cv.rect(px0, ptop, px1 - px0, pbot - ptop, fc="#fbfaf1", ec="#999", lw=1.2)
    cv.line([px0, px1], [104, 104], color=C["teal"], lw=1.3)
    cv.line([px0, px1], [400, 400], color="#999", lw=1, ls=(0, (3, 3)))
    xs_l = [68, 128, 189, 249, 310]
    ys = 266
    amts = AMT + [SAMPLE]
    for i, (x, m) in enumerate(zip(xs_l, amts)):
        a = 0.35 + 0.65 * m / 6
        spot(cv, x, ys, 22 + 5 * m, 16 + 2 * m, "#a23d9e", alpha=a)
        lab = f"{m} μg" if i < 4 else L("样品", "Sample")
        cv.text(x, 455, lab, size=9.5, ha="center", color=C["red"] if i == 4 else C["ink"])
    lane_T = 2.2
    lane = min(4, int(max(0, t - 0.4) / lane_T))
    u = seg(t - 0.4 - lane * lane_T, 0, lane_T * 0.9)
    scanning = t < 0.4 + 5 * lane_T
    bx = xs_l[lane]
    by = lerp(390, 120, u)
    if scanning:
        cv.rect(bx - 22, by - 3, 44, 7, fc="#ffd966", ec="#d4a017", lw=1, z=6)
        cv.arrow(bx + 28, by + 4, bx + 28, by - 20, color="#d4a017", lw=1.4, head=6)
    # profile
    cv.text(426, 66, L(f"当前扫描：{amts[lane]} μg" if lane < 4 else "当前扫描：样品",
                       f"Scanning: {amts[lane]} μg" if lane < 4 else "Scanning: sample"), size=10.5)
    ax = cv.inset(426, 80, 492, 140)
    pos = np.linspace(0, 1, 300)
    m = amts[lane]
    prof = (0.15 + 0.85 * m / 6) * gauss(pos, 0.47, 0.05 + 0.004 * m)
    upto = u if scanning else 1
    k = pos <= upto
    ax.plot(pos[k], prof[k], color="#a23d9e", lw=1.8)
    ax.fill_between(pos[k], prof[k], color="#a23d9e", alpha=0.18, lw=0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(L("吸光度", "Absorbance"))
    ax.set_xlabel(L("扫描位置（展开方向）", "Position along the development direction"), labelpad=2)
    # calibration
    ax2 = cv.inset(426, 296, 492, 152)
    done = [i for i in range(4) if (i < lane) or (i == lane and u >= 0.98)]
    if not scanning:
        done = list(range(4))
    for i in done:
        ax2.plot(AMT[i], _area(AMT[i]), "o", color=C["navy"], ms=7)
    if not scanning or (lane == 4 and u > 0.98):
        al = fade(t, 11.6, 12.2) if not scanning else 0
        mm = np.linspace(0, 7, 100)
        ax2.plot(mm, _area(mm), color=C["navy"], lw=1.4, alpha=al)
        Ay = _area(SAMPLE)
        ax2.plot([SAMPLE], [Ay], "s", color=C["red"], ms=8, alpha=max(al, 0.0001))
        ax2.plot([0, SAMPLE, SAMPLE], [Ay, Ay, 0], ls="--", color=C["red"], lw=1, alpha=al)
        ax2.text(SAMPLE + 0.15, 3, L(f"样品 ≈ {SAMPLE} μg", f"sample ≈ {SAMPLE} μg"), color=C["red"], fontsize=10,
                 fontweight="bold", alpha=al)
    elif lane == 4 and u > 0.6:
        pass
    ax2.set_xlim(0, 7)
    ax2.set_ylim(0, 60)
    ax2.set_yticks([])
    ax2.set_xlabel(L("点样量 / μg", "Amount spotted / μg"), labelpad=1)
    ax2.set_ylabel(L("峰面积", "Peak area"))


ANIMS = [
    ("01-development-rf", development, 13),
    ("02-solvent-polarity", polarity, 11),
    ("03-densitometry", densitometry, 14),
]
