"""Chapter: 紫外-可见分光光度法 / UV–Vis Spectrophotometry."""
import math
import numpy as np
from common import *

CH = "uv-vis"


# ------------------------------------------------------------------ 01
def transitions(cv, t):
    D = 12
    cv.title(L("分子吸收光子后，电子从低能级轨道跃迁到高能级轨道",
               "On absorbing a photon, an electron moves from a lower to a higher orbital"))
    lv = {"s*": 112, "p*": 220, "n": 312, "p": 358, "s": 425}
    names = {"s*": L("σ*（反键轨道）", "σ* (antibonding)"), "p*": L("π*（反键轨道）", "π* (antibonding)"),
             "n": L("n（非键轨道）", "n (non-bonding)"), "p": L("π（成键轨道）", "π (bonding)"),
             "s": L("σ（成键轨道）", "σ (bonding)")}
    cv.arrow(48, 448, 48, 80, color=C["gray"], lw=1.2)
    cv.text(34, 260, L("能\n量", "Energy"), size=10, color=C["gray"], ha="center",
            rotation=0 if is_zh() else 90)
    for k, y in lv.items():
        cv.line([130, 372], [y, y], lw=2, color=C["ink"])
        cv.text(379, y, names[k], size=10.5)
    T = [  # from, to, x, colour, label, photon nm, bar (lo, hi, y), texts
        ("s", "s*", 165, "#7f9cc8", "σ→σ*", 150, (100, 150, 125),
         [L("饱和烃中的 C–C、C–H 键", "Saturated C–C and C–H bonds"),
          L("λ < 150 nm，处于远紫外区", "λ < 150 nm — far-UV region"),
          L("如甲烷 125 nm、乙烷 135 nm", "e.g. methane 125 nm, ethane 135 nm")]),
        ("n", "s*", 220, C["orange"], "n→σ*", 183, (150, 250, 168),
         [L("含 O、N、S、卤素的饱和化合物", "Saturated compounds with O, N, S or halogens"),
          L("λ 约 150–250 nm，多在远紫外区边缘", "λ ≈ 150–250 nm, mostly at the far-UV edge"),
          L("如甲醇 183 nm、甲胺 215 nm", "e.g. methanol 183 nm, methylamine 215 nm")]),
        ("p", "p*", 278, C["teal"], "π→π*", 180, (165, 200, 212),
         [L("孤立双键约 165–200 nm", "Isolated C=C: about 165–200 nm"),
          L("ε ≥ $10^4$，为强吸收", "ε ≥ $10^4$ — strong absorption"),
          L("形成共轭后能量降低，移至 200 nm 以上", "Conjugation lowers the gap → above 200 nm")]),
        ("n", "p*", 335, C["magenta"], "n→π*", 279, (270, 300, 256),
         [L("含杂原子的不饱和基团（C=O、N=O 等）", "Unsaturated groups with heteroatoms (C=O, N=O)"),
          L("约 270–300 nm，ε 仅 10–100（弱吸收）", "About 270–300 nm, ε only 10–100 (weak)"),
          L("如丙酮 279 nm", "e.g. acetone 279 nm")]),
    ]
    P = 2.6
    cur = min(3, int(t / P))
    u = (t - cur * P) / P
    # chart
    ax0, ay0, aw, ah = 540, 70, 378, 214
    def X(nm):
        return ax0 + (nm - 100) / 300 * aw
    cv.rect(X(100), ay0, X(200) - X(100), ah, fc="#ececec", z=0)
    cv.rect(X(200), ay0, X(400) - X(200), ah, fc="#f1eaf6", z=0)
    cv.text((X(100) + X(200)) / 2, ay0 + 16, L("远紫外区（<200 nm）\n普通仪器测不到", "Far UV (<200 nm)\nnot measurable"),
            size=8.5, color="#777", ha="center", linespacing=1.1)
    cv.text((X(200) + X(400)) / 2, ay0 + 16, L("近紫外区（200–400 nm）\n紫外光谱的测定范围", "Near UV (200–400 nm)\nrange of UV spectrometers"),
            size=8.5, color=C["magenta"], ha="center", linespacing=1.1)
    cv.line([ax0, ax0 + aw], [ay0 + ah, ay0 + ah], color=C["ink"], lw=1)
    for nm in range(100, 401, 50):
        cv.line([X(nm)] * 2, [ay0 + ah, ay0 + ah + 4], color=C["ink"], lw=1)
        cv.text(X(nm), ay0 + ah + 14, str(nm), size=9, ha="center")
    cv.text(X(250), ay0 + ah + 32, L("吸收波长 λ / nm", "Absorption wavelength λ / nm"), size=10, ha="center")
    for i, (a, b, x, col, lab, nm, bar, texts) in enumerate(T):
        if i > cur:
            continue
        done = 1.0 if i < cur else eseg(u, 0.25, 0.5)
        if done > 0:
            cv.arrow(x, lv[a], x, lerp(lv[a], lv[b], done) + 2, color=col, lw=2, alpha=0.9)
            if done > 0.6:
                cv.text(x + 5, [262, 170, 286, 262][i], lab, size=9.5, color=col, weight="bold",
                        bbox=dict(fc="white", ec="none", pad=1))
        lo, hi, by = bar
        bw = (1.0 if i < cur else eseg(u, 0.45, 0.65))
        if bw > 0:
            cv.rect(X(lo), by - 6, (X(hi) - X(lo)) * bw, 12, fc=col, alpha=0.85, z=3)
            cv.text(X(lo) - 5, by, lab, size=9.5, color=col, weight="bold", ha="right")
        if i == 2 and (i < cur or u > 0.65):
            al = 1.0 if i < cur else eseg(u, 0.65, 0.8)
            cv.arrow(X(205), by, X(280), by, color=col, lw=1.4, ls="--", alpha=al)
            cv.text(X(245), by - 13, L("共轭后", "conjugated"), size=9, color=col, ha="center", alpha=al)
    # current transition: photon + electron
    a, b, x, col, lab, nm, bar, texts = T[cur]
    if u < 0.3:
        fx = lerp(60, x - 25, eseg(u, 0.0, 0.25))
        xs, ys = wave(fx - 30, fx, lv[a], 7, 9, phase=u * 30)
        cv.line(xs, ys, color=col, lw=1.8)
    cv.text(95, lv[a] + 30, L(f"光子 hν\nλ≈{nm} nm", f"photon hν\nλ≈{nm} nm"), size=9, color=col, ha="center",
            alpha=fade(u, 0, 0.1, 0.4, 0.5), linespacing=1.1)
    ey = lerp(lv[a], lv[b], eseg(u, 0.25, 0.5))
    cv.circle(x, ey, 6.5, fc=C["red"], z=6)
    al = fade(u, 0.35, 0.5) if cur < 3 or u < 0.5 else 1
    cv.text(540, 345, lab + L(" 跃迁", " transition"), size=15, weight="bold", color=col, alpha=al)
    cv.lines(540, 392, texts, size=10.5, gap=24, alpha=al)


