"""Chapter: 色谱联用技术 / Hyphenated techniques (LC/GC–MS)."""
import math
import numpy as np
from common import *

CH = "hyphenated"
MZC = {150: C["orange"], 230: C["magenta"], 310: C["teal"]}


# ------------------------------------------------------------------ 01
_QI = np.random.default_rng(41).random((60, 3))


def quadrupole(cv, t):
    D = 12
    P = D / 3
    k = min(2, int(t / P))
    target = [150, 230, 310][k]
    cv.title(L("四极杆质量分析器：只有特定 m/z 的离子能稳定通过，扫描电压即可得到质谱",
               "Quadrupole mass analyser: only one m/z passes stably at a time; scanning the voltages gives the spectrum"),
             size=13.5 if is_zh() else 12.5)
    x0, x1, yc = 116, 528, 212
    cv.rect(x0, 118, x1 - x0, 26, fc="#b0bec8", ec="#6b7b88", lw=1)
    cv.rect(x0, 280, x1 - x0, 26, fc="#b0bec8", ec="#6b7b88", lw=1)
    cv.text((x0 + x1) / 2, 98, L("四极杆（侧视）", "Quadrupole rods (side view)"), size=10, color="#555", ha="center")
    cv.rect(32, 165, 60, 94, fc="#ffe0b3", ec=C["orange"], lw=1.2)
    cv.text(62, 286, L("离子源", "Ion source"), size=10, color=C["orange"], ha="center")
    cv.rect(564, 174, 36, 78, fc="#c9e8cf", ec=C["green"], lw=1.2)
    cv.text(582, 274, L("检测器", "Detector"), size=10, color=C["green"], ha="center")
    def ypos(f, stable, ph):
        if stable:
            return yc + 16 * math.sin(f * 26 + ph) * (0.6 + 0.4 * math.sin(f * 7 + ph))
        return yc + 3.5 * math.exp(f * 5.2) * math.sin(f * 24 + ph)
    for i, (a, b, c_) in enumerate(_QI[:36]):
        mz = [150, 230, 310][i % 3]
        col = MZC[mz]
        stable = mz == target
        start = b * P
        age = ((t - k * P) - start) % P
        f = age / 2.2
        ph = c_ * 6.28
        if f > 1.02:
            continue
        # where would it hit a rod?
        fs = np.linspace(max(0, f - 0.12), f, 25)
        ys = np.array([ypos(q, stable, ph) for q in fs])
        hit = np.abs(ys - yc) > 62
        if hit.any() and not stable:
            j = int(np.argmax(hit))
            if j == 0:
                continue
            fs, ys = fs[:j + 1], np.clip(ys[:j + 1], yc - 62, yc + 62)
            xs = x0 - 10 + fs * (x1 - x0 + 50)
            cv.line(xs, ys, color=col, lw=1.2, alpha=0.5, z=4)
            cv.circle(xs[-1], ys[-1], 5.5, fc=col, z=5, alpha=0.6)
            continue
        xs = x0 - 10 + fs * (x1 - x0 + 50)
        cv.line(xs, ys, color=col, lw=1.2, alpha=0.5, z=4)
        cv.circle(xs[-1], ys[-1], 5.5, fc=col, z=5)
    cv.text(322, 336, L(f"当前电压条件下可通过：m/z {target}", f"Passes at the current voltages: m/z {target}"), size=12,
            weight="bold", color=MZC[target], ha="center")
    for i, mz in enumerate((150, 230, 310)):
        cv.rect(66 + i * 160, 397, 16, 14, fc=MZC[mz])
        cv.text(90 + i * 160, 404, f"m/z {mz}", size=10)
    cv.text(800, 76, L("依次扫描得到的质谱", "Spectrum built up by the scan"), size=10.5, ha="center")
    ax = cv.inset(672, 92, 252, 232)
    for j, (mz, h) in enumerate(((150, 0.55), (230, 1.0), (310, 0.4))):
        if j < k or (j == k and (t - k * P) > 1.6):
            ax.bar([mz], [h], width=11, color=MZC[mz])
    ax.set_xlim(100, 360)
    ax.set_ylim(0, 1.1)
    ax.set_yticks([])
    ax.set_xlabel("m/z")
    cv.text(470, 466, L("其他 m/z 的离子振幅越来越大，撞到电极上被“过滤”掉，因此四极杆又称“质量过滤器”",
                        "Ions of other m/z oscillate ever wider and hit the rods — hence the name “mass filter”"),
            size=10, color=C["green"], ha="center")


