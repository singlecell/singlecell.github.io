"""Chapter: 经典液相色谱法 / Classical Liquid Chromatography."""
import math
import numpy as np
import matplotlib.colors as mc
from common import *

CH = "classical-lc"


def band_strip(cv, x0, x1, y0, y1, comps, bg, vertical=False):
    """Draw a column interior as an image: comps = [(colour, centre, sigma, peak_alpha)] in px along the axis."""
    n = 500
    if vertical:
        pos = np.linspace(y0, y1, n)
    else:
        pos = np.linspace(x0, x1, n)
    rgb = np.tile(np.array(mc.to_rgb(bg)), (n, 1))
    for col, c, s, a0 in comps:
        a = np.clip(a0 * np.exp(-0.5 * ((pos - c) / s) ** 2), 0, 1)[:, None]
        rgb = rgb * (1 - a) + np.array(mc.to_rgb(col))[None, :] * a
    img = rgb[:, None, :] if vertical else rgb[None, :, :]
    cv.ax.imshow(img, extent=(x0, x1, y1, y0), aspect="auto", zorder=2, interpolation="bilinear")


_rng = np.random.default_rng(21)
_GRAIN = _rng.random((160, 2))


def grains(cv, x0, x1, y0, y1, n=120, col="#c9c3b0", r=1.1):
    for (u, v) in _GRAIN[:n]:
        cv.circle(x0 + 3 + u * (x1 - x0 - 6), y0 + 3 + v * (y1 - y0 - 6), r, fc=col, z=3)


# ------------------------------------------------------------------ 01
_SOLV = np.random.default_rng(4).random((26, 3))
_ANA = np.random.default_rng(8).random((6, 3))


