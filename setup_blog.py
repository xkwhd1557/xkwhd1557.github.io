import os
from pathlib import Path

# 1. 기존 불필요 파일 및 오타 파일 정리
for old_file in ["custum.scss", "math.qmd", "stats.qmd", "cs.qmd", "ds.qmd", "articles.qmd", "text.qmd"]:
    p = Path(old_file)
    if p.exists():
        p.unlink()

# 2. 전체 카테고리 및 69개 세부 과목 정의
CATEGORIES = [
    {
        "id": "math",
        "title": "수학",
        "en_title": "Mathematics",
        "levels": [
            ("기초 (Foundations)", [
                ("analysis", "해석학"),
                ("linear-algebra", "선형대수학"),
                ("discrete-math", "이산수학"),
                ("math-programming", "수학적 프로그래밍 (Python)"),
                ("latex", "LaTeX"),
            ]),
            ("핵심 (Core)", [
                ("complex-analysis", "복소해석학"),
                ("ode", "상미분방정식"),
                ("dynamical-systems", "동적 시스템"),
                ("measure-theory", "측도론"),
                ("pde-intro", "기초 편미분방정식"),
                ("general-topology", "일반위상수학"),
                ("algebra", "대수학"),
                ("number-theory", "정수론"),
                ("geometry", "기하학"),
                ("mathematical-logic", "수리논리학"),
                ("set-theory", "공리적 집합론"),
                ("numerical-methods", "수치적 방법론"),
                ("optimization", "수학적 최적화"),
            ]),
            ("심화 (Advanced)", [
                ("functional-analysis", "함수해석학"),
                ("pde-advanced", "편미분방정식"),
                ("manifold-analysis", "다양체 해석학"),
                ("rkhs", "RKHS 이론"),
                ("differential-geometry", "미분기하학"),
            ]),
        ],
    },
    {
        "id": "stats",
        "title": "확률과 통계",
        "en_title": "Probability & Statistics",
        "levels": [
            ("기초 (Foundations)", [
                ("prob-theory", "기초 확률론"),
                ("basic-stats", "기초 통계학"),
                ("stat-programming", "통계적 프로그래밍"),
            ]),
            ("핵심 (Core)", [
                ("measure-prob", "측도론적 확률론"),
                ("stochastic-processes", "확률과정론"),
                ("math-stats", "수리통계학"),
                ("stochastic-simulation", "확률적 시뮬레이션"),
                ("actuarial-math", "보험수학"),
            ]),
            ("심화 (Advanced)", [
                ("stochastic-calculus", "확률해석학"),
                ("markov-processes", "마르코프 프로세스"),
                ("diffusion-models", "디퓨전 모델"),
                ("gaussian-processes", "가우시안 프로세스"),
                ("non-euclidean-stats", "비유클리드 통계학"),
                ("stats-for-stoch-proc", "확률과정의 통계추론"),
            ]),
        ],
    },
    {
        "id": "cs",
        "title": "컴퓨터 공학",
        "en_title": "Computer Science",
        "levels": [
            ("기초 (Foundations)", [
                ("cs-intro", "컴퓨터 과학 원론"),
                ("c-programming", "C언어"),
            ]),
            ("핵심 (Core)", [
                ("algorithms-data-structures", "알고리즘과 자료구조"),
                ("theoretical-cs", "이론 컴퓨터과학"),
                ("database-systems", "데이터베이스 시스템"),
                ("formal-systems", "형식 시스템"),
            ]),
            ("심화 (Advanced)", [
                ("advanced", "심화 과정 (준비 중)"),
            ]),
        ],
    },
    {
        "id": "ds-ai",
        "title": "데이터 사이언스·AI",
        "en_title": "Data Science & AI",
        "levels": [
            ("기초 (Foundations)", [
                ("ds-intro", "데이터 사이언스 개론"),
                ("ds-society", "데이터 사이언스와 사회"),
                ("ai-math-intro", "고등학교 인공지능 수학"),
            ]),
            ("핵심 (Core)", [
                ("numerical-optimization", "수치적 방법론과 최적화"),
                ("machine-learning", "머신러닝"),
                ("deep-learning-cv", "딥러닝과 컴퓨터 비전"),
                ("ai-intro", "인공지능 원론"),
            ]),
            ("심화 (Advanced)", [
                ("statistical-foundations", "데이터 사이언스의 통계적 기초"),
                ("mathematical-foundations", "머신러닝의 수리적 기초"),
                ("advanced-linear-algebra", "데이터 사이언스를 위한 선형대수학"),
            ]),
        ],
    },
    {
        "id": "biz-econ",
        "title": "경영/경제",
        "en_title": "Business & Economics",
        "levels": [
            ("기초 (Foundations)", [
                ("biz-intro", "경영학 원론"),
                ("econ-intro", "경제학 원론"),
            ]),
            ("핵심 (Core)", [
                ("accounting", "회계학"),
                ("production-logistics", "생산물류관리"),
                ("decision-theory", "의사결정론"),
                ("microeconomics", "미시경제학"),
                ("macroeconomics", "거시경제학"),
                ("finance-investment", "재무와 투자론"),
                ("monetary-economics", "화폐금융론"),
                ("labor-economics", "노동경제학"),
                ("game-theory", "게임이론 개론"),
                ("supply-chain", "공급망 관리 (SCM)"),
                ("market-research", "시장조사론의 기초"),
            ]),
            ("심화 (Advanced)", [
                ("time-series", "시계열 분석"),
                ("econometrics", "계량경제학"),
                ("insurance-economics", "보험경제학"),
                ("quantitative-risk", "계량 리스크 관리"),
                ("corporate-finance", "기업재무론"),
            ]),
        ],
    },
    {
        "id": "biostat",
        "title": "의학통계·바이오메트리",
        "en_title": "Biostatistics & Biometry",
        "levels": [
            ("기초 (Foundations)", [
                ("biostat-intro", "의학통계학 개론"),
                ("epidemiology", "역학 연구방법론"),
            ]),
            ("핵심 (Core)", [
                ("clinical-trials", "임상시험 통계방법론"),
                ("survival-analysis", "생존분석"),
                ("bioinformatics", "생물정보통계학"),
            ]),
            ("심화 (Advanced)", [
                ("causal-inference", "인과추론"),
                ("longitudinal-data", "종단적 데이터 분석"),
            ]),
        ],
    },
]

