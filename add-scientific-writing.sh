#!/usr/bin/env bash
# 새 과목 "수학 학술 논문 작성법(Scientific Writing for Mathematics)"을 수학 › 기초에 추가
# 레포 루트(xkwhd1557.github.io)에서 실행: bash add-scientific-writing.sh
# 글 파일(math/scientific-writing/...)은 함께 받은 zip에 들어 있습니다.
# 이 스크립트는 메뉴·사이드바·카드·CATEGORIES만 고치고, 과목 소개 글이 없을 때만 자리를 만듭니다.
set -euo pipefail

SLUG="scientific-writing"
NAME_KO="수학 학술 논문 작성법"
NAME_EN="Scientific Writing for Mathematics"
TODAY="2026-11-24"

for f in _quarto.yml math/index.qmd index.qmd setup_blog.py; do
  [[ -f "$f" ]] || { echo "오류: $f 이 없습니다. 레포 루트에서 실행하세요." >&2; exit 1; }
done

if grep -q "math/$SLUG/" _quarto.yml; then
  echo "이미 _quarto.yml에 $SLUG 가 있습니다. 아무것도 바꾸지 않고 종료합니다."
  exit 0
fi

# 줄바꿈(CRLF/LF)을 파일마다 유지하면서, 기준 줄 뒤에 새 줄들을 끼워 넣는 함수
#   $1: 파일, $2: 기준 줄(앞뒤 공백·\r 제외하고 정확히 일치), $3: 끼워 넣을 내용(\n 구분)
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

# 1) _quarto.yml 상단 메뉴: 수학 › 기초의 LaTeX 바로 아래
insert_after _quarto.yml "href: math/latex/index.qmd" \
"          - text: \"$NAME_KO\"
            href: math/$SLUG/index.qmd"

# 2) _quarto.yml 사이드바 블록: LaTeX 블록 바로 아래
insert_after _quarto.yml "contents: \"math/latex/**\"" \
"    - id: \"math-$SLUG\"
      title: \"$NAME_KO\"
      style: \"docked\"
      collapse-level: 4
      search: true
      contents:
        - href: math/$SLUG/index.qmd
          contents: \"math/$SLUG/**\""

# 3) math/index.qmd 기초(Foundations) 카드: LaTeX 카드 바로 뒤
insert_after math/index.qmd "[![LaTeX](../images/placeholder.svg)](latex/index.qmd)" \
"::: {.subject-card}
### [$NAME_KO]($SLUG/index.qmd)
[![$NAME_KO](../images/placeholder.svg)]($SLUG/index.qmd)
:::" next

# 4) 홈 index.qmd 수학 기초 카드: LaTeX 카드 바로 뒤
insert_after index.qmd "[![LaTeX](images/placeholder.svg)](math/latex/index.qmd)" \
"::: {.subject-card}
#### [$NAME_KO](math/$SLUG/index.qmd)
[![$NAME_KO](images/placeholder.svg)](math/$SLUG/index.qmd)
:::" next

# 5) setup_blog.py CATEGORIES: LaTeX 바로 아래
insert_after setup_blog.py "(\"latex\", \"LaTeX\")," \
"                (\"$SLUG\", \"$NAME_KO\"),"

# 6) 과목 소개 글: zip에서 이미 풀었다면 건드리지 않음
mkdir -p "math/$SLUG"
if [[ ! -f "math/$SLUG/index.qmd" ]]; then
  cat > "math/$SLUG/index.qmd" <<EOF
---
title: "$NAME_KO($NAME_EN)"
subtitle: "이 과목은 무엇을 다루는가"
date: "$TODAY"
categories: ["수학", "$NAME_KO"]
---

이 과목의 소개 글은 준비 중입니다.
EOF
  echo "  (math/$SLUG/index.qmd 가 없어 자리만 만들었습니다. zip의 글 파일을 풀어 덮어쓰세요.)"
fi

echo "완료: $NAME_KO 과목을 수학 › 기초에 추가했습니다."
echo "  - _quarto.yml (상단 메뉴, 사이드바)"
echo "  - math/index.qmd (기초 카드)"
echo "  - index.qmd (홈 수학 기초 카드)"
echo "  - setup_blog.py (CATEGORIES)"
echo "확인: git diff --stat && quarto preview"
