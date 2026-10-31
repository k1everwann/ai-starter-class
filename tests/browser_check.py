from pathlib import Path
import os
import json, re
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'ai-starter-qa'
OUT.mkdir(exist_ok=True)
import base64
html=(ROOT/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="style.css">','<style>'+(ROOT/'style.css').read_text()+'</style>')
parts=[]
for name in ['content.js','starter.js','screens.js','app.js']:
    html=html.replace(f'<script src="{name}" defer></script>','')
    parts.append((ROOT/name).read_text().replace('</script','<\\/script'))
html=html.replace('</body>','<script>'+ '\n'.join(parts)+'</script></body>')
checks=[]
errors=[]
def ok(name,value=True):
    assert value, name
    checks.append(name)

def route(p,where):
    p.evaluate('(hash)=>location.hash=hash',where)
    p.wait_for_timeout(100)

def shot(p,name):
    p.locator('#toast').evaluate('(e)=>e.textContent=""')
    path=OUT/(name+'.png')
    p.screenshot(path=str(path),full_page=True)
    Image.open(path).convert('RGB').save(ROOT/'assets'/'screens'/(name+'.webp'),quality=83,method=6)

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None),args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1240,'height':900},accept_downloads=True)
    p=context.new_page()
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.set_content(html,wait_until='load')
    route(p,'home')
    ok('Home: four independent tasks',p.locator('.task-row').count()==4)
    ok('Course totals 90 minutes',p.evaluate('COURSE.lessons.reduce((n,l)=>n+l.minutes,0)+10')==90)
    for name in ['ask','learn','find','make']:
        for n in range(1,4):
            route(p,f'{name}/{n}')
            ok(f'{name}/{n}: visible heading',p.locator('h1').is_visible())
            ok(f'{name}/{n}: step navigation',p.locator('.steps a[aria-current=step]').count()==1)
            ok(f'{name}/{n}: no overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            if name=='ask' and n==2:
                p.locator('[data-action=assemble]').click()
                ok('Prompt: empty fields rejected',not p.locator('#assembled-wrap').is_visible())
                p.locator('[data-action=fill-example]').click()
                p.locator('[data-action=assemble]').click()
                ok('Prompt: combined output visible',p.locator('#assembled').is_visible())
                ok('Prompt: four composed lines',len(p.locator('#assembled').inner_text().splitlines())==4)
            if name=='learn' and n==2:
                p.locator('details > summary').first.click()
                p.locator('[data-action=hint]').click()
                ok('Practice: hint visible',p.locator('#hint').is_visible())
                for i,answer in enumerate([1,0,1]):
                    p.locator(f'input[name=practice-choice][value="{answer}"]').check()
                    p.locator('[data-action=answer-practice]').click()
                    ok(f'Practice: answer {i+1} correct',p.locator('#practice-feedback .feedback:not(.bad)').count()==1)
                    if i<2:p.locator('[data-action=next-practice]').click()
            if name=='find' and n==2:
                ok('Evidence: nine records',p.locator('.source').count()==9)
                p.locator('.source').nth(1).locator('summary').click()
            if name=='find' and n==3:
                p.locator('#meeting').select_option('rumor')
                p.locator('#source').select_option('E03')
                p.locator('[data-action=check-evidence]').click()
                ok('Evidence: rumor rejected',p.locator('#evidence-feedback .bad').count()==1)
                p.locator('#meeting').select_option('correct')
                p.locator('#source').select_option('E02')
                p.locator('[data-action=check-evidence]').click()
                ok('Evidence: formal update accepted',p.locator('#evidence-feedback .feedback:not(.bad)').count()==1)
            if name=='make' and n==2:
                p.locator('[data-action=starter]').click()
                ok('Sandbox: no same-origin privilege',p.locator('#preview').get_attribute('sandbox')=='allow-scripts')
                fr=p.frame_locator('#preview')
                ok('Game: unanswered next disabled',fr.locator('#next').is_disabled())
                fr.locator('#answers button').nth(0).click()
                for _ in range(3):fr.locator('#answers button').nth(0).evaluate('(b)=>b.click()')
                ok('Game: repeated clicks add one point',fr.locator('#score').inner_text().endswith('1'))
                ok('Game: answers lock',fr.locator('#answers button:disabled').count()==4)
                fr.locator('#next').click()
                fr.locator('#answers button').nth(0).click()
                ok('Game: wrong answer no score',fr.locator('#score').inner_text().endswith('1'))
                for ans in [1,3,0]:
                    fr.locator('#next').click()
                    fr.locator('#answers button').nth(ans).click()
                fr.locator('#next').click()
                ok('Game: final score 4/5',fr.locator('#word').inner_text().endswith('4 / 5'))
                fr.locator('#reset').click()
                ok('Game: reset score zero',fr.locator('#score').inner_text().endswith('0'))
                ok('Game: reset returns first question',fr.locator('#word').inner_text()=='discover')
            shot(p,f'{name}-{n}')
    route(p,'make/2')
    p.locator('#code-details summary').click()
    code=p.locator('#code').input_value()
    p.locator('#code').fill(code.replace('discover','discovery'))
    ok('Code change: stale preview hidden',not p.locator('#preview').is_visible())
    p.locator('[data-action=preview]').click()
    ok('Code change: fresh preview visible',p.locator('#preview').is_visible())
    route(p,'make/3')
    with p.expect_download() as dl:p.locator('[data-action=download-game]').click()
    d=dl.value;d.save_as(str(OUT/'my-word-game.html'))
    ok('Game: downloadable HTML',Path(d.path()).read_text().startswith('<!doctype html>'))
    p.locator('[data-save=test-a-0]').check()
    p.locator('[data-action=complete]').click()
    ok('Progress: self-reported state',p.locator('#side .after').inner_text().startswith('1 / 4'))
    route(p,'home');route(p,'make/3')
    ok('Progress: retained across tasks',p.locator('#side .after').inner_text().startswith('1 / 4'))
    ok('Checks: retained across tasks',p.locator('[data-save=test-a-0]').is_checked())
    route(p,'ask/2')
    p.locator('#ask-goal').fill('<img src=x onerror=alert(1)>')
    ok('Prompt edit invalidates combined text',not p.locator('#assembled-wrap').is_visible())
    p.locator('[data-action=assemble]').click()
    ok('User input rendered as text',p.locator('#assembled img').count()==0)
    ok('Escaped text preserved',p.locator('#assembled').inner_text().find('<img')>=0)
    route(p,'find/2')
    with p.expect_download() as dl:p.locator('[data-action=data]').click()
    contents=Path(dl.value.path()).read_text()
    ok('Evidence download: nine records',len(re.findall(r'\[[EDC]0[123]\]',contents))==9)
    with p.expect_download() as dl:p.locator('.top [data-action=export]').click()
    ok('Notes: download available',dl.value.suggested_filename=='my-ai-notes.txt')
    images=[]
    for name in ['ask','learn','find','make']:
        for n in range(1,4):
            images.append('data:image/webp;base64,'+base64.b64encode((ROOT/'assets'/'screens'/f'{name}-{n}.webp').read_bytes()).decode())
    p.evaluate('(images)=>SHOTS.forEach((s,i)=>s.src=images[i])',images)
    for name in ['ask','learn','find','make']:
        for n in range(1,4):
            route(p,f'{name}/{n}')
            p.locator('[data-action=picture]').click()
            p.locator('#picture-img').wait_for()
            p.wait_for_function('document.querySelector("#picture-img").complete && document.querySelector("#picture-img").naturalWidth>0')
            ok(f'Screenshot {name}/{n}: loads')
            p.keyboard.press('Escape')
            ok(f'Screenshot {name}/{n}: Escape closes',not p.locator('#picture').is_visible())
    for width in [390,360]:
        p.set_viewport_size({'width':width,'height':844})
        for where in ['home','ask/1','ask/2','learn/2','find/1','find/2','find/3','make/1','make/2','make/3','teacher','finish']:
            route(p,where)
            ok(f'Mobile {width} {where}: no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        route(p,'home');p.screenshot(path=str(OUT/f'home-{width}.png'),full_page=True)
    p.set_viewport_size({'width':1240,'height':900})
    route(p,'home');p.on('dialog',lambda d:d.accept())
    p.locator('footer [data-action=clear]').click()
    ok('Clear: resets task marks',p.locator('#side .after').inner_text().startswith('0 / 4'))
    p.locator('#toast').evaluate('(e)=>e.textContent=""')
    p.screenshot(path=str(ROOT.parent/'ai-starter-class-home.png'),full_page=True)
    route(p,'find/1');p.screenshot(path=str(ROOT.parent/'ai-starter-class-lesson.png'),full_page=True)
    ok('No uncaught JavaScript errors',not errors)
    browser.close()
(ROOT/'tests'/'results.json').write_text(json.dumps({'checks':checks,'count':len(checks),'errors':errors,'limits':['Loaded inline using set_content because local URL navigation is blocked by the managed browser.','Session storage refresh persistence and real external accounts are not verified.']},indent=2))
print(json.dumps({'passed':len(checks),'errors':errors}))