# ------------------------------------------------------------------ 02
def _uv_curve(lam):
    lam = np.asarray(lam, dtype=float)
    return (1.1 * np.exp(-(lam - 200) / 7) + 0.11 * gauss(lam, 232, 14)
            + 0.78 * gauss(lam, 275, 11) + 0.22 * gauss(lam, 300, 9))


def absorption_spectrum(cv, t):
    D = 12
    lam = lerp(200, 400, seg(t, 0.4, 7.8))
    A = float(_uv_curve(lam))
    cv.title(L("单色器逐个波长扫描，记录每个波长下的吸光度 → 得到吸收光谱",
               "The monochromator scans wavelength by wavelength, recording A → absorption spectrum"))
    y = 175
    cv.circle(44, y, 18, fc="#ffe08a", ec=C["orange"], lw=1.5)
    cv.text(44, y + 36, L("光源", "Source"), size=10, ha="center")
    cv.rect(62, y - 4, 34, 8, fc="#e1c47a", z=1)
    cv.rect(96, y - 36, 80, 72, fc=C["bg"], ec=C["teal"], lw=1.5, r=3)
    for k, cc in enumerate(["#d62728", "#e8a33d", "#2ca02c", "#1f77b4", "#7b4fa0"]):
        cv.line([110, 160], [y, y - 18 + k * 9], color=cc, lw=1)
    cv.text(136, y + 50, L("单色器", "Monochromator"), size=10, ha="center")
    beam = "#7b5ea7"
    cv.rect(176, y - 4, 108, 8, fc=beam, z=1)
    cv.text(230, y - 20, f"λ = {lam:.0f} nm", size=11, color=beam, weight="bold", ha="center")
    cv.rect(284, y - 42, 34, 84, fc="#dbeaf3", ec=C["ink"], lw=1.6, z=2)
    cv.text(301, y + 56, L("样品池", "Sample cell"), size=10, ha="center")
    cv.rect(318, y - 3, 48, 6, fc=beam, alpha=max(0.06, 10 ** (-A)), z=1)
    cv.rect(366, y - 30, 46, 60, fc="#555", r=2)
    cv.text(389, y + 50, L("检测器", "Detector"), size=10, ha="center")
    cv.rect(352, 98, 108, 36, fc="#14263d", r=2)
    cv.text(406, 116, f"A = {A:.3f}", size=12, color="#7ef0a0", ha="center", family="DejaVu Sans Mono")
    cv.text(406, 86, L("读数", "Reading"), size=9, color=C["gray"], ha="center")
    cv.text(24, 280, L("紫外光（200–400 nm）肉眼不可见，图中以紫色示意",
                       "UV light (200–400 nm) is invisible; it is drawn in purple here"), size=9, color=C["gray"])
    fin = fade(t, 8.0, 8.6)
    if fin < 0.5:
        cv.lines(24, 345, [L("每一个波长 λ 都测得一个吸光度 A，", "At each wavelength λ an absorbance A is measured;"),
                           L("以 A 为纵坐标、λ 为横坐标描点连线，", "plotting A against λ and joining the points"),
                           L("就得到该物质的吸收光谱（吸收曲线）。", "gives the absorption spectrum of the substance.")],
                 size=11, gap=30, alpha=1 - 2 * fin)
    else:
        cv.lines(24, 345, [L("吸收光谱的形状和 λmax 由分子结构决定：", "Shape and λmax depend on molecular structure:"),
                           (L("•  λmax、λmin、肩峰位置 —— 定性依据", "•  λmax, λmin, shoulders — for identification"), dict(color=C["red"])),
                           (L("•  在 λmax 处测定，灵敏度最高 —— 定量首选波长", "•  Measure at λmax: highest sensitivity for assays"), dict(color=C["red"]))],
                 size=11, gap=30, alpha=2 * fin - 1)
    ax = cv.inset(535, 50, 385, 380)
    xs = np.linspace(200, 400, 600)
    m = xs <= lam
    ax.plot(xs[m], _uv_curve(xs[m]), color=C["teal"], lw=2.2)
    ax.axvline(lam, color="#c9bfdc", lw=1)
    ax.plot([lam], [A], "o", color=C["red"], ms=7, zorder=5)
    ax.set_xlim(200, 400)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(L("波长 λ / nm", "Wavelength λ / nm"))
    ax.set_ylabel(L("吸光度 A", "Absorbance A"))
    if fin > 0:
        lmin = xs[(xs > 235) & (xs < 265)][np.argmin(_uv_curve(xs[(xs > 235) & (xs < 265)]))]
        kw = dict(fontsize=10, fontweight="bold", alpha=fin)
        ap = lambda c: dict(arrowstyle="->", color=c, lw=1.2, alpha=fin)
        ax.annotate(L("吸收峰\nλmax = 275 nm", "Peak\nλmax = 275 nm"), (275, 0.8), (305, 0.93), color=C["red"],
                    ha="center", arrowprops=ap(C["red"]), **kw)
        ax.annotate(L(f"吸收谷 λmin = {lmin:.0f} nm", f"Trough λmin = {lmin:.0f} nm"), (lmin, _uv_curve(lmin)), (203, 0.02),
                    color=C["magenta"], arrowprops=ap(C["magenta"]), **kw)
        ax.annotate(L("肩峰", "Shoulder"), (301, 0.33), (335, 0.5), color=C["orange"], arrowprops=ap(C["orange"]), **kw)
        ax.annotate(L("末端吸收", "End absorption"), (201.5, 0.9), (212, 0.98), color=C["gray"], arrowprops=ap(C["gray"]), **kw)


