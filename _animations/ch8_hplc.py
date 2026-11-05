"""Chapter: 高效液相色谱法 / HPLC."""
import math
import numpy as np
from common import *

CH = "hplc"
SAMPLE = C["magenta"]
MOBILE = "#7fb0d6"


# ------------------------------------------------------------------ 01
def pump(cv, t):
    D = 12
    period = 3.0
    ph = (t % period) / period * 2 * math.pi
    disp = -math.cos(ph)                      # -1 retracted .. +1 pushed in
    vel = math.sin(ph)                        # >0 delivering
    deliver = vel > 0
    cv.title(L("柱塞往复泵：凸轮带动柱塞往复运动，两个单向阀交替开闭，把流动相连续“推”向色谱柱",
               "Reciprocating piston pump: a cam drives the piston; two check valves open alternately"))
    cv.rect(28, 228, 60, 70, fc="#e6e6e6", ec="#777", lw=1)
    cv.text(58, 263, L("电动机", "Motor"), size=9.5, ha="center")
    cv.circle(143, 263, 38, fc="#d0d6dc", ec="#555", lw=1.4, z=2)
    cv.text(143, 316, L("凸轮", "Cam"), size=9.5, ha="center")
    ex, ey = 143 + 16 * math.cos(ph + math.pi), 263 + 16 * math.sin(ph + math.pi)
    cv.line([143, ex], [263, ey], color="#555", lw=2, z=3)
    cv.circle(ex, ey, 5, fc="#555", z=4)
    # cylinder
    cv.rect(244, 207, 131, 111, fc="#d6e7f5", ec="#333", lw=1.6, z=2)
    px = 181 + 34 * (disp + 1) / 2
    cv.rect(181, 253, px - 181 + 60, 20, fc="#8fa3b0", ec="#556", lw=1, z=3)
    cv.rect(240, 246, 6, 34, fc="#5c6b78", z=4)
    cv.text(200, 240, L("柱塞", "Piston"), size=9, color="#556", ha="center")
    cv.text(222, 300, L("密封圈", "Seal"), size=8.5, color="#556", ha="center")
    # valves
    for y, top, is_out in ((182, True, True), (348, False, False)):
        open_ = deliver if is_out else not deliver
        cv.rect(317, y - 23, 36, 46, fc="white", ec="#555", lw=1.1, z=3)
        cv.poly([(320, y + 21), (350, y + 21), (342, y + 7), (328, y + 7)], fc="#bbb", ec="#777", z=4)
        by = y - 6 + (-4 if open_ and is_out else 4 if open_ else 0)
        cv.circle(335, by, 9, fc=C["red"] if open_ else C["purple"], z=5)
        lab = (L("出口单向阀", "Outlet check valve") if is_out else L("进口单向阀", "Inlet check valve"))
        st = L("（开）", " (open)") if open_ else L("（关）", " (closed)")
        cv.text(362, y, lab + st, size=9.5, color=C["green"] if open_ else "#777")
    cv.line([335, 335, 456], [159, 121, 121], color="#555", lw=2, z=2)
    cv.text(462, 121, L("→ 色谱柱", "→ column"), size=10)
    cv.line([335, 335, 456], [371, 409, 409], color="#555", lw=2, z=2)
    cv.text(462, 409, L("← 储液瓶", "← reservoir"), size=10)
    for k in range(4):
        f = ((t * 1.2 + k / 4) % 1)
        if deliver:
            x, y = (335, lerp(159, 121, f * 2)) if f < 0.5 else (lerp(335, 450, (f - 0.5) * 2), 121)
        else:
            x, y = (lerp(450, 335, f * 2), 409) if f < 0.5 else (335, lerp(409, 371, (f - 0.5) * 2))
        cv.circle(x, y, 3.2, fc=C["teal"], z=6)
    msg = (L("排液冲程：柱塞推入，出口阀开、进口阀关", "Delivery stroke: piston in, outlet open, inlet closed") if deliver else
           L("吸液冲程：柱塞退出，进口阀开、出口阀关", "Fill stroke: piston out, inlet open, outlet closed"))
    cv.text(130, 446, msg, size=11, weight="bold", color=C["red"])
    # flow plots
    ts = np.linspace(0, t, 500)
    single = np.maximum(0, np.sin(ts / period * 2 * math.pi))
    dual = 1 + 0.06 * np.sin(ts / period * 4 * math.pi)
    cv.text(588, 88, L("单泵：输液脉动大", "Single piston: strongly pulsed flow"), size=10.5, color=C["orange"])
    ax = cv.inset(588, 100, 330, 138)
    ax.plot(ts, single, color=C["orange"], lw=1.8)
    ax.set_xlim(0, D)
    ax.set_ylim(-0.05, 1.25)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(L("流量", "Flow"))
    cv.text(588, 280, L("双泵串联补偿：流量基本恒定", "Two pistons in series: nearly constant flow"), size=10.5, color=C["green"])
    ax2 = cv.inset(588, 292, 330, 138)
    ax2.plot(ts, dual, color=C["green"], lw=1.8)
    ax2.set_xlim(0, D)
    ax2.set_ylim(-0.05, 1.6)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_ylabel(L("流量", "Flow"))
    ax2.text(D, -0.3, L("时间 →", "time →"), ha="right", fontsize=9)
    cv.text(588, 476, L("液缸容积小，流量由电机转速调节，不受柱阻影响", "Flow is set by motor speed, not by column back-pressure"),
            size=9.5, color="#555")


