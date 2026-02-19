import os
from bs4 import BeautifulSoup
import collections

directory = '2.1/public'
form_stats = collections.defaultdict(list)

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                forms = soup.find_all('form')
                for form in forms:
                    # ignore search forms
                    form_class = form.get('class', [])
                    if isinstance(form_class, list):
                        form_class = ' '.join(form_class)
                    form_id = form.get('id', '')
                    action = form.get('action', '')
                    
                    if 'search' in form_class.lower() or 'search' in form_id.lower() or 'search' in action.lower():
                        continue
                        
                    key = f"ID: {form_id}, Class: {form_class}, Action: {action}"
                    form_stats[key].append(filepath)
            except Exception as e:
                print(f"Error parsing {filepath}: {e}")

print("Form Analysis Results:")
if not form_stats:
    print("No non-search forms found.")
for key, files in dict(form_stats).items():
    print(f"\n{key}")
    print(f"Found in {len(files)} files. Examples: {files[:3]}")
    if len(files) > 3:
        print(f"... and {len(files) - 3} more.")
