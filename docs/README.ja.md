# Gemini Build Parity Scaffold

Gemini CLI と Hermes のデザインワーカーを、AI Studio Build に近いフロントエンド成果物へ寄せるための、アプリ優先スキャフォールドです。

[English](../README.md) · [한국어](README.ko.md) · 日本語 · [中文](README.zh-CN.md)

モデルに、より良い作業媒体を与えるためのものです。実際の Vite アプリ、ローカル設計指示、任意の source prompt スロット、デザインスキルノート、アプリソースから standalone HTML へ出力する経路を提供します。

## 何が変わるか

Gemini CLI に直接依頼すると、結果は静的な HTML ファイル 1 つに寄りやすくなります。このリポジトリでは、まず実際のフロントエンドプロジェクト内で作業させ、アプリが成立したあとに HTML として出力します。

この表の出力は、すべて同じ公開安全 brief に対する one-shot 結果です。

| 経路 | One-shot の公開安全出力 |
| --- | --- |
| バニラ単純指示 v1 | <img src="../evidence/baseline-1818/desktop-fullpage.png" alt="バニラ単純指示 v1 one-shot output" width="520"> |
| バニラ単純指示 v2 | <img src="../evidence/baseline-1848/desktop-fullpage.png" alt="バニラ単純指示 v2 one-shot output" width="520"> |
| Build-parity scaffold 0003 | <img src="../evidence/final-0003/desktop-fullpage.png" alt="Build-parity scaffold 0003 one-shot output" width="520"> |

## 0003 のインタラクション

最終成果物は静的ページではありません。ボタン操作により view context 全体が切り替わり、異なるアプリ状態が表示されます。

<img src="../evidence/final-0003/interaction-demo.gif" alt="0003 interaction demo" width="900">

すべての画像は架空データを使用しています。ワークフローの実効性を示すためのものです。

## Gemini CLI クイックスタート

```powershell
git clone https://github.com/heelee912/gemini-build-parity-scaffold.git
cd gemini-build-parity-scaffold
python scripts\run_gemini_design_once.py out\fictional-profile --name "Fictional Profile" --brief-file examples\fictional-recruiter-profile\brief.md --force
```

runner が行うこと:

1. Vite + React + TypeScript + Tailwind の作業環境を作成します。
2. `profile/GEMINI.md`, `profile/SKILL.md`, `design_skills/`, `prompt-seeds/`, `source-prompts/` を作業環境へコピーします。
3. ユーザー brief を `task.md` として書き込みます。
4. 生成された作業環境内で Gemini CLI を実行し、Gemini が scaffold ファイルを直接読めるようにします。
5. `npm install`, `npm run lint`, `npm run build` を実行します。
6. Vite `dist` を `standalone.html` にパッケージ化します。

出力:

```text
out\fictional-profile\standalone.html
```

## 手動エージェント経路

すでに Gemini を制御するエージェントがある場合は、scaffold だけを作成します。

```powershell
python scripts\create_build_like_web_app.py out\my-artifact --name "My Artifact" --brief-file brief.md --force
```

その後、デザインワーカーはリポジトリルートではなく `out\my-artifact` 内で実行します。ワーカーが読むべきファイルは次の通りです。

```text
GEMINI.md
task.md
BUILD_ENVIRONMENT.md
AIS_REFERENCE_COMMONS.md
design_skills/
prompt-seeds/
source-prompts/
src/
```

ワーカーがアプリを編集した後:

```powershell
cd out\my-artifact
npm install
npm run lint
npm run build
cd ..\..
python scripts\package_vite_dist_single_html.py out\my-artifact\dist out\my-artifact\standalone.html
```

## Hermes セットアップ

design profile を Hermes home にインストールします。

```powershell
python scripts\install_hermes_profile.py --hermes-home C:\path\to\.hermes-home --profile design --force
```

インストール先:

```text
<hermes-home>\profiles\design\skills\build-parity-design-director
```

Hermes のメインエージェントは、次の形で使用できます。