# ------------------------------------------------------------------ 02
_DR = np.random.default_rng(55).random((40, 3))


def esi(cv, t):
    D = 12
    cv.title(L("电喷雾电离（ESI）：带电液滴不断蒸发、分裂，最终释放出气相离子进入质谱",
               "Electrospray ionisation (ESI): charged droplets shrink, burst, and release gas-phase ions"))
    cv.rect(20, 172, 120, 20, fc="#b0bec8", ec="#6b7b88", lw=1)
    cv.poly([(140, 172), (180, 182), (140, 192)], fc="#7fb3e6", ec="#2b7bc9", lw=1)
    cv.text(80, 146, L("喷雾毛细管\n（+3～5 kV）", "Spray capillary\n(+3–5 kV)"), size=9.5, ha="center", linespacing=1.05)
    cv.text(80, 218, L("LC 流出液", "LC eluent"), size=9.5, color="#666", ha="center")
    cv.text(180, 218, L("泰勒锥", "Taylor cone"), size=9.5, color="#2b7bc9", ha="center")
    cv.poly([(800, 100), (818, 88), (902, 88), (902, 178), (850, 178), (800, 184)], fc="#d0d9df", ec="#6b7b88", lw=1.2)
    cv.poly([(800, 192), (850, 186), (902, 186), (902, 276), (818, 276), (800, 264)], fc="#d0d9df", ec="#6b7b88", lw=1.2)
    cv.text(850, 290, L("质谱入口", "MS inlet"), size=10, ha="center")
    cv.arrow(674, 88, 560, 102, color="#999", lw=1.2)
    cv.arrow(674, 278, 560, 264, color="#999", lw=1.2)
    cv.text(684, 88, L("$N_2$ 干燥气", "$N_2$ drying gas"), size=9, color="#888")
    for i, (a, b, c_) in enumerate(_DR):
        f = ((t * 0.32 + a) % 1)
        x = 186 + f * 620
        spread = 70 * f
        y = 182 + (b - 0.5) * 2 * spread
        if f < 0.35:
            r = lerp(12, 7, f / 0.35)
            cv.circle(x, y, r, fc="#bfe0fb", ec="#2b8ad6", lw=1, z=4)
            cv.text(x, y, "+", size=7, color=C["red"], ha="center", zorder=5)
        elif f < 0.62:
            for d in range(3):
                cv.circle(x + (d - 1) * 9, y + ((d * 7) % 3 - 1) * 9, 5, fc="#bfe0fb", ec="#2b8ad6", lw=0.8, z=4)
        else:
            for d in range(3):
                xx = x + (d - 1) * 9 + 6 * math.sin(i + d)
                yy = y + ((d * 5) % 3 - 1) * 9
                if xx < 806:
                    cv.text(xx, yy, "⊕", size=8, color=C["red"], ha="center", zorder=5)
    stages = [L("带电液滴", "charged droplet"),
              L("溶剂蒸发，\n液滴缩小、电荷密度增大", "solvent evaporates:\nsmaller, higher charge density"),
              L("达到瑞利极限，\n库仑爆炸（分裂）", "Rayleigh limit:\nCoulomb fission"),
              L("释放出气相离子\n[M+H]$^+$", "gas-phase ions\n[M+H]$^+$ released")]
    cyc = (t % 8) / 8
    xs = [124, 306, 520, 760]
    for i, lab in enumerate(stages):
        on = cyc >= i * 0.22
        al = 1 if on else 0.25
        x = xs[i]
        if i == 0:
            cv.circle(x, 386, 38, fc="#bfe0fb", ec="#2b8ad6", lw=1.4, z=3, alpha=al)
            for k in range(8):
                a = k * math.pi / 4
                cv.text(x + 26 * math.cos(a), 386 + 26 * math.sin(a), "+", size=8, color=C["red"], ha="center", alpha=al)
        elif i == 1:
            cv.circle(x, 386, 26, fc="#bfe0fb", ec="#2b8ad6", lw=1.4, z=3, alpha=al)
            for k in range(8):
                a = k * math.pi / 4
                cv.text(x + 18 * math.cos(a), 386 + 18 * math.sin(a), "+", size=8, color=C["red"], ha="center", alpha=al)
        elif i == 2:
            for (dx, dy) in ((-35, -16), (40, -20), (5, 18), (48, 16)):
                cv.circle(x + dx, 386 + dy, 11, fc="#bfe0fb", ec="#2b8ad6", lw=1.2, z=3, alpha=al)
                cv.text(x + dx, 386 + dy, "+", size=7, color=C["red"], ha="center", alpha=al)
        else:
            for (dx, dy) in ((-35, -14), (30, -18), (-38, 16), (2, 14), (40, 16)):
                cv.text(x + dx, 386 + dy, "⊕", size=11, color=C["red"], ha="center", alpha=al)
        cv.text(x, 452, lab, size=10, ha="center", alpha=al, linespacing=1.15)
        if i < 3:
            cv.arrow(x + (56 if i else 86), 386, x + (124 if i else 156), 386, color="#999", lw=1.2, alpha=al)


