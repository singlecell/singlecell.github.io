"""Chapter: 气相色谱法 / Gas Chromatography."""
import math
import numpy as np
from common import *

CH = "gc"


def _coil(u):
    """Point on the coiled capillary path, u in [0, 1]."""
    u = np.asarray(u, dtype=float)
    x0, x1, yc = 300, 560, 230
    n = 4
    x = x0 + (x1 - x0) * u + 50 * np.sin(2 * np.pi * n * u)
    y = yc + 30 * np.cos(2 * np.pi * n * u)
    return x, y


def _path(u):
    """Injector → down → coil → across → detector, u in [0, 1]."""
    u = np.atleast_1d(np.asarray(u, dtype=float))
    xs, ys = np.empty_like(u), np.empty_like(u)
    a, b = 0.08, 0.92
    m1 = u < a
    xs[m1] = 258
    ys[m1] = 130 + (260 - 130) * (u[m1] / a)
    m2 = (u >= a) & (u <= b)
    cx, cy = _coil((u[m2] - a) / (b - a))
    xs[m2], ys[m2] = cx, cy
    m3 = u > b
    f = (u[m3] - b) / (1 - b)
    xs[m3] = 610 + (676 - 610) * f
    ys[m3] = 230 - (230 - 205) * f
    return xs, ys


# ------------------------------------------------------------------ 01
GCC = [(C["orange"], 4.6, 0.28), (C["teal"], 8.0, 0.4)]


def gc_flow(cv, t):
    D = 11
    cv.title(L("气相色谱仪的工作流程：载气 → 进样口（汽化）→ 色谱柱（分离）→ 检测器 → 色谱图",
               "GC: carrier gas → inlet (vaporise) → column (separate) → detector → chromatogram"))
    cv.rect(40, 140, 62, 166, fc="#9fb3c8", ec="#555", lw=1.2, r=14)
    cv.rect(62, 126, 18, 16, fc="#777")
    cv.text(71, 223, L("载\n气", "carrier\ngas"), size=11 if is_zh() else 9, color="white", ha="center", weight="bold",
            linespacing=1.1)
    cv.line([71, 71, 132], [126, 112, 112], color="#666", lw=1.6)
    cv.rect(132, 98, 66, 28, fc="#efefef", ec="#777", lw=1)
    cv.text(165, 112, L("稳压稳流", "regulator"), size=8.5, ha="center")
    cv.line([198, 232], [112, 112], color="#666", lw=1.6)
    cv.rect(232, 90, 52, 42, fc="#f4c4a2", ec=C["orange"], lw=1.2)
    cv.text(294, 102, L("进样口（加热汽化）", "Inlet (heated, vaporises)"), size=9.5, color=C["orange"])
    cv.rect(228, 148, 408, 168, fc="#fff3e6", ec=C["orange"], lw=1.3, r=6, ls=(0, (4, 3)))
    cv.text(432, 300, L("柱温箱（程序控温）", "Column oven (temperature programmed)"), size=9.5, color=C["orange"], ha="center")
    cv.text(432, 164, L("毛细管色谱柱", "capillary column"), size=9.5, color="#666", ha="center")
    us = np.linspace(0, 1, 900)
    px, py = _path(us)
    cv.line(px, py, color="#9a9a9a", lw=1.6, z=2)
    cv.rect(644, 158, 64, 46, fc="#dfe7f0", ec=C["navy"], lw=1.4)
    cv.text(676, 181, L("检测器", "Detector"), size=9.5, ha="center")
    cv.line([708, 752], [181, 181], color="#666", lw=1.2)
    cv.rect(752, 162, 98, 38, fc="#efefef", ec="#777", lw=1)
    cv.text(801, 181, L("数据处理\n系统", "data\nsystem"), size=8.5, ha="center", linespacing=1.0)
    # carrier gas dots
    for k in range(6):
        f = ((t * 0.35 + k / 6) % 1)
        if f < 0.5:
            x = lerp(71, 132, f * 2) if f < 0.25 else lerp(198, 232, (f - 0.25) * 4)
            cv.circle(x, 112, 2.3, fc="#5b7fa6", z=4)
    t_inj = 0.6
    if t < t_inj + 0.4:
        cv.arrow(258, 70, 258, 92, color=C["red"], lw=2, alpha=fade(t, 0, 0.2, 0.7, 1.0))
        cv.text(270, 72, L("进样", "inject"), size=9, color=C["red"], alpha=fade(t, 0, 0.2, 0.7, 1.0))
    for col, tR, st in GCC:
        f = (t - t_inj) / (tR - t_inj)
        if 0 < f < 1.02:
            w = 0.012 + 0.03 * f
            uu = np.linspace(max(0, f - w), min(1, f + w), 40)
            bx, by = _path(uu)
            cv.line(bx, by, color=col, lw=5, z=5)
    ax = cv.inset(114, 350, 756, 118)
    ts = np.linspace(0, max(0.01, t), 600)
    sig = sum(gauss(ts, tR + 0.25, st) for col, tR, st in GCC) + 0.25 * gauss(ts, 1.5, 0.1)
    ax.plot(ts, sig, color=C["navy"], lw=1.8)
    for col, tR, st in GCC:
        if t > tR + 0.25:
            ax.plot([tR + 0.25] * 2, [0, 1], ls=":", color=col, lw=1)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.03, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(L("检测器响应", "Response"), fontsize=9)
    ax.text(10.5, -0.2, L("时间 →", "time →"), ha="right", fontsize=9)


