from scrape import process_page, BASE_URL, OUTPUT_DIR, ASSETS_DIR, make_local_path, visited_pages
import os

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Test the streams URL which is known to redirect
target_url = "https://www.saucrew.de/streams"

print(f"Manual processing of {target_url}...")
process_page(target_url)

# Check if redirect file exists
local_path = make_local_path(target_url)
full_path = os.path.join(OUTPUT_DIR, local_path)

if os.path.exists(full_path):
    print(f"SUCCESS: Redirect file created at {full_path}")
    with open(full_path, "r") as f:
        print("--- Content ---")
        print(f.read())
        print("---------------")
else:
    print(f"FAILURE: No file at {full_path}")