def competitive(cv, t):
    D = 12
    p = eseg(t, 0.6, 10.0)
    ea = 7 + 73 * p                       # % ethyl acetate
    cv.title(L("吸附色谱中的竞争吸附：洗脱剂极性越大，越能把组分从硅胶表面“顶替”下来",
               "Competitive adsorption: a more polar eluent displaces solutes from the silica surface"))
    bx0, bx1, by0, sy = 28, 578, 100, 380
    cv.rect(bx0, by0, bx1 - bx0, sy - by0, fc="#f1f6fb", z=0)
    cv.rect(bx0, sy, bx1 - bx0, 74, fc="#efe9da", z=0)
    cv.text(bx1 - 8, sy + 46, L("硅胶表面", "silica surface"), size=10, color="#9a8a62", ha="right")
    cv.arrow(450, 120, 552, 120, color=C["teal"], lw=1.3)
    cv.text(440, 120, L("洗脱剂流动", "eluent flow"), size=9.5, color=C["teal"], ha="right")
    sites = [62 + i * 54 for i in range(10)]
    for x in sites:
        cv.circle(x, sy, 8, fc="#e06666", z=2)
        cv.text(x, sy + 18, "Si–OH", size=7.5, color="#b04a4a", ha="center")
    ana_sites = [0, 2, 3, 5, 6, 8]
    thr = [0.15, 0.32, 0.5, 0.64, 0.8, 1.2]       # p at which each solute is displaced
    order = [4, 1, 3, 0, 5, 2]
    n_ads = 0
    occupied = set()
    for j in range(6):
        sx = sites[ana_sites[j]]
        th = thr[order[j]]
        d = eseg(p, th, th + 0.1)
        fx = bx0 + 30 + ((j * 88 + 55 * t) % (bx1 - bx0 - 60))
        fy = 160 + (j % 3) * 62 + 10 * math.sin(t * 1.3 + j)
        x, y = lerp(sx, fx, d), lerp(sy - 22, fy, d)
        if d < 0.5:
            n_ads += 1
            occupied.add(ana_sites[j])
        cv.ax.add_patch(Ellipse((x, y), 34, 36, fc=C["teal"], ec="none", zorder=5))
    # solvent molecules
    for i, (a, b, c_) in enumerate(_SOLV):
        polar = a < ea / 100
        x = bx0 + 12 + ((b * (bx1 - bx0 - 24) + 70 * t * (0.6 + c_)) % (bx1 - bx0 - 24))
        y = 140 + c_ * 200
        cv.ax.add_patch(Ellipse((x, y), 13, 12, fc=C["orange"] if polar else "#b9b9b9", ec="none", zorder=4))
    # polar solvent molecules bound on free sites
    for k, x in enumerate(sites):
        if k in occupied:
            continue
        if ea / 100 > 0.15 + 0.08 * ((k * 7) % 10) / 10 * 6:
            cv.ax.add_patch(Ellipse((x, sy - 16), 16, 16, fc=C["orange"], ec="none", zorder=4))
    leg = [(C["teal"], L("待分离组分（极性）", "Solute (polar)")),
           (C["orange"], L("极性溶剂分子（如乙酸乙酯）", "Polar solvent (e.g. ethyl acetate)")),
           ("#b9b9b9", L("非极性溶剂分子（如正己烷）", "Non-polar solvent (e.g. hexane)"))]
    for i, (col, lab) in enumerate(leg):
        cv.ax.add_patch(Ellipse((624, 136 + i * 35), 20, 12, fc=col, ec="none"))
        cv.text(642, 136 + i * 35, lab, size=10 if is_zh() else 9.3)
    cv.text(624, 238, L(f"正己烷 : 乙酸乙酯  ≈  {100 - ea:.0f} : {ea:.0f}", f"Hexane : ethyl acetate  ≈  {100 - ea:.0f} : {ea:.0f}"),
            size=10.5)
    cv.text(912, 268, L(f"被吸附的组分：{n_ads}/6", f"Solutes adsorbed: {n_ads}/6"), size=10.5, weight="bold",
            color=C["teal"], ha="right")
    ax = cv.inset(624, 254, 294, 182)
    xs = np.linspace(0, 1, 200)
    k = lambda x: 0.08 + 0.9 * np.exp(-2.6 * x)
    ax.plot(xs, k(xs), color=C["navy"], lw=2)
    ax.plot([p], [k(p)], "o", color=C["red"], ms=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(L("洗脱剂极性 →", "Eluent polarity →"))
    ax.set_ylabel(L("组分保留（k）", "Retention (k)"))
    cv.text(473, 484, L("组分分子与溶剂分子竞争硅胶表面的吸附位点（硅醇基）：洗脱剂极性↑ → 组分被吸附越少 → 迁移越快、k 越小",
                        "Solute and solvent compete for silanol sites: eluent polarity ↑ → less solute adsorbed → faster, smaller k"),
            size=9.5, color=C["green"], ha="center")


# ------------------------------------------------------------------ 02
def np_rp(cv, t):
    D = 12
    cv.title(L("正相与反相色谱：固定相与流动相的极性相反，组分的洗脱顺序也相反",
               "Normal vs reversed phase: opposite phase polarities give opposite elution orders"))
    panels = [(28, L("正相色谱", "Normal phase"),
               L("固定相：硅胶（极性）  流动相：正己烷-乙酸乙酯（弱极性）", "Stationary: silica (polar)   Mobile: hexane–EtOAc (weakly polar)"),
               (C["orange"], 3.6), (C["teal"], 7.4)),
              (500, L("反相色谱", "Reversed phase"),
               L("固定相：C18（非极性）  流动相：甲醇-水（极性）", "Stationary: C18 (non-polar)   Mobile: methanol–water (polar)"),
               (C["teal"], 3.6), (C["orange"], 7.4))]
    for x0, name, sub, fast, slow in panels:
        cv.text(x0, 94, name, size=12.5, weight="bold", color=C["green"])
        cv.text(x0, 128, sub, size=9.5 if is_zh() else 8.8, color="#555")
        cx0, cx1, cy0, cy1 = x0 + 6, x0 + 62, 182, 438
        cv.text(x0 + 34, 166, "↓", size=13, color=C["teal"], ha="center")
        comps = []
        for col, tR in (fast, slow):
            f = (t - 0.4) / (tR - 0.4)
            if 0 <= f <= 1.12:
                c = cy0 + f * (cy1 - cy0)
                s = 6 + 10 * f
                comps.append((col, c, s, 0.85))
        band_strip(cv, cx0, cx1, cy0, cy1, comps, "#f1f1ec", vertical=True)
        cv.rect(cx0, cy0, cx1 - cx0, cy1 - cy0, ec="#666", lw=1.3, z=4)
        grains(cv, cx0, cx1, cy0, cy1, n=90, col="#c6c6bb", r=1.0)
        ax = cv.inset(x0 + 104, 182, 284, 242)
        ts = np.linspace(0, max(0.01, t), 500)
        sig = sum(gauss(ts, tR + 0.5, 0.32 + 0.04 * tR) for col, tR in (fast, slow))
        ax.plot(ts, sig, color=C["navy"], lw=1.8)
        for col, tR in (fast, slow):
            if t > tR + 1.2:
                xx = np.linspace(tR - 1, tR + 2, 200)
                ax.fill_between(xx, gauss(xx, tR + 0.5, 0.32 + 0.04 * tR), color=col, alpha=0.4, lw=0)
        ax.set_xlim(0, 11)
        ax.set_ylim(0, 1.15)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(11, -0.1, L("时间 →", "time →"), ha="right", fontsize=9)
    cv.text(28, 478, L("相似相吸：", "Like attracts like: "), size=10.5, weight="bold", color=C["green"])
    cv.text(28 + (78 if is_zh() else 130), 478, L("与固定相极性相近的组分保留更强", "solutes resembling the stationary phase are retained longer"),
            size=10.5)
    for i, (col, lab) in enumerate(((C["orange"], L("非极性组分", "non-polar solute")),
                                    (C["teal"], L("极性组分", "polar solute")))):
        cv.rect(612 + i * 150, 470, 16, 16, fc=col)
        cv.text(634 + i * 150, 478, lab, size=10.5)


# ------------------------------------------------------------------ 03
PIG = [("#e8a01d", 3.3, ("胡萝卜素（橙黄）", "Carotene (orange)")),
       ("#c9c42a", 6.3, ("叶黄素（黄）", "Xanthophyll (yellow)")),
       ("#3c8c34", 9.3, ("叶绿素（绿）", "Chlorophyll (green)"))]


def column_chrom(cv, t):
    D = 13
    cv.title(L("柱色谱的操作：装柱 → 加样 → 洗脱 → 分段收集", "Column chromatography: pack → load → elute → collect fractions"))
    cx0, cx1 = 106, 166
    ytop, ysil, ybot = 92, 158, 418
    cv.rect(cx0, ytop + 6, cx1 - cx0, ysil - ytop - 6, fc="#e2edf6", z=1)
    cv.text(cx0 - 10, 128, L("洗脱剂", "eluent"), size=10, color=C["teal"], ha="right")
    comps = []
    for col, tR, _l in PIG:
        f = (t - 0.6) / (tR - 0.6)
        if f < 1.15:
            c = ysil + 8 + max(0, f) * (ybot - ysil - 8)
            comps.append((col, c, 5 + 12 * max(0, f), 0.9))
    band_strip(cv, cx0, cx1, ysil, ybot, comps, "#f2efe4", vertical=True)
    grains(cv, cx0, cx1, ysil, ybot, n=140, col="#cdc6ae", r=0.9)
    cv.rect(cx0, ybot, cx1 - cx0, 16, fc="#e6d6a8", z=3)
    cv.line([cx0, cx0, cx0 + 24, cx0 + 24], [ytop, ybot + 16, ybot + 34, ybot + 52], color="#777", lw=1.6, z=5)
    cv.line([cx1, cx1, cx1 - 24, cx1 - 24], [ytop, ybot + 16, ybot + 34, ybot + 52], color="#777", lw=1.6, z=5)
    cv.line([cx0 + 24, cx1 - 24], [ybot + 34, ybot + 34], color="#777", lw=1.2, z=5)
    cv.line([cx0 - 2, cx1 + 2], [ytop, ytop], color="#777", lw=2, z=5)
    cv.text(cx0 - 10, 290, L("硅胶\n（吸附剂）", "silica\n(adsorbent)"), size=9.5, color="#9a8a62", ha="right", linespacing=1.1)
    cv.arrow(183, 205, 183, 305, color=C["teal"], lw=1.6)
    cv.text(193, 250, L("洗脱剂在重力\n作用下向下流动", "eluent flows\ndown by gravity"), size=9.5, color=C["teal"], linespacing=1.1)
    # fractions
    ntube = 9
    tube_t = [1.2 * k + 1.0 for k in range(ntube + 1)]
    cur = None
    for k in range(ntube):
        tx = 272 + k * 27
        ta, tb = tube_t[k], tube_t[k + 1]
        cv.rect(tx - 9, 392, 18, 82, fc="white", ec="#888", lw=1.1, r=6, z=2)
        if t < ta:
            continue
        fill = eseg(t, ta, tb)
        if ta <= t < tb:
            cur = tx
        # colour = pigments eluting in this window
        w = []
        for col, tR, _l in PIG:
            mid = (ta + tb) / 2
            w.append((col, math.exp(-0.5 * ((mid - tR - 0.6) / 0.75) ** 2)))
        tot = sum(v for _c, v in w)
        if tot < 0.08:
            col = "#dde9f3"
        else:
            rgb = sum(np.array(mc.to_rgb(c)) * v for c, v in w) / tot
            col = tuple(np.array(mc.to_rgb("#f4f4ee")) * (1 - min(1, tot)) + rgb * min(1, tot))
        hh = 72 * fill
        cv.rect(tx - 8, 472 - hh, 16, hh, fc=col, z=3, r=4)
    if cur is not None:
        u = np.linspace(0, 1, 60)
        p0, p1, p2 = np.array([136, ybot + 52]), np.array([(136 + cur) / 2, 300]), np.array([cur, 386])
        pts = ((1 - u) ** 2)[:, None] * p0 + (2 * u * (1 - u))[:, None] * p1 + (u ** 2)[:, None] * p2
        cv.line(pts[:, 0], pts[:, 1], color="#9ab", lw=1.4, z=1)
    cv.text(380, 492, L("按体积分段收集流出液", "collect the eluate in fractions"), size=10.5, ha="center")
    cv.text(548, 88, L("以菠菜色素的分离为例", "Example: spinach pigments"), size=11.5, weight="bold", color=C["green"])
    for i, (col, tR, lab) in enumerate(PIG):
        cv.rect(548, 145 + i * 42, 24, 22, fc=col)
        cv.text(584, 156 + i * 42, L(*lab), size=10.5)
    cv.lines(548, 300, [L("极性小的胡萝卜素吸附最弱，最先被洗下；", "Non-polar carotene is held least and elutes first;"),
                        L("极性大的叶绿素吸附最强，最后流出。", "polar chlorophyll is held most and elutes last.")], size=10.5, gap=24)
    cv.lines(548, 388, [L("洗脱不动时，可逐步增大洗脱剂的极性", "If bands stop moving, raise the eluent polarity"),
                        L("（梯度洗脱）", "step by step (gradient elution)")], size=10, gap=23, color="#555")


ANIMS = [
    ("01-competitive-adsorption", competitive, 12),
    ("02-elution-order", np_rp, 12),
    ("03-column-chromatography", column_chrom, 13),
]