```text
build-parity-design-director profile を使用する。
run_gemini_design_once.py で artifact 作業環境を作成する。
生成された artifact 作業環境内で Gemini デザインワーカーを実行する。
実行可能な source path と standalone.html path を返す。
```

または:

```text
create_build_like_web_app.py を先に使用する。
生成された作業環境内で Gemini に委譲する。
Gemini がアプリを編集した後、npm install、npm run lint、npm run build、package_vite_dist_single_html.py を実行する。
```

Hermes core を fork する必要はありません。このリポジトリの接続点は profile と external runner です。

## Gemini が見るもの

生成された artifact は自己説明的な構造を持ちます。

```text
artifact/
  GEMINI.md
  SKILL.md
  task.md
  BUILD_ENVIRONMENT.md
  AIS_REFERENCE_COMMONS.md
  design_skills/
  prompt-seeds/
  source-prompts/
  package.json
  vite.config.ts
  tsconfig.json
  index.html
  src/
    App.tsx
    data.ts
    types.ts
    index.css
    components/
      README.md
```

重要なのは実行文脈です。Gemini は単一プロンプトだけを受け取るのではなく、実装媒体、利用可能な依存関係、モバイル要件、パッケージング経路、任意の source context を説明するアプリ作業環境内で実行されます。

## 任意の Source Prompts

AI Studio の raw prompt ファイルは、このリポジトリでは再配布しません。法的に利用可能な prompt ファイルがある場合は、次の場所に置いてください。

```text
profile\source-prompts\
```

scaffold はこのフォルダを生成される各 artifact へコピーするため、Gemini がローカルで読めます。

## リポジトリ構成

| Path | Purpose |
| --- | --- |
| `profile/GEMINI.md` | Gemini にアプリ優先で作らせ、視覚方向を自律的に決めさせる実行カーネルです。 |
| `profile/SKILL.md` | Hermes や他のエージェントシステム向けの skill wrapper です。 |
| `profile/design_skills/` | 各 artifact にコピーされる補助デザインノートです。 |
| `profile/prompt-seeds/` | タスク内容を除去した汎用的な高性能 prompt driver です。 |
| `profile/source-prompts/README.md` | 再配布しない任意 source prompt corpus の置き場です。 |
| `scripts/run_gemini_design_once.py` | scaffold 作成、Gemini CLI 実行、install、lint、build、standalone HTML パッケージ化を一度に行います。 |
| `scripts/create_build_like_web_app.py` | Vite/React/Tailwind scaffold だけを作成します。他のエージェントが Gemini を制御する場合に使います。 |
| `scripts/install_hermes_profile.py` | profile を Hermes home にインストールします。 |
| `scripts/package_vite_dist_single_html.py` | Vite `dist` asset をブラウザで開ける単一 HTML に inline します。 |
| `examples/fictional-recruiter-profile/` | 公開安全な example brief です。 |
| `evidence/` | 架空データベースのスクリーンショットとインタラクション GIF です。 |

## 関連研究

このリポジトリは、単一プロンプトに頼るのではなく、workspace 構造、ツール、指示、状態、実行 feedback でモデルを囲む scaffolding の考え方に近いものです。

- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](https://arxiv.org/abs/2604.03515)
- [app.build: A Production Framework for Scaling Agentic Prompt-to-App Generation with Environment Scaffolding](https://arxiv.org/abs/2509.03310)
- [BISCUIT: Scaffolding LLM-Generated Code with Ephemeral UIs in Computational Notebooks](https://machinelearning.apple.com/research/biscuit-scaffolding-llm)
- [TableTalk: Scaffolding Spreadsheet Development with a Language Agent](https://www.microsoft.com/en-us/research/publication/tabletalk-scaffolding-spreadsheet-development-with-a-language-agent/)

## 公開境界

この公開パッケージは次のものを意図的に除外します。

- 個人のキャリアデータ
- アカウント名、OAuth 状態、cookie、API key、token、local auth folder
- 会社内部の事実や機密実装情報
- 再配布権利が不明または非互換な外部 prompt raw corpus
- コピーされた browser-extension backend や native messaging code

## License

MIT. `LICENSE` を参照してください。
