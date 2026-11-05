"""Usage: run.py preview|render MODULE [name ...] [--lang zh,en] [--out DIR] [--times a,b,c,d]"""
import sys, os, importlib, argparse, tempfile
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

ap = argparse.ArgumentParser()
ap.add_argument("mode"); ap.add_argument("modules")
ap.add_argument("names", nargs="*")
ap.add_argument("--lang", default="zh,en")
ap.add_argument("--out", default=os.path.join(tempfile.gettempdir(), "anim-prev"))
ap.add_argument("--times", default="0.15,0.4,0.65,0.92")
ap.add_argument("-j", type=int, default=4)
a = ap.parse_args()

jobs = []
for modname in a.modules.split(","):
    mod = importlib.import_module(modname)
    for name, fn, dur in mod.ANIMS:
        if a.names and not any(n in name for n in a.names):
            continue
        for lang in a.lang.split(","):
            jobs.append((modname, mod.CH, name, dur, lang))

def work(job):
    try:
        return _work(job)
    except Exception as e:
        return f"ERROR {job[2]} [{job[4]}]: {type(e).__name__}: {e}"

def _work(job):
    modname, ch, name, dur, lang = job
    mod = importlib.import_module(modname)
    fn = dict((n, f) for n, f, d in mod.ANIMS)[name]
    if a.mode == "preview":
        os.makedirs(a.out, exist_ok=True)
        p = os.path.join(a.out, f"{ch}__{name}__{lang}.png")
        common.preview(fn, dur, p, times=[float(x) for x in a.times.split(",")], lang=lang)
        return p
    out = os.path.join(a.out, lang, ch, name)
    common.render(fn, dur, out, lang=lang)
    return out

with Pool(a.j) as pool:
    for r in pool.imap_unordered(work, jobs):
        print(r, flush=True)