# ------------------------------------------------------------------ 03
SOLV = [("正己烷", "Hexane", 230, 329), ("氯仿", "Chloroform", 238, 315),
        ("甲醇", "Methanol", 237, 309), ("水", "Water", 243, 305)]


def solvent_effect(cv, t):
    D = 11
    P = D / 4
    k = min(3, int(t / P))
    u = (t - k * P) / P
    prev = SOLV[max(0, k - 1)]
    s = SOLV[k]
    f = eseg(u, 0, 0.3) if k > 0 else 1
    lpp = lerp(prev[2], s[2], f)
    lnp = lerp(prev[3], s[3], f)
    Epp, Enp = 1239.84 / lpp, 1239.84 / lnp
    cv.title(L("溶剂极性增大：π→π* 吸收红移，n→π* 吸收蓝移（以异亚丙基丙酮为例）",
               "More polar solvent: π→π* shifts red, n→π* shifts blue (mesityl oxide)"))
    K = 50
    yp = 365
    ypi = yp - K * Epp
    yn = ypi + K * Enp
    ypi0 = yp - K * 1239.84 / 230
    yn0 = ypi0 + K * 1239.84 / 329
    if k > 0:
        cv.line([62, 300], [ypi0, ypi0], color=C["gray"], lw=0.9, ls=":")
        cv.line([62, 300], [yn0, yn0], color=C["gray"], lw=0.9, ls=":")
        cv.text(58, yn0 - 4, L("正己烷中\n的位置", "in hexane"), size=8, color=C["gray"], ha="right", linespacing=1.0)
    for y, lab in ((ypi, "π*"), (yn, "n"), (yp, "π")):
        cv.line([62, 300], [y, y], lw=2.2, color=C["ink"])
        cv.text(308, y, lab, size=12)
    cv.arrow(125, yp, 125, ypi + 2, color=C["teal"], lw=2)
    cv.text(131, (yp + ypi) / 2 + 20, f"π→π*\nΔE={Epp:.2f} eV\nλ={lpp:.0f} nm", size=9.5, color=C["teal"],
            weight="bold", linespacing=1.05)
    cv.arrow(230, yn, 230, ypi + 2, color=C["magenta"], lw=2)
    cv.text(236, (yn + ypi) / 2 - 2, f"n→π*\nΔE={Enp:.2f} eV\nλ={lnp:.0f} nm", size=9.5, color=C["magenta"],
            weight="bold", linespacing=1.05)
    for i, (zh, en, *_r) in enumerate(SOLV):
        on = i == k
        cv.rect(34 + i * 99, 422, 88, 26, fc=C["teal"] if on else "#eef3f8", ec=C["teal"], lw=1, r=2)
        cv.text(78 + i * 99, 435, L(zh, en), size=10.5, ha="center", color="white" if on else C["ink"],
                weight="bold" if on else "normal")
    cv.arrow(34, 456, 418, 456, color=C["gray"], lw=1, head=6)
    cv.text(226, 468, L("溶剂极性增大 →", "solvent polarity increases →"), size=9, color=C["gray"], ha="center")
    ax = cv.inset(500, 70, 418, 284)
    xs = np.linspace(200, 380, 600)
    ax.spines["left"].set_visible(True)
    ax.set_yticks([])
    if k > 0:
        ax.plot(xs, gauss(xs, 230, 8.5), "--", color="#999", lw=1.2)
        ax.plot(xs, 0.45 * gauss(xs, 329, 11), "--", color="#999", lw=1.2)
        ax.text(372, 1.02, L("虚线：正己烷中", "dashed: in hexane"), fontsize=8.5, color="#888", ha="right")
    ax.plot(xs, gauss(xs, lpp, 8.5), color=C["teal"], lw=2.2)
    ax.plot(xs, 0.45 * gauss(xs, lnp, 11), color=C["magenta"], lw=2.2)
    ax.text(lpp + 6, 0.94, L("π→π*（K带，强）", "π→π* (K band, strong)"), color=C["teal"], fontsize=9.5, fontweight="bold")
    ax.text(lnp + 4, 0.62, L("n→π*（R带，弱；\n图中已放大显示）", "n→π* (R band, weak;\nenlarged here)"), color=C["magenta"],
            fontsize=9, fontweight="bold", ha="center")
    if k > 0 and f > 0.5:
        d1, d2 = s[2] - 230, s[3] - 329
        ax.annotate("", (lpp, 1.08), (230, 1.08), arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.5))
        ax.text(225, 1.12, L(f"红移 +{d1} nm", f"red shift +{d1} nm"), color=C["red"], fontsize=10, fontweight="bold")
        ax.annotate("", (lnp, 0.5), (329, 0.5), arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.5))
        ax.text(320, 0.53, L(f"蓝移 {d2} nm", f"blue shift {d2} nm").replace("-", "−"), color=C["red"], fontsize=10,
                fontweight="bold", ha="center")
    ax.set_xlim(200, 380)
    ax.set_ylim(0, 1.22)
    ax.set_xlabel(L("波长 λ / nm", "Wavelength λ / nm"))
    ax.set_ylabel(L("吸收强度（示意）", "Absorbance (schematic)"))


