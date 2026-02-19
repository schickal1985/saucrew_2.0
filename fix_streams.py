import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

FILE_PATH = "public/sea-of-thieves/streams/index.html"
BASE_URL = "https://www.saucrew.de/sea-of-thieves/streams"
OUTPUT_DIR = "public"
ASSETS_DIR = "assets"

def make_local_asset_path(url):
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith("/"):
        path = path[1:]
    return os.path.join(OUTPUT_DIR, ASSETS_DIR, os.path.basename(path))

def download_file(url, local_path):
    if os.path.exists(local_path):
        return True
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        print(f"Downloading {url} to {local_path}")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

with open(FILE_PATH, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1. Fix protocol relative URLs
for tag in soup.find_all(True):
    for attr in ["src", "href"]:
        if tag.has_attr(attr):
            val = tag[attr]
            if val.startswith("//"):
                tag[attr] = "https:" + val
                print(f"Fixed protocol relative URL: {val} -> {tag[attr]}")

# 2. Fix Navbar Link "Twitch"
for a in soup.find_all("a"):
    href = a.get("href")
    text = a.get_text(strip=True)
    if href == "https://www.saucrew.de/streams" and "Twitch" in text:
        a["href"] = "../../streams/index.html"
        print("Fixed Navbar Twitch link")

# 3. Handle Lazy Loaded Images (data-src)
for img in soup.find_all("img"):
    data_src = img.get("data-src")
    if data_src:
        # Check if it's the stream image
        parent = img.find_parent("a")
        if parent and "twitch.tv" in parent.get("href", ""):
             # Download image
             full_url = urljoin(BASE_URL, data_src)
             if full_url.startswith("//"):
                 full_url = "https:" + full_url
             
             local_file_path = make_local_asset_path(full_url)
             if download_file(full_url, local_file_path):
                 # Update src to point to local file
                 # rel path from public/sea-of-thieves/streams/index.html to public/assets/...
                 # ../../../assets/...
                 rel_path = "../../../" + ASSETS_DIR + "/" + os.path.basename(local_file_path)
                 img["src"] = rel_path
                 img["data-src"] = rel_path # Update data-src too just in case
                 # Remove lazyload class to force load? Or keep it specific
                 classes = img.get("class", [])
                 if "lazyload" in classes:
                     classes.remove("lazyload")
                     img["class"] = classes
                 print(f"Fixed Twitch image: {full_url}")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Done fixing streams page.")
