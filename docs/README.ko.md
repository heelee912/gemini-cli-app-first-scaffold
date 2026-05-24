# Gemini Build Parity Scaffold

Gemini CLI와 Hermes 디자인 워커가 AI Studio Build에 가까운 프론트엔드 산출물을 만들도록 돕는 앱 우선 스캐폴딩입니다.

[English](../README.md) · 한국어 · [日本語](README.ja.md) · [中文](README.zh-CN.md)

이 저장소는 모델에게 더 좋은 작업 매체를 제공합니다. 즉 실제 Vite 앱, 로컬 디자인 지침, 선택적 source prompt 슬롯, 디자인 스킬 노트, 앱 소스에서 standalone HTML로 가는 패키징 경로를 제공합니다.

## 무엇이 달라지는가

Gemini CLI에 바로 요청하면 결과가 정적 HTML 하나로 수렴하기 쉽습니다. 이 저장소는 먼저 실제 프론트엔드 프로젝트 안에서 작업하게 만든 뒤, 앱이 존재한 다음에 HTML로 내보냅니다.

| 경로 | 공개 안전 예시 |
| --- | --- |
| baseline 1818 | <img src="../evidence/baseline-1818/desktop-fullpage.png" alt="1818 near-baseline snapshot" width="360"> |
| baseline 1848 | <img src="../evidence/baseline-1848/desktop-fullpage.png" alt="1848 near-baseline snapshot" width="360"> |
| 0003 앱 우선 경로. Gemini가 scaffold 안에서 작업하고 HTML 패키징 전에 더 풍부한 앱 상태를 만듭니다. | <img src="../evidence/final-0003/desktop-fullpage.png" alt="0003 app-first output" width="360"> |

## 0003 인터랙션

최종 산출물은 정적 페이지가 아닙니다. 버튼을 누르면 전체 view context가 바뀌고 다른 앱 상태가 드러납니다.

<img src="../evidence/final-0003/interaction-demo.gif" alt="0003 interaction demo" width="720">

모든 이미지는 가상 데이터를 사용합니다. 작업 방식의 효과를 보여주기 위한 문서입니다.

## Gemini CLI 빠른 시작

```powershell
git clone https://github.com/heelee912/gemini-build-parity-scaffold.git
cd gemini-build-parity-scaffold
python scripts\run_gemini_design_once.py out\fictional-profile --name "Fictional Profile" --brief-file examples\fictional-recruiter-profile\brief.md --force
```

이 runner가 하는 일:

1. Vite + React + TypeScript + Tailwind 작업 공간을 만듭니다.
2. `profile/GEMINI.md`, `profile/SKILL.md`, `design_skills/`, `prompt-seeds/`, `source-prompts/`를 작업 공간에 복사합니다.
3. 사용자 brief를 `task.md`로 씁니다.
4. 생성된 작업 공간 안에서 Gemini CLI를 실행해서 Gemini가 scaffold 파일을 직접 읽게 합니다.
5. `npm install`, `npm run lint`, `npm run build`를 실행합니다.
6. Vite `dist`를 `standalone.html`로 패키징합니다.

결과물:

```text
out\fictional-profile\standalone.html
```

## 수동 에이전트 경로

이미 Gemini를 제어하는 에이전트가 있다면 scaffold만 만들면 됩니다.

```powershell
python scripts\create_build_like_web_app.py out\my-artifact --name "My Artifact" --brief-file brief.md --force
```

그 다음 디자인 워커를 저장소 루트가 아니라 `out\my-artifact` 안에서 실행해야 합니다. 워커가 읽어야 하는 파일은 아래입니다.

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

워커가 앱을 수정한 뒤:

```powershell
cd out\my-artifact
npm install
npm run lint
npm run build
cd ..\..
python scripts\package_vite_dist_single_html.py out\my-artifact\dist out\my-artifact\standalone.html
```

## Hermes 적용 방법

Hermes home에 design profile을 설치합니다.

```powershell
python scripts\install_hermes_profile.py --hermes-home C:\path\to\.hermes-home --profile design --force
```

설치 위치:

```text
<hermes-home>\profiles\design\skills\build-parity-design-director
```