# ------------------------------------------------------------------ 02
ISO2 = [("1", 2.3, 0.35, 0.8), ("2", 2.6, 0.38, 0.65), ("3", 3.9, 0.45, 0.4),
        ("4", 7.5, 0.75, 0.3), ("5", 15.6, 1.4, 0.16), ("6", 33.0, 2.8, 0.07)]
GRAD = [("1", 3.5), ("2", 6.5), ("3", 10.5), ("4", 15.0), ("5", 19.5), ("6", 24.0)]


def gradient(cv, t):
    D = 12
    tm = lerp(0, 40, seg(t, 0.3, 10.0))
    cv.title(L("等度洗脱与梯度洗脱：组分性质差别大时，梯度洗脱使各组分都能在合适的 k 值下流出",
               "Isocratic vs gradient elution: with very different solutes, a gradient elutes each at a suitable k"),
             size=13 if is_zh() else 12)
    rows = [(84, L("等度洗脱（甲醇-水 30 : 70，组成不变）", "Isocratic (methanol–water 30 : 70, constant)"), "iso"),
            (296, L("梯度洗脱（甲醇 10% → 90%，比例随时间增加）", "Gradient (methanol 10% → 90% over time)"), "grad")]
    for y0, name, kind in rows:
        cv.text(66, y0 - 12, name, size=11.5, weight="bold", color=C["teal"] if kind == "iso" else C["green"])
        ax = cv.inset(66, y0, 624, 152)
        ts = np.linspace(0, max(0.01, tm), 900)
        if kind == "iso":
            sig = sum(h * np.exp(-0.5 * ((ts - c) / w) ** 2) for _n, c, w, h in ISO2)
            comp = 30 + 0 * ts
            peaks = [(n, c, h) for n, c, w, h in ISO2]
        else:
            sig = sum(0.8 * np.exp(-0.5 * ((ts - c) / 0.4) ** 2) for _n, c in GRAD)
            comp = np.clip(10 + 80 * (ts - 1) / 27, 10, 90)
            peaks = [(n, c, 0.8) for n, c in GRAD]
        ax.plot(ts, sig, color=C["navy"], lw=1.5)
        for n, c, h in peaks:
            if tm > c + 0.3:
                ax.text(c + (0.6 if n == "2" and kind == "iso" else 0), h + 0.05, n, fontsize=8.5, ha="center", color="#555")
        ax.set_xlim(0, 40)
        ax.set_ylim(0, 1.05)
        ax.set_yticks([])
        if kind == "grad":
            ax.set_xlabel(L("时间 / min", "Time / min"), labelpad=1)
        ax2 = ax.twinx()
        ax2.plot(ts, comp, "--", color=C["orange"], lw=1.2)
        ax2.set_ylim(0, 100)
        ax2.set_yticks([10, 30, 90])
        ax2.tick_params(labelsize=8, colors=C["orange"])
        ax2.spines["right"].set_visible(True)
        ax2.spines["right"].set_color(C["orange"])
        ax2.spines["top"].set_visible(False)
        ax2.set_ylabel(L("甲醇 / %", "MeOH / %"), color=C["orange"], fontsize=8.5)
    if tm >= 39:
        cv.text(690, 228, L("6 号峰 > 40 min 才流出", "peak 6 elutes after 40 min"), size=9, color=C["red"], ha="right",
                alpha=fade(t, 9.8, 10.3))
    cv.text(756, 100, L("等度", "Isocratic"), size=11.5, weight="bold", color=C["teal"])
    cv.lines(758, 128, [L("• 前面的峰挤在一起", "• early peaks crowd"), L("• 后面的峰出得慢，", "• late peaks are slow,"),
                        L("  峰宽而矮，难以检测", "  broad and hard to detect")], size=9.5, gap=19)
    cv.text(756, 312, L("梯度", "Gradient"), size=11.5, weight="bold", color=C["green"])
    cv.lines(758, 340, [L("• 有机相比例逐渐增大，", "• organic share rises,"), L("  洗脱能力逐渐增强", "  eluting power grows"),
                        L("• 峰间距均匀、峰形窄，", "• even spacing, sharp"), L("  分析时间短", "  peaks, shorter run")],
             size=9.5, gap=19)


