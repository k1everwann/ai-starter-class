from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
handler = partial(SimpleHTTPRequestHandler, directory=str(root))
server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_port}/play/"
evidence = Path(__file__).resolve().parent / "pocket-screens"
evidence.mkdir(exist_ok=True)
checks = []

def check(label, value):
    assert value, label
    checks.append(label)

try:
    with sync_playwright() as w:
        browser = w.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        response = page.goto(url, wait_until="load")
        check("HTTP 200", response.status == 200)
        check("Page title", "AI 口袋任務" in page.title())
        check("Five distinct topics", page.locator(".card").count() == 5)
        check("Two offline mini activities", page.locator(".mini").count() == 2)
        page.screenshot(path=str(evidence / "desktop.png"), full_page=True)
        page.locator(".card").first.click()
        check("Card opens three-step activity", page.locator(".step").count() == 3)
        check("Accessible prompt in first task", "HTML" in page.locator("#prompt").inner_text())
        page.locator("#topic").fill("海洋")
        check("Learner topic changes prompt", "海洋" in page.locator("#prompt").inner_text())
        check("Linked tool is Codex", "codex" in page.locator("#openTool").get_attribute("href"))
        page.locator("#doneButton").click()
        check("Progress marked locally", "已經玩過" in page.locator(".card").first.inner_text())
        page.reload(wait_until="load")
        check("Progress survives reload", "已經玩過" in page.locator(".card").first.inner_text())
        page.locator("#guess").fill("21")
        page.locator("#guessButton").click()
        check("Guessing game rejects out-of-range", "1 到 20" in page.locator("#guessMessage").inner_text())
        page.locator("#restartGame").click()
        check("Guessing game restarts", "5 次" in page.locator("#guessMessage").inner_text())
        page.locator("[data-answer='official']").click()
        check("Source check gives feedback", "正式更新" in page.locator("#sourceFeedback").inner_text())
        page.locator("#resetProgress").click()
        check("Progress can be cleared", "已經玩過" not in page.locator(".card").first.inner_text())
        check("No uncaught script errors", not errors)
        phone = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        m = phone.new_page()
        m.goto(url, wait_until="load")
        m.screenshot(path=str(evidence / "mobile.png"), full_page=True)
        check("Mobile has no horizontal overflow", m.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"))
        m.locator(".card").nth(3).click()
        check("Mobile task accessible", "規劃自己的時間" in m.locator("#task-title").inner_text())
        check("Mobile task has no horizontal overflow", m.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"))
        phone.close()
        ctx.close()
        browser.close()
finally:
    server.shutdown()
print(f"{len(checks)} pocket-hub checks passed:")
print("\n".join("OK: " + x for x in checks))