# ------------------------------------------------------------------ 04
POLY = [("乙烯", "Ethylene", 1, 170, "1.5×$10^4$"), ("1,3-丁二烯", "1,3-Butadiene", 2, 217, "2.1×$10^4$"),
        ("1,3,5-己三烯", "1,3,5-Hexatriene", 3, 258, "3.5×$10^4$"),
        ("1,3,5,7-辛四烯", "1,3,5,7-Octatetraene", 4, 296, "5.2×$10^4$"),
        ("1,3,5,7,9-癸五烯", "1,3,5,7,9-Decapentaene", 5, 334, "1.2×$10^5$")]


def conjugation(cv, t):
    D = 12
    P = D / 5
    k = min(4, int(t / P))
    u = (t - k * P) / P
    zh, en, n, lmax, eps = POLY[k]
    cv.title(L("共轭体系越长 → π→π* 跃迁能量越小 → λmax 红移、吸收增强",
               "Longer conjugation → smaller π→π* gap → λmax shifts red, absorption grows"))
    cv.text(48, 66, L(zh, en), size=13, weight="bold", color=C["teal"])
    # skeletal formula: 2n carbons, double bonds at 0-1, 2-3, ...
    N = 2 * n
    dx, dy = 30, 16
    pts = [(48 + i * dx, 128 + (dy if i % 2 else -dy) * (1 if i % 2 else 0) - (0 if i % 2 else 0)) for i in range(N)]
    pts = [(48 + i * dx, 112 if i % 2 == 0 else 138) for i in range(N)]
    if n == 1:
        pts = [(48, 125), (90, 125)]
    for i in range(N - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        cv.line([x0, x1], [y0, y1], color=C["ink"], lw=2.2)
        if i % 2 == 0:
            nx, ny = -(y1 - y0), (x1 - x0)
            ln = math.hypot(nx, ny)
            ox, oy = 6 * nx / ln, 6 * ny / ln
            if oy > 0:
                ox, oy = -ox, -oy
            cv.line([x0 + ox + 0.2 * (x1 - x0), x1 + ox - 0.2 * (x1 - x0)],
                    [y0 + oy + 0.2 * (y1 - y0), y1 + oy - 0.2 * (y1 - y0)], color=C["ink"], lw=2.2)
    cv.text(48, 178, L(f"共轭双键数：{n}", f"Conjugated C=C bonds: {n}"), size=11)
    cv.text(70, 222, L("π 分子轨道能级（示意）", "π molecular orbitals (schematic)"), size=10.5)
    ymid = 335
    lev = []
    for j in range(1, N + 1):
        e = math.cos(j * math.pi / (N + 1))
        lev.append((ymid + 80 * e, j <= n))
    for y, occ in lev:
        cv.line([76, 222], [y, y], color=C["teal"] if occ else "#9a9aaa", lw=1.8)
        if occ:
            cv.circle(138, y, 3.2, fc=C["ink"], z=4)
            cv.circle(162, y, 3.2, fc=C["ink"], z=4)
    homo = lev[n - 1][0]
    lumo = lev[n][0]
    cv.arrow(242, homo, 242, lumo, color=C["red"], lw=1.5, both=True, head=6)
    cv.text(252, (homo + lumo) / 2, "ΔE\n(HOMO→LUMO)", size=9, color=C["red"], linespacing=1.0)
    cv.text(76, 456, L("青色：已占轨道   灰色：空轨道", "teal: occupied   grey: empty"), size=8.5, color=C["gray"])
    ax = cv.inset(472, 72, 446, 282)
    xs = np.linspace(150, 520, 700)
    for j in range(k):
        l2, h2 = POLY[j][3], 0.35 + 0.13 * j
        ax.plot(xs, gauss(xs, l2, 16) * h2, color="#bbb", lw=1.2)
        ax.text(l2, h2 + 0.03, str(l2), fontsize=8, color="#999", ha="center")
    grow = eseg(u, 0.05, 0.35)
    h = (0.35 + 0.13 * k) * grow
    ax.plot(xs, gauss(xs, lmax, 16) * h, color=C["teal"], lw=2.4)
    ax.text(lmax + 6, h + 0.06, f"λmax ≈ {lmax} nm", color=C["red"], fontsize=12, fontweight="bold", alpha=grow)
    for i in range(60):
        nm = 400 + i * 2
        ax.axvspan(nm, nm + 2, ymin=0, ymax=0.035, color=wl_color(nm), lw=0)
    ax.axvline(400, color="#999", lw=0.8, ls=":")
    ax.text(460, 0.07, L("可见光区", "visible"), fontsize=8.5, color="#888", ha="center")
    ax.set_xlim(150, 520)
    ax.set_ylim(0, 1.05)
    ax.set_yticks([])
    ax.set_xlabel(L("波长 λ / nm", "Wavelength λ / nm"))
    ax.set_ylabel(L("吸收强度（示意）", "Absorbance (schematic)"))
    cv.text(472, 412, f"ε ≈ {eps} L·mol$^{{-1}}$·cm$^{{-1}}$", size=11)
    cv.text(472, 446, L("每增加一个共轭双键，λmax 约红移 30–40 nm", "Each extra conjugated C=C moves λmax ~30–40 nm red"),
            size=11, color=C["navy"])


# ------------------------------------------------------------------ 05
def stray_light(cv, t):
    D = 11
    A = lerp(0.02, 3.2, eseg(t, 0.3, 9.3))
    s_ex = 0.001
    T = 10 ** (-A)
    Ap = -math.log10((T + s_ex) / (1 + s_ex))
    cv.title(L("杂散光使测得的吸光度偏低，吸光度越大偏差越严重",
               "Stray light makes measured absorbance too low — worse at high A"))
    beam = "#7b5ea7"
    cv.text(30, 100, L("目标波长 λ 的单色光", "Monochromatic light at λ"), size=10, color=beam)
    cv.rect(28, 124, 176, 7, fc=beam)
    cv.rect(204, 88, 56, 136, fc="#c9ddef", ec=C["ink"], lw=1.6, z=2)
    cv.text(232, 238, L("样品池", "Sample"), size=10, ha="center")
    cv.rect(260, 125, 122, 5, fc=beam, alpha=max(0.05, T ** 0.35))
    cv.text(321, 146, L(f"透过 {T * 100:.2g}%", f"through: {T * 100:.2g}%"), size=9.5, color=beam, ha="center")
    cv.line([28, 382], [184, 184], color=C["orange"], lw=1.6, ls=(0, (5, 3)), z=3)
    cv.text(30, 210, L("杂散光（其他波长，\n样品几乎不吸收）", "Stray light (other λ,\nhardly absorbed)"), size=9.5,
            color=C["orange"], linespacing=1.1)
    cv.rect(382, 100, 48, 110, fc="#555", r=2)
    cv.text(406, 228, L("检测器", "Detector"), size=10, ha="center")
    cv.text(38, 264, L("以 0.1% 杂散光为例：", "Example with 0.1% stray light:"), size=10.5, color=C["teal"])
    rows = [(L("真实吸光度：", "True absorbance:"), f"A = {A:.2f}", C["navy"]),
            (L("检测器收到：", "Detector receives:"), f"{T * 100:.3g}% + 0.1% = {(T + s_ex) * 100:.3g}%", C["navy"]),
            (L("仪器显示：", "Instrument shows:"), f"A' = {Ap:.3f}" + (L(f"（偏低 {A - Ap:.3f}）", f"  (low by {A - Ap:.3f})") if A - Ap > 0.005 else ""), C["red"])]
    for i, (lab, val, col) in enumerate(rows):
        cv.text(38, 300 + 38 * i, lab, size=11, color=C["gray"])
        cv.text(165 if is_zh() else 200, 300 + 38 * i, val, size=12, weight="bold", color=col)
    ax = cv.inset(540, 76, 378, 364)
    xs = np.linspace(0, A, 300)
    ax.plot([0, 4], [0, 4], "--", color="#888", lw=1.4, label=L("无杂散光", "no stray light"))
    for s, col in ((1e-4, C["red"]), (1e-3, C["orange"]), (1e-2, C["magenta"])):
        ys = -np.log10((10 ** -xs + s) / (1 + s))
        ax.plot(xs, ys, color=col, lw=2.2, label=L(f"杂散光 {s * 100:g}%", f"stray light {s * 100:g}%"))
        ax.plot([A], [ys[-1]], "o", color=col, ms=6)
    ax.axvline(A, color="#bbb", lw=1)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_xlabel(L("真实吸光度 A", "True absorbance A"))
    ax.set_ylabel(L("测得吸光度 A'", "Measured absorbance A'"))


# ------------------------------------------------------------------ 06
def _source(tm):
    return 1 - 0.012 * tm + 0.035 * np.sin(tm * 1.9) - 0.01 * np.sin(tm * 0.7)


def beams(cv, t):
    D = 12
    tm = lerp(0, 10, seg(t, 0.3, 10.5))
    cv.title(L("双光束：参比与样品几乎同时测量，光源波动被“比值”抵消",
               "Double beam: reference and sample measured almost together — drift cancels in the ratio"))
    beam = "#7b5ea7"
    y = 152
    def common_parts(x0, label):
        cv.text(x0 - 22, 66, label, size=12, weight="bold", color=C["teal"])
        cv.circle(x0, y, 15, fc="#ffe08a", ec=C["orange"], lw=1.4)
        cv.text(x0, y + 28, L("光源", "Source"), size=9, ha="center")
        cv.rect(x0 + 15, y - 3, 30, 6, fc="#e1c47a")
        cv.rect(x0 + 45, y - 23, 52, 46, fc=C["bg"], ec=C["teal"], lw=1.4, r=2)
        cv.text(x0 + 71, y + 36, L("单色器", "Monochr."), size=9, ha="center")
    # single beam
    common_parts(44, L("单光束", "Single beam"))
    cv.rect(141, y - 3, 96, 6, fc=beam)
    cv.rect(237, y - 19, 22, 38, fc="#f2c6d6", ec=C["ink"], lw=1.2)
    cv.text(248, y - 30, L("样品池", "Sample"), size=9, ha="center")
    cv.rect(259, y - 2, 74, 4, fc=beam, alpha=0.6)
    cv.rect(333, y - 22, 34, 44, fc="#555", r=2)
    cv.text(350, y + 36, L("检测器", "Detector"), size=9, ha="center")
    cv.text(220, 222, L("先放参比调零，再换样品测定（前后有时间差）", "Blank first, then sample — at different times"),
            size=9, color=C["gray"], ha="center")
    # double beam with chopper
    common_parts(508, L("双光束", "Double beam"))
    cx = 668
    cv.rect(605, y - 3, 50, 6, fc=beam)
    ang = t * 6.0
    toR = math.cos(ang) > 0
    cv.circle(cx, y, 14, fc="white", ec=C["ink"], lw=1.3, z=4)
    cv.ax.add_patch(Wedge((cx, y), 14, math.degrees(ang) - 90, math.degrees(ang) + 90, fc=C["teal"], zorder=5))
    cv.text(cx - 4, y + 30, L("旋转扇面镜", "Chopper"), size=8.5, ha="center", bbox=dict(fc="white", ec="none", pad=1), zorder=6)
    Rx, Ry, Sx, Sy = 740, 100, 740, 206
    cv.rect(Rx - 11, Ry - 19, 22, 38, fc="#dcecf5", ec=C["ink"], lw=1.2)
    cv.text(Rx, Ry - 30, L("参比池 R", "Reference R"), size=9, ha="center")
    cv.rect(Sx - 11, Sy - 19, 22, 38, fc="#f2c6d6", ec=C["ink"], lw=1.2)
    cv.text(Sx, Sy + 30, L("样品池 S", "Sample S"), size=9, ha="center")
    dx = 840
    for (bx, by), on in (((Rx, Ry), toR), ((Sx, Sy), not toR)):
        cv.line([cx + 10, bx - 11], [y, by], color=beam if on else "#d8d0e6", lw=2.6 if on else 1.5)
        cv.line([bx + 11, dx - 16], [by, y], color=beam if on else "#d8d0e6", lw=1.8 if on else 1.2)
    cv.rect(dx - 16, y - 22, 34, 44, fc="#555", r=2)
    cv.text(dx + 1, y + 36, L("检测器", "Detector"), size=9, ha="center")
    cv.text(918, 90, "A = lg($I_R$ / $I_S$)", size=10.5, color=C["red"], ha="right", weight="bold")
    # readings
    ts = np.linspace(0, tm, 400)
    I = _source(ts)
    single = 0.5 + np.log10(1 / I)
    double = 0.5 + 0.002 * np.sin(ts * 7)
    ax = cv.inset(76, 292, 520, 166)
    ax.plot(ts, single, color=C["orange"], lw=2.2, label=L("单光束读数", "single-beam reading"))
    ax.plot(ts, double, color=C["teal"], lw=2.2, label=L("双光束读数", "double-beam reading"))
    ax.plot([tm], [single[-1]], "o", color=C["orange"], ms=6)
    ax.plot([tm], [double[-1]], "o", color=C["teal"], ms=6)
    ax.axhline(0.5, color="#bbb", lw=0.8, ls=":")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.4, 0.62)
    ax.set_xlabel(L("测量时间 / min", "Time / min"))
    ax.set_ylabel(L("吸光度 A", "Absorbance A"))
    ax.legend(loc="upper left", ncol=2, frameon=False, fontsize=9)
    ax2 = ax.twinx()
    ax2.plot(ts, I, "--", color="#999", lw=1.2)
    ax2.set_ylim(0.75, 1.1)
    ax2.tick_params(labelsize=8, colors="#999")
    ax2.set_ylabel(L("光源强度（相对）", "Source intensity (rel.)"), color="#999", fontsize=8.5)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color("#bbb")
    ax.text(9.9, 0.405, L("灰色虚线：光源强度缓慢漂移", "grey dashed: slowly drifting source"), fontsize=8, color="#999", ha="right")
    cv.lines(668, 320, [(L(f"光源强度：{I[-1] * 100:.1f}%", f"Source intensity: {I[-1] * 100:.1f}%"), dict(color=C["gray"])),
                        (L(f"单光束：A = {single[-1]:.3f}", f"Single beam: A = {single[-1]:.3f}"), dict(color=C["orange"], weight="bold")),
                        (L(f"双光束：A = {double[-1]:.3f}", f"Double beam: A = {double[-1]:.3f}"), dict(color=C["teal"], weight="bold"))],
             size=11.5, gap=30)
    cv.lines(668, 418, [L("单光束：光源漂移 → 读数漂移", "Single: source drift → reading drift"),
                        L("双光束：$I_R$、$I_S$ 同比变化，", "Double: $I_R$ and $I_S$ change together,"),
                        (L("比值不变 → 读数稳定", "ratio unchanged → stable reading"), dict(color=C["red"]))],
             size=10, gap=24, alpha=fade(t, 9.5, 10.3))


