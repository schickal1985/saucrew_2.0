import os

output_dir = "public"
streams_dir = os.path.join(output_dir, "streams")
target_dir = os.path.join(output_dir, "sea-of-thieves", "streams")

os.makedirs(streams_dir, exist_ok=True)
os.makedirs(target_dir, exist_ok=True)

# 1. Ensure target content exists (we assume main scraper or previous runs got it, or we create a placeholder/redownload)
# usage of simple redirect 
redirect_html = """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="0; url=../sea-of-thieves/streams/index.html">
</head>
<body>
<p>Redirecting to <a href="../sea-of-thieves/streams/index.html">../sea-of-thieves/streams/index.html</a>...</p>
</body>
</html>"""

redirect_file = os.path.join(streams_dir, "index.html")
with open(redirect_file, "w", encoding="utf-8") as f:
    f.write(redirect_html)

print(f"Force-created redirect at {redirect_file}")
