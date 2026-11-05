"""Chapter: 红外吸收光谱法 / Infrared Spectroscopy."""
import math
import numpy as np
from common import *

CH = "infrared"
CM = "cm$^{-1}$"


def TT(zh, en):
    """Deferred translation for module-level tables (resolved with tr() at draw time)."""
    return (zh, en)


def tr(x):
    return L(*x) if isinstance(x, tuple) else x


def atom(cv, x, y, r, label, fc, tc="white", ec="#333", lw=1.4, size=None, z=5):
    cv.circle(x, y, r, fc=fc, ec=ec, lw=lw, z=z)
    if label:
        cv.text(x, y, label, size=size or max(7, r * 0.75), color=tc, ha="center", weight="bold", zorder=z + 1)


# ------------------------------------------------------------------ 01
def ch2_modes(cv, t):
    cv.title(L("以亚甲基（—CH$_2$—）为例：6 种基本振动形式", "Methylene (—CH$_2$—): the six fundamental vibrations"))
    cols = [(165, C["orange"], L("伸缩振动", "Stretching")),
            (470, C["teal"], L("面内弯曲振动", "In-plane bending")),
            (775, C["magenta"], L("面外弯曲振动", "Out-of-plane bending"))]
    for x, col, lab in cols:
        cv.badge(x, 62, lab, col, ha="center", size=10.5)
    modes = [  # col, row, name, symbol, wavenumber, kind
        (0, 0, L("对称伸缩", "Symmetric stretch"), r"$\nu_s$", 2853, "ss"),
        (0, 1, L("不对称伸缩", "Asymmetric stretch"), r"$\nu_{as}$", 2926, "as"),
        (1, 0, L("剪式振动", "Scissoring"), r"$\delta$", 1465, "sc"),
        (1, 1, L("面内摇摆", "Rocking"), r"$\rho$", 720, "ro"),
        (2, 0, L("面外摇摆", "Wagging"), r"$\omega$", 1300, "wa"),
        (2, 1, L("扭曲振动", "Twisting"), r"$\tau$", 1250, "tw"),
    ]
    for ci, ri, name, sym, wn, kind in modes:
        cx, col, _ = cols[ci]
        cy = 200 + ri * 200
        cv.text(cx, cy - 98, f"{name}（{sym}）" if is_zh() else f"{name} ({sym})", size=11.5, color=col,
                weight="bold", ha="center")
        ph = 2 * math.pi * t * wn / 1000 * 0.75
        s = math.sin(ph)
        # R groups
        for sx in (-1, 1):
            cv.line([cx, cx + sx * 52], [cy, cy + 34], color="#9a9a9a", lw=2.4, z=2)
            cv.text(cx + sx * 60, cy + 42, "R", size=8.5, color="#777", ha="center")
        base = [(-1, math.radians(145)), (1, math.radians(35))]
        Lb = 58
        for idx, (sx, ang) in enumerate(base):
            Lh, a = Lb, ang
            r = 10
            sign = None
            if kind == "ss":
                Lh = Lb * (1 + 0.16 * s)
            elif kind == "as":
                Lh = Lb * (1 + 0.16 * s * (1 if idx == 0 else -1))
            elif kind == "sc":
                a = ang + sx * 0.22 * s
            elif kind == "ro":
                a = ang + 0.3 * s
            elif kind == "wa":
                r = 10 + 2.5 * s
                sign = s
            elif kind == "tw":
                sg = s * (1 if idx == 0 else -1)
                r = 10 + 2.5 * sg
                sign = sg
            hx, hy = cx + Lh * math.cos(a), cy - Lh * math.sin(a)
            cv.line([cx, hx], [cy, hy], color="#555", lw=2.6, z=3)
            cv.circle(hx, hy, r, fc="#dce9f5", ec=C["ink"], lw=1.4, z=4)
            if sign is not None and abs(sign) > 0.15:
                cv.text(hx, hy, "+" if sign > 0 else "−", size=10, color=C["red"] if sign > 0 else C["ink"],
                        ha="center", weight="bold", zorder=6)
        atom(cv, cx, cy, 15, "C", "#5f5f5f")
        cv.text(cx, cy + 66, L(f"约 {wn} ", f"≈ {wn} ") + CM, size=10, ha="center")
    cv.text(24, 486, L("“+”“−”表示 H 原子垂直于纸面向前、向后运动；动画快慢示意振动频率高低：伸缩振动 > 弯曲振动",
                       "“+”/“−”: H moves toward/away from the viewer. Animation speed reflects frequency: stretching > bending"),
            size=9, color=C["gray"])