# ------------------------------------------------------------------ 03
def _port(i, r=100, cx=290, cy=276):
    a = math.radians(90 - 60 * i)     # i=0 top, clockwise
    return cx + r * math.cos(a), cy - r * math.sin(a)


def _groove(cv, i, j, col, lw=5, cx=290, cy=276):
    a0, a1 = math.radians(90 - 60 * i), math.radians(90 - 60 * j)
    angs = np.linspace(a0, a1, 30)
    r = 100 - 22 * np.sin(np.linspace(0, math.pi, 30))
    cv.line(cx + r * np.cos(angs), cy - r * np.sin(angs), color=col, lw=lw, z=4)


def six_port(cv, t):
    D = 13
    cv.title(L("六通进样阀：装样时样品充满定量环，切换到进样后被流动相带入色谱柱",
               "Six-port injection valve: fill the loop in LOAD, then switch to INJECT to send it to the column"))
    cx, cy = 290, 276
    # ports: 0 top (loop end A), 1 upper-right (pump), 2 lower-right (column), 3 bottom (loop end B), 4 lower-left (waste), 5 upper-left (syringe)
    load_end, rot_end = 5.4, 6.6
    rot = eseg(t, load_end, rot_end)
    inject = t >= rot_end
    loop_fill = eseg(t, 0.6, 4.6) if not inject else 1 - eseg(t, rot_end + 0.3, rot_end + 3.5)
    loop_col_sample = SAMPLE
    # loop tubing (outer)
    P0, P3 = _port(0), _port(3)
    lx = 90
    loop_pts_x = [P0[0], P0[0], lx, lx, P3[0], P3[0]]
    loop_pts_y = [P0[1], 122, 122, 430, 430, P3[1]]
    base = "#c0c0c0"
    cv.line(loop_pts_x, loop_pts_y, color=base, lw=5, z=2)
    # sample filling along loop (from port 5 side: enters at port 0 in LOAD)
    seglen = np.hypot(np.diff(loop_pts_x), np.diff(loop_pts_y))
    cum = np.concatenate([[0], np.cumsum(seglen)])
    total = cum[-1]
    def partial(f0, f1, col):
        if f1 <= f0:
            return
        xs, ys = [], []
        for s in np.linspace(f0 * total, f1 * total, 120):
            i = min(len(seglen) - 1, np.searchsorted(cum, s) - 1)
            i = max(i, 0)
            u = (s - cum[i]) / seglen[i]
            xs.append(loop_pts_x[i] + u * (loop_pts_x[i + 1] - loop_pts_x[i]))
            ys.append(loop_pts_y[i] + u * (loop_pts_y[i + 1] - loop_pts_y[i]))
        cv.line(xs, ys, color=col, lw=5, z=3)
    if not inject:
        partial(0, loop_fill, loop_col_sample)
    else:
        # mobile phase enters at port 0 end pushing sample out at port 3
        pushed = 1 - loop_fill
        partial(0, pushed, MOBILE)
        partial(pushed, 1, loop_col_sample)
    cv.text(P0[0] - 160, 100, L("定量环（如 20 μL）", "Sample loop (e.g. 20 μL)"), size=10)
    # external lines
    p1, p2, p4, p5 = _port(1), _port(2), _port(4), _port(5)
    cv.line([p1[0], 450], [p1[1], p1[1]], color=MOBILE, lw=5, z=2)
    cv.text(456, p1[1], L("来自高压泵（流动相）", "from pump"), size=10)
    col_out = MOBILE if not inject else (SAMPLE if loop_fill > 0.02 and t < rot_end + 3.8 else MOBILE)
    cv.line([p2[0], 450], [p2[1], p2[1]], color=col_out, lw=5, z=2)
    cv.text(456, p2[1], L("至色谱柱", "to column"), size=10)
    cv.line([p5[0], 150], [p5[1], p5[1]], color=SAMPLE if not inject and t < 4.8 else "#999", lw=4, z=2)
    cv.text(108, 210, L("注射器进样", "syringe"), size=10)
    cv.line([p4[0], 150], [p4[1], p4[1]], color=SAMPLE if (not inject and 3.6 < t < 5.2) else "#999", lw=4, z=2)
    cv.text(128, 342, L("废液", "waste"), size=10)
    # rotor body
    cv.circle(cx, cy, 100, fc="#f2f2f2", ec="#666", lw=1.6, z=3)
    # grooves rotate: LOAD connects 5-0, 1-2, 3-4 ; INJECT connects 0-1, 2-3, 4-5
    off = rot
    pairs = [(5, 6), (1, 2), (3, 4)]
    for a, b in pairs:
        ia, ib = a + off, b + off
        if not inject and rot == 0:
            col = SAMPLE if (a == 5 and t < 4.8) or (a == 3 and 3.6 < t < 5.2) else (MOBILE if a == 1 else "#999")
        elif inject:
            col = MOBILE if a in (5,) else (SAMPLE if a == 1 and t < rot_end + 3.8 else (MOBILE if a == 1 else "#999"))
        else:
            col = "#999"
        _groove(cv, ia, ib, col)
    for i in range(6):
        x, y = _port(i)
        cv.circle(x, y, 7, fc="white", ec="#555", lw=1.2, z=5)
    # text
    if t < load_end:
        head, items = L("① 装样（Load）", "① LOAD"), [
            L("• 注射器把样品推入定量环，", "• The syringe pushes sample into the loop;"),
            L("  多余样品从废液口排出", "  excess goes to waste"),
            L("• 泵 → 色谱柱 直接相通，", "• Pump → column are connected directly;"),
            L("  流动相照常流过色谱柱", "  mobile phase keeps flowing")]
    elif not inject:
        head, items = L("转动阀芯 60°", "Rotate the rotor 60°"), [
            L("• 阀芯上的三条沟槽", "• The three rotor grooves"), L("  转到相邻的接口上", "  move to the next ports")]
    else:
        head, items = L("② 进样（Inject）", "② INJECT"), [
            L("• 泵 → 定量环 → 色谱柱 相通", "• Pump → loop → column are connected"),
            L("• 流动相把定量环中的样品", "• Mobile phase sweeps the whole"),
            L("  全部冲入色谱柱", "  loop volume onto the column")]
    cv.text(624, 96, head, size=14, weight="bold", color=C["green"])
    cv.lines(626, 166, items, size=10.5, gap=24)
    cv.rect(624, 266, 26, 12, fc=MOBILE)
    cv.text(658, 272, L("流动相", "mobile phase"), size=10)
    cv.rect(624, 296, 26, 12, fc=SAMPLE)
    cv.text(658, 302, L("样品", "sample"), size=10)
    cv.lines(624, 334, [L("定量环“满环进样”体积准确，", "A full loop gives an exact volume,"),
                        L("重复性好；切换时对系统压力", "good repeatability, and barely"),
                        L("和流速的影响很小", "disturbs pressure or flow")], size=9.5, gap=21, color="#555")


