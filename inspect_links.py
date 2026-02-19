from bs4 import BeautifulSoup
import os

with open("public/index.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

links = soup.find_all("a")
for link in links:
    href = link.get("href")
    text = link.get_text(strip=True)
    if href and ("shop" in href.lower() or "mediathek" in href.lower() or "wiki" in href.lower() or "enzyklopädie" in href.lower() or "shop" in text.lower() or "mediathek" in text.lower()):
        print(f"Text: '{text}' -> Href: '{href}'")
