"""Chapter: 光谱分析法概论 / Introduction to Spectroscopy."""
import math
import numpy as np
from common import *

CH = "spectroscopy-intro"


# ------------------------------------------------------------------ 01
def energy_levels(cv, t):
    D = 10.5
    ph = min(2, int(t / (D / 3)))
    u = (t - ph * D / 3) / (D / 3)
    col = [C["red"], C["green"], C["blue"]][ph]
    titles = [L("① 吸收：光子被吸收，粒子跃迁到高能级", "① Absorption: a photon is absorbed and the particle jumps up"),
              L("② 发射：粒子退激，放出特征光子", "② Emission: the particle relaxes and emits a characteristic photon"),
              L("③ 散射（拉曼）：经虚拟能级折返，频率改变", "③ Raman scattering: via a virtual level, the frequency changes")]
    notes = [L("条件：光子能量 hν 恰好等于能级差 ΔE  →  UV-Vis、IR、原子吸收",
               "Condition: photon energy hν equals the level gap ΔE  →  UV-Vis, IR, AAS"),
             L("信号在暗背景上测量  →  原子发射、荧光、化学发光，灵敏度更高",
               "Signal measured on a dark background  →  AES, fluorescence, chemiluminescence"),
             L("落回不同振动能级  →  散射光能量减少，位移量只取决于振动能级差",
               "Lands on a vibrational level  →  scattered light loses energy; shift = vibrational gap")]
    cv.title(titles[ph], color=col)
    # levels
    x0, x1 = 62, 560
    yV, yE1, yv, yE0 = 112, 196, 352, 408
    cv.line([240, 560], [yV, yV], color=C["gray"], lw=1.4, ls=(0, (4, 3)))
    cv.text(470, yV - 13, L("虚拟能级", "virtual level"), size=9.5, color=C["gray"], ha="center")
    cv.line([x0, x1], [yE1, yE1], lw=2.4)
    cv.text(x0, yE1 - 16, L("激发态 $E_1$", "Excited state $E_1$"), size=10.5, weight="bold", color=C["navy"])
    cv.line([380, 540], [yv, yv], lw=1.4)
    cv.text(460, yv - 12, L("振动能级", "vibrational level"), size=9.5, color=C["ink"], ha="center")
    cv.line([x0, x1], [yE0, yE0], lw=2.4)
    cv.text(x0, yE0 + 17, L("基态 $E_0$", "Ground state $E_0$"), size=10.5, weight="bold", color=C["navy"])
    cv.text(x0, yE0 + 42, notes[ph], size=10.5, color=C["ink"], alpha=fade(u, 0.05, 0.2))
    # spectrum box
    bx, by, bw, bh = 640, 92, 285, 318
    cv.rect(bx, by, bw, bh, ec=C["ink"], lw=1.1)
    cv.text(bx + bw / 2, by - 14, L("对应谱图", "Resulting spectrum"), size=10.5, ha="center", color=C["navy"])
    cv.text(bx + bw / 2, by + bh + 15, L("波长 →", "wavelength →"), size=10, ha="center", color=C["ink"])

    px = 300
    if ph == 0:
        # photon packet flies in, particle jumps
        fx = lerp(60, px - 70, eseg(u, 0.05, 0.4))
        if u < 0.42:
            xs, ys = wave(fx - 70, fx + 70, 290, 22, 28, phase=u * 40, envelope="packet")
            cv.line(xs, ys, color=col, lw=2)
            cv.arrow(fx + 72, 290, fx + 90, 290, color=col, lw=1.6)
        jump = eseg(u, 0.42, 0.6)
        cv.arrow(px, yE0, px, yE1, color=col, lw=2, alpha=fade(u, 0.42, 0.5))
        cv.circle(px, lerp(yE0, yE1, jump), 9, fc=C["red"])
        cv.text(px + 14, (yE0 + yE1) / 2, "ΔE = hν", size=11, color=col, weight="bold", alpha=fade(u, 0.5, 0.6))
        # absorption spectrum: bright background with a dip
        a = fade(u, 0.55, 0.75)
        xs = np.linspace(bx + 10, bx + bw - 10, 300)
        ys = by + 70 + 190 * gauss(xs, bx + bw * 0.5, 9) * a
        cv.line(xs, ys, color=col, lw=2)
        cv.text(bx + bw * 0.5 + 16, by + 230, L("吸收线", "absorption line"), size=10, color=col, alpha=a)
        cv.text(bx + 12, by + 55, L("透过光强", "transmitted intensity"), size=9, color=C["gray"], alpha=a)
    elif ph == 1:
        drop = eseg(u, 0.15, 0.4)
        cv.circle(px, lerp(yE1, yE0, drop), 9, fc=C["red"])
        cv.arrow(px, yE1, px, yE0, color=col, lw=2, alpha=fade(u, 0.1, 0.2))
        if u > 0.35:
            fx = lerp(px + 20, 560, eseg(u, 0.35, 0.75))
            xs, ys = wave(fx - 60, fx + 60, 290, 22, 28, phase=u * 40, envelope="packet")
            cv.line(xs, ys, color=col, lw=2, alpha=1 - seg(u, 0.75, 0.85))
        a = fade(u, 0.6, 0.8)
        cv.rect(bx + 1, by + 1, bw - 2, bh - 2, fc="#202733", alpha=0.9 * a, z=0)
        cv.line([bx + bw * 0.5] * 2, [by + 2, by + bh - 2], color="#6fdc6f", lw=4, alpha=a)
        cv.text(bx + bw * 0.5 + 10, by + 40, L("发射线", "emission line"), size=10, color="#bff0bf", alpha=a)
    else:
        # photon in -> virtual level -> down to vibrational level -> photon out
        fx = lerp(60, px - 70, eseg(u, 0.02, 0.25))
        if u < 0.27:
            xs, ys = wave(fx - 70, fx + 70, 290, 22, 28, phase=u * 40, envelope="packet")
            cv.line(xs, ys, color=C["gray"], lw=2)
        up = eseg(u, 0.27, 0.4)
        down = eseg(u, 0.45, 0.6)
        y = lerp(yE0, yV, up) if u < 0.45 else lerp(yV, yv, down)
        x = px if u < 0.45 else lerp(px, 440, down)
        cv.arrow(px, yE0, px, yV, color=C["gray"], lw=1.8, alpha=fade(u, 0.27, 0.33))
        cv.arrow(px + 8, yV, 440, yv, color=col, lw=1.8, alpha=fade(u, 0.45, 0.5))
        cv.circle(x, y, 9, fc=C["red"])
        if u > 0.55:
            fx = lerp(450, 600, eseg(u, 0.55, 0.85))
            xs, ys = wave(fx - 60, fx + 60, 260, 20, 38, phase=u * 40, envelope="packet")
            cv.line(xs, ys, color=col, lw=2, alpha=1 - seg(u, 0.85, 0.92))
        a = fade(u, 0.65, 0.8)
        xr, xs_ = bx + bw * 0.3, bx + bw * 0.66
        cv.line([xr, xr], [by + 2, by + bh - 2], color=C["gray"], lw=2.5, alpha=0.8)
        cv.text(xr - 6, by + 22, L("瑞利（入射）", "Rayleigh"), size=9, color=C["gray"], ha="right")
        cv.line([xs_, xs_], [by + 2, by + bh - 2], color=col, lw=3.5, alpha=a)
        cv.text(xs_ + 6, by + 22, L("拉曼", "Raman"), size=9, color=col, alpha=a)
        cv.arrow(xr + 3, by + 210, xs_ - 3, by + 210, color=col, lw=1.5, both=True, alpha=a)
        cv.text((xr + xs_) / 2, by + 192, L("拉曼位移", "Raman shift"), size=9.5, color=col, ha="center", alpha=a)