# ------------------------------------------------------------------ 04
_C18 = np.linspace(40, 460, 22)
_RP = np.random.default_rng(13).random((70, 3))


def rp_retention(cv, t):
    D = 12
    m = lerp(0.33, 0.65, eseg(t, 0.4, 10.0))
    k_np = 11.9 * math.exp(-(m - 0.33) / 0.156)
    k_p = 0.84 * math.exp(-(m - 0.33) / 0.231)
    cv.title(L("反相色谱的保留：非极性组分“钻进”C18 键合层而被保留；流动相中有机溶剂比例↑，保留↓",
               "Reversed phase: non-polar solutes partition into the C18 layer; more organic solvent → less retention"),
             size=13 if is_zh() else 12)
    x0, x1 = 28, 472
    cv.rect(x0, 80, x1 - x0, 222, fc="#eef5fb", z=0)
    cv.rect(x0, 302, x1 - x0, 124, fc="#f7efe2", z=0)
    cv.rect(x0, 426, x1 - x0, 38, fc="#e2dccb", z=0)
    cv.text(x1 - 8, 445, L("硅胶基质", "silica support"), size=9, color="#777", ha="right")
    cv.text(x0 + 6, 92, L("流动相（甲醇-水）", "mobile phase (methanol–water)"), size=9.5, color=C["teal"])
    cv.text(x1 - 8, 314, L("C18 键合层（非极性）", "C18 bonded layer (non-polar)"), size=9.5, color="#9a7b4f", ha="right",
            bbox=dict(fc="#f7efe2", ec="none", pad=1), zorder=6)
    for x in _C18:
        ys = np.linspace(426, 308, 40)
        cv.line(x + 4 * np.sin((ys - 300) / 8 + t * 2 + x), ys, color="#b08d57", lw=1.4, z=1)
    for i, (a, b, c_) in enumerate(_RP):
        x = x0 + 6 + ((a * (x1 - x0 - 12) + 25 * t * (0.5 + c_)) % (x1 - x0 - 12))
        y = 104 + b * 186
        cv.circle(x, y, 2.4, fc=C["orange"] if c_ < m else "#8ec5e8", z=2, alpha=0.9)
    # solutes: 6 non-polar (orange), 6 polar (teal)
    for kind, kk, col, n in (("np", k_np, C["orange"], 6), ("p", k_p, C["teal"], 6)):
        frac_in = kk / (1 + kk)
        n_in = int(round(frac_in * n))
        for j in range(n):
            seed = (j * 37 + (11 if kind == "p" else 0)) % 97 / 97
            inside = j < n_in
            if inside:
                x = x0 + 30 + ((seed * 380 + 9 * t) % 400)
                y = 360 + 46 * ((j * 13 % 7) / 7)
            else:
                x = x0 + 30 + ((seed * 380 + 40 * t) % 400)
                y = 130 + 140 * ((j * 29 % 11) / 11)
            cv.circle(x, y, 11 if kind == "np" else 10, fc=col, ec="white", lw=1, z=5)
            if kind == "p":
                cv.text(x, y, "OH", size=6.5, color="white", ha="center", weight="bold", zorder=6)
    cv.text(28, 482, L("小圆点：蓝 = 水，橙 = 甲醇；位于 C18 层内的组分分子比例 ≈ k/(1+k)",
                       "Small dots: blue = water, orange = methanol. Fraction of solute inside C18 ≈ k/(1+k)"), size=9, color="#555")
    cv.text(522, 94, L(f"甲醇比例：{m * 100:.0f}%", f"Methanol: {m * 100:.0f}%"), size=14, weight="bold", color=C["green"])
    cv.text(522, 128, L(f"k（非极性组分）= {k_np:.1f}      k（极性组分）= {k_p:.2f}",
                        f"k (non-polar) = {k_np:.1f}      k (polar) = {k_p:.2f}"), size=10.5)
    ax = cv.inset(530, 176, 388, 228)
    ts = np.linspace(0, 30, 900)
    t0 = 1.3
    for kk, col, fcol in ((k_p, C["navy"], "#9cc3d5"), (k_np, C["navy"], "#f6c9b2")):
        tr = t0 * (1 + kk)
        w = 0.12 + 0.045 * tr
        y = (0.9 / (1 + 0.25 * w * 4)) * np.exp(-0.5 * ((ts - tr) / w) ** 2)
        ax.fill_between(ts, y, color=fcol, lw=0)
        ax.plot(ts, y, color=col, lw=1.4)
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel(L("时间 / min", "Time / min"))
    for i, (col, lab) in enumerate(((C["teal"], L("极性组分（先流出）", "polar (elutes first)")),
                                    (C["orange"], L("非极性组分（后流出）", "non-polar (elutes later)")))):
        cv.ax.add_patch(Ellipse((544 + i * 200, 462), 18, 10, fc=col, ec="none"))
        cv.text(558 + i * 200, 462, lab, size=10)