# ------------------------------------------------------------------ 02
def spring(cv, x0, x1, y, coils, amp, lw=1.3, color="#555", offset=0):
    n = coils * 2
    xs = np.linspace(x0, x1, n + 1)
    ys = np.array([y + offset + (amp if i % 2 else -amp) for i in range(n + 1)])
    ys[0] = ys[-1] = y + offset
    cv.line(xs, ys, color=color, lw=lw, z=3)


def springs(cv, t):
    cv.title(L("把化学键看作弹簧：力常数 k 越大、约化质量 μ 越小，振动频率越高",
               "A bond as a spring: larger k or smaller μ → higher vibrational frequency"))
    cv.text(24, 92, L("① 原子相同（C–C），键强度不同", "① Same atoms (C–C), different bond strength"), size=11,
            color=C["orange"], weight="bold")
    cv.text(500, 92, L("② 键强度相近，原子质量不同", "② Similar bond strength, different masses"), size=11,
            color=C["teal"], weight="bold")
    rows = [("C–C", 5, 6.0, 1, 172), ("C=C", 10, 6.0, 2, 267), ("C≡C", 15, 6.0, 3, 362)]
    for lab, k, mu, nb, y in rows:
        wn = 1307 * math.sqrt(k / mu)
        d = 9 * math.sin(2 * math.pi * t * wn / 1000 * 0.6)
        xa, xb = 95 - d, 182 + d
        for j in range(nb):
            off = (j - (nb - 1) / 2) * 6
            spring(cv, xa + 20, xb - 20, y, 9, 5, offset=off)
        atom(cv, xa, y, 21, "C", "#5f5f5f")
        atom(cv, xb, y, 21, "C", "#5f5f5f")
        cv.text(266, y - 10, lab, size=12, weight="bold")
        cv.text(266, y + 22, f"k ≈ {k} N/cm", size=9.5, color=C["gray"])
        cv.text(348, y, f"{wn:.0f} " + CM, size=11.5, color=C["red"], weight="bold")
    cv.arrow(452, 148, 452, 378, color=C["red"], lw=1.5)
    cv.text(462, 263, L("频\n率\n升\n高", "higher\nfreq."), size=9, color=C["red"], linespacing=1.0)
    rows2 = [("C–H", 1.0, 13 / 12 * 12 / 13, "H", 172), ("C–D", 2.0, 0, "D", 267)]
    for lab, m, _x, sym, y in rows2:
        mu = 12 * m / (12 + m)
        wn = 1307 * math.sqrt(5 / mu)
        ph = math.sin(2 * math.pi * t * wn / 1000 * 0.6)
        dl = 14 * ph * 12 / (12 + m)
        dh = 14 * ph * m / (12 + m)
        xc = 552 - dh
        xh = 646 + dl
        spring(cv, xc + 20, xh - 13, y, 9, 5)
        atom(cv, xc, y, 21, "C", "#5f5f5f")
        atom(cv, xh, y, 14 if sym == "H" else 16, sym, "#dce9f5", tc=C["ink"])
        cv.text(738, y - 10, lab, size=12, weight="bold")
        cv.text(738, y + 22, f"μ ≈ {mu:.3f} u", size=9.5, color=C["gray"])
        cv.text(820, y, f"{wn:.0f} " + CM, size=11.5, color=C["red"], weight="bold")
    cv.lines(500, 338, [L("H 原子很轻，C–H 伸缩频率高达约 3000 " + CM + "；",
                          "H is very light, so C–H stretches near 3000 " + CM + ";"),
                        L("换成质量为其 2 倍的 D（氘），频率降为约 0.73 倍",
                          "with D (twice the mass) the frequency drops to ~0.73×")], size=10.5, gap=30)
    cv.text(220, 470, r"$\tilde{\nu}$ (cm$^{-1}$) = 1307 $\sqrt{k/\mu}$", size=14)
    cv.text(470, 470, L("（k：N/cm，μ：原子质量单位 u）", "(k in N/cm, μ in atomic mass units u)"), size=11.5)


