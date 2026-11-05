"""Chapter: 色谱分析法基本理论 / Chromatographic Theory."""
import math
import numpy as np
from common import *

CH = "chromatography-theory"

_rng = np.random.default_rng(5)
_DOTS = _rng.random((260, 2))


# ------------------------------------------------------------------ 01
COMP = [  # colour, tR (s), sigma_t (s), label
    ("#8a8f98", 2.6, 0.18, ("不保留组分", "Unretained")),
    (C["orange"], 5.0, 0.32, ("组分 1（K 小）", "Comp. 1 (small K)")),
    (C["teal"], 8.4, 0.5, ("组分 2（K 大）", "Comp. 2 (large K)")),
]


def separation(cv, t):
    D = 11
    cv.title(L("色谱分离过程：各组分在两相间反复分配，分配系数 K 不同 → 迁移速度不同 → 逐渐分开",
               "Separation: components partition repeatedly between phases; different K → different speeds"))
    x0, x1, yc, h = 70, 650, 180, 70
    t_inj = 0.4
    cv.arrow(70, 116, 190, 116, color=C["teal"], lw=1.6)
    cv.text(200, 116, L("流动相流动方向", "mobile-phase flow"), size=10, color=C["teal"])
    cv.rect(x0, yc - h / 2, x1 - x0, h, fc="#eef2e9", ec="#666", lw=1.6, r=8)
    for (u, v) in _DOTS:
        cv.circle(x0 + 6 + u * (x1 - x0 - 12), yc - h / 2 + 5 + v * (h - 10), 1.1, fc="#a9bfa3", z=1)
    # bands: composite colour profile drawn as one image strip
    import matplotlib.colors as mc
    xs = np.linspace(x0 + 4, x1 - 4, 700)
    img = np.ones((1, len(xs), 4))
    img[..., 3] = 0
    for col, tR, st, _l in COMP:
        if t < t_inj:
            continue
        frac = (t - t_inj) / (tR - t_inj)          # 1 when band centre reaches the outlet
        xc = x0 + frac * (x1 - x0)
        sig = 6 + 0.5 * (st / (tR - t_inj)) * (x1 - x0) * math.sqrt(max(frac, 0.02))
        a = np.clip(0.9 / (1 + 0.04 * sig) * np.exp(-0.5 * ((xs - xc) / sig) ** 2) * 1.6, 0, 0.92)
        rgb = np.array(mc.to_rgb(col))
        A0 = img[0, :, 3].copy()
        out_a = a + A0 * (1 - a)
        for ch in range(3):
            img[0, :, ch] = np.where(out_a > 0, (rgb[ch] * a + img[0, :, ch] * A0 * (1 - a)) / np.maximum(out_a, 1e-6), 1)
        img[0, :, 3] = out_a
    cv.ax.imshow(img, extent=(x0 + 4, x1 - 4, yc + h / 2 - 4, yc - h / 2 + 4), aspect="auto", zorder=2,
                 interpolation="bilinear")
    cv.rect(660, yc - 30, 70, 60, fc="#dfe7f0", ec=C["navy"], lw=1.4)
    cv.text(695, yc, L("检测器", "Detector"), size=10, ha="center", color=C["navy"])
    cv.text(56, 236, L("进样", "inject"), size=9.5, color=C["gray"])
    cv.text(360, 236, L("色谱柱（内装固定相）", "Column (packed with stationary phase)"), size=10, color=C["green"], ha="center")
    for i, (col, tR, st, lab) in enumerate(COMP):
        cv.rect(752, 115 + i * 46, 18, 18, fc=col)
        cv.text(778, 124 + i * 46, L(*lab), size=9.5 if not is_zh() else 10)
    # chromatogram
    ax = cv.inset(66, 292, 700, 152)
    ts = np.linspace(0, max(0.01, t), 600)
    sig = sum(gauss(ts, tR, st) * (0.6 if i == 0 else 1.0) for i, (c_, tR, st, _l) in enumerate(COMP))
    ax.plot(ts, sig, color=C["navy"], lw=1.8)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.05, 1.25)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(L("检测器响应", "Detector response"))
    ax.text(10.5, -0.22, L("时间 t →", "time t →"), ha="right", fontsize=9.5)
    for i, (col, tR, st, lab) in enumerate(COMP):
        if t > tR + 0.1:
            hgt = 0.6 if i == 0 else 1.0
            ax.plot([tR, tR], [0, hgt], ls=":", color=col, lw=1.2)
            lbl = "$t_0$" if i == 0 else f"$t_{{R{i}}}$"
            ax.text(tR, hgt + 0.07, lbl, color=col, ha="center", fontsize=11)