# ------------------------------------------------------------------ 05
def ion_suppression(cv, t):
    D = 12
    pH = lerp(7.5, 2.0, eseg(t, 0.4, 10.2))
    pKa = 4.5
    fHA = 1 / (1 + 10 ** (pH - pKa))
    k = 0.4 + 7.6 * fHA
    cv.title(L("反相离子抑制色谱：降低流动相 pH，抑制弱酸解离，分子形式增多 → 保留增强、峰形改善",
               "Ion suppression: lowering the pH suppresses ionisation of a weak acid → more retention, better peak shape"),
             size=13 if is_zh() else 12)
    cv.text(28, 98, L(f"流动相 pH = {pH:.1f}", f"Mobile-phase pH = {pH:.1f}"), size=14, weight="bold", color=C["green"])
    cv.text(28, 130, L("弱酸 HA（pKa = 4.5）", "Weak acid HA (pKa = 4.5)"), size=10.5)
    nHA = int(round(fHA * 12))
    for i in range(12):
        r, c = divmod(i, 4)
        x, y = 62 + c * 68, 203 + r * 80
        is_ha = i < nHA
        cv.ax.add_patch(Ellipse((x, y), 48, 60, fc=C["orange"] if is_ha else C["teal"], ec="none", zorder=4))
        cv.text(x, y, "HA" if is_ha else "A$^{-}$", size=10, color="white", ha="center", weight="bold", zorder=5)
    cv.text(28, 428, L(f"分子形式 HA：{fHA * 100:.0f}%", f"Molecular HA: {fHA * 100:.0f}%"), size=11, weight="bold", color=C["orange"])
    cv.text(28, 464, L(f"离子形式 A$^{{-}}$：{(1 - fHA) * 100:.0f}%", f"Ionised A$^{{-}}$: {(1 - fHA) * 100:.0f}%"), size=11, weight="bold",
            color=C["teal"])
    ax = cv.inset(398, 92, 510, 150)
    ps = np.linspace(7.5, 2.0, 200)
    ax.plot(ps, 0.4 + 7.6 / (1 + 10 ** (ps - pKa)), color=C["navy"], lw=2)
    ax.plot([pH], [k], "o", color=C["red"], ms=8, zorder=5)
    ax.axvline(pKa, color="#999", lw=0.8, ls=":")
    ax.text(pKa - 0.05, 7.6, "pH = pKa", fontsize=8.5, color="#888")
    ax.set_xlim(7.5, 2.0)
    ax.set_ylim(0, 8.8)
    ax.set_xlabel(L("流动相 pH（向右 pH 降低）", "Mobile-phase pH (decreasing →)"), labelpad=1)
    ax.set_ylabel(L("保留因子 k", "Retention factor k"))
    ax2 = cv.inset(398, 314, 510, 146)
    ts = np.linspace(0, 12, 800)
    tr = 1.0 * (1 + k)
    tail = 1 - fHA
    sig_l, sig_r = 0.35, 0.35 + 1.6 * tail
    y = np.where(ts < tr, np.exp(-0.5 * ((ts - tr) / sig_l) ** 2), np.exp(-0.5 * ((ts - tr) / sig_r) ** 2))
    y /= (sig_l + sig_r) / 0.7
    y = y / max(1e-6, y.max()) * (0.5 + 0.3 * fHA)
    ax2.fill_between(ts, y, color="#f6c9b2" if fHA > 0.5 else "#bcd3df", lw=0)
    ax2.plot(ts, y, color=C["navy"], lw=1.6)
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 1.05)
    ax2.set_yticks([])
    ax2.set_xlabel(L("时间 / min", "Time / min"), labelpad=1)
    msg = (L("解离多：保留弱，峰拖尾", "Mostly ionised: weak retention, tailing") if fHA < 0.5 else
           L("解离受抑制：保留增强，峰形对称", "Ionisation suppressed: stronger retention, symmetric peak"))
    ax2.text(0.97 if fHA < 0.5 else 0.03, 0.93, msg, transform=ax2.transAxes, ha="right" if fHA < 0.5 else "left",
             fontsize=10, color=C["red"] if fHA < 0.5 else C["green"])


