import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import shutil

# Konfiguration
BASE_URL = "https://www.saucrew.de/"
OUTPUT_DIR = "public"
ASSETS_DIR = "assets"

# Sets um bereits besuchte URLs und heruntergeladene Assets zu tracken
visited_pages = set()
downloaded_assets = set()

def make_local_path(url, base_url=BASE_URL):
    """Erstellt einen lokalen Pfad basierend auf der URL."""
    parsed = urlparse(url)
    path = parsed.path
    if path.endswith("/") or not path:
        path += "index.html"
    elif not path.endswith(".html") and "." not in path.split("/")[-1]:
         path += "/index.html"
    
    # Entferne führenden Slash
    if path.startswith("/"):
        path = path[1:]
        
    return path

def download_file(url, local_path):
    """Lädt eine Datei herunter."""
    if os.path.exists(local_path):
        return True # Bereits da
        
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {url} -> {local_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def process_page(url):
    """Verarbeitet eine Seite: Lädt sie, parst Assets und Links."""
    if url in visited_pages:
        return
    visited_pages.add(url)
    
    print(f"Processing: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Assets herunterladen (CSS, JS, Images)
        for tag, attr in [('link', 'href'), ('script', 'src'), ('img', 'src'), ('source', 'srcset')]:
            for element in soup.find_all(tag):
                asset_url = element.get(attr)
                if not asset_url:
                    continue
                
                # Absolute URL erstellen
                full_asset_url = urljoin(url, asset_url)
                
                # Nur Assets von der gleichen Domain oder explizit erlaubten CDNs
                # Vereinfachung: Wir versuchen alles was relativ ist oder auf saucrew.de zeigt
                parsed_asset = urlparse(full_asset_url)
                if parsed_asset.netloc == "www.saucrew.de" or parsed_asset.netloc == "saucrew.de" or not parsed_asset.netloc:
                     # Lokaler Pfad für Asset
                    local_asset_path = os.path.join(OUTPUT_DIR, ASSETS_DIR, os.path.basename(parsed_asset.path))
                    # URL im HTML anpassen (Relativ zum Root)
                    # Wir speichern alles flach in assets/ für den Anfang, um Konflikte bei gleicher Benennung in Ordnern zu vermeiden?
                    # Besser: Ordnerstruktur beibehalten.
                    
                    relative_path = parsed_asset.path
                    if relative_path.startswith("/"):
                        relative_path = relative_path[1:]
                    
                    local_asset_path = os.path.join(OUTPUT_DIR, relative_path)
                    
                    if download_file(full_asset_url, local_asset_path):
                        # Link im HTML ersetzen
                        # Berechne relativen Pfad von der aktuellen HTML Datei zum Asset
                        current_page_path = make_local_path(url)
                        current_page_dir = os.path.dirname(os.path.join(OUTPUT_DIR, current_page_path))
                        
                        rel_path_to_asset = os.path.relpath(local_asset_path, current_page_dir)
                        # Windows Backslashes ersetzen
                        rel_path_to_asset = rel_path_to_asset.replace("\\", "/")
                        
                        element[attr] = rel_path_to_asset

        # 2. Links zu anderen Seiten finden und rekursiv verarbeiten
        for a in soup.find_all('a', href=True):
            link_url = a['href']
            full_link_url = urljoin(url, link_url)
            parsed_link = urlparse(full_link_url)
            
            # Nur interne Links verarbeiten
            if parsed_link.netloc in ["www.saucrew.de", "saucrew.de"]:
                # Rekursion
                # process_page(full_link_url) # Rekursion erst mal deaktiviert oder begrenzt
                # Wir sammeln erst alle Links und machen dann weiter, oder simple Rekursion
                
                # Link im HTML anpassen
                local_link_path = make_local_path(full_link_url)
                
                current_page_path = make_local_path(url)
                current_page_dir = os.path.dirname(os.path.join(OUTPUT_DIR, current_page_path))
                target_path = os.path.join(OUTPUT_DIR, local_link_path)
                
                rel_path_to_link = os.path.relpath(target_path, current_page_dir)
                rel_path_to_link = rel_path_to_link.replace("\\", "/")
                
                a['href'] = rel_path_to_link
                
                # Zur Warteschlange hinzufügen (für echtes crawling)
                # Hier vereinfacht: Rufe rekursiv auf
                if full_link_url not in visited_pages and "#" not in full_link_url: # Hash links ignorieren für fetch
                     # Einfache Rekursionsbremse oder Queue wäre besser, aber für kleine Seite okay
                     pass 

        # 3. HTML speichern
        local_path = make_local_path(url)
        full_local_path = os.path.join(OUTPUT_DIR, local_path)
        os.makedirs(os.path.dirname(full_local_path), exist_ok=True)
        
        with open(full_local_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
            
        # Nach dem Speichern Rekursion für gefundene Links?
        # Um Stack Overflow zu vermeiden und besser zu kontrollieren,
        # sollten wir eine Queue verwenden. Aber für den ersten Wurf:
        # Wir iterieren noch mal über die Links die wir gerade umgeschrieben haben? 
        # Nein, wir machen es richtig mit Queue.

    except Exception as e:
        print(f"Error processing {url}: {e}")

def crawl():
    queue = [BASE_URL]
    
    while queue:
        url = queue.pop(0)
        
        # Normalisieren: entfernen trailing slash für vergleich, aber behalten für request
        # url_clean = url.rstrip("/") # Vorsicht bei params
        
        if url in visited_pages:
            continue
            
        print(f"Crawling: {url}")
        
        # Seite laden und Links extrahieren (Logic von process_page hier rein oder aufsplitten)
        # Ich nutze eine angepasste process_page logik hier direkt
        
        visited_pages.add(url)
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Use the final URL after redirects to determine the file path
            final_url = response.url
            
            # If the final URL is different (redirect), we should use that for the path
            # to avoid overwriting index.html with a subpage content
            if final_url != url:
                print(f"Redirected: {url} -> {final_url}")
                
                # Check if we should create a local redirect file
                # URL -> Final URL
                # public/streams/index.html -> public/sea-of-thieves/streams/index.html
                
                local_original = make_local_path(url)
                local_final = make_local_path(final_url)
                
                # Only if paths are different (query params might not change path)
                if local_original != local_final:
                    full_original_path = os.path.join(OUTPUT_DIR, local_original)
                    full_final_path = os.path.join(OUTPUT_DIR, local_final)
                    
                    # Calculate relative path for redirect
                    # from dir of original to final file
                    orig_dir = os.path.dirname(full_original_path)
                    rel_target = os.path.relpath(full_final_path, orig_dir).replace("\\", "/")
                    
                    redirect_html = f"""<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="0; url={rel_target}">
</head>
<body>
<p>Redirecting to <a href="{rel_target}">{rel_target}</a>...</p>
</body>
</html>"""
                    
                    os.makedirs(os.path.dirname(full_original_path), exist_ok=True)
                    # Write redirect file if it's not index.html of root (safety check)
                    if local_original != "index.html":
                        with open(full_original_path, "w", encoding="utf-8") as f:
                            f.write(redirect_html)
                        print(f"Created redirect: {local_original} -> {local_final}")

                # Mark final URL as visited too
                if final_url in visited_pages:
                    continue
                visited_pages.add(final_url)
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # --- ASSETS ---
            for tag, attr in [('link', 'href'), ('script', 'src'), ('img', 'src'), ('source', 'srcset')]:
                for element in soup.find_all(tag):
                    asset_val = element.get(attr)
                    if not asset_val: continue
                    
                    full_asset_url = urljoin(final_url, asset_val)
                    parsed_asset = urlparse(full_asset_url)
                    
                    if parsed_asset.netloc in ["www.saucrew.de", "saucrew.de", ""]:
                        path = parsed_asset.path
                        if path.endswith("/") or "." not in os.path.basename(path):
                             continue 

                        relative_path = unquote(parsed_asset.path).lstrip("/")
                        local_asset_path = os.path.join(OUTPUT_DIR, relative_path)
                        
                        download_file(full_asset_url, local_asset_path)
                        
                        current_page_local = make_local_path(final_url)
                        current_page_dir = os.path.dirname(os.path.join(OUTPUT_DIR, current_page_local))
                        rel_path = os.path.relpath(local_asset_path, current_page_dir).replace("\\", "/")
                        element[attr] = rel_path

            # --- LINKS ---
            for a in soup.find_all('a', href=True):
                link_val = a['href']
                if link_val.startswith("#") or link_val.startswith("mailto:") or link_val.startswith("tel:"):
                    continue
                    
                full_link_url = urljoin(final_url, link_val)
                parsed_link = urlparse(full_link_url)
                
                if parsed_link.netloc in ["www.saucrew.de", "saucrew.de"]:
                    clean_link = full_link_url.split("#")[0]
                    # Don't queue if it has query params that might cause duplicate content issues
                    # unless we handle them. For now, strict static mapping.
                    if clean_link not in visited_pages and clean_link not in queue:
                        queue.append(clean_link)
                    
                    target_local = make_local_path(full_link_url)
                    current_page_local = make_local_path(final_url)
                    current_page_dir = os.path.dirname(os.path.join(OUTPUT_DIR, current_page_local))
                    
                    target_full_path = os.path.join(OUTPUT_DIR, target_local)
                    rel_link = os.path.relpath(target_full_path, current_page_dir).replace("\\", "/")
                    
                    if "#" in full_link_url:
                        rel_link += "#" + full_link_url.split("#")[1]
                        
                    a['href'] = rel_link

            # --- SPEICHERN ---
            # Use final_url for saving
            local_path = make_local_path(final_url)
            
            # Check if we are about to overwrite index.html with something that isn't the root
            if local_path == "index.html" and urlparse(final_url).path not in ["/", "", "/index.html"]:
                 print(f"SKIPPING OVERWRITE of index.html from {final_url}")
                 continue

            full_save_path = os.path.join(OUTPUT_DIR, local_path)
            os.makedirs(os.path.dirname(full_save_path), exist_ok=True)
            
            # Don't overwrite if it exists and we are not on the first pass?
            # Actually, we want to update it if we are re-running.
            # But we must ensure uniqueness.
            
            with open(full_save_path, "w", encoding="utf-8") as f:
                f.write(str(soup))
                
        except Exception as e:
            print(f"FAILED {url}: {e}")

if __name__ == "__main__":
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    crawl()
    print("Fertig!")
