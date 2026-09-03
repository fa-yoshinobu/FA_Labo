# vendor/

Third-party front-end assets are vendored here so the site loads them from its
own origin instead of a CDN. This removes render-blocking cross-origin requests
and stops visitor IPs from being sent to `fonts.googleapis.com` / `cdnjs` /
`jsdelivr` on every page view.

| Path | Upstream | Version |
| --- | --- | --- |
| `bootstrap/bootstrap.min.css`, `bootstrap/bootstrap.bundle.min.js` | https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/ | 5.3.3 |
| `fontawesome/css/all.min.css` | https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css | 6.5.0 (Free) |
| `fontawesome/webfonts/fa-solid-900.woff2`, `fa-brands-400.woff2` | Font Awesome 6.5.0 webfonts | **subset** to the 54 icons used on the site |
| `fonts/notosansjp/NotoSansJP-{400,500,700,800}.woff2` | Google Fonts "Noto Sans JP" (SIL OFL 1.1) | **subset** to JIS X 0208 Level 1 kanji + kana + Latin + punctuation + every glyph currently on the site |

Bootstrap is MIT, Font Awesome Free icons are CC BY 4.0 / the toolkit MIT,
Noto Sans JP is SIL OFL 1.1 — all fine to redistribute in-repo.

## Regenerating

`build_fonts.py` re-downloads Bootstrap + Font Awesome CSS and re-subsets the
webfonts. It needs `pip install fonttools brotli` and a copy of
`NotoSansJP[wght].ttf` (the variable font from
https://fonts.google.com/noto/specimen/Noto+Sans+JP — set `VF` at the top of the
script to its path).

```
pip install fonttools brotli
python vendor/build_fonts.py
```

If you add a new Font Awesome icon or use a kanji outside JIS Level 1, re-run it
so the subset covers the new glyph (until then the browser falls back to a
system font for the missing glyph only).
