from pathlib import Path
import base64, json, re

ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text(encoding='utf-8')
html=html.replace('<link rel="stylesheet" href="style.css">','<style>'+(ROOT/'style.css').read_text(encoding='utf-8')+'</style>')
parts=[]
for name in ['content.js','starter.js','screens.js','app.js']:
    html=html.replace(f'<script src="{name}" defer></script>','')
    text=(ROOT/name).read_text(encoding='utf-8')
    if name=='screens.js':
        shots=json.loads(text[len('window.SHOTS='):].strip().rstrip(';'))
        for shot in shots:
            source=ROOT/shot['src']
            shot['src']='data:image/webp;base64,'+base64.b64encode(source.read_bytes()).decode('ascii')
        text='window.SHOTS='+json.dumps(shots,ensure_ascii=False)+';'
    parts.append(re.sub('</script',r'<\\/script',text,flags=re.I))
html=html.replace('</body>','<script>'+'\n'.join(parts)+'</script></body>')
dest=ROOT.parent/'ai-starter-class-standalone.html'
dest.write_text(html,encoding='utf-8')
print(dest)