# ------------------------------------------------------------------ 02
BANDS = [(-3, -2, "γ 射线", "γ-rays", "核能级跃迁", "nuclear transitions"),
         (-2, 1, "X 射线", "X-rays", "内层电子", "inner-shell electrons"),
         (1, math.log10(380), "紫外", "UV", "价电子", "valence electrons"),
         (math.log10(380), math.log10(780), "可见", "Visible", "价电子", "valence electrons"),
         (math.log10(780), 6, "红外", "IR", "分子振动·转动", "molecular vibration/rotation"),
         (6, 9, "微波", "Microwave", "转动·电子自旋", "rotation, electron spin"),
         (9, 12, "射频", "Radio", "核自旋", "nuclear spin")]


def em_spectrum(cv, t):
    D = 12
    # log10(lambda/nm) sweeps up and back down
    s = 0.5 - 0.5 * math.cos(2 * math.pi * t / D)
    lg = lerp(-2.6, 11.6, s)
    lam = 10 ** lg
    nu = 2.998e17 / lam
    E = 1239.84 / lam
    band = next(b for b in BANDS if b[0] <= lg < b[1]) if lg < 12 else BANDS[-1]
    cv.title(L("同一束光：波长越短 → 频率越高 → 能量越大",
               "Same light: shorter wavelength → higher frequency → more energy"), y=30)
    # wave: visual wavelength from 30 px (short) to 260 px (long)
    vis = lerp(30, 260, (lg + 2.6) / 14.2)
    if band[2] == "可见":
        r, g, b = wl_color(lam)
        wc = (r * 0.85, g * 0.85, b * 0.85)
    else:
        wc = C["blue"]
    xs, ys = wave(24, 590, 150, 66, vis, phase=t * 6)
    cv.line(xs, ys, color=wc, lw=2.4)

    def fmt(v):
        return f"{v:.3g}" if 1e-3 <= v < 1e4 else f"{v:.2e}".replace("e+0", "e+").replace("e-0", "e-")
    unit = ""
    if lam >= 1e6:
        unit = f"  ({lam / 1e6:.3g} mm)" if lam < 1e9 else f"  ({lam / 1e9:.3g} m)"
    cv.lines(620, 78, [
        L("波长 λ = ", "Wavelength λ = ") + fmt(lam) + " nm" + unit,
        L("频率 ν = c/λ = ", "Frequency ν = c/λ = ") + fmt(nu) + " Hz",
        L("能量 E = hν = ", "Energy E = hν = ") + fmt(E) + " eV",
        "",
        L("所属波段：", "Region: ") + L(band[2], band[3]),
        L("激发的运动：", "Excites: ") + L(band[4], band[5]),
    ], size=12, gap=29, color=C["navy"])
    # band bar
    x0, x1, y0, h = 24, 900, 334, 64
    def X(v):
        return x0 + (v + 3) / 15 * (x1 - x0)
    for lo, hi, zh, en, *_ in BANDS:
        if zh == "可见":
            for k in range(40):
                nm = 380 + 400 * k / 40
                cv.rect(X(math.log10(nm)), y0, X(math.log10(nm + 10)) - X(math.log10(nm)) + 0.3, h,
                        fc=wl_color(nm), z=2)
            continue
        cv.rect(X(lo), y0, X(hi) - X(lo), h, fc=C["bg"], ec=C["blue"], lw=0.8)
        cv.text((X(lo) + X(hi)) / 2, y0 + h / 2, L(zh, en), size=9.5 if is_zh() else 8.5,
                ha="center", color=C["ink"])
    cv.rect(x0, y0, x1 - x0, h, ec=C["ink"], lw=1.1, z=3)
    vx = X(math.log10(580))
    cv.line([vx, vx], [y0 - 22, y0], color=C["ink"], lw=0.9)
    cv.text(vx, y0 - 30, L("可见", "Visible"), size=9.5, ha="center")
    for k in range(-3, 13):
        cv.line([X(k), X(k)], [y0 + h, y0 + h + 5], color=C["ink"], lw=0.9)
        cv.text(X(k), y0 + h + 15, f"$10^{{{k}}}$", size=8.5, ha="center")
    cv.text((x0 + x1) / 2, y0 + h + 38, L("波长 λ / nm", "Wavelength λ / nm"), size=10.5, ha="center", color=C["ink"])
    mx = X(lg)
    cv.poly([(mx - 7, y0 - 12), (mx + 7, y0 - 12), (mx, y0 - 1)], fc=C["red"], z=5)
    cv.line([mx, mx], [y0, y0 + h], color=C["red"], lw=1.6, z=5)


