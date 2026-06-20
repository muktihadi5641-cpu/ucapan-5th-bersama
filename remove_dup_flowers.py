"""
Remove duplicate flower <img> tags that are still inside section elements.
We keep: flower-layer div, intro flowers.
We remove: hero-dec-*, letter-dec-*, timeline-dec-*, cherish-dec-*, garden-dec-*, mem-dec-*, closing-dec-*
"""
import re

path = r"c:\Claude\Project\ucapan-5th-bersama\index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern: img tags that have class containing old dec- class names
pattern = r'\s*<img src="photos/bunga/[^"]+" class="floral-dec (?:hero-dec|letter-dec|timeline-dec|cherish-dec|garden-dec|mem-dec|closing-dec)[^"]*"[^>]*>\r?\n?'

removed = re.findall(pattern, content)
print(f"Found {len(removed)} duplicate img tags to remove:")
for r in removed:
    print(" ", r[:80])

new_content = re.sub(pattern, "", content)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("\nDone. Duplicate flower imgs removed from sections.")
