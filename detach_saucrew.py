import os
import re
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

directory = r"c:\Users\patri\Desktop\Antigravity\saucrew_2.0_scrape\public"

# Matches href="..." or src="..." containing saucrew.de
pattern = re.compile(r'(href|src)=["\'](https?://(?:www\.)?saucrew\.de([^"\']*)?)["\']', re.IGNORECASE)

# File extensions to download
asset_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.pdf', '.zip', '.mp4', '.mp3', '.ttf', '.woff', '.woff2', '.eot')

downloaded_count = 0
updated_files_count = 0

print("Starting detachment process...")

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            matches = pattern.findall(content)
            
            if matches:
                new_content = content
                updated = False
                for match in matches:
                    attr_name = match[0] # href or src
                    full_url = match[1]  # https://saucrew.de/path/to/file.jpg
                    url_path = match[2]  # /path/to/file.jpg
                    
                    if not url_path:
                        url_path = '/'
                    
                    # Parse URL to get clean path without query params for file saving
                    parsed_url = urlparse(full_url)
                    clean_path = parsed_url.path
                    
                    is_asset = clean_path.lower().endswith(asset_extensions)
                    
                    if is_asset:
                        # Construct local file path
                        # Removing leading slash to join correctly with the public directory
                        local_relative_path = clean_path.lstrip('/')
                        local_file_path = os.path.join(directory, os.path.normpath(local_relative_path))
                        local_dir = os.path.dirname(local_file_path)
                        
                        # Create directories if they don't exist
                        if not os.path.exists(local_dir):
                            os.makedirs(local_dir, exist_ok=True)
                            
                        # Download if it doesn't exist
                        if not os.path.exists(local_file_path):
                            print(f"Downloading: {full_url}")
                            try:
                                # Adding user agent to prevent 403 Forbidden errors sometimes
                                req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
                                with urllib.request.urlopen(req) as response, open(local_file_path, 'wb') as out_file:
                                    out_file.write(response.read())
                                downloaded_count += 1
                                print(f"  -> Saved to: {local_file_path}")
                            except HTTPError as e:
                                print(f"  -> Error downloading {full_url}: HTTP {e.code}")
                            except URLError as e:
                                print(f"  -> Error downloading {full_url}: {e.reason}")
                            except Exception as e:
                                print(f"  -> Unexpected error downloading {full_url}: {e}")
                    
                    # Replace the URL in the HTML
                    # Use the URL path (including query params if any) as the new local link
                    # e.g., /wp-content/uploads/file.png or /sea-of-thieves
                    replacement = f'{attr_name}="{url_path}"'
                    
                    # Escape the original match for regex replacement to avoid regex issues
                    original_string = f'{attr_name}="{full_url}"'
                    # Also try with single quotes just in case
                    original_string_sq = f"{attr_name}='{full_url}'"
                    
                    if original_string in new_content:
                        new_content = new_content.replace(original_string, replacement)
                        updated = True
                    elif original_string_sq in new_content:
                        new_content = new_content.replace(original_string_sq, replacement)
                        updated = True

                if updated:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_files_count += 1

print("\n--- Summary ---")
print(f"Files updated: {updated_files_count}")
print(f"New assets downloaded: {downloaded_count}")
print("Detachment complete!")