Hermes 메인 에이전트는 아래 형태로 사용하면 됩니다.

```text
build-parity-design-director profile을 사용한다.
run_gemini_design_once.py로 artifact 작업 공간을 만든다.
생성된 artifact 작업 공간 안에서 Gemini 디자인 워커를 실행한다.
실행 가능한 source 경로와 standalone.html 경로를 반환한다.
```

또는:

```text
create_build_like_web_app.py를 먼저 사용한다.
생성된 작업 공간 안에서 Gemini에게 위임한다.
Gemini가 앱을 수정한 뒤 npm install, npm run lint, npm run build, package_vite_dist_single_html.py를 실행한다.
```

Hermes core를 fork할 필요는 없습니다. 이 저장소의 연결 지점은 profile과 외부 runner입니다.

## Gemini가 보는 것

생성된 artifact는 자체 설명 가능한 구조를 갖습니다.

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

중요한 점은 실행 문맥입니다. Gemini는 단일 프롬프트만 받는 것이 아니라, 구현 매체, 사용 가능한 의존성, 모바일 요구사항, 패키징 경로, 선택적 source context를 설명하는 앱 작업 공간 안에서 실행됩니다.

## 선택적 Source Prompts

AI Studio 원문 prompt 파일은 이 저장소에 재배포하지 않습니다. 합법적으로 사용할 수 있는 prompt 파일이 있다면 아래에 넣으십시오.

```text
profile\source-prompts\
```

scaffold는 이 폴더를 생성되는 모든 artifact에 복사하므로 Gemini가 로컬에서 읽을 수 있습니다.

## 저장소 구성

| 경로 | 목적 |
| --- | --- |
| `profile/GEMINI.md` | Gemini가 앱 우선으로 만들고 시각 방향을 직접 결정하도록 하는 실행 커널입니다. |
| `profile/SKILL.md` | Hermes나 다른 에이전트 시스템용 skill wrapper입니다. |
| `profile/design_skills/` | 생성되는 artifact마다 복사되는 보조 디자인 노트입니다. |
| `profile/prompt-seeds/` | 작업 내용이 제거된 일반적인 고성능 prompt driver입니다. |
| `profile/source-prompts/README.md` | 재배포하지 않는 선택적 source prompt corpus 자리입니다. |
| `scripts/run_gemini_design_once.py` | scaffold 생성, Gemini CLI 실행, install, lint, build, standalone HTML 패키징을 한 번에 수행합니다. |
| `scripts/create_build_like_web_app.py` | Vite/React/Tailwind scaffold만 만듭니다. 다른 에이전트가 Gemini를 제어할 때 사용합니다. |
| `scripts/install_hermes_profile.py` | profile을 Hermes home에 설치합니다. |
| `scripts/package_vite_dist_single_html.py` | Vite `dist` asset을 브라우저에서 열 수 있는 단일 HTML로 inline합니다. |
| `examples/fictional-recruiter-profile/` | 공개 안전한 예시 brief입니다. |
| `evidence/` | 가상 데이터 기반 스크린샷과 인터랙션 GIF입니다. |

## 관련 연구

이 저장소는 단일 프롬프트에 기대는 대신 workspace 구조, 도구, 지침, 상태, 실행 feedback으로 모델을 둘러싸는 scaffolding 아이디어와 연결됩니다.

- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](https://arxiv.org/abs/2604.03515)
- [BISCUIT: Scaffolding LLM-Generated Code with Ephemeral UIs in Computational Notebooks](https://machinelearning.apple.com/research/biscuit-scaffolding-llm)
- [TableTalk: Scaffolding Spreadsheet Development with a Language Agent](https://www.microsoft.com/en-us/research/publication/tabletalk-scaffolding-spreadsheet-development-with-a-language-agent/)

## 공개 경계

이 공개 패키지는 아래를 의도적으로 제외합니다.

- 개인 커리어 데이터
- 계정명, OAuth 상태, 쿠키, API key, token, local auth folder
- 회사 내부 사실이나 기밀 구현 세부사항
- 재배포 권리가 불명확하거나 호환되지 않는 외부 prompt 원문 corpus
- 복사된 browser-extension backend나 native messaging code

## License

MIT. `LICENSE`를 보십시오.