# 3. 기본 썸네일 플레이스홀더 이미지 생성 (추후 개별 과목 사진으로 교체 가능)
Path("images").mkdir(exist_ok=True)
svg_placeholder = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="340" viewBox="0 0 600 340">
  <rect width="600" height="340" fill="#f0f4f8" rx="12"/>
  <path d="M 60 260 Q 180 100 300 220 T 540 120" fill="none" stroke="#2b7a78" stroke-width="4" stroke-dasharray="8,8"/>
  <circle cx="180" cy="160" r="6" fill="#17252a"/>
  <circle cx="300" cy="220" r="6" fill="#17252a"/>
  <circle cx="420" cy="170" r="6" fill="#17252a"/>
  <text x="300" y="295" font-family="sans-serif" font-size="18" fill="#556677" text-anchor="middle">Course Archive</text>
</svg>
"""
Path("images/placeholder.svg").write_text(svg_placeholder, encoding="utf-8")

# 4. 메인 페이지 (index.qmd) + 일반 아티클 목록 페이지 (articles/index.qmd) 생성
#    - 메인: 추천 아티클(front matter에 featured: true 인 글) 최대 3개 → 제목·부제만 표시
#            그 아래에 각 대분류의 '기초' 과목 카드(텍스트 + 이미지)
#    - articles/index.qmd: 일반 아티클 전체 목록 (상단 메뉴 '일반 아티클'이 여기로 연결)
index_lines = [
    "---",
    'title: "Study Archive"',
    'subtitle: "수학 · 통계 · 데이터 사이언스 공부 기록"',
    "page-layout: full",
    "sidebar: false",
    "toc: false",
    "listing:",
    "  - id: featured-articles",
    "    contents: \"articles/*.qmd\"",
    "    include:",
    "      featured: true",
    "    sort: \"date desc\"",
    "    max-items: 3",
    "    type: grid",
    "    grid-columns: 3",
    "    fields: [title, subtitle]",
    "---",
    "",
    "## 추천 아티클",
    "",
    "::: {#featured-articles}",
    ":::",
    "",
    "::: {.home-more}",
    "[일반 아티클 전체 보기 →](articles/index.qmd)",
    ":::",
    "",
    "## 기초부터 시작하기",
    "",
    "각 분야의 기초 과목입니다. 과목을 선택하면 첫 번째 개념 노트로 이동합니다.",
    "",
]
for cat in CATEGORIES:
    level_title, subjects = cat["levels"][0]
    index_lines.append(f"### {cat['title']} ({cat['en_title']}) {{.home-category}}")
    index_lines.append("")
    index_lines.append("::: {.subject-grid}")
    for subj_slug, subj_name in subjects:
        first_post = f"{cat['id']}/{subj_slug}/text.qmd"
        index_lines.extend([
            "::: {.subject-card}",
            f"#### [{subj_name}]({first_post})",
            f"[![{subj_name}](images/placeholder.svg)]({first_post})",
            ":::",
        ])
    index_lines.append(":::")
    index_lines.append("")
    index_lines.append("::: {.home-more}")
    index_lines.append(f"[{cat['title']} 전체 과목 보기 →]({cat['id']}/index.qmd)")
    index_lines.append(":::")
    index_lines.append("")
Path("index.qmd").write_text("\n".join(index_lines), encoding="utf-8")

Path("articles").mkdir(exist_ok=True)
Path("articles/index.qmd").write_text("""---
title: "일반 아티클 (Articles)"
subtitle: "수학, 통계, 데이터 사이언스에 관한 에세이와 단상"
listing:
  contents:
    - "*.qmd"
  sort: "date desc"
  type: default
  categories: true
