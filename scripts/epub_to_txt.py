# -*- coding: utf-8 -*-
"""好讀網 epub → data/*.txt(build_wiki 可解析的純文字)
每章 xhtml:<h3>回目標題</h3> + <br/><br/> 分段、段首全形空格。
輸出格式:回目標題獨立一行(半形空白分隔),每段一行、以全形空格開頭。
用法: python epub_to_txt.py <epub檔> [輸出txt,預設 config.RAW]
"""
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import RAW, HEADING

TAG = re.compile(r"<[^>]+>")
BR2 = re.compile(r"<br\s*/?>\s*<br\s*/?>", re.I)


def clean(s: str) -> str:
    s = TAG.sub("", s)
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return s.strip("﻿ \t\r\n")


def main():
    epub = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else RAW
    z = zipfile.ZipFile(epub)
    names = [n for n in z.namelist() if re.search(r"/(\d+)\.xhtml$", n)]
    names.sort(key=lambda n: int(re.search(r"(\d+)\.xhtml$", n).group(1)))

    out = []
    n_chapters = 0
    for name in names:
        xhtml = z.read(name).decode("utf-8")
        m = re.search(r"<body[^>]*>(.*)</body>", xhtml, re.S)
        if not m:
            continue
        # 回目標題可能在 <h3>,也可能(第一回)是書名頁後的一個純文字段落:
        # 逐段掃描,第一個符合章回格式的段落即標題,之前的門面文字丟棄
        heading = None
        paras = []
        for seg in BR2.split(m.group(1)):
            text = clean(seg)
            if not text:
                continue
            if heading is None:
                cand = text.replace("　", " ")
                if HEADING.match(cand):
                    heading = cand
                continue  # 標題前的書名/版本頁丟棄
            paras.append("　　" + text.lstrip("　"))
        if heading is None:  # 目錄頁(0.xhtml)等,略過
            print(f"skip {name}: 找不到章回標題")
            continue
        n_chapters += 1
        out.append(heading)
        out.extend(paras)
        out.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"{n_chapters} chapters, {sum(len(l) for l in out)} chars -> {out_path}")


if __name__ == "__main__":
    main()
