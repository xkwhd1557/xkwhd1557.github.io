#!/usr/bin/env bash
# 레포 루트에서 실행: 1장 소개, 1.1, 1.2의 링크·목록 몇 줄만 고칩니다.
# - 고칠 줄을 각각 정확히 한 번씩 찾지 못하면 아무 파일도 건드리지 않고 멈춥니다.
set -euo pipefail
PY=$(command -v python3 || command -v python) || { echo "python이 필요합니다"; exit 1; }

"$PY" - <<'EOF'
import io, sys

D = "ds-ai/ds-intro/01-foundations/"

def load(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        s = f.read()
    nl = "\r\n" if "\r\n" in s else "\n"
    return s, nl

def find_one(lines, pred, what, path):
    hits = [i for i, l in enumerate(lines) if pred(l)]
    if len(hits) != 1:
        sys.exit(f"[중단] {path}: '{what}' 줄을 {len(hits)}개 찾았습니다(1개여야 함). 아무 파일도 바꾸지 않았습니다.")
    return hits[0]

plans = {}   # path -> (원문, 새 내용)

# 1) 1.2: 다음 개념 -> 1.3
p = D + "02-applications.qmd"
s, nl = load(p); L = s.split(nl)
i = find_one(L, lambda l: "**다음 개념:**" in l and "추후 작성 예정" in l, "다음 개념: 추후 작성 예정", p)
L[i] = "* $\\rightarrow$ **다음 개념:** [1.3 데이터 분석의 과정](03-analysis-process.qmd)"
plans[p] = (s, nl.join(L))

# 2) 1.1: 다음 개념 링크 문구를 바뀐 1.2 제목으로
p = D + "01-big-data.qmd"
s, nl = load(p); L = s.split(nl)
i = find_one(L, lambda l: "**다음 개념:**" in l and "(02-applications.qmd)" in l, "다음 개념: 1.2 링크", p)
L[i] = "* $\\rightarrow$ **다음 개념:** [1.2 데이터 사이언스의 응용 분야](02-applications.qmd)"
plans[p] = (s, nl.join(L))

# 3) 1장 소개: '이 장의 흐름' 목록과 그 아래 문단
p = D + "index.qmd"
s, nl = load(p); L = s.split(nl)
if "(03-analysis-process.qmd)" in s:
    sys.exit(f"[중단] {p}: 이미 1.3 링크가 들어 있습니다. 아무 파일도 바꾸지 않았습니다.")
i = find_one(L, lambda l: l.startswith("- [1.2 ") and "(02-applications.qmd)" in l, "이 장의 흐름의 1.2 항목", p)
j = find_one(L, lambda l: l.startswith('여기까지가 "데이터 사이언스란 무엇인가"에 대한 정성적인 이야기입니다.'), "'여기까지가 …' 문단", p)
L[j] = ('1.1과 1.2가 "데이터 사이언스란 무엇인가"에 대한 이야기라면, 1.3과 1.4는 "데이터 사이언티스트는 문제에 어떻게 접근하는가"에 대한 이야기입니다. '
        '이 장은 전체적으로 수식보다 생각하는 방식에 초점을 맞춘 정성적인 내용이고, 다음 장부터 각 단계에서 쓰는 기술적이고 수학적인 도구들을 본격적으로 다루겠습니다.')
L[i] = "- [1.2 데이터 사이언스의 응용 분야](02-applications.qmd): 금융, 공공정책과 정치, 의학과 생활과학에서 데이터 사이언스가 어떻게 쓰이는지, 그리고 데이터 사이언티스트에게 어떤 소양이 필요한지 이야기합니다."
L[i+1:i+1] = [
    "- [1.3 데이터 분석의 과정](03-analysis-process.qmd): 데이터 사이언스의 세 갈래를 구분하고, 질문 설정부터 커뮤니케이션까지 데이터 분석이 어떤 단계를 거쳐 진행되는지 살펴봅니다.",
    "- [1.4 데이터의 출처와 편향](04-sampling-bias.qmd): 모집단과 표본, i.i.d. 가정을 소개하고, 데이터가 한쪽으로 치우쳤을 때 어떤 일이 벌어지는지 실제 사례와 시뮬레이션으로 확인합니다.",
]
plans[p] = (s, nl.join(L))

# 모든 확인이 끝난 뒤에만 씁니다.
for p, (old, new) in plans.items():
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print(f"[완료] {p}")
EOF