page-layout: full
sidebar: false
---
""", encoding="utf-8")

# 5. 다국어 준비중 페이지 생성
Path("lang").mkdir(exist_ok=True)
Path("lang/en-coming-soon.qmd").write_text("""---
title: "Under Construction"
page-layout: full
sidebar: false
---

::: {.callout-note icon=false}
## Notice
The English version of this archive is currently under preparation. Please check back later.

[Return to Korean Main Page](../index.qmd)
:::
""", encoding="utf-8")

Path("lang/de-coming-soon.qmd").write_text("""---
title: "In Vorbereitung"
page-layout: full
sidebar: false
---

::: {.callout-note icon=false}
## Hinweis
Die deutsche Version dieses Archivs befindet sich derzeit im Aufbau. Bitte besuchen Sie die Seite zu einem späteren Zeitpunkt erneut.

[Zurück zur koreanischen Hauptseite](../index.qmd)
:::
""", encoding="utf-8")

LEVEL_DESCRIPTIONS = [
    ("Foundations", "사전 지식 없이 시작할 수 있는 전공 기초 과목입니다."),
    ("Core", "기초를 바탕으로 각 분야의 본격적인 주제에 첫발을 내딛는 과목입니다."),
    ("Advanced", "핵심 과목 이후, 깊이 있는 이론과 고급 주제를 본격적으로 다루는 과목입니다."),
]

# 6. 각 대분류 랜딩 페이지(<cat>/index.qmd) 및 과목별 기본 글(<cat>/<subj>/text.qmd) 생성
for cat in CATEGORIES:
    cat_dir = Path(cat["id"])
    cat_dir.mkdir(exist_ok=True)

    # 대분류 랜딩 페이지 작성 (텍스트 + 아래 이미지 카드 그리드)
    landing_lines = [
        "---",
        f'title: "{cat["title"]} ({cat["en_title"]})"',
        'subtitle: "기초에서 출발해 핵심을 거쳐 심화로 나아갑니다. 과목을 선택하면 첫 번째 노트로 이동합니다."',
        "page-layout: full",
        "sidebar: false",
        "---",
        "",
    ]

    for level_title, subjects in cat["levels"]:
        landing_lines.append(f"## {level_title}\n")
        for tag, desc in LEVEL_DESCRIPTIONS:
            if f"({tag}" in level_title:
                landing_lines.extend([desc, ""])
                break
        landing_lines.append("::: {.subject-grid}")
        for subj_slug, subj_name in subjects:
            first_post = f"{subj_slug}/text.qmd"
            landing_lines.extend([
                "::: {.subject-card}",
                f"### [{subj_name}]({first_post})",
                f"[![{subj_name}](../images/placeholder.svg)]({first_post})",
                ":::",
            ])
        landing_lines.append(":::\n")

    (cat_dir / "index.qmd").write_text("\n".join(landing_lines), encoding="utf-8")

    # 각 세부 과목 폴더 및 text.qmd 생성
    for level_title, subjects in cat["levels"]:
        for subj_slug, subj_name in subjects:
            subj_dir = cat_dir / subj_slug
            subj_dir.mkdir(parents=True, exist_ok=True)
            text_qmd_path = subj_dir / "text.qmd"

            text_content = f"""---
