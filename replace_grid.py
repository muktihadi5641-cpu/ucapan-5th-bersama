import re

html_path = r'c:\Claude\Project\ucapan-5th-bersama\index.html'
grid_path = r'c:\Claude\Project\ucapan-5th-bersama\grid_output.txt'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(grid_path, 'r', encoding='utf-8') as f:
    new_grid = f.read().replace('\r\n', '\n').replace('\r', '\n')

# Find the grid div using string search, more reliable
start_marker = '    <div class="grid">'
end_marker = '    </div>\n  </div>\n</section>'

start_idx = html.find(start_marker)
if start_idx < 0:
    print('Start marker not found!')
    # Try to find it
    idx = html.find('<div class="grid">')
    print('Simple search found at:', idx)
else:
    # Find the closing </div> of the grid
    # The grid is inside the memories section shell div
    # Look for the pattern: </div>\n  </div>\n</section> which closes grid + shell + section
    end_search_start = start_idx + len(start_marker)
    # Find "    </div>" that closes the grid
    # Count from the grid opening
    depth = 1
    pos = start_idx + len(start_marker)
    while depth > 0 and pos < len(html):
        open_tag = html.find('<div', pos)
        close_tag = html.find('</div>', pos)
        if close_tag < 0:
            break
        if open_tag >= 0 and open_tag < close_tag:
            depth += 1
            pos = open_tag + 4
        else:
            depth -= 1
            pos = close_tag + 6

    grid_end = pos  # position after the closing </div> of .grid
    
    print(f'Grid found: {start_idx} to {grid_end}')
    print('Grid content starts:', repr(html[start_idx:start_idx+60]))
    print('Grid content ends:', repr(html[grid_end-30:grid_end+30]))
    
    html_new = html[:start_idx] + new_grid + html[grid_end:]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_new)
    print('Done! Grid replaced successfully.')
    print('New file length:', len(html_new))