# ------------------------------------------------------------------ 07
def _err(A):
    T = 10 ** (-np.asarray(A, dtype=float))
    return np.abs(0.434 * 0.005 / (T * np.log10(T))) * 100


def abs_error(cv, t):
    D = 12
    # A goes 0.05 -> 1.6, then back to 0.434
    if t < 8:
        A = lerp(0.05, 1.6, eseg(t, 0.3, 7.6))
    else:
        A = lerp(1.6, 0.434, eseg(t, 8.2, 10.5))
    T = 10 ** (-A)
    e = float(_err(A))
    cv.title(L("透光率读数误差相同（ΔT = ±0.5%）时，浓度相对误差随吸光度变化",
               "Same reading error (ΔT = ±0.5%): relative concentration error depends on A"))
    cv.text(46, 104, L("透光率读数 T", "Transmittance reading T"), size=10.5)
    x0, x1 = 46, 446
    cv.rect(x0, 156, x1 - x0, 32, fc="#eef2f7", ec=C["ink"], lw=1.1)
    cv.rect(x0, 156, (x1 - x0) * T, 32, fc="#b9d7ea", z=2)
    tx = x0 + (x1 - x0) * T
    cv.line([tx, tx], [142, 198], color=C["red"], lw=2, z=3)
    cv.text(tx, 131, f"T = {T * 100:.1f}%", size=10.5, color=C["red"], weight="bold", ha="center")
    for p in range(0, 101, 20):
        xx = x0 + (x1 - x0) * p / 100
        cv.line([xx, xx], [188, 193], color=C["ink"], lw=1)
        cv.text(xx, 210, f"{p}%", size=8.5, ha="center")
    cv.text(246, 244, L("读数误差：同样 ±0.5%（仪器噪声、刻度读数等）", "Reading error is always ±0.5% (noise, scale reading…)"),
            size=9, color=C["gray"], ha="center")
    good = 0.2 <= A <= 0.7
    col = C["green"] if good else C["red"]
    msg = (L("处于适宜范围：误差较小", "Within the optimal range: small error") if good else
           L("A 过小：透过光太强，两次读数差别小，误差大", "A too small: little light absorbed, error large") if A < 0.2 else
           L("A 过大：透过光太弱，读数误差占比大", "A too large: too little light, error large"))
    if t > 10.5:
        msg = L("A = 0.434（T = 36.8%）时误差最小", "Minimum error at A = 0.434 (T = 36.8%)")
        col = C["green"]
    cv.text(48, 306, L(f"吸光度 A = {A:.3f}", f"Absorbance A = {A:.3f}"), size=12, weight="bold", color=C["navy"])
    cv.text(48, 346, L(f"浓度相对误差 ≈ {e:.2f}%", f"Relative error in c ≈ {e:.2f}%"), size=12.5, weight="bold", color=col)
    cv.text(48, 386, msg, size=11)
    cv.text(48, 458, "Δc/c = 0.434ΔT / (T·lgT)", size=10, color=C["gray"])
    ax = cv.inset(512, 80, 406, 354)
    xs = np.linspace(0.02, 1.6, 400)
    ax.axvspan(0.2, 0.7, color="#dff0e4")
    ax.text(0.45, 5.4, L("适宜范围\nA = 0.2 ~ 0.7", "Optimal range\nA = 0.2 – 0.7"), color=C["green"], fontsize=10,
            fontweight="bold", ha="center")
    ax.plot(xs, _err(xs), color=C["teal"], lw=2.2)
    ax.plot([A], [e], "o", color=C["red"], ms=8, zorder=5)
    ax.set_xlim(0, 1.6)
    ax.set_ylim(0, 6)
    ax.set_xlabel(L("吸光度 A", "Absorbance A"))
    ax.set_ylabel(L("浓度相对误差 |Δc/c| / %", "Relative error |Δc/c| / %"))


ANIMS = [
    ("01-electronic-transitions", transitions, 12),
    ("02-absorption-spectrum", absorption_spectrum, 12),
    ("03-solvent-effect", solvent_effect, 11),
    ("04-conjugation-red-shift", conjugation, 12),
    ("05-stray-light", stray_light, 11),
    ("06-single-double-beam", beams, 12),
    ("07-absorbance-error", abs_error, 12),
]