title: "text"
subtitle: "{subj_name} · 1.1절 기본 양식"
date: "2026-10-31"
categories: ["{cat['title']}", "{subj_name}"]
---

::: {{.concept-meta}}
[← {cat['title']} 과목 목록으로](../index.qmd) | **선수 개념:** [기초 개념](#) | **다음 개념:** [심화 개념](#)
:::

::: {{.callout-note icon=false .callout-definition}}
### 정의 1.1 (Definition)
여기에 **{subj_name}**의 핵심 정의를 작성합니다. 임의의 대상 $x, y \\in X$에 대하여 다음 조건이 성립한다.
$$f(x) = y$$
:::

::: {{.callout-important icon=false .callout-satz}}
### 정리 1.2 (Satz)
위 정의로부터 유도되는 주요 정리를 서술합니다.
$$\\int_a^b f(x)\\,dx = F(b) - F(a)$$
:::

::: {{.callout-tip collapse="false" icon=false .callout-beweis}}
### 증명 (Beweis)
정리에 대한 논리적 증명 과정을 단계별로 서술합니다. $\\blacksquare$
:::

---

### 연결되는 개념
* $\\leftarrow$ **이전 개념:** [과목 전체 목차](../index.qmd)
* $\\rightarrow$ **다음 개념:** 추후 작성 예정
"""
            text_qmd_path.write_text(text_content, encoding="utf-8")

# 7. 스타일시트 (custom.scss) 생성 - Aleph1 박스 + 과목 카드 그리드 + 상단 드롭다운 호버
custom_scss = """/*-- scss:defaults --*/

/*-- scss:rules --*/

/* 상단 네비게이션바 마우스 호버 시 드롭다운 자동 펼침 (PC 화면) */
@media (min-width: 992px) {
  .navbar .nav-item.dropdown:hover > .dropdown-menu {
    display: block;
    margin-top: 0;
  }
}

/* ------------------------------------------------------------------
   메가 메뉴: 그룹(기초/핵심/심화)을 가로 열로 펼친 드롭다운
   (nav-click.html 의 스크립트가 .mega-menu 구조로 재배치함)
   ------------------------------------------------------------------ */
.navbar .dropdown-menu.mega-menu .mega-items {
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar .dropdown-menu.mega-menu .mega-top {
  padding-bottom: 0.35rem;
  margin-bottom: 0.35rem;
  border-bottom: 1px solid #e9ecef;
}

/* 모바일(접힌 메뉴): 세로 목록 유지, 그룹 사이 구분선만 */
.navbar .dropdown-menu.mega-menu .mega-group + .mega-group {
  border-top: 1px solid #e9ecef;
  margin-top: 0.35rem;
  padding-top: 0.35rem;
}

.navbar .dropdown-menu.mega-menu .mega-group .dropdown-header {
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.02em;
  text-transform: none;
  color: #2b7a78;
}

@media (min-width: 992px) {
  .navbar .dropdown-menu.mega-menu {
    width: max-content;
    max-width: calc(100vw - 2rem);
    max-height: calc(100vh - 5rem);
    overflow-y: auto;
    padding: 0.6rem 0.5rem 0.5rem;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    box-shadow: 0 14px 34px rgba(23, 37, 42, 0.14);
  }

  .navbar .dropdown-menu.mega-menu .mega-top {
    padding: 0 0.25rem 0.5rem;
    margin-bottom: 0.5rem;
  }

  .navbar .dropdown-menu.mega-menu .mega-top .dropdown-item {
    display: inline-block;
    width: auto;
    font-weight: 600;
    border-radius: 6px;
  }

  .navbar .dropdown-menu.mega-menu .mega-groups {
    display: flex;
    align-items: stretch;
  }

  .navbar .dropdown-menu.mega-menu .mega-group {
    padding: 0 0.35rem;
  }

  .navbar .dropdown-menu.mega-menu .mega-group + .mega-group {
    border-top: 0;
    margin-top: 0;
    padding-top: 0;
    border-left: 1px solid #eef0f3;
  }

  .navbar .dropdown-menu.mega-menu .mega-group .dropdown-header {
    white-space: nowrap;
    padding: 0.2rem 0.75rem 0.45rem;
  }

  /* 한 그룹 안 과목이 많으면 여러 열로 (행 수는 스크립트가 --mega-rows 로 지정) */
  .navbar .dropdown-menu.mega-menu .mega-items {
    display: grid;
    grid-auto-flow: column;
    grid-template-rows: repeat(var(--mega-rows, 7), auto);
    column-gap: 0.25rem;
  }

  .navbar .dropdown-menu.mega-menu .mega-items .dropdown-item {
    padding: 0.3rem 0.75rem;
    border-radius: 6px;
    white-space: nowrap;
  }
}

/* Aleph1 스타일 정의(Definition), 정리(Satz), 증명(Beweis) 박스 */
.callout-definition {
  border-left-color: #2b7a78 !important;
  background-color: #f4fbfb !important;
}

.callout-satz {
  border-left-color: #17252a !important;
  background-color: #f0f4f8 !important;
}

.callout-beweis {
  border-left-color: #3aafa9 !important;
  background-color: #fafbfc !important;
}

.concept-meta {
  font-size: 0.92em;
  color: #555;
  margin-bottom: 1.5rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid #e5e5e5;
}

/* 대분류 페이지의 세부 과목 카드 그리드 */
.subject-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
  margin-bottom: 2.5rem;
}

.subject-card {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem;
  background: #ffffff;
  text-align: center;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.subject-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.subject-card h3 {
  font-size: 1.1rem;
  margin-top: 0.2rem;
  margin-bottom: 0.75rem;
}

.subject-card h3 a {
  text-decoration: none;
  color: #17252a;
  font-weight: 600;
}

.subject-card h3 a:hover {
  color: #2b7a78;
}

.subject-card img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 0;
}
"""
Path("custom.scss").write_text(custom_scss, encoding="utf-8")

# 8. 상단 메뉴 클릭 시 대분류 랜딩 페이지로 바로 이동시키는 스크립트 생성
nav_script = """<script>
document.addEventListener("DOMContentLoaded", function() {
  const categoryLinks = {
    "수학": "/math/index.html",
    "확률과 통계": "/stats/index.html",
    "컴퓨터 공학": "/cs/index.html",
    "데이터 사이언스·AI": "/ds-ai/index.html",
    "경영/경제": "/biz-econ/index.html",
    "의학통계·바이오메트리": "/biostat/index.html"
  };
  document.querySelectorAll('.navbar-nav .nav-item.dropdown > a.nav-link').forEach(function(el) {
    const label = el.textContent.trim();
    if (categoryLinks[label]) {
      el.setAttribute('href', categoryLinks[label]);
      el.addEventListener('click', function(e) {
        if (window.innerWidth >= 992) {
          window.location.href = categoryLinks[label];
        }
      });
    }
  });

  /* ---------------------------------------------------------------
     메가 메뉴: 드롭다운을 그룹(헤더 단위)별 가로 열로 재배치
     - 첫 헤더 이전 항목(예: "전체 과목 보기")은 상단 한 줄로
     - 한 그룹의 과목이 MAX_ROWS 개를 넘으면 그 그룹 안에서 열을 나눔
     --------------------------------------------------------------- */
  const MAX_ROWS = 7;      // 한 열에 들어갈 최대 과목 수
  const EDGE = 16;         // 화면 가장자리 여백(px)

  document.querySelectorAll('.navbar .nav-item.dropdown > .dropdown-menu').forEach(function(menu) {
    const items = Array.from(menu.children);
    if (items.filter(function(li) { return li.classList.contains('dropdown-header'); }).length < 2) return;

    const top = document.createElement('li');
    top.className = 'mega-top';
    const groupsWrap = document.createElement('li');
    groupsWrap.className = 'mega-groups';

    let current = null;
    items.forEach(function(li) {
      if (li.querySelector('.dropdown-divider')) { li.remove(); return; }
      if (li.classList.contains('dropdown-header')) {
        const group = document.createElement('div');
        group.className = 'mega-group';
        const header = document.createElement('div');
        header.className = 'dropdown-header';
        header.textContent = li.textContent.trim();
        const list = document.createElement('ul');
        list.className = 'mega-items';
        group.appendChild(header);
        group.appendChild(list);
        groupsWrap.appendChild(group);
        current = list;
        li.remove();
        return;
      }
      if (current) {
        current.appendChild(li);
      } else {
        top.appendChild(li.querySelector('a') || li);
        li.remove();
      }
    });

    groupsWrap.querySelectorAll('.mega-items').forEach(function(list) {
      const n = list.children.length;
      const cols = Math.max(1, Math.ceil(n / MAX_ROWS));
      list.style.setProperty('--mega-rows', Math.ceil(n / cols));
    });

    menu.innerHTML = '';
    if (top.children.length) menu.appendChild(top);
    menu.appendChild(groupsWrap);
    menu.classList.add('mega-menu');
  });

  /* 펼친 메뉴가 화면 오른쪽 밖으로 나가지 않도록 위치 보정 */
  function fitToViewport(menu) {
    if (window.innerWidth < 992) { menu.style.left = ''; return; }
    menu.style.left = '0px';
    const rect = menu.getBoundingClientRect();
    if (rect.width === 0) return;
    let shift = 0;
    const overflow = rect.right - (window.innerWidth - EDGE);
    if (overflow > 0) shift = -overflow;
    if (rect.left + shift < EDGE) shift = EDGE - rect.left;
    menu.style.left = shift + 'px';
  }

  document.querySelectorAll('.navbar .nav-item.dropdown').forEach(function(item) {
    const menu = item.querySelector(':scope > .dropdown-menu.mega-menu');
    if (!menu) return;
    const fit = function() { requestAnimationFrame(function() { fitToViewport(menu); }); };
    item.addEventListener('mouseenter', fit);
    item.addEventListener('focusin', fit);
    item.addEventListener('shown.bs.dropdown', fit);
  });
});
</script>
"""
Path("nav-click.html").write_text(nav_script, encoding="utf-8")

# 9. _quarto.yml 생성 (드롭다운 메뉴 + 69개 과목 각각의 독립 사이드바)
yml_lines = [
    "project:",
    "  type: website",
    "  output-dir: _site",
    "",
    "website:",
    '  title: "Study Archive"',
    "  navbar:",
    "    background: primary",
    "    search: true",
    "    left:",
    '      - text: "일반 아티클"',
    "        href: articles/index.qmd",
]

# 상단 드롭다운 메뉴 구성
for cat in CATEGORIES:
    yml_lines.append(f'      - text: "{cat["title"]}"')
    yml_lines.append("        menu:")
    yml_lines.append(f'          - text: "📋 {cat["title"]} 전체 과목 보기"')
    yml_lines.append(f'            href: {cat["id"]}/index.qmd')
    for level_title, subjects in cat["levels"]:
        yml_lines.append('          - text: "---"')
        yml_lines.append(f'          - text: "{level_title}"')
        for subj_slug, subj_name in subjects:
            yml_lines.append(f'          - text: "{subj_name}"')
            yml_lines.append(f'            href: {cat["id"]}/{subj_slug}/text.qmd')

yml_lines.extend([
    "    right:",
    '      - text: "🌐 Language"',
    "        menu:",
    '          - text: "한국어 (KO)"',
    "            href: index.qmd",
    '          - text: "English (EN)"',
    "            href: lang/en-coming-soon.qmd",
    '          - text: "Deutsch (DE)"',
    "            href: lang/de-coming-soon.qmd",
    "      - icon: github",
    "        href: https://github.com/xkwhd1557/xkwhd1557.github.io",
    "",
    "  sidebar:",
])

# 69개 과목별 독립 사이드바 생성 (해당 과목에 들어갔을 때 그 과목의 장들만 표시됨)
for cat in CATEGORIES:
    for level_title, subjects in cat["levels"]:
        for subj_slug, subj_name in subjects:
            yml_lines.extend([
                f'    - id: "{cat["id"]}-{subj_slug}"',
                f'      title: "{subj_name}"',
                '      style: "docked"',
                "      search: true",
                "      contents:",
                '        - section: "1장. 기본 개념"',
                "          contents:",
                '            - text: "1.1 text"',
                f'              href: {cat["id"]}/{subj_slug}/text.qmd',
            ])

yml_lines.extend([
    "",
    "format:",
    "  html:",
    "    theme:",
    "      - cosmo",
    "      - custom.scss",
    "    html-math-method: mathjax",
    "    toc: true",
    "    toc-depth: 3",
    "    include-after-body: nav-click.html",
])

Path("_quarto.yml").write_text("\n".join(yml_lines) + "\n", encoding="utf-8")
print("✅ 모든 폴더, 과목별 text.qmd, 대분류 카드 페이지, _quarto.yml 생성이 완료되었습니다!")