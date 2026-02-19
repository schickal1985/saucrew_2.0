import os
from bs4 import BeautifulSoup
import re

directory = '2.1/public'
processed_count = 0
modified_count = 0

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Using BeautifulSoup to parse and modify the HTML
                soup = BeautifulSoup(content, 'html.parser')
                
                # The comment form is usually within a div with id "respond" or class "comment-respond"
                respond_div = soup.find('div', id='respond')
                changed = False
                if respond_div:
                    respond_div.decompose()
                    changed = True
                
                # Just in case, also look for the form itself if the wrapper wasn't found
                form_element = soup.find('form', id='commentform')
                if form_element:
                    form_element.decompose()
                    changed = True
                    
                # Also remove the "Schreibe einen Kommentar" heading if it's outside the respond div
                reply_title = soup.find(id='reply-title')
                if reply_title:
                   reply_title.decompose()
                   changed = True

                if changed:
                    # Write back to file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                    modified_count += 1
                
                processed_count += 1
                    
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print(f"Processed {processed_count} HTML files.")
print(f"Removed comment forms from {modified_count} files.")
