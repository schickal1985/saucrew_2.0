import os
import re

directory = r"c:\Users\patri\Desktop\Antigravity\saucrew_2.0_scrape\public"

# Matches href="..." or src="..." containing saucrew.de
pattern = re.compile(r'(?:href|src)=["\'](https?://(?:www\.)?saucrew\.de[^"\']*)["\']', re.IGNORECASE)

found_links = set()

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = pattern.findall(content)
                if matches:
                    for match in matches:
                        found_links.add(match)

output_file = r"c:\Users\patri\Desktop\Antigravity\saucrew_2.0_scrape\remaining_saucrew_links.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Total unique absolute links found: {len(found_links)}\n\n")
    for link in sorted(found_links):
        f.write(link + "\n")

print(f"Successfully wrote {len(found_links)} links to {output_file}")
