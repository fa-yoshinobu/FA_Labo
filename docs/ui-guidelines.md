# UI更新ガイドライン

FA LaboサイトのHTMLを更新するときの見た目のルールです。
同じ種類のリンクやカードは、既存ページと同じクラス・アイコン指定にそろえてください。

## GitHubリンクボタン

ツールカード内のGitHubリンクは、無料ツール・有料ツールのどちらでもオレンジの主要ボタンにします。

正しい指定:

```html
<a href="https://github.com/fa-yoshinobu/..." class="btn btn-sm btn-accent" target="_blank">
  <i class="fab fa-github me-1"></i>GitHub
</a>
```

使わない指定:

```html
<a href="https://github.com/fa-yoshinobu/..." class="btn btn-sm btn-outline-secondary" target="_blank">
  <i class="fab fa-github me-1"></i>GitHub
</a>
```

`btn-outline-secondary` はグレーの枠線ボタンになり、`tools.html` のGitHubボタンと見た目がそろいません。

## アイコン

このサイトはFont Awesomeを読み込んでいます。GitHubアイコンはインラインSVGに置き換えず、既存ページと同じFont Awesome指定を使います。

```html
<i class="fab fa-github me-1"></i>
```

`tools.html` で同じアイコンが表示されている場合、Font AwesomeやCDNではなく、対象ページ側のHTMLクラス差分を先に確認してください。

## 更新時の確認

ツールや有料ツールのリンクを追加・修正したら、次を確認します。

```powershell
rg -n "btn-outline-secondary|fa-github|btn-accent" tools.html paid-tools.html
git diff --check
```

- ツールカードのGitHubリンクが `btn btn-sm btn-accent` になっていること。
- GitHubアイコンが `<i class="fab fa-github me-1"></i>` になっていること。
- `tools.html` と `paid-tools.html` で同種ボタンの見た目がそろっていること。
