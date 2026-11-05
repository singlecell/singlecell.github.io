"""Shared helpers for the bilingual HD teaching animations.

Every animation is drawn on a 946 x 505 "design canvas" (pixel coordinates,
origin top-left, y down) and rendered at DPI so the output is 2x (1892 x 1010).
"""
import os, subprocess, math, warnings, logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
warnings.filterwarnings("error", message=".*[Gg]lyph.*missing")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import (Rectangle, FancyBboxPatch, Circle, Polygon,
                                FancyArrowPatch, Ellipse, Wedge, Arc)
from matplotlib.lines import Line2D

FONT_DIR = os.environ.get("ANIM_FONT_DIR")
for w in ("400Regular", "500Medium", "700Bold"):
    font_manager.fontManager.addfont(f"{FONT_DIR}/{w}/NotoSansSC_{w}.ttf")
plt.rcParams.update({
    "font.family": "Noto Sans SC",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Noto Sans SC",
    "mathtext.it": "Noto Sans SC:italic",
    "mathtext.bf": "Noto Sans SC:bold",
    "axes.unicode_minus": False,
    "font.size": 11,
    "axes.linewidth": 1.0,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.labelsize": 10,
})

W_PX, H_PX = 946, 505          # design canvas
SCALE = 2                      # output = 1892 x 1010
DPI = 100 * SCALE
FIGSIZE = (W_PX / 100, H_PX / 100)
OUT_W, OUT_H = W_PX * SCALE, H_PX * SCALE

C = dict(
    navy="#1f3864", ink="#22324a", blue="#2e75b6", teal="#1b6f8a", sky="#7fb3d5",
    orange="#e8743b", red="#c00000", green="#2e7d32", magenta="#a12d8f",
    purple="#6a3d9a", gray="#8a8a8a", lgray="#d9d9d9", bg="#eef3f9",
    yellow="#f2c14e", sand="#f3e6c4", pink="#fbe9ea", mint="#e6f2ea",
)

LANG = "zh"


def is_zh():
    return LANG == "zh"


_Q = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})


def L(zh, en):
    """Pick the string for the current language (CJK curly quotes are too wide in Latin text)."""
    return zh if LANG == "zh" else en.translate(_Q)


# ---------------------------------------------------------------- timing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    """Linear progress of t through [a, b], clamped to [0, 1]."""
    return clamp((t - a) / (b - a)) if b > a else float(t >= b)


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eseg(t, a, b):
    return ease(seg(t, a, b))


def lerp(a, b, x):
    return a + (b - a) * x


def fade(t, a, b, c=None, d=None):
    """Alpha that rises over [a, b] and (optionally) falls over [c, d]."""
    al = eseg(t, a, b)
    if c is not None:
        al *= 1 - eseg(t, c, d)
    return al


# ---------------------------------------------------------------- canvas
class Canvas:
    """Full-figure axes in design-pixel coordinates (y down)."""

    def __init__(self, fig):
        self.fig = fig
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, W_PX)
        ax.set_ylim(H_PX, 0)
        ax.axis("off")
        self.ax = ax

    # text ---------------------------------------------------------------
    def text(self, x, y, s, size=11, color=None, weight="normal", ha="left",
             va="center", alpha=1.0, **kw):
        if alpha <= 0.001:
            return None
        return self.ax.text(x, y, s, fontsize=size, color=color or C["ink"],
                            fontweight=weight, ha=ha, va=va, alpha=alpha, **kw)

    def title(self, s, color=None, x=24, y=26, size=13.5):
        return self.text(x, y, s, size=size, color=color or C["navy"], weight="bold")

    def lines(self, x, y, items, size=11, gap=22, color=None, alpha=1.0, **kw):
        """Several lines of text; items may be str or (str, dict)."""
        for i, it in enumerate(items):
            if isinstance(it, tuple):
                s, extra = it
            else:
                s, extra = it, {}
            if s:
                opts = dict(size=size, color=color, alpha=alpha)
                opts.update(kw)
                opts.update(extra)
                self.text(x, y + i * gap, s, **opts)

    # shapes ---------------------------------------------------------------
    def rect(self, x, y, w, h, fc="none", ec=None, lw=1.2, alpha=1.0, z=1, r=0, **kw):
        if r:
            p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                               fc=fc, ec=ec or "none", lw=lw, alpha=alpha, zorder=z, **kw)
        else:
            p = Rectangle((x, y), w, h, fc=fc, ec=ec or "none", lw=lw, alpha=alpha, zorder=z, **kw)
        self.ax.add_patch(p)
        return p

    def circle(self, x, y, r, fc=None, ec="none", lw=1, alpha=1.0, z=3):
        p = Circle((x, y), r, fc=fc or C["red"], ec=ec, lw=lw, alpha=alpha, zorder=z)
        self.ax.add_patch(p)
        return p

    def line(self, xs, ys, color=None, lw=1.6, ls="-", alpha=1.0, z=2, **kw):
        return self.ax.plot(xs, ys, color=color or C["navy"], lw=lw, ls=ls,
                            alpha=alpha, zorder=z, solid_capstyle="round", **kw)

    def arrow(self, x0, y0, x1, y1, color=None, lw=1.6, head=8, alpha=1.0, z=4,
              style="-|>", ls="-", both=False):
        if alpha <= 0.001:
            return None
        st = "<|-|>" if both else style
        a = FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=f"{st},head_length={head*0.55},head_width={head*0.32}",
                            color=color or C["navy"], lw=lw, alpha=alpha, zorder=z,
                            mutation_scale=1.6, shrinkA=0, shrinkB=0, linestyle=ls)
        self.ax.add_patch(a)
        return a

    def poly(self, pts, fc, ec="none", lw=1, alpha=1.0, z=1):
        p = Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z)
        self.ax.add_patch(p)
        return p

    def badge(self, x, y, s, fc, size=10.5, color="white", pad=5, ha="left", alpha=1.0):
        return self.text(x, y, s, size=size, color=color, weight="bold", ha=ha, alpha=alpha,
                         bbox=dict(boxstyle=f"round,pad=0.35,rounding_size=0.3", fc=fc, ec="none", alpha=alpha))

    def inset(self, x, y, w, h):
        """A normal matplotlib axes placed at design-pixel box (x, y, w, h)."""
        ax = self.fig.add_axes([x / W_PX, 1 - (y + h) / H_PX, w / W_PX, h / H_PX])
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(length=3, color=C["gray"])
        return ax


