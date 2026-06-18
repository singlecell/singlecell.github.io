# -*- coding: utf-8 -*-
"""Extract the most graphical-abstract-like figure from each paper PDF.
Outputs thumbnails to assets/img/publication_preview/<bibkey>.jpg and a
labeled contact sheet to bin/_contact_sheet.jpg for visual review."""
import os, math
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

PDF_DIR = r"C:\Users\Li\OneDrive\Linnan Li"
OUT_DIR = r"C:\Users\Li\OneDrive\AI4S\L Homepage\assets\img\publication_preview"
SHEET   = r"C:\Users\Li\OneDrive\AI4S\L Homepage\bin\_contact_sheet.jpg"
os.makedirs(OUT_DIR, exist_ok=True)

MAP = {
    "pei2026phytomed":"2026-PWH-Phytomedicine.pdf","zhang2026talanta":"2026-ZYM-Talanta.pdf",
    "fan2026fri":"2026-FWX-FRI.pdf","xie2026aca":"2026-XYQ-ACA.pdf","zhao2026jca":"2026-ZWM-JCA.pdf",
    "wang2026chemcomm":"2026-WXY-CC.pdf","xie2025trac":"2026-XYQ-TRAC.pdf",
    "liu2025jpbashengmai":"2025-LLC-JPBA.pdf","zhao2025microchim":"2025-ZWM-MCA.pdf",
    "si2025jpc":"2025-SZH-JPC.pdf","wang2025jpbadanning":"2025-WY-JPBA.pdf",
    "li2023frontchem":"2023-LLN-FIC.pdf","chen2025jpa":"2026-CYL-JPA.pdf",
    "yang2025analyst":"2025-YXY-Analyst.pdf","xie2025jat":"2025-XYQ-JAT.pdf",
    "ding2025cjnm":"2025-DH-CJNM.pdf","fan2025talanta":"2025-FWX-Talanta.pdf",
    "hu2025jpba":"2025-HZZ-JPBA.pdf","fu2025jpba":"2025-FKN-JPBA.pdf",
    "wang2024rcm":"2024-WXY-RCM.pdf","wang2024analyst":"2024-WXY-Analyst.pdf",
    "xie2024chemcomm":"2024-XYQ-CC.pdf","liu2024jca":"2024-LYM-JCA.pdf",
    "liu2024phytomed":"2024-LYM-Phytomedicine.pdf","chen2024foodchem":"2024-CYL-Food Chem.pdf",
    "lu2024phytochemrev":"2024-LWX-PHR.pdf","zhang2024jpba":"2025-ZSY-JPBA.pdf",
    "liu2024phytomed2":"2024-LLC-Phytomedicine.pdf","fan2024jar":"2024-FWX-JAR.pdf",
    "fan2024jep":"2024-FXW-JEP.pdf","liu2023analchem":"2023-LLC-AC.pdf",
    "wei2023jpa":"2023-WJJ-JPA.pdf","fan2023acssce":"2023-FLH-ACS SCE.pdf",
    "liu2023rcm":"2023-LYM-RCM.pdf","zhang2023jpba":"2023-ZJY-JPBA.pdf",
    "li2023phytomed":"2023-LW-Phytomedicine.pdf","chen2023msr":"2023-CYL-MSR.pdf",
    "yang2022analyst":"2022-YY-Analyst.pdf","tu2022molecules":"2022-TYJ-Molecules.pdf",
    "mei2022jep":"2023-MYQ-JEP.pdf","wang2022jca":"2022-WY-JCA.pdf",
    "fan2022tifst":"2022-FLH-TIFS.pdf","fan2022phytomed":"2022-FWX-Phytomedicine.pdf",
    "zhang2022rcm":"2022-ZYX-RCM.pdf","yan2022jpba":"2022-YX-JPBA.pdf",
    "yang2022jpc":"2022-YF-JPC.pdf","chen2021jca":"2021-CYL-JCA.pdf",
    "chen2021foodchem":"2021-CYL-Food Chem.pdf","li2021jss":"2021-LLN-JSS.pdf",
    "tu2021jpba":"2021-TYJ-JPBA.pdf","li2020ccr":"2020-LLN-CCR.pdf",
    "li2020abc":"2020-LLN-ABC.pdf","zheng2020abc":"2020-ZRR-ABC.pdf",
    "xie2020pca":"2020-XYQ-PCA.pdf","tian2020cjnm":"2020-TM-CJNM.pdf",
    "li2019abc":"2019-LLN-ABC.pdf","li2018sab":"2018-LLN-Sensor B.pdf",
    "shen2018nanoscale":"2018-SSS-Nanoscale.pdf","shen2018ijms":"2018-SSS-IJMS.pdf",
    "shen2018aca":"2018-SSS-ACA.pdf","li2017chemcomm":"2017-LLN-CC.pdf",
    "shen2017jcb":"2017-SSS-JCB.pdf","yang2017abc":"2017-YL-ABC.pdf",
    "li2016acsami":"2016-LLN-ACS AMI.pdf","li2016electrophoresis":"2016-LLN-Electrophresis.pdf",
    "shen2016srep":"2016-SSS-SCI REP.pdf","zhang2015electrophoresis":"2015-ZYD-Electrophoresis.pdf",
    "li2015msl":"2015-LXJ-MSL-Review.pdf",
}