# ------------------------------------------------------------------ 06
_SEC = [(x, y) for y in (206, 332) for x in (84, 194, 303, 412, 521)]


def _bead(cv, x, y):
    cv.circle(x, y, 46, fc="#e6dcc4", ec="#b8a77c", lw=1.4, z=2)
    for k in range(8):
        a = k * math.pi / 4
        cv.line([x + 14 * math.cos(a), x + 46 * math.cos(a)], [y + 14 * math.sin(a), y + 46 * math.sin(a)],
                color="white", lw=2.6, z=3)


def size_exclusion(cv, t):
    D = 12
    cv.title(L("分子排阻色谱：按分子大小分离，大分子进不了孔先流出，小分子钻进孔内路径长、后流出",
               "Size exclusion: large molecules skip the pores and elute first; small ones wander through the pores"),
             size=13 if is_zh() else 12)
    x0, x1, y0, y1 = 20, 586, 138, 400
    cv.rect(x0, y0, x1 - x0, y1 - y0, fc="#f5f8fb", ec="#999", lw=1.2)
    cv.arrow(490, 145, 572, 145, color=C["teal"], lw=1.3)
    cv.text(482, 145, L("流动相", "mobile phase"), size=9, color=C["teal"], ha="right")
    for x, y in _SEC:
        _bead(cv, x, y)
    groups = [(SAMPLE, 13, 5, 2.2, 0.0), (C["orange"], 7, 7, 4.8, 0.45), (C["teal"], 3.6, 7, 7.6, 0.85)]
    for gi, (col, r, n, tR, pore) in enumerate(groups):
        prog = (t - 0.5) / tR
        for j in range(n):
            f = prog + 0.03 * math.sin(j * 1.7)
            if f < 0 or f > 1.08:
                continue
            x = x0 + 18 + f * (x1 - x0 - 30)
            # meander into beads for small molecules
            ytrack = 269 + 30 * math.sin(j * 2.1 + gi)
            if pore > 0:
                bead = min(_SEC, key=lambda p: abs(p[0] - x) + abs(p[1] - ytrack))
                wob = pore * math.sin(f * 40 + j)
                y = lerp(ytrack, bead[1] + 20 * math.sin(j + f * 30), max(0, wob))
            else:
                y = ytrack + 8 * math.sin(j * 1.3)
            if x < x1 - 6:
                cv.circle(x, y, r, fc=col, ec="white", lw=0.8, z=5)
    ax = cv.inset(624, 100, 296, 200)
    ts = np.linspace(0, max(0.01, t), 600)
    for col, r, n, tR, pore in groups:
        y = gauss(ts, tR + 0.5, 0.32)
        ax.fill_between(ts, y, color=col, alpha=0.3, lw=0)
        ax.plot(ts, y, color=C["navy"], lw=1.4)
    labs = [L("大分子", "large"), L("中等分子", "medium"), L("小分子", "small")]
    for (col, r, n, tR, pore), lab in zip(groups, labs):
        if t > tR + 0.7:
            ax.text(tR + 0.5, 1.07, lab, fontsize=9, color=col, ha="center")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(10, -0.12, L("洗脱体积 →", "elution volume →"), ha="right", fontsize=9)
    cv.lines(628, 364, [L("• 比所有孔都大的分子：完全排阻，", "• Larger than every pore: fully"),
                        L("  最先流出（不被保留）", "  excluded, elutes first"),
                        "",
                        L("• 比所有孔都小的分子：可进入全部孔，", "• Smaller than every pore: enters"),
                        L("  最后流出", "  all pores, elutes last")], size=9.5, gap=19)
    cv.text(300, 484, L("常用于蛋白质、多肽及高分子聚合物的分子量与分子量分布测定",
                        "Used for molecular weight and its distribution in proteins, peptides and polymers"),
            size=10, color=C["green"], ha="center")


