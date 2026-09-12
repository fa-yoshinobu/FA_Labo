"""Rebuild the vendored front-end assets.

  pip install fonttools brotli
  python vendor/build_fonts.py            # uses %NOTO_VF% or the default path below

Downloads Bootstrap + Font Awesome from their CDNs, then subsets the Font Awesome
webfonts to the icons used on the site and Noto Sans JP to
JIS X 0208 Level 1 + every glyph currently in the HTML.
"""
import os, re, sys, glob, shutil, subprocess, tempfile, urllib.request

REPO   = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
VENDOR = os.path.join(REPO, "vendor")
# Path to the Noto Sans JP *variable* font (wght axis). Download from
# https://fonts.google.com/noto/specimen/Noto+Sans+JP  ->  static/ or the VF file.
VF = os.environ.get("NOTO_VF", r"C:\Windows\Fonts\NotoSansJP-VF.ttf")

BS_VER, FA_VER = "5.3.3", "6.5.0"
DOWNLOADS = {
    os.path.join(VENDOR, "bootstrap", "bootstrap.min.css"):
        f"https://cdn.jsdelivr.net/npm/bootstrap@{BS_VER}/dist/css/bootstrap.min.css",
    os.path.join(VENDOR, "bootstrap", "bootstrap.bundle.min.js"):
        f"https://cdn.jsdelivr.net/npm/bootstrap@{BS_VER}/dist/js/bootstrap.bundle.min.js",
    os.path.join(VENDOR, "fontawesome", "css", "all.min.css"):
        f"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/{FA_VER}/css/all.min.css",
    os.path.join(VENDOR, "fontawesome", "webfonts", "fa-solid-900.woff2"):
        f"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/{FA_VER}/webfonts/fa-solid-900.woff2",
    os.path.join(VENDOR, "fontawesome", "webfonts", "fa-brands-400.woff2"):
        f"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/{FA_VER}/webfonts/fa-brands-400.woff2",
}

TMP = tempfile.mkdtemp(prefix="fa-labo-vendor-")
NSJP_OUT = os.path.join(VENDOR, "fonts", "notosansjp")
FA_CSS = os.path.join(VENDOR, "fontawesome", "css", "all.min.css")
FA_WF = os.path.join(VENDOR, "fontawesome", "webfonts")


def run(*a):
    print(">", " ".join(map(str, a)))
    subprocess.check_call([sys.executable, "-m", *a])


def fetch():
    for dst, url in DOWNLOADS.items():
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        print("GET", url)
        with urllib.request.urlopen(url) as r:
            open(dst, "wb").write(r.read())


def subset_icons():
    css = open(FA_CSS, encoding="utf-8").read()
    name2cp = {}
    for m in re.finditer(
            r'((?:\.fa-[a-z0-9-]+:{1,2}before\s*,\s*)*\.fa-[a-z0-9-]+:{1,2}before)\s*'
            r'\{\s*content:\s*"\\([0-9a-fA-F]+)"\s*\}', css):
        for nm in re.findall(r'\.fa-([a-z0-9-]+):{1,2}before', m.group(1)):
            name2cp.setdefault(nm, m.group(2))

    brands, solid, missing = set(), set(), []
    for f in glob.glob(os.path.join(REPO, "*.html")):
        s = open(f, encoding="utf-8").read()
        for kind, nm in re.findall(r'fa([bsr]) fa-([a-z0-9-]+)', s):
            cp = name2cp.get(nm)
            if not cp:
                missing.append(nm)
            elif kind == "b":
                brands.add(cp)
            else:
                solid.add(cp)
    if missing:
        sys.exit("Font Awesome classes with no codepoint: " + ", ".join(sorted(set(missing))))

    for fname, cps in [("fa-solid-900.woff2", solid), ("fa-brands-400.woff2", brands)]:
        dst = os.path.join(FA_WF, fname)
        src = os.path.join(TMP, fname)
        shutil.copy(dst, src)
        run("fontTools.subset", src, "--unicodes=" + ",".join(sorted(cps)),
            "--layout-features=", "--no-hinting", "--desubroutinize",
            "--flavor=woff2", "--output-file=" + dst)
        print(" ", fname, os.path.getsize(dst), "bytes")


def subset_noto():
    if not os.path.isfile(VF):
        sys.exit(f"Noto Sans JP variable font not found: {VF}\nSet NOTO_VF to its path.")
    l1 = set()
    for lead in range(0x88, 0x99):
        for trail in range(0x40, 0xFD):
            if trail == 0x7F:
                continue
            try:
                ch = bytes([lead, trail]).decode("cp932")
            except UnicodeDecodeError:
                continue
            if "\u4e00" <= ch <= "\u9fff":
                l1.add(ch)

    site = set()
    for f in glob.glob(os.path.join(REPO, "*.html")):
        s = open(f, encoding="utf-8").read()
        s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
        site |= set(re.sub(r"<[^>]+>", " ", s))

    charfile = os.path.join(TMP, "charset.txt")
    open(charfile, "w", encoding="utf-8").write("".join(sorted(l1 | {c for c in site if c > " "})))

    ranges = ("U+0020-007F,U+00A0-00FF,U+2000-206F,U+2070-209F,U+20A0-20BF,U+2100-214F,"
              "U+2190-21FF,U+2460-24FF,U+2500-257F,U+25A0-25FF,U+2600-26FF,U+3000-303F,"
              "U+3040-309F,U+30A0-30FF,U+31F0-31FF,U+3200-32FF,U+3300-33FF,U+FF00-FFEF,U+FE30-FE4F")

    os.makedirs(NSJP_OUT, exist_ok=True)
    for w in (400, 500, 700, 800):
        inst = os.path.join(TMP, f"nsjp-{w}.ttf")
        run("fontTools.varLib.instancer", VF, f"wght={w}", "-o", inst)
        out = os.path.join(NSJP_OUT, f"NotoSansJP-{w}.woff2")
        run("fontTools.subset", inst, "--text-file=" + charfile, "--unicodes=" + ranges,
            "--layout-features=kern,palt,liga,calt,ccmp,locl,mark,mkmk",
            "--name-IDs=1,2,3,4,6", "--no-hinting", "--desubroutinize",
            "--flavor=woff2", "--output-file=" + out)
        print(f"  NotoSansJP-{w}.woff2 {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    fetch()
    subset_icons()
    subset_noto()
    shutil.rmtree(TMP, ignore_errors=True)
    print("done")
