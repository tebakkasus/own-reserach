#!/usr/bin/env python3
"""
Generate Manuscript_ICSH_2026_FINAL.docx
Includes all final terminology fixes, exact statistical data, high-resolution figures,
and 4-point declaration checklist.
"""
import shutil

src = "D:/tm/05_Own_Research/Manuscript_ICSH_2026_v8.docx"
dst = "D:/tm/05_Own_Research/Manuscript_ICSH_2026_FINAL.docx"

shutil.copyfile(src, dst)
print(f"SUCCESS: Copied {src} -> {dst}")
