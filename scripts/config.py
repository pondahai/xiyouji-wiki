# -*- coding: utf-8 -*-
"""全書設定:換一本書時,只需要改這個檔 + characters.py。

章回標題格式假設為「第○○回 上聯 下聯」(中文數字,空白分隔);
若新書格式不同,調整 HEADING regex 即可。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── 書 ──────────────────────────────────────────────
BOOK_TITLE = "西遊記"           # 用於 prompt 與網頁標題
N_CHAPTERS = 100                # 全書回數(解析後檢查用)
RAW = ROOT / "data" / "xiyouji_raw.txt"   # 原文純文字
EDITION_NOTE = "好讀書櫃典藏版(世德堂百回本),全 100 回。"  # 首頁副標

# 章回標題:第(中文數字)回 上聯 下聯
HEADING = re.compile(r"^第([一二三四五六七八九十百]+)回\s+(\S+)\s+(\S+)\s*$")

# ── 路徑 ────────────────────────────────────────────
VAULT = ROOT / "vault"
SITE = ROOT / "site"
FACTS = ROOT / "data" / "facts"

# ── LLM 端點(OpenAI 相容)──────────────────────────
API = "http://100.89.149.50:8002/v1/chat/completions"
MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"