# ------------------------------------------------------------------ 07
SPE_STEPS = [(L, "① 活化", "① Condition", "先用甲醇、再用水冲洗，\n使 C18 吸附剂充分溶剂化", "Rinse with methanol, then water,\nto solvate the C18 sorbent"),
             (L, "② 上样", "② Load", "样品溶液通过小柱：目标物\n被吸附，强极性杂质直接流出", "Pass the sample: the analyte is\nretained, very polar impurities pass"),
             (L, "③ 淋洗", "③ Wash", "用弱溶剂（如 5% 甲醇-水）\n洗去吸附较弱的杂质", "A weak solvent (e.g. 5% MeOH)\nremoves weakly held impurities"),
             (L, "④ 洗脱", "④ Elute", "用强溶剂（如甲醇）把目标物\n洗脱下来，收集后进样分析", "A strong solvent (e.g. MeOH)\nreleases the analyte for analysis")]
_SP = np.random.default_rng(17).random((40, 2))


def spe(cv, t):
    D = 14
    P = 3.2
    step = min(3, int(max(0, t - 0.3) / P))
    u = seg(t - 0.3 - step * P, 0, P)
    cv.title(L("固相萃取（SPE）：用小柱中的吸附剂富集目标物、除去干扰杂质",
               "Solid-phase extraction (SPE): a sorbent cartridge concentrates the analyte, removes interferences"))
    cx0, cx1 = 220, 292
    cv.rect(cx0, 98, cx1 - cx0, 240, fc="white", ec="#666", lw=1.6, z=1)
    cv.rect(cx0 + 1, 232, cx1 - cx0 - 2, 86, fc="#efe6d1", z=2)
    for (a, b) in _SP:
        cv.circle(cx0 + 4 + a * (cx1 - cx0 - 8), 236 + b * 78, 1.0, fc="#c1b48d", z=3)
    cv.rect(cx0 + 1, 318, cx1 - cx0 - 2, 6, fc="#bbb", z=3)
    cv.rect(cx0 + 1, 228, cx1 - cx0 - 2, 5, fc="#bbb", z=3)
    cv.text(cx1 + 10, 275, L("吸附剂\n（C18）", "sorbent\n(C18)"), size=9, color="#9a8a62", linespacing=1.1)
    cv.text(cx1 + 10, 321, L("筛板", "frit"), size=9, color="#666")
    cv.poly([(cx0, 338), (cx1, 338), (cx0 + 42, 366), (cx0 + 30, 366)], fc="white", ec="#666", lw=1.6, z=1)
    cv.rect(cx0 + 30, 366, 12, 26, fc="#ddd", ec="#666", lw=1.2)
    liquid = ["#9cc9ea", "#f7cdb1", "#bcdcf0", "#ddc9e6"][step]
    lvl = lerp(182, 228, u)
    cv.rect(cx0 + 1, lvl, cx1 - cx0 - 2, 228 - lvl, fc=liquid, z=2)
    # analyte (red), weak impurity (orange), polar impurity (grey)
    rng = np.random.default_rng(3)
    pts = rng.random((30, 2))
    vial = L("废液", "waste") if step < 3 else L("收集管", "collect")
    cv.rect(228, 416, 56, 58, fc="white", ec="#888", lw=1.2, r=6)
    cv.text(256, 488, vial, size=9.5, color=C["red"] if step == 3 else "#666", ha="center")
    def dot(x, y, col, r=4.5):
        cv.circle(x, y, r, fc=col, z=6)
    for i in range(10):
        a, b = pts[i]
        # analyte
        if step == 0:
            continue
        if step == 1:
            y = lerp(190 + b * 30, 240 + b * 26, eseg(u, 0.1, 0.7))
        elif step in (2,):
            y = 240 + b * 26
        else:
            y = lerp(240 + b * 26, 438 + b * 26, eseg(u, 0.15, 0.85))
        if y < 470:
            x = cx0 + 10 + a * (cx1 - cx0 - 20)
            if step == 3 and y > 392:
                x = 238 + a * 36
            dot(x, y, C["red"])
    for i in range(10, 18):
        a, b = pts[i]
        if step == 0:
            continue
        if step == 1:
            y = lerp(190 + b * 30, 250 + b * 40, eseg(u, 0.1, 0.7))
            dot(cx0 + 10 + a * (cx1 - cx0 - 20), y, C["orange"], 4)
        elif step == 2:
            y = lerp(250 + b * 40, 430 + b * 30, eseg(u, 0.1, 0.85))
            dot((cx0 + 10 + a * (cx1 - cx0 - 20)) if y < 400 else 240 + a * 32, y, C["orange"], 4)
        else:
            dot(240 + a * 32, 432 + b * 30, C["orange"], 4) if False else None
    for i in range(18, 26):
        a, b = pts[i]
        if step == 1:
            y = lerp(190 + b * 30, 440 + b * 26, eseg(u, 0.1, 0.9))
            x = (cx0 + 10 + a * (cx1 - cx0 - 20)) if y < 360 else 236 + a * 40
            dot(x, y, "#9a9a9a", 4)
    for i, (_f, zh, en, dzh, den) in enumerate(SPE_STEPS):
        on = i == step
        y = 106 + i * 82
        cv.text(512, y, L(zh, en), size=13 if on else 11, weight="bold" if on else "normal",
                color=C["green"] if on else "#aaa")
        cv.text(596 if is_zh() else 640, y + 10, L(dzh, den), size=10 if on else 9.5, color=C["ink"] if on else "#aaa",
                linespacing=1.35)
    for i, (col, lab) in enumerate(((C["red"], L("目标物", "analyte")), (C["orange"], L("弱保留杂质", "weak impurity")),
                                    ("#9a9a9a", L("强极性杂质", "polar impurity")))):
        dx = 138 if is_zh() else 150
        cv.rect(512 + i * dx, 426, 14, 14, fc=col)
        cv.text(532 + i * dx, 433, lab, size=9.5 if is_zh() else 9)


ANIMS = [
    ("01-piston-pump", pump, 12),
    ("02-isocratic-gradient", gradient, 12),
    ("03-six-port-valve", six_port, 13),
    ("04-rp-retention", rp_retention, 12),
    ("05-ion-suppression", ion_suppression, 12),
    ("06-size-exclusion", size_exclusion, 12),
    ("07-spe", spe, 14),
]