# ------------------------------------------------------------------ 03
def co2(cv, t):
    D = 11
    cv.title(L("只有使偶极矩发生变化的振动才吸收红外光（以 CO$_2$ 为例）",
               "Only vibrations that change the dipole moment absorb IR (CO$_2$)"))
    rows = [(128, L("对称伸缩", "Symmetric stretch"), "1340 " + CM, L("红外非活性", "IR inactive"), C["gray"], "sym"),
            (264, L("不对称伸缩", "Asymmetric stretch"), "2349 " + CM, L("红外活性", "IR active"), C["red"], "asym"),
            (400, L("弯曲振动", "Bending"), "667 " + CM, L("红外活性", "IR active"), C["red"], "bend")]
    tm = seg(t, 0.3, 10.5)
    for y, name, wn, act, ac, kind in rows:
        w = 2 * math.pi * {"sym": 0.8, "asym": 1.1, "bend": 0.45}[kind]
        s = math.sin(w * t)
        cx = 190
        dO = 76
        oxL, oxR, cxp, cy, oyL, oyR = cx - dO, cx + dO, cx, y, y, y
        dip = 0.0
        if kind == "sym":
            oxL -= 10 * s
            oxR += 10 * s
        elif kind == "asym":
            cxp += 12 * s
            oxL += 4 * s
            oxR += 4 * s
            dip = s
        else:
            cy = y - 14 * s
            oyL = oyR = y + 5 * s
            dip = s
        for (ox, oy) in ((oxL, oyL), (oxR, oyR)):
            for o in (-3, 3):
                cv.line([ox, cxp], [oy + o, cy + o], color="#555", lw=1.6, z=3)
        atom(cv, oxL, oyL, 21, "O", "#d9534f")
        atom(cv, oxR, oyR, 21, "O", "#d9534f")
        atom(cv, cxp, cy, 15, "C", "#5f5f5f")
        cv.text(oxL, oyL - 40, "δ−", size=8.5, color=C["gray"], ha="center")
        cv.text(oxR, oyR - 40, "δ−", size=8.5, color=C["gray"], ha="center")
        cv.text(cxp, cy - 40, "δ+", size=8.5, color=C["gray"], ha="center")
        if kind == "asym":
            cv.arrow(190, y + 52, 190 + 34 * dip, y + 52, color=C["orange"], lw=2.2, alpha=min(1, abs(dip) * 3))
        if kind == "bend":
            cv.arrow(318, y, 318, y - 22 * dip, color=C["orange"], lw=2.2, alpha=min(1, abs(dip) * 3))
        cv.text(372, y - 30, name, size=11.5, weight="bold", color=C["navy"])
        cv.text(372, y + 10, wn, size=10.5, color=C["gray"])
        cv.text(372, y + 50, act, size=11.5, weight="bold", color=ac)
        ax = cv.inset(548, y - 48, 370, 96)
        ts = np.linspace(0, 10.5 * tm, 400)
        ax.axhline(0, color="#ccc", lw=0.8)
        if kind == "sym":
            ax.plot(ts, 0 * ts, color="#888", lw=2)
            ax.text(10.3, 0.65, L("偶极矩始终为零 → 不吸收红外光", "dipole stays zero → no IR absorption"), fontsize=9,
                    color="#888", ha="right")
        else:
            ax.plot(ts, np.sin(w * ts), color=C["orange"], lw=2)
        ax.set_xlim(0, 10.5)
        ax.set_ylim(-1.25, 1.25)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylabel(L("偶极矩", "dipole"), fontsize=8.5, color="#888")
    cv.text(733, 462, L("时间 →", "time →"), size=9, color=C["gray"], ha="center")
    cv.text(24, 486, L("橙色箭头：瞬时偶极矩。对比：H$_2$O 为弯曲形分子，三种振动都改变偶极矩，均为红外活性。",
                       "Orange arrows: instantaneous dipole. By contrast, bent H$_2$O changes its dipole in all three modes — all IR active."),
            size=9.5)


# ------------------------------------------------------------------ 04
_NU = np.linspace(500, 4000, 700)          # cm-1
_SRC = np.exp(-((_NU - 1900) / 1500) ** 2)
_TRANS = 1 - (0.75 * gauss(_NU, 2950, 40) + 0.85 * gauss(_NU, 1715, 22) + 0.5 * gauss(_NU, 1450, 25)
              + 0.6 * gauss(_NU, 1250, 30) + 0.45 * gauss(_NU, 3400, 120) + 0.4 * gauss(_NU, 1050, 25)
              + 0.35 * gauss(_NU, 820, 18))


