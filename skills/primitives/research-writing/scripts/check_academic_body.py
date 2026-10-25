#!/usr/bin/env python3
"""Non-mutating Markdown check for implementation leaks in academic prose."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

BOUNDARY = re.compile(r"^#{1,6}\s*(?:References\b|Bibliography\b|參考文獻|參考書目|(?:附錄\s*\w*\s*)?技術附錄|Technical appendix\b|AI.assistance disclosure\b|AI\s*協助聲明|人工智慧協助聲明)",re.I)
PATTERNS = [
    ("workflow",re.compile(r"\b(?:Research[- ]OS|research-assistant|research-[1-6]-[a-z-]+|to-paper|canonical|workpackages?|executors?|handoffs?|receipts?|pytest|unittest|SHA-?256)\b|SKILL\.md|執行器|測試框架|工作包|操作日誌",re.I)),
    ("implementation",re.compile(r"\b(?:Python|JavaScript|statsmodels|pandas|numpy|JSON|YAML|CSV|HTML|GitHub|git|uv|extra-rows|Mkt-RF)\b",re.I)),
    ("code-identifier",re.compile(r"\b[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+\b|\.(?:fit|shift|dropna|read_csv|to_csv)\s*\(")),
    ("source-file",re.compile(r"\b[A-Za-z][\w.-]*\.(?:py|ps1|yaml|yml|json|csv|tsv|ipynb)\b",re.I)),
    ("reproducibility-metadata",re.compile(r"\b(?:random\s+)?seed\s*[:=]?\s*\d+|(?:隨機)?種子\s*[:：=]?\s*\d+",re.I)),
    ("filesystem-path",re.compile(r"[A-Za-z]:[\\/][^\s，。；]+|(?:\.research|\d{2}_[A-Za-z_]+)[\\/][^\s，。；]+|(?<![\w:])/(?:home|Users|tmp|workspace)/[^\s，。；]+")),
]

def check(text: str,allow_terms: tuple[str,...]=()) -> list[dict[str,object]]:
    allowed={x.casefold() for x in allow_terms};findings=[];heading="<preamble>";frontmatter=False;fence=False
    for number,line in enumerate(text.splitlines(),1):
        if number==1 and line.strip()=="---":frontmatter=True;continue
        if frontmatter:
            if line.strip()=="---":frontmatter=False
            continue
        if BOUNDARY.match(line):break
        if line.startswith('#'):heading=line.lstrip('#').strip()
        if re.match(r"\s*(```|~~~)",line):
            if not fence:findings.append({'line':number,'section':heading,'category':'code-block','match':line.strip()})
            fence=not fence;continue
        # URLs/image destinations are document structure, not visible academic prose.
        visible=re.sub(r"!?\[([^\]]*)\]\([^)]*\)",r"\1",line)
        visible=re.sub(r"(?<!\$)\$[^$\n]+\$|\\\(.*?\\\)","",visible)
        if '`' in visible:findings.append({'line':number,'section':heading,'category':'inline-code','match':visible.strip()})
        for category,pattern in PATTERNS:
            for match in pattern.finditer(visible):
                if match.group().casefold() not in allowed:
                    findings.append({'line':number,'section':heading,'category':category,'match':match.group()})
    return findings

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('manuscript',type=Path);parser.add_argument('--allow-term',action='append',default=[]);parser.add_argument('--output',type=Path)
    args=parser.parse_args();findings=check(args.manuscript.read_text(encoding='utf-8-sig'),tuple(args.allow_term))
    result={'file':str(args.manuscript),'scope':'academic body only','findings':findings,'status':'needs-review' if findings else 'no-detected-leaks','limits':'Not a style/validity certificate; inspect methods and rendered prose manually.'}
    encoded=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:args.output.write_text(encoded,encoding='utf-8')
    print(encoded);return 1 if findings else 0

if __name__=='__main__':raise SystemExit(main())
