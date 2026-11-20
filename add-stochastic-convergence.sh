#!/usr/bin/env bash
# 새 과목 "확률적 수렴과 오차 분석(Stochastic Convergence and Error Analysis)" 추가
# 레포 루트(xkwhd1557.github.io)에서 실행: bash add-stochastic-convergence.sh
set -euo pipefail

SLUG="stochastic-convergence"
NAME_KO="확률적 수렴과 오차 분석"
NAME_EN="Stochastic Convergence and Error Analysis"
TODAY="2026-11-20"

for f in _quarto.yml stats/index.qmd setup_blog.py; do
  [[ -f "$f" ]] || { echo "오류: $f 이 없습니다. 레포 루트에서 실행하세요." >&2; exit 1; }
done

if grep -q "stats/$SLUG/" _quarto.yml; then
  echo "이미 _quarto.yml에 $SLUG 가 있습니다. 아무것도 바꾸지 않고 종료합니다."
  exit 0
fi

# 줄바꿈(CRLF/LF)을 파일마다 유지하면서, 기준 줄 뒤에 새 줄들을 끼워 넣는 함수
#   $1: 파일, $2: 기준 줄(공백·\r 제외하고 정확히 일치), $3: 끼워 넣을 내용(\n 구분)
#   $4: "next"면 기준 줄 다음 줄 뒤에 넣음
insert_after() {
  local file="$1" anchor="$2" block="$3" mode="${4:-}"
  local tmp; tmp="$(mktemp)"
  awk -v anchor="$anchor" -v block="$block" -v mode="$mode" '
    function trim(s) { sub(/\r$/, "", s); gsub(/^[ \t]+|[ \t]+$/, "", s); return s }
    function emit(eol,   n, i, parts) {
      n = split(block, parts, "\n")
      for (i = 1; i <= n; i++) printf "%s%s\n", parts[i], eol
      done = 1
    }
    {
      eol = ($0 ~ /\r$/) ? "\r" : ""
      print
      if (done) next
      if (wait) { wait = 0; emit(eol); next }
      if (trim($0) == anchor) { if (mode == "next") wait = 1; else emit(eol) }
    }
    END { if (!done) exit 3 }
  ' "$file" > "$tmp" || { rm -f "$tmp"; echo "오류: $file 에서 기준 줄 \"$anchor\" 을 찾지 못했습니다." >&2; exit 1; }
  # 원래 파일이 마지막 줄바꿈 없이 끝났다면 그대로 유지
  if [[ -n "$(tail -c1 "$file")" ]]; then
    head -c -1 "$tmp" > "$tmp.2" && mv "$tmp.2" "$tmp"
  fi
  cat "$tmp" > "$file"   # 원래 파일 권한 유지
  rm -f "$tmp"
}

# 1) _quarto.yml 상단 메뉴: 측도론적 확률론 바로 아래
insert_after _quarto.yml "href: stats/measure-prob/index.qmd" \
"          - text: \"$NAME_KO\"
            href: stats/$SLUG/index.qmd"

# 2) _quarto.yml 사이드바 블록: 측도론적 확률론 블록 바로 아래
insert_after _quarto.yml "contents: \"stats/measure-prob/**\"" \
"    - id: \"stats-$SLUG\"
      title: \"$NAME_KO\"
      style: \"docked\"
      collapse-level: 4
      search: true
      contents:
        - href: stats/$SLUG/index.qmd
          contents: \"stats/$SLUG/**\""

# 3) stats/index.qmd 핵심(Core) 카드: 측도론적 확률론 카드 바로 뒤
insert_after stats/index.qmd "[![측도론적 확률론](../images/placeholder.svg)](measure-prob/index.qmd)" \
"::: {.subject-card}
### [$NAME_KO]($SLUG/index.qmd)
[![$NAME_KO](../images/placeholder.svg)]($SLUG/index.qmd)
:::" next

# 4) setup_blog.py CATEGORIES: 측도론적 확률론 바로 아래
insert_after setup_blog.py "(\"measure-prob\", \"측도론적 확률론\")," \
"                (\"$SLUG\", \"$NAME_KO\"),"

# 5) 과목 소개 글 (자리만 만들어 둠)
mkdir -p "stats/$SLUG"
cat > "stats/$SLUG/index.qmd" <<EOF
---
title: "$NAME_KO($NAME_EN)"
subtitle: "이 과목은 무엇을 다루는가"
description: "확률변수의 여러 가지 수렴 개념과 확률 부등식, 큰 수의 법칙, 중심극한정리를 복습하며, 확률적 시뮬레이션과 통계에서 오차의 크기와 수렴 속도를 어떻게 이해하는지 정리합니다."
date: "$TODAY"
categories: ["확률과 통계", "$NAME_KO"]
---

이 과목의 소개 글은 준비 중입니다.
EOF

echo "완료: $NAME_KO 과목을 추가했습니다."
echo "  - _quarto.yml (상단 메뉴, 사이드바)"
echo "  - stats/index.qmd (핵심 카드)"
echo "  - setup_blog.py (CATEGORIES)"
echo "  - stats/$SLUG/index.qmd (새 파일)"
echo "확인: git diff --stat && quarto preview"