def _ifg(delta_um, poly):
    if not poly:
        return np.cos(2 * np.pi * 0.2 * delta_um)
    S = _SRC * _TRANS
    I = (S[None, :] * np.cos(2 * np.pi * (_NU[None, :] * 1e-4) * delta_um[:, None])).sum(1)
    return I / S.sum()


def ftir(cv, t):
    D = 14
    poly = t >= 6.0
    tt = t - 6.0 if poly else t
    scan_end = 4.6
    p = seg(tt, 0.3, scan_end)
    delta = lerp(-40, 40, p)
    cv.title(L("傅里叶变换红外光谱仪：干涉仪记录干涉图，经傅里叶变换得到光谱",
               "FT-IR: the interferometer records an interferogram; Fourier transform gives the spectrum"))
    beam = C["orange"] if not poly else "#d4a017"
    # interferometer
    bx, by = 200, 232
    cv.circle(46, by, 18, fc="#ffd9b3" if not poly else "#ffe08a", ec=C["orange"], lw=1.4)
    cv.text(46, by + 36, L("光源", "Source"), size=10, ha="center")
    cv.text(50, by + 56, L("单色光", "monochromatic") if not poly else L("红外复合光", "broadband IR"), size=8.5,
            color=C["gray"], ha="center")
    mx = 356 + 10 * (delta / 40)
    cv.line([64, mx], [by, by], color=beam, lw=2.6)
    cv.line([bx, bx], [112, 410], color=beam, lw=2.6)
    cv.line([bx - 22, bx + 22], [by + 22, by - 22], color=C["navy"], lw=3, z=4)
    cv.text(bx + 30, by - 36, L("分束器", "Beam splitter"), size=10)
    cv.line([168, 232], [110, 110], color=C["navy"], lw=5, z=4)
    cv.text(238, 110, L("定镜", "Fixed mirror"), size=10)
    cv.line([mx, mx], [200, 264], color=C["navy"], lw=5, z=4)
    cv.text(mx, 182, L("动镜", "Moving mirror"), size=10, ha="center")
    cv.arrow(322, 276, 404, 276, color=C["red"], lw=1.3, both=True, head=6)
    cv.text(363, 295, L("来回移动", "moves back and forth"), size=9, color=C["red"], ha="center")
    if poly:
        cv.rect(182, 312, 36, 40, fc="#dbeaf3", ec=C["ink"], lw=1.2, z=5)
        cv.text(174, 332, L("样品", "Sample"), size=10, ha="right")
    cv.rect(174, 408, 52, 40, fc="#555", r=2)
    cv.text(166, 428, L("检测器", "Detector"), size=10, ha="right")
    cv.text(242, 360, L(f"光程差 δ = {delta:+.1f} μm", f"Path difference δ = {delta:+.1f} μm"), size=11,
            color=C["red"], weight="bold")
    cv.lines(246, 396, [L("两束光相遇发生干涉，", "The two beams interfere;"), L("光强随 δ 起伏", "intensity varies with δ")],
             size=10, gap=24)
    # interferogram
    cv.text(500, 72, L("单色光的干涉图：余弦波", "Monochromatic light: a cosine wave") if not poly else
            L("复合光的干涉图：中心处出现“中心爆发”", "Broadband light: centre burst at δ = 0"), size=10.5)
    ax = cv.inset(500, 86, 418, 150)
    ds = np.linspace(-40, delta, max(2, int(800 * p)))
    I = _ifg(ds, poly)
    ax.plot(ds, I, color=C["teal"], lw=1.4 if poly else 1.8)
    ax.plot([delta], [I[-1]], "o", color=C["red"], ms=5)
    ax.set_xlim(-40, 40)
    ax.set_ylim(-1.1, 1.1) if not poly else ax.set_ylim(-0.7, 1.1)
    ax.set_yticks([])
    ax.set_xlabel(L("光程差 δ / μm", "Path difference δ / μm"), labelpad=1)
    # spectrum
    ax2 = cv.inset(500, 322, 418, 142)
    ax2.set_xlim(4000, 450)
    ax2.set_xlabel(L("波数 / ", "Wavenumber / ") + CM, labelpad=1)
    sp = eseg(tt, scan_end + 0.2, scan_end + 1.0)
    if not poly:
        ax2.set_ylim(0, 1.1)
        ax2.set_ylabel(L("强度", "Intensity"))
        if sp > 0:
            ax2.plot([2000, 2000], [0, sp], color=C["orange"], lw=3)
            ax2.text(1900, 0.85, L("单色光 → 光谱中只有一条谱线", "monochromatic → one single line"), fontsize=9.5,
                     color="#777", alpha=sp)
        else:
            ax2.text(2225, 0.5, L("采集完整干涉图后进行傅里叶变换", "Fourier transform after the full scan"),
                     fontsize=9.5, color="#999", ha="center")
    else:
        ax2.set_ylim(0, 1.08)
        ax2.set_ylabel("T")
        if sp > 0:
            m = _NU >= 4000 - 3500 * sp
            ax2.plot(_NU[m], _TRANS[m], color=C["teal"], lw=1.6)
            ax2.text(4000 - 30, 0.12, "FT ✓", fontsize=10, color=C["red"], fontweight="bold", alpha=sp)
        else:
            ax2.text(2225, 0.5, L("采集完整干涉图后进行傅里叶变换", "Fourier transform after the full scan"),
                     fontsize=9.5, color="#999", ha="center")