# ------------------------------------------------------------------ 03
COMPS = [(2.5, [(200, 1.0), (158, 0.55)]), (4.2, [(312, 0.9), (290, 0.6)]),
         (6.1, [(334, 1.0), (214, 0.6), (172, 0.5), (290, 0.35)]), (8.1, [(512, 0.6), (358, 0.5)])]
_NZ = np.random.default_rng(66).random((300, 251))


def _intensity(tt, mz):
    v = np.zeros(np.broadcast(tt, mz).shape)
    for tc, peaks in COMPS:
        g = np.exp(-0.5 * ((tt - tc) / 0.28) ** 2)
        for m, h in peaks:
            v = v + h * g * np.exp(-0.5 * ((mz - m) / 2.2) ** 2)
    return v


def tic_eic(cv, t):
    D = 14
    phase2 = t > 7.4
    tm = 10 * seg(t, 0.2, 7.0)
    cv.title(L("全扫描数据：总离子流图（TIC）与提取离子流图（EIC）",
               "Full-scan data: total ion chromatogram (TIC) and extracted ion chromatogram (EIC)"))
    cv.text(66, 62, L("三维数据（时间 × m/z × 强度）", "3-D data (time × m/z × intensity)"), size=10)
    ax = cv.inset(66, 76, 522, 192)
    ts = np.linspace(0, 10, 300)
    mzs = np.linspace(100, 600, 251)
    T, M = np.meshgrid(ts, mzs)
    I = _intensity(T, M) + 0.04 * _NZ.T[: M.shape[0], : M.shape[1]]
    I = np.where(T <= tm, I, np.nan)
    ax.imshow(I, extent=(0, 10, 100, 600), origin="lower", aspect="auto", cmap="Blues", vmin=0, vmax=0.9,
              interpolation="bilinear")
    ax.axvline(tm, color=C["teal"], lw=1.2)
    ax.set_xlim(0, 10)
    ax.set_xticks([])
    ax.set_ylabel("m/z")
    for s in ax.spines.values():
        s.set_visible(True)
    if phase2:
        a = fade(t, 7.5, 8.2)
        ax.axhspan(312 - 4, 312 + 4, color=C["red"], alpha=0.25 * a)
        ax.text(9.9, 330, "m/z 312", color=C["red"], fontsize=9.5, ha="right", alpha=a, fontweight="bold")
    # current spectrum
    tc = min(tm, 9.99)
    cv.text(662, 62, L(f"当前扫描的质谱（t = {tc:.1f} min）", f"Current scan (t = {tc:.1f} min)") if not phase2 else
            L("提取：只取 m/z 312 的强度", "Extract: intensity at m/z 312 only"), size=10)
    ax2 = cv.inset(662, 76, 256, 192)
    spec = _intensity(tc, mzs) + 0.03 * _NZ[int(tc * 29.9)]
    ax2.vlines(mzs, 0, spec, color=C["navy"], lw=1)
    if phase2:
        ax2.axvspan(308, 316, color=C["red"], alpha=0.25)
    ax2.set_xlim(100, 600)
    ax2.set_ylim(0, 1.1)
    ax2.set_yticks([])
    ax2.set_xlabel("m/z", labelpad=1)
    # chromatograms
    ax3 = cv.inset(66, 308, 522, 152)
    tt = np.linspace(0, tm, 400)
    tic = np.array([_intensity(x, mzs).sum() for x in tt]) / 4.5 + 0.08 + 0.02 * np.sin(tt * 37)
    ax3.plot(tt, tic, color=C["navy"], lw=1.6, label=L("TIC（所有离子强度之和）", "TIC (sum of all ions)"))
    if phase2:
        a = eseg(t, 7.8, 10.5)
        te = np.linspace(0, 10 * a, 300)
        eic = _intensity(te, 312) * 1.0
        ax3.plot(te, eic, color=C["red"], lw=2, label=L("EIC m/z 312", "EIC m/z 312"))
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 1.75)
    ax3.set_yticks([])
    ax3.set_xlabel(L("时间 / min", "Time / min"), labelpad=1)
    ax3.legend(loc="upper left", frameon=False, fontsize=9)
    msg = ([L("质谱每隔零点几秒扫描一次", "The MS scans the whole m/z range"),
            L("全部 m/z 范围（如 100～600）", "(e.g. 100–600) every fraction of a second")] if not phase2 else
           [L("TIC：每次扫描所有离子强度相加，", "TIC: all ions summed per scan;"),
            L("峰多、易受基质干扰", "many peaks, prone to matrix interference"),
            (L("EIC：只看目标物的 m/z，", "EIC: one target m/z only,"), dict(color=C["red"])),
            (L("选择性好，可从重叠峰中“提取”目标物", "selective; pulls the target out of overlaps"), dict(color=C["red"]))])
    cv.lines(624, 342, msg, size=10.5, gap=24)


