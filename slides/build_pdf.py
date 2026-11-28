"""Xuất slides/demo-slides.html thành demo-slides.pdf ở thư mục gốc repo.

Chạy: python slides/build_pdf.py
Cần: pip install playwright && python -m playwright install chromium
"""
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "slides" / "demo-slides.html"
OUT = ROOT / "demo-slides.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(SRC.as_uri())
    page.pdf(path=str(OUT), prefer_css_page_size=True, print_background=True)
    browser.close()
print("Đã xuất", OUT)
