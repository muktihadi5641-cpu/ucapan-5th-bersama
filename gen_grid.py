import os, urllib.parse

folder = r'c:\Claude\Project\ucapan-5th-bersama\photos\adik'
files = sorted(os.listdir(folder))

words = ['love','you','us','always','smile','heart','forever','together','bloom','shine',
         'joy','grace','warm','sweet','dream','wish','hope','glow','rise','care',
         'trust','laugh','dance','song','star','moon','sun','sky','light','home',
         'soul','still','now','here','stay','hold','feel','know','live','give',
         'be','mine','yours','close','safe','calm','dear','soft','real','free',
         'true','yes','us']

lines = ['    <div class="grid">']
lines.append('      <!-- all 53 photos from photos/adik -->')
for i, f in enumerate(files):
    enc = urllib.parse.quote(f)
    delay = (i % 4) + 1
    label = words[i % len(words)]
    lines.append('      <figure class="tile reveal" data-delay="' + str(delay) + '">')
    lines.append('        <div class="photo"><img src="photos/adik/' + enc + '" alt="" onerror="this.remove()"></div>')
    lines.append('        <figcaption class="label">' + label + '</figcaption>')
    lines.append('      </figure>')
lines.append('    </div>')

output = '\n'.join(lines)

out_path = r'c:\Claude\Project\ucapan-5th-bersama\grid_output.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(output)

print('Done. Total photos:', len(files))
print('Output written to:', out_path)