# ------------------------------------------------------------------ 04
_MR = np.random.default_rng(77).random((70, 3))


def mrm(cv, t):
    D = 12
    cv.title(L("多反应监测（MRM）：Q1 选母离子 → q2 碰撞碎裂 → Q3 选特征子离子，干扰被两次“过滤”",
               "MRM: Q1 selects the precursor → q2 fragments it → Q3 selects a product ion; interference is filtered twice"),
             size=13.5 if is_zh() else 12)
    sx0 = [(108, 316, "#b0bec8", L("Q1：选择母离子\nm/z 449", "Q1: select precursor\nm/z 449")),
           (344, 544, "#fbd97a", L("q2：碰撞室（$N_2$/Ar）\n碰撞诱导解离", "q2: collision cell (N$_2$/Ar)\ncollision-induced dissociation")),
           (572, 780, "#b0bec8", L("Q3：选择子离子\nm/z 287", "Q3: select product\nm/z 287"))]
    for a, b, col, lab in sx0:
        cv.rect(a, 120, b - a, 14, fc=col, ec="#6b7b88", lw=1)
        cv.rect(a, 238, b - a, 14, fc=col, ec="#6b7b88", lw=1)
        cv.text((a + b) / 2, 92, lab, size=9.5, ha="center", linespacing=1.1)
    cv.rect(26, 152, 46, 68, fc="#ffe0b3", ec=C["orange"], lw=1.2)
    cv.text(49, 238, L("离子源", "Ion source"), size=9.5, color=C["orange"], ha="center")
    cv.rect(816, 152, 46, 68, fc="#c9e8cf", ec=C["green"], lw=1.2)
    cv.text(839, 238, L("检测器", "Detector"), size=9.5, color=C["green"], ha="center")
    yc = 186
    for i, (a, b, c_) in enumerate(_MR):
        kind = "target" if i % 3 == 0 else ("isobar" if i % 3 == 1 else "other")
        f = ((t * 0.18 + a) % 1)
        x = 80 + f * 760
        col = {"target": C["red"], "isobar": C["magenta"], "other": C["orange"]}[kind]
        y = yc + 12 * math.sin(i + f * 20)
        if kind == "other" and x > 220:
            dy = (x - 220) * (1 if b > 0.5 else -1) * 0.9
            if abs(dy) > 52:
                continue
            y += dy
        if x > 344:
            if x < 544:
                # fragmentation
                if kind == "other":
                    continue
                if x > 380:
                    for d in range(2):
                        cv.circle(x + d * 6, y + (d * 2 - 1) * 8 * min(1, (x - 380) / 60), 3.2,
                                  fc=col if d == 0 else "#999", z=5)
                    continue
            else:
                if kind == "isobar":
                    dy = (x - 572) * (1 if b > 0.5 else -1) * 0.8
                    if abs(dy) > 50:
                        continue
                    y += dy
                if kind == "other":
                    continue
                if x > 812:
                    continue
                cv.circle(x, y, 4.5, fc=col, z=5)
                continue
        cv.circle(x, y, 5.5, fc=col, z=5)
    leg = [(C["red"], L("目标物 母离子 449 → 子离子 287", "Target: precursor 449 → product 287")),
           (C["magenta"], L("同为 m/z 449 的干扰离子（碎片不同）", "Interference also at m/z 449 (different fragments)")),
           (C["orange"], L("其他 m/z 的离子", "Ions of other m/z"))]
    for i, (col, lab) in enumerate(leg):
        cv.rect(24, 330 + i * 33, 16, 14, fc=col)
        cv.text(48, 337 + i * 33, lab, size=10)
    cv.lines(24, 440, [L("选择性和灵敏度高，常用于复杂基质中", "High selectivity and sensitivity — the workhorse"),
                       L("痕量成分的定量分析", "for trace quantitation in complex matrices")], size=10, gap=22, color=C["green"])
    ax = cv.inset(470, 312, 448, 170)
    ts = np.linspace(0, max(0.01, t), 500)
    rng = np.random.default_rng(1)
    base = 0.35 + 0.02 * np.sin(ts * 23)
    sim = base + 0.45 * gauss(ts, 6.5, 1.1)
    mrmc = 0.03 + 0.012 * np.sin(ts * 31) + 0.5 * gauss(ts, 6.5, 1.1)
    ax.plot(ts, sim, color=C["magenta"], lw=1.4, label=L("SIM m/z 449（只用 Q1）", "SIM m/z 449 (Q1 only)"))
    ax.plot(ts, mrmc, color=C["red"], lw=2, label="MRM 449 → 287")
    ax.set_xlim(0, D)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper left", ncol=2, frameon=False, fontsize=9)
    ax.text(D, -0.12, L("时间 →", "time →"), ha="right", fontsize=9)
    ax.text(0.2, 0.42, L("基线高、噪声大", "high, noisy baseline"), color=C["magenta"], fontsize=8.5)
    ax.text(0.2, 0.1, L("基线低、信噪比高", "low baseline, high S/N"), color=C["red"], fontsize=8.5)


ANIMS = [
    ("01-quadrupole", quadrupole, 12),
    ("02-esi", esi, 12),
    ("03-tic-eic", tic_eic, 14),
    ("04-mrm", mrm, 12),
]