# ------------------------------------------------------------------ 02
def resolution(cv, t):
    D = 13
    if t < 6.5:
        step = 1
        f = eseg(t, 0.6, 5.4)
        d = lerp(1.0, 1.85, f)        # separation of means
        sd = 0.30
    else:
        step = 2
        f = eseg(t, 7.1, 11.9)
        d = 1.0
        sd = lerp(0.30, 0.165, f)
    W = 4 * sd
    R = d / W
    cv.title(L("分离度 R = 2($t_{R2}$ − $t_{R1}$)/($W_1$ + $W_2$)：峰间距越大、峰越窄，分离越好",
               "Resolution R = 2($t_{R2}$ − $t_{R1}$)/($W_1$ + $W_2$): wider spacing and narrower peaks separate better"))
    ax = cv.inset(58, 90, 566, 330)
    xs = np.linspace(0, 4.4, 900)
    m1 = 1.5
    m2 = m1 + d
    g1, g2 = gauss(xs, m1, sd), gauss(xs, m2, sd)
    ax.fill_between(xs, g1, color="#f5c6b0", lw=0)
    ax.fill_between(xs, g2, color="#a9c6d3", lw=0, alpha=0.95)
    ax.fill_between(xs, np.minimum(g1, g2), color="#9a9a9a", lw=0, alpha=0.8)
    ax.plot(xs, g1 + g2, color=C["ink"], lw=2)
    ax.plot([m1, m1], [0, 1], ls=":", color=C["orange"], lw=1)
    ax.plot([m2, m2], [0, 1], ls=":", color=C["teal"], lw=1)
    ax.annotate("", (m2, 1.12), (m1, 1.12), arrowprops=dict(arrowstyle="<->", color="#444", lw=1.2))
    ax.text((m1 + m2) / 2, 1.17, r"$\Delta t_R$", ha="center", fontsize=11, color="#444")
    ax.plot([m1 - W / 2, m1 + W / 2], [-0.06, -0.06], color=C["orange"], lw=3, solid_capstyle="butt")
    ax.plot([m2 - W / 2, m2 + W / 2], [-0.09, -0.09], color=C["teal"], lw=3, solid_capstyle="butt")
    ax.text(m1 - W / 2, -0.17, "W", fontsize=9, color="#555")
    ax.set_xlim(0, 4.4)
    ax.set_ylim(-0.2, 1.3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["bottom"].set_position(("data", -0.12))
    ax.text(4.4, -0.27, L("时间 t →", "time t →"), ha="right", fontsize=9.5)
    st = (L("第一步：峰宽不变，拉大峰间距", "Step 1: same width, larger spacing") if step == 1 else
          L("第二步：峰间距不变，减小峰宽", "Step 2: same spacing, narrower peaks"))
    sub = (L("（提高选择性 α、保留因子 k）", "(raise selectivity α or retention factor k)") if step == 1 else
           L("（提高柱效 n，例如减小填料粒径）", "(raise efficiency n, e.g. smaller particles)"))
    cv.text(656, 120, st, size=11.5 if is_zh() else 10.8, weight="bold", color=C["green"])
    cv.text(662, 160, sub, size=9.5, color=C["gray"])
    col = C["red"] if R < 1 else (C["orange"] if R < 1.5 else C["green"])
    cv.text(656, 224, f"R = {R:.2f}", size=26, weight="bold", color=col)
    msg = (L("两峰明显重叠", "Peaks clearly overlap") if R < 1 else
           L("部分重叠\n（R = 1 时约 98% 分开）", "Partial overlap\n(≈98% separated at R = 1)") if R < 1.5 else
           L("R ≥ 1.5：基线分离\n（分开程度约 99.7%）", "R ≥ 1.5: baseline separation\n(≈99.7% separated)"))
    cv.text(656, 318, msg, size=11, color=C["ink"], linespacing=1.15)
    bx0, bx1 = 656, 916
    cv.rect(bx0, 382, bx1 - bx0, 16, fc="#eeeeee")
    def BX(r):
        return bx0 + (r - 0.4) / 1.3 * (bx1 - bx0)
    cv.rect(bx0, 382, BX(min(R, 1.7)) - bx0, 16, fc=col, alpha=0.9)
    for r in (0.5, 1.0, 1.5):
        cv.line([BX(r)] * 2, [378, 402], color="#888", lw=1)
        cv.text(BX(r), 414, f"{r:.1f}", size=8.5, ha="center", color="#666")
    cv.text(340, 478, L("W：基线峰宽（两侧拐点切线与基线交点间的距离，W = 4σ）",
                        "W: baseline peak width (between tangent intercepts at the inflection points, W = 4σ)"),
            size=9.5, color=C["gray"], ha="center")


# ------------------------------------------------------------------ 03
def _plates(n_tr):
    m = np.zeros(10)
    s = np.zeros(10)
    m[0] = s[0] = 0.5
    out = []
    states = [(m.copy(), s.copy(), None)]
    for k in range(n_tr):
        out.append(m[-1])
        shifted = np.concatenate([[0.0], m[:-1]])
        states.append((shifted.copy(), s.copy(), "shift"))
        tot = shifted + s
        m, s = tot / 2, tot / 2
        states.append((m.copy(), s.copy(), "eq"))
    return states, out


_PL_STATES, _PL_OUT = _plates(42)


def plate_theory(cv, t):
    D = 12
    rate = 3.6
    n = int(clamp((t - 0.4) * rate, 0, 41))
    half = ((t - 0.4) * rate) % 1 > 0.5 if t > 0.4 else False
    idx = min(len(_PL_STATES) - 1, 2 * n + (2 if half else 1)) if t > 0.4 else 0
    m, s, _ = _PL_STATES[idx]
    ntr = n + (1 if t > 0.4 else 0)
    cv.title(L("塔板理论：把色谱柱看成许多“塔板”，组分在每块塔板内达到分配平衡后随流动相转移到下一块",
               "Plate theory: the column as many ‘plates’; equilibrium in each, then the mobile phase moves on"), size=12.5)
    cv.arrow(72, 94, 228, 94, color=C["teal"], lw=1.6)
    cv.text(238, 94, L("流动相每次前移一块塔板", "mobile phase advances one plate per step"), size=10, color=C["teal"])
    cv.text(792, 94, L(f"第 {ntr} 次转移", f"Transfer #{ntr}"), size=11.5, color=C["red"], weight="bold", ha="right")
    pw = 70
    for i in range(10):
        x = 72 + i * (pw + 3)
        cv.rect(x, 110, pw, 62, fc="#e6eef6", ec=C["teal"], lw=1.4)
        cv.rect(x, 174, pw, 62, fc="#e7efe2", ec=C["green"], lw=1.4)
        mx = max(1e-9, max(m.max(), s.max()))
        hm = 56 * m[i] / mx
        hs = 56 * s[i] / mx
        cv.rect(x + 18, 172 - hm, pw - 36, hm, fc="#2e6f8e", z=2)
        cv.rect(x + 18, 236 - hs, pw - 36, hs, fc="#2e6f8e", z=2)
        cv.text(x + pw / 2, 244, str(i + 1), size=8.5, ha="center", color="#555")
    cv.text(812, 141, L("流动相", "mobile"), size=10.5, color=C["teal"])
    cv.text(812, 205, L("固定相", "stationary"), size=10.5, color=C["green"])
    cv.text(245, 284, L("组分在柱内各塔板中的分布", "Amount in each plate"), size=10.5, ha="center")
    ax = cv.inset(58, 298, 378, 132)
    ax.bar(np.arange(1, 11), m + s, color="#4a83a0", width=0.7)
    ax.set_xlim(0.3, 10.7)
    ax.set_ylim(0, max(0.02, (m + s).max()) * 1.12)
    ax.set_xticks(range(1, 11))
    ax.set_yticks([])
    ax.set_xlabel(L("塔板编号", "Plate number"), labelpad=1)
    cv.text(718, 284, L("柱出口的流出曲线", "Elution curve at the outlet"), size=10.5, ha="center")
    ax2 = cv.inset(530, 298, 378, 132)
    outs = _PL_OUT[:ntr]
    ax2.bar(np.arange(1, len(outs) + 1), outs, color=C["orange"], width=0.7)
    ax2.set_xlim(0, 41)
    ax2.set_ylim(0, 0.1)
    ax2.set_yticks([])
    ax2.set_xlabel(L("流出体积（转移次数）", "Eluted volume (number of transfers)"), labelpad=1)
    cv.text(473, 490, L("图中 k = 1（每块塔板内组分在两相中各占一半）；塔板数 n 越大，峰越窄，柱效越高",
                        "Here k = 1 (half in each phase per plate). More plates n → narrower peak, higher efficiency"),
            size=9.5, color=C["green"], ha="center")


# ------------------------------------------------------------------ 04
_PART = [(x, y) for x in range(0, 12) for y in range(3)]
_PATHS = None


def _eddy_paths():
    rng = np.random.default_rng(2)
    paths = []
    for k in range(3):
        pts = [(0, 1.0 + k * 0.0)]
        y = [0.5, 1.5, 1.0][k]
        x = 0
        while x < 12:
            x += 1
            y = clamp(y + rng.choice([-1, 0, 1]) * 0.9, 0.2, 1.9)
            pts.append((x, y))
        paths.append(np.array(pts))
    return paths


_EDDY = _eddy_paths()
_rngB = np.random.default_rng(7)
_BW = _rngB.standard_normal((70, 2))
_rngC = np.random.default_rng(9)
_CSW = _rngC.random((22, 40))


def broadening(cv, t):
    D = 11
    cv.title(L("速率理论：色谱峰展宽的三个原因（H = A + B/u + Cu）",
               "Rate theory: three causes of band broadening (H = A + B/u + Cu)"))
    px0, px1 = 252, 918
    rows = [(76, 116, C["orange"], L("涡流扩散项 A", "Eddy diffusion A"),
             [L("填料颗粒间路径长短不一，", "Paths around particles differ"), L("同时进柱的分子先后到达", "in length: molecules spread out")]),
            (228, 88, C["teal"], L("纵向扩散项 B/u", "Longitudinal diffusion B/u"),
             [L("分子沿柱轴方向自发扩散，", "Molecules diffuse along the column;"), L("流速越慢、停留越久，展宽越大", "slower flow → more time → wider")]),
            (358, 98, C["magenta"], L("传质阻力项 Cu", "Mass transfer Cu"),
             [L("分子进出固定相需要时间，", "Moving in/out of the stationary"), L("流速越快，跟不上平衡，展宽越大", "phase takes time; faster → wider")])]
    for y, h, col, name, desc in rows:
        cv.text(24, y + 24, name, size=12 if is_zh() else 11, weight="bold", color=col)
        cv.lines(24, y + 58, desc, size=9.2 if is_zh() else 8.8, gap=19)
    # A: packed bed
    y0, h0 = 76, 116
    cv.rect(px0, y0, px1 - px0, h0, fc="#f3f6ef", ec="#999", lw=1)
    sx = (px1 - px0) / 12
    for (i, j) in _PART:
        cx = px0 + sx * (i + (0.0 if j % 2 == 0 else 0.5)) + 32
        cy = y0 + 22 + j * 36
        if cx < px1 - 18:
            cv.ax.add_patch(Ellipse((cx, cy), 36, 30, fc="#d0dfc6", ec="#9fb795", lw=1, zorder=2))
    prog = seg(t, 0.4, 10.2)
    for k, P in enumerate(_EDDY):
        xs = px0 + P[:, 0] * sx
        ys = y0 + 10 + P[:, 1] * 48
        cv.line(xs, ys, color=C["orange"], lw=1.1, ls=(0, (3, 2)), alpha=0.6, z=3)
        seglen = np.hypot(np.diff(xs), np.diff(ys))
        cum = np.concatenate([[0], np.cumsum(seglen)])
        dist = prog * 820
        if dist <= cum[-1]:
            i = np.searchsorted(cum, dist) - 1
            i = max(0, min(i, len(seglen) - 1))
            f = (dist - cum[i]) / max(seglen[i], 1e-6)
            mx, my = xs[i] + f * (xs[i + 1] - xs[i]), ys[i] + f * (ys[i + 1] - ys[i])
            cv.circle(mx, my, 6, fc=C["orange"], z=6)
    # B: diffusion cloud
    y0, h0 = 228, 88
    cv.rect(px0, y0, px1 - px0, h0, fc="#f2f6fa", ec="#999", lw=1)
    cv.arrow(806, 216, 902, 216, color=C["teal"], lw=1.2)
    cv.text(796, 216, L("流动相", "mobile phase"), size=9, color=C["teal"], ha="right")
    xc = px0 + 90 + prog * 470
    spread = 8 + 28 * math.sqrt(prog)
    for (a, b) in _BW:
        x = xc + a * spread
        y = y0 + h0 / 2 + b * 16
        if px0 < x < px1:
            cv.circle(x, clamp(y, y0 + 4, y0 + h0 - 4), 2.2, fc=C["teal"], z=4)
    # C: mass transfer
    y0, h0 = 358, 98
    cv.rect(px0, y0, px1 - px0, h0, fc="#f2f6fa", ec="#999", lw=1)
    cv.rect(px0, y0 + h0 - 28, px1 - px0, 28, fc="#ead7ea", z=1)
    cv.text(px1 - 8, y0 + h0 - 14, L("固定相", "stationary phase"), size=9, color=C["magenta"], ha="right")
    nsteps = 40
    for p in range(22):
        x = px0 + 80 + _CSW[p, 0] * 30
        stuck = False
        tt = prog * nsteps
        for s_ in range(int(tt) + 1):
            frac = 1 if s_ < int(tt) else tt - int(tt)
            stuck = _CSW[p, s_ % 40] < 0.45
            if not stuck:
                x += 13 * frac
        y = (y0 + h0 - 14) if stuck else (y0 + 14 + _CSW[p, (p * 7) % 40] * 50)
        if x < px1 - 6:
            cv.circle(x, y, 4, fc=C["magenta"], z=4)
    cv.text(473, 484, L("三者叠加使谱带随时间逐渐变宽；减小填料粒径并使填充均匀、选择合适流速，可减小塔板高度 H",
                        "Together they widen the band over time. Small, evenly packed particles and a suitable flow rate reduce H"),
            size=9.5, color=C["green"], ha="center")


# ------------------------------------------------------------------ 05
VA, VB, VC = 1.0, 1.6, 0.45


def van_deemter(cv, t):
    D = 12
    uopt = math.sqrt(VB / VC)
    if t < 8:
        u = lerp(0.45, 5.6, 0.5 - 0.5 * math.cos(math.pi * seg(t, 0.4, 7.6)))
    else:
        u = lerp(5.6, uopt, eseg(t, 8.0, 10.0))
    H = VA + VB / u + VC * u
    cv.title(L("Van Deemter 方程：H = A + B/u + Cu —— 塔板高度 H 随流速 u 的变化",
               "Van Deemter equation: H = A + B/u + Cu — plate height H versus flow velocity u"))
    ax = cv.inset(66, 82, 530, 352)
    us = np.linspace(0.25, 6, 400)
    ax.plot(us, VA + 0 * us, "--", color=C["orange"], lw=1.4, label=L("A（涡流扩散）", "A (eddy diffusion)"))
    ax.plot(us, VB / us, "--", color=C["teal"], lw=1.4, label=L("B/u（纵向扩散）", "B/u (longitudinal)"))
    ax.plot(us, VC * us, "--", color=C["magenta"], lw=1.4, label=L("Cu（传质阻力）", "Cu (mass transfer)"))
    ax.plot(us, VA + VB / us + VC * us, color=C["navy"], lw=2.4, label=L("H（总和）", "H (total)"))
    ax.axvline(u, color="#aaa", lw=0.8, ls=":")
    ax.plot([u], [H], "o", color=C["red"], ms=9, zorder=5)
    if t > 9.5:
        ax.annotate(L("$u_{opt}$", "$u_{opt}$"), (uopt, VA + 2 * math.sqrt(VB * VC)), (uopt + 0.3, 1.6),
                    color=C["green"], fontsize=11, arrowprops=dict(arrowstyle="->", color=C["green"], alpha=fade(t, 9.5, 10)), alpha=fade(t, 9.5, 10))
    ax.set_xlim(0, 6.2)
    ax.set_ylim(0, 5.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(L("流动相线速度 u", "Mobile-phase linear velocity u"))
    ax.set_ylabel(L("塔板高度 H", "Plate height H"))
    ax.legend(loc="upper center", ncol=2, frameon=False, fontsize=9)
    # stacked bar
    bx, by0, scale = 676, 432, 38
    parts = [(VA, C["orange"], "A"), (VB / u, C["teal"], "B/u"), (VC * u, C["magenta"], "Cu")]
    y = by0
    for v, col, lab in parts:
        hh = v * scale
        cv.rect(bx, y - hh, 66, hh, fc=col, ec="white", lw=1)
        if hh > 14:
            cv.text(bx + 33, y - hh / 2, lab, size=9.5, color="white", ha="center", weight="bold")
        y -= hh
    cv.text(bx + 33, y - 12, f"H = {H:.2f}", size=11, weight="bold", ha="center")
    if abs(u - uopt) < 0.35:
        msg, col = L("接近最佳流速：\nH 最小，柱效最高", "Near the optimum:\nH is minimal,\nbest efficiency"), C["green"]
    elif u < uopt:
        msg, col = L("流速太低：\n纵向扩散 B/u\n占主导", "Too slow:\nlongitudinal\ndiffusion B/u\ndominates"), C["red"]
    else:
        msg, col = L("流速太高：\n传质阻力 Cu\n占主导", "Too fast:\nmass transfer\nresistance Cu\ndominates"), C["red"]
    cv.text(770, 200, msg, size=12, color=col, linespacing=1.4, va="center")
    cv.text(770, 370, L("实际工作中常略高于\n$u_{opt}$，以缩短分析时间", "In practice u is set a little\nabove $u_{opt}$ to save time"),
            size=9.5, color="#666", linespacing=1.3)
    cv.text(330, 478, L(r"最佳线速度 $u_{opt}=\sqrt{B/C}$，此时 $H_{min}=A+2\sqrt{BC}$",
                        r"Optimum velocity $u_{opt}=\sqrt{B/C}$, where $H_{min}=A+2\sqrt{BC}$"), size=11.5, ha="center")


ANIMS = [
    ("01-separation-process", separation, 11),
    ("02-resolution", resolution, 13),
    ("03-plate-theory", plate_theory, 12.5),
    ("04-band-broadening", broadening, 11),
    ("05-van-deemter", van_deemter, 12),
]