# ------------------------------------------------------------------ 02
_P = np.random.default_rng(31).random((60, 4))


def split_splitless(cv, t):
    D = 12
    cv.title(L("毛细管气相色谱的进样方式：分流进样与不分流进样", "Capillary GC injection: split and splitless"))
    panels = [(48, "split", L("分流进样（split）", "Split injection"),
               [L("汽化后大部分样品随载气从分流口放空，", "Most of the vaporised sample leaves through"),
                L("只有少量进入色谱柱（如分流比 50:1）", "the split vent; a little enters the column (e.g. 50:1)")]),
              (520, "splitless", L("不分流进样（splitless）", "Splitless injection"),
               [L("进样时关闭分流阀，样品几乎全部进入色谱柱；", "Split valve closed: nearly all sample enters the column;"),
                L("约 0.5～1 min 后打开分流阀，吹扫残留溶剂", "after 0.5–1 min the valve opens to purge the rest")])]
    t_open = 7.0
    for x0, mode, name, desc in panels:
        cv.text(x0, 76, name, size=12.5, weight="bold", color=C["green"])
        cv.lines(x0, 110, desc, size=9.5 if is_zh() else 8.8, gap=19, color="#444")
        lx0 = x0 + 78
        cv.rect(lx0, 176, 136, 222, fc="#f4c4a2", ec=C["orange"], lw=1.4)
        cv.rect(lx0 + 36, 186, 62, 196, fc="#fffdf6", ec="#999", lw=1.2, z=2)
        cv.rect(lx0 + 34, 172, 66, 12, fc="#555", z=3)
        cv.text(lx0 - 6, 180, L("隔垫", "septum"), size=8.5, color="#666", ha="right")
        cv.arrow(lx0 + 200, 202, lx0 + 104, 202, color=C["teal"], lw=1.3)
        cv.text(lx0 + 206, 202, L("载气", "carrier"), size=9, color=C["teal"])
        # split line + valve
        cv.line([lx0 + 98, lx0 + 260], [384, 384], color="#777", lw=1.4, z=3)
        open_ = mode == "split" or t > t_open
        cv.circle(lx0 + 176, 384, 12, fc="#7cc47c" if open_ else "#e36b6b", ec="#555", lw=1, z=4)
        cv.text(lx0 + 176, 406, (L("分流阀 开", "valve open") if open_ else L("分流阀 关", "valve closed")), size=9,
                color=C["green"] if open_ else C["red"], ha="center")
        cv.text(lx0 + 266, 384, L("分流\n出口", "split\nvent"), size=9, color="#555", linespacing=1.0)
        cv.line([lx0 + 64, lx0 + 64], [382, 464], color="#777", lw=1.4, z=3)
        cv.line([lx0 + 70, lx0 + 70], [382, 464], color="#777", lw=1.4, z=3)
        cv.text(lx0 + 80, 452, L("→ 色谱柱", "→ column"), size=9)
        n_col = 0
        for i in range(60):
            a, b, c, d = _P[i]
            to_col = (a < 0.05) if mode == "split" else (a < 0.85)
            start = 1.0 + b * 0.6
            if t < 0.8:
                continue
            # vapour cloud expanding near the top
            cx = lx0 + 67 + (c - 0.5) * 40 * min(1, (t - 0.8) * 2)
            cy = 240 + (d - 0.5) * 60 * min(1, (t - 0.8) * 2)
            if mode == "split":
                go = start + 0.4 + b * 3.2
            else:
                go = (start + 0.6 + b * 5.0) if to_col else (t_open + 0.2 + b * 1.5)
            f = seg(t, go, go + 1.6)
            if f <= 0:
                x, y = cx, cy
            elif to_col:
                if f < 0.6:
                    x, y = lerp(cx, lx0 + 67, f / 0.6), lerp(cy, 384, f / 0.6)
                else:
                    x, y = lx0 + 67, lerp(384, 470, (f - 0.6) / 0.4)
                    if f >= 0.62:
                        n_col += 1
            else:
                if f < 0.6:
                    x, y = lerp(cx, lx0 + 92, f / 0.6), lerp(cy, 384, f / 0.6)
                else:
                    x, y = lerp(lx0 + 92, lx0 + 270, (f - 0.6) / 0.4), 384
            if y < 468 and x < lx0 + 262:
                cv.ax.add_patch(Ellipse((x, y), 9, 7, fc=C["magenta"], ec="none", alpha=0.85, zorder=6))
        cv.text(lx0 + 186, 268, L("进入色谱柱：", "Into column:"), size=11, weight="bold")
        cv.text(lx0 + 186, 292, f"{n_col} / 60", size=12, weight="bold", color=C["red"] if n_col else C["ink"])
    cv.text(473, 488, L("分流：适合浓度较高的样品，峰形窄；不分流：适合痕量分析，灵敏度高",
                        "Split: concentrated samples, narrow peaks.  Splitless: trace analysis, high sensitivity"),
            size=10, color=C["green"], ha="center")