# ------------------------------------------------------------------ 03
def grating(cv, t):
    D = 10
    s = 0.5 - 0.5 * math.cos(2 * math.pi * t / D)
    dens = lerp(520, 1450, s)          # lines / mm
    d = 1e6 / dens                     # nm
    R = int(round(40 * dens))
    gx, gy = 285, 236
    cv.text(24, 36, L("入射白光", "Incident white light"), size=11, weight="bold", color=C["gray"])
    cv.line([gx, gx], [62, 412], color=C["gray"], lw=1.1, ls=(0, (3, 3)))
    for k in range(-3, 5):
        cv.line([gx - 16, gx + 16], [gy + 38 * k - 0, gy + 38 * k], color=C["navy"], lw=3)
    cv.text(gx - 10, 432, L("光栅", "Grating"), size=11, weight="bold", color=C["navy"], ha="right")
    # incident beam: white (drawn as rainbow-ish gray)
    cv.arrow(60, 110, gx - 18, gy - 4, color=C["gray"], lw=3, head=10)
    L_ray = 215
    lams = [430, 480, 530, 580, 630, 680]
    last_th = None
    for i, lam in enumerate(lams):
        th = math.asin(min(0.999, lam / d))
        ex, ey = gx + L_ray * math.cos(th), gy - L_ray * math.sin(th)
        col = wl_color(lam)
        cv.line([gx, ex], [gy, ey], color=col, lw=2.3, z=3)
        lx, ly = gx + (L_ray + 14) * math.cos(th), gy - (L_ray + 14) * math.sin(th)
        # label a ray only when it is far enough from the last labelled one
        if lam not in (430, 680) and last_th is not None and (th - last_th) * L_ray < 15:
            continue
        if lam == 680 and last_th is not None and (th - last_th) * L_ray < 15:
            ly -= 6
        last_th = th
        cv.text(lx, ly, f"{lam} nm", size=8.5, color=tuple(c * 0.8 for c in col), ha="left" if th < 1.2 else "center",
                va="center" if th < 1.2 else "bottom", weight="bold")
    cv.lines(600, 64, [
        L(f"刻线密度  {dens:.0f} 线/mm", f"Groove density  {dens:.0f} lines/mm"),
        L(f"栅距 d = {d:.0f} nm", f"Groove spacing d = {d:.0f} nm"),
        "",
        L("一级衍射 (n = 1)", "First order (n = 1)"),
        "   sin θ = λ / d",
        "",
        L("分辨本领 R = n·N", "Resolving power R = n·N"),
        L(f"   照亮 40 mm → R ≈ {R:,}", f"   40 mm illuminated → R ≈ {R:,}"),
        "",
        (L("→ 刻线越密，各色分得越开", "→ Denser grooves spread colours wider"), dict(weight="bold")),
    ], size=12, gap=29, color=C["navy"])


