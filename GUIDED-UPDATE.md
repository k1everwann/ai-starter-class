# Guided classroom edition

User request: make the independent classroom intuitive without a live guide.

## Applied changes
- A single start action and a concrete outcome preview instead of a menu-first landing page.
- First win: ask for a 30-minute study plan, then change one condition. No blank four-field prompt form.
- Each step states its action location and expected outcome.
- Copy / open tool / return instructions include paste shortcuts and persistent status.
- A clearly labelled, fixed three-stage visual demonstration of entering a question.
- Connector lesson starts with three readable fictional notices, not terminology.
- Pasting materials is explicitly distinguished from teacher-operated real app connections.
- Game lesson starts with a playable prepared example. Local HTML file selection/drag-drop replaces mandatory code pasting.
- Safe DOM title editing, immediate sandbox preview, learner modification recording and downloadable HTML.
- The testing step includes the learner's playable game on the same page.
- Specific next-action labels replace generic next-step buttons; completion remains self-reported.
- Keyboard access, source checks, permission boundaries, consent notes and export/clear controls retained.

## Verification
See tests/results.json and tests/standalone-results.json for actual execution results and limits.
The CI browser uses a real localhost origin to test reload persistence and clipboard, as well as guided actions and sandboxed game logic.
All twelve screenshots are regenerated from the updated page. They are this teaching site's screenshots, not official ChatGPT or Codex screenshots.
True external AI outputs, authenticated apps and student usability have not been tested.
The guided design addresses navigation issues; it is not a claim of validated learning outcomes.

## Scope
Only k1everwann/ai-starter-class is changed. The ai-life-lab repository is untouched.