# ------------------------------------------------------------------ 03
ISO = [("C8", 1.3, 0.12, 0.9), ("C10", 1.8, 0.15, 0.8), ("C12", 2.9, 0.22, 0.55),
       ("C14", 5.3, 0.38, 0.33), ("C16", 11.1, 0.75, 0.17), ("C18", 23.0, 1.5, 0.08)]
PROG = [("C8", 2.0), ("C10", 4.4), ("C12", 6.8), ("C14", 9.2), ("C16", 11.6), ("C18", 14.0)]


def temp_program(cv, t):
    D = 12
    tm = lerp(0, 30, seg(t, 0.3, 10.0))
    cv.title(L("等温与程序升温：样品沸点范围宽时，程序升温使高沸点组分更早流出、峰形更窄",
               "Isothermal vs programmed temperature: programming elutes late peaks sooner and sharper"),
             size=13 if is_zh() else 12)
    rows = [(84, L("等温（150 °C）", "Isothermal (150 °C)"), "iso"),
            (296, L("程序升温（60 °C → 10 °C/min → 280 °C）", "Programmed (60 °C → 10 °C/min → 280 °C)"), "prog")]
    for y0, name, kind in rows:
        cv.text(66, y0 - 12, name, size=11.5, weight="bold", color=C["teal"] if kind == "iso" else C["green"])
        ax = cv.inset(66, y0, 624, 152)
        ts = np.linspace(0, max(0.01, tm), 900)
        if kind == "iso":
            sig = sum(h * np.exp(-0.5 * ((ts - c) / w) ** 2) for _n, c, w, h in ISO)
            temp = 150 + 0 * ts
        else:
            sig = sum(0.85 * np.exp(-0.5 * ((ts - c) / 0.22) ** 2) for _n, c in PROG)
            temp = np.minimum(60 + 10 * ts, 280)
        ax.plot(ts, sig, color=C["navy"], lw=1.5)
        peaks = [(n, c, h) for n, c, w, h in ISO] if kind == "iso" else [(n, c, 0.85) for n, c in PROG]
        for n, c, h in peaks:
            if tm > c + 0.3:
                ax.text(c + (0.55 if n == "C10" and kind == "iso" else 0), h + 0.05, n, fontsize=8, ha="center", color="#555")
        ax.set_xlim(0, 30)
        ax.set_ylim(0, 1.15)
        ax.set_yticks([])
        if kind == "prog":
            ax.set_xlabel(L("时间 / min", "Time / min"), labelpad=1)
        ax2 = ax.twinx()
        ax2.plot(ts, temp, "--", color=C["orange"], lw=1.2)
        ax2.set_ylim(20, 320)
        ax2.set_yticks([60, 150, 280])
        ax2.tick_params(labelsize=8, colors=C["orange"])
        ax2.spines["right"].set_visible(True)
        ax2.spines["right"].set_color(C["orange"])
        ax2.spines["top"].set_visible(False)
        ax2.set_ylabel(L("柱温 / °C", "T / °C"), color=C["orange"], fontsize=8.5)
    cv.text(756, 100, L("等温", "Isothermal"), size=11.5, weight="bold", color=C["teal"])
    cv.lines(758, 128, [L("• 低沸点组分挤在", "• early peaks crowd"), L("  一起、分不开", "  together"),
                        L("• 高沸点组分出峰", "• late peaks are slow,"), L("  慢，峰宽而矮", "  broad and low")],
             size=9.5, gap=19)
    cv.text(756, 312, L("程序升温", "Programmed"), size=11.5, weight="bold", color=C["green"])
    cv.lines(758, 340, [L("• 各组分都在适宜", "• each compound elutes"), L("  温度下流出", "  at a suitable T"),
                        L("• 峰间距均匀、峰形", "• even spacing, sharp"), L("  窄，分析时间短", "  peaks, shorter run")],
             size=9.5, gap=19)


