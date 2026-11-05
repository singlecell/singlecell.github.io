# Teaching animations (source)

Python sources for the analytical-chemistry animations on `/teaching/` and
`/zh/teaching/`. Each chapter file (`ch1_*.py` … `ch9_*.py`) draws every frame
with matplotlib; `run.py` renders Chinese and English versions at 1892 × 1010
and encodes them to MP4 with a poster JPG. Jekyll ignores this folder.

## Requirements

- Python 3 with `matplotlib`, `numpy`, `Pillow`
- `ffmpeg` with libx264
- Noto Sans SC (TTF), e.g. from the npm package `@expo-google-fonts/noto-sans-sc`;
  point `ANIM_FONT_DIR` at the folder that holds `400Regular/`, `500Medium/`, `700Bold/`

## Usage

```sh
export ANIM_FONT_DIR=/path/to/noto-sans-sc/package
cd _animations

# quick check: a 2x2 sheet of frames per animation, saved in <tmp>/anim-prev/
python3 run.py preview ch8_hplc 03- --lang en

# render to assets/teaching/<lang>/<chapter>/<name>.mp4 + .jpg
python3 run.py render ch8_hplc 03- --out ../assets/teaching
```

Arguments: a comma-separated list of chapter modules, then optional name
filters (substring match, e.g. `03-`). `--lang zh,en` is the default.

Every on-screen string is written as `L("中文", "English")`. A missing glyph
in the font raises an error, so problems show up when you preview.