def wave(x0, x1, y, amp, wavelength, phase=0.0, n=400, envelope=None):
    xs = np.linspace(x0, x1, n)
    ys = amp * np.sin(2 * np.pi * (xs - x0) / wavelength - phase)
    if envelope == "packet":
        mid, half = (x0 + x1) / 2, (x1 - x0) / 2
        ys *= np.exp(-((xs - mid) / (half * 0.55)) ** 2)
    return xs, y + ys


def gauss(x, mu, sig, h=1.0):
    return h * np.exp(-0.5 * ((x - mu) / sig) ** 2)


def wl_color(nm):
    """Approximate visible colour for a wavelength in nm."""
    stops = [(380, (0.38, 0.0, 0.62)), (440, (0.15, 0.1, 1.0)), (490, (0.0, 0.75, 1.0)),
             (530, (0.25, 0.9, 0.1)), (580, (1.0, 0.92, 0.0)), (630, (1.0, 0.35, 0.0)),
             (700, (0.85, 0.0, 0.0)), (780, (0.5, 0.0, 0.0))]
    nm = clamp(nm, 380, 780)
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if a <= nm <= b:
            f = (nm - a) / (b - a)
            return tuple(ca[i] + (cb[i] - ca[i]) * f for i in range(3))
    return stops[-1][1]


# ---------------------------------------------------------------- render
def render(draw, duration, out_base, fps=25, poster_t=None, lang="zh"):
    """Render draw(cv, t) for t in [0, duration) to out_base.mp4 and out_base.jpg."""
    global LANG
    LANG = lang
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    n = int(round(duration * fps))
    os.makedirs(os.path.dirname(out_base), exist_ok=True)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{OUT_W}x{OUT_H}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-tune", "animation",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", out_base + ".mp4"],
        stdin=subprocess.PIPE)
    pt = duration * 0.75 if poster_t is None else poster_t
    poster_i = min(n - 1, int(pt * fps))
    for i in range(n):
        frame(fig, draw, i / fps)
        buf = np.asarray(fig.canvas.buffer_rgba())
        assert buf.shape[1] == OUT_W and buf.shape[0] == OUT_H, buf.shape
        proc.stdin.write(buf.tobytes())
        if i == poster_i:
            from PIL import Image
            Image.fromarray(buf[..., :3]).save(out_base + ".jpg", quality=86)
    proc.stdin.close()
    proc.wait()
    plt.close(fig)


def frame(fig, draw, t):
    fig.clf()
    cv = Canvas(fig)
    draw(cv, t)
    fig.canvas.draw()


def preview(draw, duration, path, times=(0.15, 0.4, 0.65, 0.92), lang="zh"):
    """Save a 2x2 sheet of frames (at 1x) for checking."""
    global LANG
    LANG = lang
    from PIL import Image
    fig = plt.figure(figsize=FIGSIZE, dpi=100, facecolor="white")
    tiles = []
    for f in times:
        frame(fig, draw, f * duration)
        tiles.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[..., :3].copy()))
    plt.close(fig)
    w, h = tiles[0].size
    sheet = Image.new("RGB", (w * 2 + 6, h * 2 + 6), (120, 120, 120))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % 2) * (w + 6), (k // 2) * (h + 6)))
    sheet.save(path)