# ------------------------------------------------------------------ 05
CONC = [(0.01, (1.0, 0.0, 0.0), 5,
         TT("浓度很低：分子彼此远离，O–H 处于游离状态", "Very dilute: molecules are far apart, O–H is free"),
         TT("3640 " + CM + " 处为尖锐的吸收峰", "a sharp peak at 3640 " + CM)),
        (0.1, (0.55, 0.85, 0.45), 14,
         TT("浓度增大：开始形成二聚体", "Higher c: dimers start to form"),
         TT("3515 " + CM + " 附近出现新峰", "a new band appears near 3515 " + CM)),
        (0.5, (0.12, 0.35, 1.0), 26,
         TT("浓度更大：形成多聚体", "Higher still: polymeric chains form"),
         TT("3350 " + CM + " 处出现宽而强的吸收带", "a broad, strong band at 3350 " + CM)),
        (1.0, (0.05, 0.25, 1.25), 34,
         TT("高浓度：以多聚体为主", "High c: mostly polymeric association"),
         TT("游离峰几乎消失，宽峰占主导", "free peak almost gone; broad band dominates"))]


def _ethanol(cv, x, y, ang, alpha=1):
    ox, oy = x, y
    hx, hy = x + 11 * math.cos(ang), y + 11 * math.sin(ang)
    c1x, c1y = x - 15 * math.cos(ang - 0.9), y - 15 * math.sin(ang - 0.9)
    c2x, c2y = c1x - 14 * math.cos(ang + 0.3), c1y - 14 * math.sin(ang + 0.3)
    cv.line([ox, hx], [oy, hy], color="#777", lw=1.2, z=3)
    cv.line([ox, c1x, c2x], [oy, c1y, c2y], color="#777", lw=1.5, z=3)
    cv.circle(c2x, c2y, 5.5, fc="#8a8a8a", z=4)
    cv.circle(c1x, c1y, 5.5, fc="#8a8a8a", z=4)
    cv.circle(ox, oy, 6.5, fc="#d9534f", z=5)
    cv.circle(hx, hy, 3.8, fc="white", ec="#333", lw=0.8, z=5)
    return (hx, hy)


