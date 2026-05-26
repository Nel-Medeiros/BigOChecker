# BigO Checker — TODO

## In Progress
_Nothing currently in progress._

## Planned

### Features
- [x] **Add syntax highlighting to the code editor** — CodeMirror 6 with Catppuccin Mocha theme and Python language support
- [x] **Python indentation in the textarea** — Tab → 4 spaces and Enter auto-indent handled natively by CodeMirror
- [ ] **LLM-based analysis** — pivot from static AST analysis to Claude API for richer, more accurate explanations and support for complex algorithm patterns
- [ ] **Support `async def` functions** — the current AST visitor only handles `def`; async functions are silently ignored
- [ ] **Support class methods** — detect and analyze methods inside class definitions, not just top-level functions
- [ ] **Support lambda and nested functions** — currently out of scope; nested `def` inside a function body is skipped
- [ ] **Detect `list()` / `dict()` / `set()` constructor calls for space complexity** — only comprehensions are currently detected; explicit constructor calls are missed
- [ ] **More complexity patterns** — O(n!) permutation recursion, O(log n) divide-and-conquer recursion, mixed loop + sort → O(n² log n)

### UX
- [ ] **Copy result to clipboard** — add a copy button to each result card
- [ ] **Share link** — encode the source in the URL so results can be shared
- [ ] **Dark/light theme toggle**
- [ ] **Keyboard shortcut** — Ctrl+Enter to trigger analysis

### Infrastructure
- [ ] **Mobile layout** — the current UI is desktop-only
- [ ] **User accounts + history** — save past analyses (requires auth + database)
- [ ] **Deploy to a public host** (e.g. Railway, Fly.io, Render)

## Completed
- [x] Project scaffolding (FastAPI + plain HTML/JS)
- [x] AST-based Big O analysis for Python `def` functions
- [x] Time complexity detection: O(1), O(log n), O(n), O(n log n), O(n²), O(n³), O(2^n)
- [x] Space complexity detection: O(1), O(n), O(n²)
- [x] Multi-function support — all top-level functions analyzed separately
- [x] FastAPI `/analyze` endpoint with Pydantic validation
- [x] Error handling: syntax errors (400), empty input (422), no functions (200 + info)
- [x] Catppuccin Mocha dark theme UI
- [x] XSS-safe DOM rendering
