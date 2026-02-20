import os
import re

directory = r"c:\Users\patri\Desktop\Antigravity\saucrew_2.0_scrape\public"

updated_files_count = 0

print("Starting to convert root-absolute paths to local-relative paths...")

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            # Calculate depth relative to directory
            rel_dir = os.path.relpath(root, directory)
            if rel_dir == '.':
                prefix = './'
            else:
                depth = len(rel_dir.split(os.sep))
                prefix = '../' * depth
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Replace attributes like href="/", src="/", data-src="/", data-bg="/", poster="/", etc.
            def replacer_attr(match):
                attr = match.group(1)
                quote = match.group(2)
                path = match.group(3)
                
                if not path:
                    return match.group(0)
                
                # Check if it's a protocol relative URL (like //google.com)
                if path.startswith('//'):
                    return match.group(0) 
                
                path_no_slash = path.lstrip('/')
                if not path_no_slash:
                    path_no_slash = 'index.html'
                    
                new_path = prefix + path_no_slash
                return f'{attr}={quote}{new_path}{quote}'
            
            # Match href="/..." or src="/..." avoiding "//..."
            pattern_attr = re.compile(r'(href|src|data-src|data-bg|poster|icon)\s*=\s*(["\'])(/[^\"\'\s>]*)?\2', re.IGNORECASE)
            new_content, count = pattern_attr.subn(replacer_attr, content)
            
            # For srcset
            def replacer_srcset(match):
                quote = match.group(1)
                srcset_val = match.group(2)
                parts = srcset_val.split(',')
                new_parts = []
                for part in parts:
                    part_stripped = part.strip()
                    if part_stripped.startswith('/'):
                        if part_stripped.startswith('//'):
                            new_parts.append(part)
                            continue
                        subparts = part_stripped.split(' ', 1)
                        path = subparts[0]
                        path_no_slash = path.lstrip('/')
                        new_path = prefix + path_no_slash
                        if len(subparts) > 1:
                            new_parts.append(f"{new_path} {subparts[1]}")
                        else:
                            new_parts.append(new_path)
                    else:
                        new_parts.append(part)
                return f'srcset={quote}{", ".join(new_parts)}{quote}'
                
            pattern_srcset = re.compile(r'srcset\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)
            new_content, count_srcset = pattern_srcset.subn(replacer_srcset, new_content)
            
            # For css url(/...)
            def replacer_url(match):
                quote = match.group(1) or ''
                path = match.group(2)
                if path.startswith('//'):
                    return match.group(0)
                path_no_slash = path.lstrip('/')
                new_path = prefix + path_no_slash
                return f'url({quote}{new_path}{quote})'
                
            pattern_url = re.compile(r'url\(\s*(["\']?)(/[^/\'"]+.*?)\1\s*\)', re.IGNORECASE)
            new_content, count_url = pattern_url.subn(replacer_url, new_content)
            
            # One issue: WordPress JSON data embedded in page with escaped slashes might point to `\/wp-content\...`
            # But the user is mostly concerned with html attributes and css url().
            # Let's write the file if any changes were made.
            
            if count > 0 or count_srcset > 0 or count_url > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files_count += 1

print(f"Updated {updated_files_count} files with relative local links.")