def hbond(cv, t):
    D = 12
    P = D / 4
    k = min(3, int(t / P))
    u = (t - k * P) / P
    c, (wf, wd, wp), nmol, l1, l2 = CONC[k]
    l1, l2 = tr(l1), tr(l2)
    prev = CONC[max(0, k - 1)][1]
    f = eseg(u, 0, 0.35) if k else 1
    wf, wd, wp = (lerp(prev[i], (wf, wd, wp)[i], f) for i in range(3))
    cv.title(L("氢键对 O–H 伸缩振动的影响：乙醇的 CCl$_4$ 溶液，浓度逐渐增大",
               "Hydrogen bonding and the O–H stretch: ethanol in CCl$_4$, increasing concentration"))
    bx, by, bw, bh = 20, 72, 376, 308
    cv.rect(bx, by, bw, bh, fc="#f5f8fc", ec="#c9d3df", lw=1.2, r=3)
    cv.text(bx + 10, by + 26, f"c ≈ {c:g} mol/L", size=12, weight="bold")
    rng = np.random.default_rng(11 + k)
    # clusters: free molecules + chains
    nfree = max(1, int(round(nmol * [1, 0.35, 0.12, 0.05][k])))
    sizes = [1] * nfree
    rest = nmol - nfree
    while rest > 0:
        sz = min(rest, 2 if k == 1 else rng.integers(3, 5))
        sizes.append(int(sz))
        rest -= sz
    cells = [(bx + 40 + (i % 4) * 86, by + 74 + (i // 4) * 62) for i in range(16)]
    rng.shuffle(cells)
    jit = lambda: rng.uniform(-10, 10)
    for ci, sz in enumerate(sizes[:len(cells)]):
        x0, y0 = cells[ci]
        wob = 2.5 * math.sin(t * 3 + ci)
        prev_h = None
        ang0 = rng.uniform(0, 2 * math.pi)
        for j in range(sz):
            x = x0 + j * 20 + jit() * 0.3 + wob
            y = y0 + (j % 2) * 18 + jit() * 0.3
            if prev_h is not None:
                cv.line([prev_h[0], x], [prev_h[1], y], color=C["red"], lw=1.1, ls=(0, (2, 2)), z=2)
            prev_h = _ethanol(cv, x, y, ang0 + j * 0.4)
    cv.text(bx + bw - 10, by + 26, L("红色虚线：分子间氢键", "red dashed: intermolecular H-bond"), size=9,
            color=C["red"], ha="right")
    for i, (cc, *_r) in enumerate(CONC):
        on = i == k
        cv.rect(34 + i * 90, 405, 78, 32, fc=C["teal"] if on else "#eef3f8", ec=C["teal"], lw=1, r=2)
        cv.text(73 + i * 90, 421, f"{cc:g} M", size=10.5, ha="center", color="white" if on else C["ink"],
                weight="bold" if on else "normal")
    ax = cv.inset(474, 76, 444, 278)
    xs = np.linspace(3000, 3800, 800)
    y = (wf * 0.95 * gauss(xs, 3640, 9) + wd * 0.8 * gauss(xs, 3515, 28) + wp * 0.62 * gauss(xs, 3350, 75))
    ymax = max(1.0, y.max() * 1.1)
    ax.plot(xs, y / ymax, color=C["teal"], lw=2)
    for (x0, lab, col, h) in ((3640, L("游离 O–H", "free O–H"), C["orange"], wf * 0.95),
                              (3515, L("二聚体", "dimer"), C["magenta"], wd * 0.8),
                              (3350, L("多聚体", "polymer"), C["red"], wp * 0.62)):
        if h > 0.05:
            yy = float(np.interp(x0, xs, y)) / ymax
            ax.annotate(f"{lab}\n{x0}", (x0, yy + 0.02), (x0, min(1.0, yy + 0.16)), ha="center", fontsize=9,
                        color=col, fontweight="bold", arrowprops=dict(arrowstyle="-", color="#bbb", lw=0.8))
    ax.set_xlim(3800, 3000)
    ax.set_ylim(0, 1.2)
    ax.set_yticks([])
    ax.set_xlabel(L("波数 / ", "Wavenumber / ") + CM)
    ax.set_ylabel(L("吸光度（归一化）", "Absorbance (normalised)"))
    cv.lines(474, 410, [l1, l2], size=10.5, gap=24, alpha=fade(u, 0.2, 0.4) if k else 1)
    cv.text(24, 482, L("氢键使 O–H 键力常数减小 → 吸收移向低波数，峰变宽、变强；分子间氢键随浓度改变，分子内氢键则不随浓度改变",
                       "H-bonding weakens O–H → lower wavenumber, broader, stronger. Intermolecular H-bonds depend on c; intramolecular ones do not"),
            size=9.2, color=C["red"])


# ------------------------------------------------------------------ 06
REG = [(4000, 2500, "#e8743b", "#fbefe7", TT("X–H 伸缩振动区", "X–H stretching"), "4000–2500"),
       (2500, 2000, "#a12d8f", "#f3e8f1", TT("三键和\n累积双键区", "Triple bonds &\ncumulated C=C"), "2500–2000"),
       (2000, 1500, "#1b6f8a", "#e6eff3", TT("双键伸缩\n振动区", "Double-bond\nstretching"), "2000–1500"),
       (1500, 400, "#2d4059", "#f1f1f1", TT("指纹区", "Fingerprint region"), "1500–400")]
BANDS = [(3650, 3200, 0, TT("O–H", "O–H"), 0), (3500, 3300, 0, TT("N–H", "N–H"), 1),
         (3100, 3000, 0, TT("=C–H、Ar–H", "=C–H, Ar–H"), 2), (3330, 3270, 0, TT("≡C–H", "≡C–H"), 3),
         (3000, 2850, 0, TT("饱和 C–H", "sat. C–H"), 3),
         (2260, 2100, 1, "C≡C", 0), (2260, 2210, 1, "C≡N", 1),
         (1850, 1650, 2, "C=O", 0), (1680, 1620, 2, "C=C", 1), (1600, 1450, 2, TT("苯环骨架", "aromatic ring"), 2),
         (1470, 1350, 3, TT("C–H 弯曲", "C–H bending"), 3),
         (1300, 1000, 3, "C–O", 0), (900, 650, 3, TT("芳环 C–H 面外弯曲", "Ar C–H out-of-plane"), 1)]


def ir_regions(cv, t):
    D = 12
    wn = lerp(4000, 400, seg(t, 0.3, 9.5))
    cv.title(L("读谱先分区：从高波数到低波数，依次对应不同类型的振动",
               "Read an IR spectrum by regions: from high to low wavenumber"))
    x0, x1, y0, y1 = 38, 918, 72, 390
    def X(w):
        return x0 + (4000 - w) / 3600 * (x1 - x0)
    for hi, lo, col, bg, name, rng in REG:
        a = 1.0 if wn <= hi - 1 else 0.0
        if wn < hi:
            right = X(max(lo, wn))
            cv.rect(X(hi), y0, right - X(hi), y1 - y0, fc=bg, z=0)
            cv.text((X(hi) + X(lo)) / 2, y0 + 22, tr(name), size=10.5, weight="bold", color=col, ha="center",
                    linespacing=1.0, alpha=eseg(hi - wn, 0, 120))
            cv.text((X(hi) + X(lo)) / 2, y0 + 58, rng, size=9, color=col, ha="center", alpha=eseg(hi - wn, 0, 120))
        cv.line([X(lo)] * 2, [y0, y1], color="#ccc", lw=0.8)
    for hi, lo, ri, name, row in BANDS:
        if wn > hi:
            continue
        col = REG[ri][2]
        yy = 152 + row * 56
        frac = eseg(hi - wn, 0, max(1, hi - lo))
        cv.rect(X(hi), yy, (X(lo) - X(hi)) * frac, 24, fc=col, alpha=0.85, z=2)
        cv.text((X(hi) + X(lo)) / 2, yy + 38, tr(name), size=9.5, weight="bold", color=col, ha="center", alpha=frac)
    cv.line([x0, x1], [y1, y1], color=C["ink"], lw=1)
    for w in range(4000, 399, -500):
        cv.line([X(w)] * 2, [y1, y1 + 5], color=C["ink"], lw=1)
        cv.text(X(w), y1 + 17, str(w), size=9.5, ha="center")
    cv.text((x0 + x1) / 2, y1 + 38, L("波数 / ", "Wavenumber / ") + CM, size=10.5, ha="center")
    if t < 9.6:
        cv.line([X(wn)] * 2, [y0, y1], color=C["red"], lw=2.2, z=6)
        cv.text(X(wn) + 4, y1 - 12, f"{wn:.0f}", size=9, color=C["red"])
    cv.text(24, 476, L("前三区为特征区（官能团区），峰少而特征，用于判断官能团；指纹区峰多而复杂，反映分子整体结构",
                       "The first three regions identify functional groups; the crowded fingerprint region reflects the whole molecule"),
            size=9.5, color=C["navy"], alpha=fade(t, 9.6, 10.4))


ANIMS = [
    ("01-ch2-vibrations", ch2_modes, 10),
    ("02-force-constant", springs, 10),
    ("03-ir-activity", co2, 11),
    ("04-ftir", ftir, 14),
    ("05-hydrogen-bonding", hbond, 12),
    ("06-ir-regions", ir_regions, 12),
]
