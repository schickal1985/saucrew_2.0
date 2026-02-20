import os
import re

directory = r"c:\Users\patri\Desktop\Antigravity\saucrew_2.0_scrape\public"

updated_files_count = 0

print("Starting to un-lazyload images and backgrounds...")

def replacer_datasrc(match):
    el = match.group(0)
    data_src_match = re.search(r'data-src=(["\'])(.*?)\1', el)
    if not data_src_match:
        return el
    real_src = data_src_match.group(2)
    
    # Remove data-src
    el = el.replace(data_src_match.group(0), '')
    
    # Replace existing src="anything", or if none, add src=real_src
    src_match = re.search(r'src=(["\']).*?\1', el)
    if src_match:
        el = el.replace(src_match.group(0), f'src="{real_src}"')
    else:
        # append before the closing > (assuming format is <img ...>)
        # sometimes tags end with />
        if el.endswith("/>"):
            el = el[:-2] + f' src="{real_src}"/>'
        else:
            el = el[:-1] + f' src="{real_src}">'
        
    # Remove lazy classes to prevent css hiding it
    el = el.replace('lazyload', '')
    el = el.replace('lazyloaded', '')
    el = el.replace('lazy-hidden', '')
    return el

def replacer_databg(match):
    el = match.group(0)
    data_bg_match = re.search(r'data-bg=(["\'])(.*?)\1', el)
    if not data_bg_match:
        return el
    bg_url = data_bg_match.group(2)
    # Remove data-bg
    el = el.replace(data_bg_match.group(0), '')
    
    style_match = re.search(r'style=(["\'])(.*?)\1', el)
    if style_match:
        old_style = style_match.group(2)
        new_style = old_style.strip()
        if new_style and not new_style.endswith(';'):
            new_style += ';'
        new_style += f" background-image: url('{bg_url}');"
        el = el.replace(style_match.group(0), f'style="{new_style}"')
    else:
        if el.endswith("/>"):
            el = el[:-2] + f' style="background-image: url(\'{bg_url}\');"/>'
        else:
            el = el[:-1] + f' style="background-image: url(\'{bg_url}\');">'
        
    # Remove lazy classes
    el = el.replace('lazyload', '')
    el = el.replace('lazyloaded', '')
    el = el.replace('lazy-hidden', '')
    return el

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            new_content = re.sub(r'<(img|iframe)\s+[^>]*data-src=[^>]*>', replacer_datasrc, content, flags=re.IGNORECASE)
            new_content = re.sub(r'<[^>]+\sdata-bg=[^>]*>', replacer_databg, new_content, flags=re.IGNORECASE)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files_count += 1

print(f"Updated {updated_files_count} files to disable lazyloading.")