MAX_W = 680


def mean_lum(page, rect):
    """Rough mean luminance (0-255) of a page region via a tiny render."""
    try:
        pix = page.get_pixmap(clip=rect, dpi=18, colorspace=fitz.csRGB)
        s = pix.samples
        if not s:
            return 255
        # average over channels/bytes
        return sum(s) / len(s)
    except Exception:
        return 255


def best_image(doc):
    """Scan all pages, score raster images for GA-likeness; return (score, page, rect)."""
    best = None
    for pno in range(doc.page_count):
        p = doc[pno]
        pw, ph = p.rect.width, p.rect.height
        for img in p.get_images(full=True):
            xref, w_pix, h_pix = img[0], img[2], img[3]
            if w_pix < 300 or h_pix < 200:
                continue
            try:
                rects = p.get_image_rects(xref)
            except Exception:
                continue
            if not rects:
                continue
            r = max(rects, key=lambda rr: rr.width * rr.height)
            dw, dh = r.width, r.height
            if dw < 90 or dh < 70:
                continue
            ar = dw / dh
            if ar < 0.45 or ar > 4.0:          # exclude very tall / very wide strips
                continue
            disp_area = dw * dh
            if disp_area > 0.93 * pw * ph:      # full-page scan
                continue
            ar_pen = 1.0 if 0.9 <= ar <= 2.6 else 0.6
            page_pen = 1.0 / (1.0 + pno * 0.12)
            score = disp_area * ar_pen * page_pen
            lum = mean_lum(p, r)
            if lum < 55:                        # mostly-black (dark MSI) -> strongly avoid
                score *= 0.12
            elif lum < 90:
                score *= 0.6
            if best is None or score > best[0]:
                best = (score, pno, r, (w_pix, h_pix))
    return best


def render_clip(doc, pno, rect):
    """Render the page region as displayed (robust to image codec quirks)."""
    target_dpi = min(300, max(120, MAX_W / rect.width * 72))
    pix = doc[pno].get_pixmap(clip=rect, dpi=round(target_dpi), colorspace=fitz.csRGB)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def main():
    results = {}
    for key, fn in MAP.items():
        path = os.path.join(PDF_DIR, fn)
        if not fn or not os.path.exists(path):
            results[key] = ("MISSING", None); continue
        try:
            doc = fitz.open(path)
        except Exception as e:
            results[key] = ("OPENERR", None); continue
        b = best_image(doc)
        if not b:
            results[key] = ("NOIMG", None); doc.close(); continue
        try:
            score, pno, rect, pix = b
            img = render_clip(doc, pno, rect)
            if img.width > MAX_W:
                img = img.resize((MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS)
            img.save(os.path.join(OUT_DIR, key + ".jpg"), "JPEG", quality=88)
            results[key] = ("p%d %dx%d" % (pno, img.width, img.height), img)
        except Exception as e:
            results[key] = ("SAVEERR:" + str(e)[:30], None)
        doc.close()

    # contact sheet
    keys = list(MAP.keys())
    cols = 6
    cellw, cellh = 230, 200
    rows = math.ceil(len(keys) / cols)
    sheet = Image.new("RGB", (cols * cellw, rows * cellh), "white")
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
    for i, key in enumerate(keys):
        cx = (i % cols) * cellw; cy = (i // cols) * cellh
        status, img = results[key]
        if img is not None:
            th = img.copy(); th.thumbnail((cellw - 10, cellh - 38))
            sheet.paste(th, (cx + 5, cy + 20))
        dr.text((cx + 4, cy + 4), key, fill="black", font=font)
        dr.text((cx + 4, cy + cellh - 14), status, fill="red", font=font)
        dr.rectangle([cx, cy, cx + cellw - 1, cy + cellh - 1], outline="#cccccc")
    sheet.save(SHEET, "JPEG", quality=85)

    ok = sum(1 for s, _ in results.values() if s[0] in "pM" and s != "MISSING")
    for k, (s, _) in results.items():
        if s in ("NOIMG", "MISSING", "OPENERR") or s.startswith("SAVEERR"):
            print("  !!", k, s)
    print("sheet ->", SHEET)


if __name__ == "__main__":
    main()
