# FA Labo

FA Labo は、フリーランスFAエンジニア「よしのぶ」のポートフォリオ兼サービス紹介サイトです。PLCプログラミング、制御盤改造、HMI/SCADA構築、試運転支援、技術発信、公開ツールをまとめています。

## 公開URL

- 公式サイト: https://fa-labo.com/
- GitHub Pages: https://fa-yoshinobu.github.io/FA_Labo/

## 主なページ

| File | 内容 |
| --- | --- |
| `index.html` | トップページ。強み、提供サービス、実績、無料ツールへの導線。 |
| `services.html` | PLCプログラミング、HMI/SCADA、制御盤改造、立ち上げ支援などのサービス詳細。 |
| `works.html` | 製鉄、医薬品、自動車、水処理などの実績紹介。 |
| `tools.html` | MIT Licenseで公開している無料ツール・PLC通信ライブラリ一覧。 |
| `paid-tools.html` | FA Labo PLC Consoleの紹介、App Store、公式サイトへの導線。 |
| `about.html` | プロフィール、技術スキル、所有PLC/開発機材。 |
| `contact.html` | お問い合わせフォームとSNSリンク。 |

## 掲載中のツール

### 無料ツール・ライブラリ

- PLC通信ライブラリまとめサイト
- MELSEC SLMP: Python / .NET / C++ minimal / Rust / Node-RED
- KEYENCE Host Link: Python / .NET / Rust / Node-RED
- MELSEC MCプロトコル シリアル通信 C++
- JTEKT TOYOPUC ComputerLink: Python / .NET
- Factory I/O SLMP / Host Link Gateway
- PLC Scope
- SysmacVariableBackupViewer
- SysmacDataTraceViewer
- PDF_Title_to_Filename
- Network_Preset_Switcher

### 公開アプリ

- FA Labo PLC Console: Android／iOSで公開中のPLC接続確認、監視、書込、記録支援アプリ。[Google Play](https://play.google.com/store/apps/details?id=com.fa_labo.plc_io_checker)／[App Store](https://apps.apple.com/jp/app/fa-labo-plc-console/id6783619471)

## 技術構成

- 静的HTML/CSSサイト
- Bootstrap 5
- Font Awesome
- Google Fonts: Noto Sans JP
- GitHub Pages
- Custom domain: `fa-labo.com`

## ローカル確認

ビルド手順はありません。HTMLを直接ブラウザで開いて確認できます。

```powershell
Start-Process .\index.html
Start-Process .\tools.html
Start-Process .\paid-tools.html
```

リンクやメタ情報を更新した場合は、以下もあわせて確認します。

- `sitemap.xml`
- `robots.txt`
- `CNAME`
- 各ページの `<title>` / `meta description` / `canonical`
- ナビゲーションとフッターのページリンク

## 更新メモ

- 共通ナビは各HTMLに直接記述しています。ページを追加した場合は全ページのナビとフッターを更新します。
- スタイルは `css/style.css` に集約しています。
- GitHubリンクボタンなどの見た目ルールは `docs/ui-guidelines.md` を確認します。
- GitHub Pages公開用に `.nojekyll` を配置しています。
- Google Search Console用の確認ファイルとして `google602250a356eea49d.html` を保持しています。

## ライセンス

このリポジトリのサイト本文・HTML/CSSはFA Laboサイト運用のためのものです。

掲載している各ツール・ライブラリのライセンスは、それぞれのリンク先リポジトリを確認してください。