# ------------------------------------------------------------------ 04
def fid(cv, t):
    D = 12
    cv.title(L("氢火焰离子化检测器（FID）：有机物在氢火焰中燃烧电离，产生的离子流被收集成电信号",
               "Flame ionisation detector (FID): organics burn and ionise in an H$_2$ flame; the ion current is measured"),
             size=13 if is_zh() else 12)
    bx0, bx1, by0, by1 = 78, 288, 76, 452
    cv.rect(bx0, by0, bx1 - bx0, by1 - by0, fc="#f3f5f7", ec="#888", lw=1.2)
    # electrodes
    cv.rect(132, 128, 12, 92, fc="#999", ec="#666", lw=1, z=3)
    cv.rect(222, 128, 12, 92, fc="#999", ec="#666", lw=1, z=3)
    cv.text(240, 140, L("收集极", "collector"), size=9, color="#555")
    # jet
    cv.rect(172, 300, 22, 152, fc="#bcc4cc", ec="#888", lw=1, z=3)
    cv.text(200, 322, L("喷嘴（极化极）", "jet (polarising\nelectrode)"), size=8.5, color="#555", linespacing=1.0, va="top")
    cv.arrow(183, 448, 183, 410, color=C["navy"], lw=1.4)
    cv.text(183, 466, L("色谱柱流出物 + $H_2$", "column effluent + $H_2$"), size=9, ha="center")
    cv.arrow(40, 375, 110, 375, color=C["teal"], lw=1.3)
    cv.text(40, 362, L("空气", "air"), size=9.5, color=C["teal"])
    # pulses of organics: two peaks
    peaks = [(3.6, 0.5, 1.0), (7.0, 0.6, 0.6)]
    conc = sum(h * math.exp(-0.5 * ((t - c) / w) ** 2) for c, w, h in peaks)
    fl = 1 + 0.06 * math.sin(t * 23) + 0.25 * conc
    cv.ax.add_patch(Ellipse((183, 268), 36 * fl, 72 * fl, fc="#ffd966", ec="none", alpha=0.85, zorder=4))
    cv.ax.add_patch(Ellipse((183, 276), 18, 42, fc="#8fc3e8", ec="none", alpha=0.9, zorder=5))
    cv.text(206, 296, L("氢火焰", "H$_2$ flame"), size=9, color=C["orange"])
    # ions drifting to collector
    rng = np.random.default_rng(int(t * 25) % 997)
    nion = int(3 + 34 * conc)
    # organic molecules rising through the jet
    for k in range(int(14 * conc)):
        ph = ((t * 2.2 + k * 0.071) % 1)
        cv.circle(178 + 10 * ((k * 37) % 7) / 7, 446 - ph * 140, 2.6, fc="#555", z=6)
    for k in range(nion):
        ph = ((t * 1.3 + k * 0.137) % 1)
        side = -1 if k % 2 else 1
        x = 183 + side * ph * 40
        y = 240 - ph * 70 + 10 * math.sin(k)
        cv.text(x, y, "+" if side < 0 else "−", size=12, color=C["red"] if side < 0 else C["teal"], ha="center",
                weight="bold", zorder=6)
    # circuit + amplifier
    cv.line([234, 330, 330], [174, 174, 236], color="#555", lw=1.2)
    cv.line([330, 330, 194], [284, 420, 420], color="#555", lw=1.2)
    cv.circle(330, 260, 24, fc="white", ec="#555", lw=1.4, z=4)
    cv.text(330, 260, "A", size=13, weight="bold", ha="center", zorder=6)
    cv.text(362, 260, L("微电流\n放大器", "current\namplifier"), size=9, linespacing=1.0)
    ax = cv.inset(520, 70, 398, 182)
    ts = np.linspace(0, max(0.01, t), 500)
    sig = 0.04 + sum(h * np.exp(-0.5 * ((ts - c) / w) ** 2) for c, w, h in peaks)
    ax.plot(ts, sig, color=C["navy"], lw=1.8)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(L("离子流（电流）", "Ion current"))
    ax.text(11, -0.1, L("时间 →", "time →"), ha="right", fontsize=9)
    bullets = [(L("• 只有载气和 $H_2$ 时，离子很少，基线电流很小", "• Carrier gas + $H_2$ alone: few ions, tiny baseline"), C["ink"], 0.5),
               (L("• 有机物进入火焰：CH + O → $CHO^+$ + $e^-$", "• Organics in the flame: CH + O → $CHO^+$ + $e^-$"), C["ink"], 3.0),
               (L("• 响应与单位时间进入火焰的碳原子数成正比\n   （质量型检测器），灵敏度高、线性范围宽",
                  "• Response ∝ carbon atoms entering per second\n   (mass-flow detector): sensitive, wide linear range"), C["ink"], 5.5),
               (L("• 对 $H_2O$、$CO_2$、$N_2$、$O_2$ 等几乎无响应", "• Almost no response to $H_2O$, $CO_2$, $N_2$, $O_2$"), C["red"], 8.0)]
    ys = [292, 326, 366, 424]
    for (s, col, ta), y in zip(bullets, ys):
        cv.text(520, y, s, size=10, color=col, alpha=fade(t, ta, ta + 0.5), linespacing=1.3)


ANIMS = [
    ("01-gc-workflow", gc_flow, 11),
    ("02-split-splitless", split_splitless, 12),
    ("03-temperature-programming", temp_program, 12),
    ("04-fid", fid, 12),
]
