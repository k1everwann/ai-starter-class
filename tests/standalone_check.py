from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ok(name,value=True):
    assert value,name
    checks.append(name)
errors=[]
html=(ROOT.parent/'ai-starter-class-standalone.html').read_text()
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE','/usr/bin/chromium'),args=['--no-sandbox'])
    p=browser.new_page(viewport={'width':390,'height':844},accept_downloads=True)
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.set_content(html,wait_until='load')
    ok('Standalone: no external script tags',p.locator('script[src]').count()==0)
    ok('Standalone: no external stylesheet',p.locator('link[rel=stylesheet]').count()==0)
    ok('Standalone: twelve embedded screenshots',p.evaluate('SHOTS.length===12 && SHOTS.every(s=>s.src.startsWith("data:image/webp;base64,"))'))
    ok('Standalone: home keeps four available tasks',p.locator('.task-row').count()==4)
    p.evaluate("location.hash='make/2'");p.wait_for_timeout(100)
    p.locator('[data-action=starter]').click()
    ok('Standalone: sandboxed game works',p.frame_locator('#preview').locator('#word').inner_text()=='discover')
    p.locator('[data-action=picture]').click()
    p.wait_for_function('document.querySelector("#picture-img").naturalWidth>0')
    ok('Standalone: embedded screenshot renders')
    p.keyboard.press('Escape')
    ok('Standalone: mobile has no overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    ok('Standalone: no JavaScript errors',not errors)
    p.evaluate("location.hash='home'");p.wait_for_timeout(100)
    p.screenshot(path=str(ROOT.parent/'ai-starter-class-mobile.png'),full_page=True)
    browser.close()
(ROOT/'tests'/'standalone-results.json').write_text(json.dumps({'checks':checks,'count':len(checks),'errors':errors},indent=2))
print(json.dumps({'passed':len(checks),'errors':errors}))