# ------------------------------------------------------------------ 04
def beer_lambert(cv, t):
    D = 11
    # concentration rises 0 -> 1, holds, falls to 0.2
    if t < 6:
        c = 0.02 + 0.98 * eseg(t, 0.3, 5.6)
        rising = True
    else:
        c = 1 - 0.8 * eseg(t, 6.5, 10.5)
        rising = False
    A = 2 * c / (1 + 0.38 * c * c)
    T = 10 ** (-A)
    cv.title(L("朗伯-比尔定律", "The Lambert–Beer law"), y=34)
    # optics
    cy = 190
    cv.rect(30, cy - 26, 44, 52, fc=C["yellow"], ec="#8a6d1d", lw=1)
    cv.rect(74, cy - 6, 112, 12, fc=C["yellow"], z=1)
    cv.text(120, cy - 20, "$I_0$", size=11, ha="center")
    blue = np.array([0.75, 0.85, 0.95]) * (1 - c) + np.array([0.2, 0.45, 0.85]) * c
    cv.rect(186, 112, 116, 156, fc=tuple(blue), ec=C["navy"], lw=2, z=2)
    rng = np.random.default_rng(3)
    pts = rng.random((60, 2))
    for k in range(int(6 + 54 * c)):
        cv.circle(196 + 96 * pts[k, 0], 122 + 136 * pts[k, 1], 3.2, fc="#1f4e8c", alpha=0.85, z=3)
    cv.text(244, 96, L("比色皿（光程 b）", "Cuvette (path length b)"), size=10.5, ha="center")
    cv.rect(302, cy - 6, 108, 12, fc=C["yellow"], alpha=max(0.05, T), z=1)
    cv.text(356, cy - 20, L("$I$（透射光减弱）", "$I$ (weakened)"), size=10.5, ha="center")
    cv.rect(410, cy - 26, 46, 52, fc=C["lgray"], ec="#666", lw=1)
    cv.text(30, 322, L("光源", "Source"), size=10.5)
    cv.text(456, 322, L("检测器", "Detector"), size=10.5, ha="right")
    msg = (L("高浓度下分子相互作用、折射率改变 → A 对 c 出现负偏离",
             "High c: molecular interactions → negative deviation from linearity")
           if c > 0.75 else
           L("稀溶液、单色光条件下 A 与 c 成正比，这是定量分析的依据",
             "Dilute solution + monochromatic light: A ∝ c — the basis of quantitation"))
    cv.lines(20, 386, [
        L(f"浓度 c = {c:.2f}（相对值）     透射比 T = I/$I_0$ = {T * 100:.1f}%",
          f"Concentration c = {c:.2f} (relative)     Transmittance T = I/$I_0$ = {T * 100:.1f}%"),
        L(f"吸光度 A = −lg T = {A:.2f}", f"Absorbance A = −lg T = {A:.2f}"),
        (msg, dict(color=C["red"] if c > 0.75 else C["navy"])),
    ], size=11, gap=29, color=C["navy"])
    # plot
    ax = cv.inset(590, 60, 330, 355)
    cs = np.linspace(0, 1, 200)
    ax.axvspan(0.75, 1.05, color=C["pink"], zorder=0)
    ax.text(0.9, 0.12, L("高浓度区\n偏离线性", "high c:\nnon-linear"), color=C["red"], fontsize=9, ha="center")
    ax.plot([0, 1], [0, 2], ls="--", color="#aaa", lw=1)
    ax.text(0.33, 1.95, L("理想线性 A = εbc", "Ideal: A = εbc"), fontsize=9, color="#555")
    upto = c if rising else 1.0
    m = cs <= upto
    ax.plot(cs[m], (2 * cs / (1 + 0.38 * cs ** 2))[m], color=C["red"], lw=2.2)
    ax.plot([c], [A], "o", color=C["red"], ms=7, zorder=5)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 2.15)
    ax.set_xlabel(L("浓度 c", "Concentration c"))
    ax.set_ylabel(L("吸光度 A", "Absorbance A"))


ANIMS = [
    ("01-energy-levels", energy_levels, 10.5),
    ("02-em-spectrum", em_spectrum, 12),
    ("03-grating", grating, 10),
    ("04-lambert-beer", beer_lambert, 11),
]
