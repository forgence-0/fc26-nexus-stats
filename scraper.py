"""
scraper.py
----------
Nexus Mods sayfasındaki "Unique DLs / Total DLs / Total views"
değerlerini çekip stats.json dosyasına yazar.

Bu betik GitHub Actions tarafından periyodik olarak çalıştırılır
(.github/workflows/update-stats.yml dosyasına bak). Elle test etmek
istersen:

    pip install playwright
    playwright install --with-deps chromium
    python scraper.py
"""

import json
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

MOD_URL = "https://www.nexusmods.com/easportsfc26/mods/1021"
OUTPUT_FILE = "stats.json"
LABELS = ["Unique DLs", "Total DLs", "Total views"]


def fetch_stats(page) -> dict:
    page.goto(MOD_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(1500)  # JS ile dolan rakamlar için kısa bekleme

    text = page.inner_text("body")
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    def value_after(label: str):
        for i, line in enumerate(lines):
            if line == label and i + 1 < len(lines):
                return lines[i + 1]
        return None

    return {label: value_after(label) for label in LABELS}


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        )
        try:
            stats = fetch_stats(page)
        finally:
            browser.close()

    data = {
        "url": MOD_URL,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "unique_dls": stats.get("Unique DLs"),
        "total_dls": stats.get("Total DLs"),
        "total_views": stats.get("Total views"),
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
