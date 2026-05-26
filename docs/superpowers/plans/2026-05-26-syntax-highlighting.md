# Syntax Highlighting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the plain `<textarea>` in `static/index.html` with a CodeMirror 6 editor that highlights Python syntax in real time using the Catppuccin Mocha color scheme.

**Architecture:** Only `static/index.html` changes — no backend modifications. The textarea is removed and a `<div id="editor">` is mounted by CodeMirror 6, loaded via `esm.sh` CDN as a single `<script type="module">`. The existing analyze fetch logic is updated to read `editor.state.doc.toString()` instead of `textarea.value`.

**Tech Stack:** CodeMirror 6 (`@codemirror/state`, `@codemirror/view`, `@codemirror/commands`, `@codemirror/lang-python`, `@codemirror/language`, `@lezer/highlight`) via `esm.sh` CDN.

---

## File Map

- Modify: `static/index.html` — only file changed
  - CSS: replace `textarea` / `textarea:focus` rules with a minimal `#editor` rule
  - HTML: replace `<textarea id="code">` with `<div id="editor">`, update label `for` attr, update hint text
  - JS: replace `<script>` with `<script type="module">` containing CDN imports, Catppuccin theme, CodeMirror init, and all existing helper functions

---

### Task 1: Replace textarea with CodeMirror editor

**Files:**
- Modify: `static/index.html:78-94` (CSS), `static/index.html:263-264` (HTML), `static/index.html:268` (hint), `static/index.html:274-368` (script)

This is a single-file change. Do all four sub-changes and then verify in the browser before committing.

---

- [ ] **Step 1: Replace the `textarea` CSS rules**

In `static/index.html`, find and replace the `textarea` block (lines 78–94):

```css
    textarea {
      width: 100%;
      height: 220px;
      background: #181825;
      border: 1px solid #313244;
      border-radius: 8px;
      color: #cdd6f4;
      font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
      font-size: 0.88rem;
      padding: 16px;
      resize: vertical;
      outline: none;
      line-height: 1.6;
      transition: border-color 0.15s;
    }

    textarea:focus { border-color: #89b4fa; }
```

Replace with:

```css
    #editor {
      width: 100%;
    }
```

The border, background, height, font, focus ring, and all other visual properties are handled by the CodeMirror theme defined in the script. This rule only ensures the editor stretches to full container width.

---

- [ ] **Step 2: Replace the textarea HTML element and update the label**

Find (line 263–264):

```html
  <label class="field-label" for="code">Paste your Python algorithm</label>
  <textarea id="code" spellcheck="false" placeholder="def bubble_sort(arr):&#10;    for i in range(len(arr)):&#10;        for j in range(len(arr) - i - 1):&#10;            if arr[j] > arr[j + 1]:&#10;                arr[j], arr[j + 1] = arr[j + 1], arr[j]"></textarea>
```

Replace with:

```html
  <label class="field-label">Paste your Python algorithm</label>
  <div id="editor"></div>
```

Note: `for` is removed from the label because `<div>` is not a labelable element. CodeMirror generates its own accessible content div internally.

---

- [ ] **Step 3: Update the hint text**

Find (line 268):

```html
    <span class="hint">Python only · top-level def functions · async def not supported</span>
```

Replace with:

```html
    <span class="hint">Python only · top-level def functions · async def not supported · Ctrl+Enter to analyze</span>
```

---

- [ ] **Step 4: Replace the entire script block**

Find and replace the entire `<script>` block (lines 274–368) with the following `<script type="module">`. This block includes the CDN imports, Catppuccin theme, Catppuccin highlight style, CodeMirror initialization, and all existing helper functions (buildCard, buildBadge, showBanner) — ported to use the editor instance instead of the textarea.

```html
<script type="module">
  import { EditorState } from 'https://esm.sh/@codemirror/state@6'
  import { EditorView, keymap, lineNumbers, highlightActiveLine,
           highlightActiveLineGutter, bracketMatching,
           placeholder } from 'https://esm.sh/@codemirror/view@6'
  import { defaultKeymap, indentWithTab } from 'https://esm.sh/@codemirror/commands@6'
  import { python } from 'https://esm.sh/@codemirror/lang-python@6'
  import { indentOnInput, HighlightStyle,
           syntaxHighlighting } from 'https://esm.sh/@codemirror/language@6'
  import { tags } from 'https://esm.sh/@lezer/highlight@1'

  const catppuccinTheme = EditorView.theme({
    '&': {
      background: '#181825',
      color: '#cdd6f4',
      height: '220px',
      fontFamily: "'Cascadia Code', 'Fira Code', 'Consolas', monospace",
      fontSize: '0.88rem',
      borderRadius: '8px',
      border: '1px solid #313244',
    },
    '&.cm-focused': { border: '1px solid #89b4fa', outline: 'none' },
    '.cm-content': { padding: '16px', lineHeight: '1.6', caretColor: '#89b4fa' },
    '.cm-scroller': { overflow: 'auto', borderRadius: '8px' },
    '.cm-gutters': {
      background: '#1e1e2e',
      borderRight: '1px solid #313244',
      color: '#585b70',
      padding: '0 4px',
    },
    '.cm-activeLineGutter': { background: '#1e1e2e', color: '#a6adc8' },
    '.cm-activeLine': { background: 'rgba(49, 50, 68, 0.3)' },
    '.cm-selectionBackground': { background: '#313244 !important' },
    '&.cm-focused .cm-selectionBackground': { background: '#313244 !important' },
    '.cm-cursor': { borderLeftColor: '#89b4fa' },
    '.cm-placeholder': { color: '#585b70' },
  }, { dark: true })

  const catppuccinHighlight = HighlightStyle.define([
    { tag: tags.keyword,         color: '#cba6f7' },
    { tag: tags.definitionKeyword, color: '#cba6f7' },
    { tag: tags.controlKeyword,  color: '#cba6f7' },
    { tag: tags.moduleKeyword,   color: '#cba6f7' },
    { tag: [tags.function(tags.variableName), tags.function(tags.propertyName)], color: '#89b4fa' },
    { tag: tags.definition(tags.variableName), color: '#89b4fa' },
    { tag: tags.number,          color: '#fab387' },
    { tag: tags.string,          color: '#a6e3a1' },
    { tag: tags.comment,         color: '#585b70', fontStyle: 'italic' },
    { tag: tags.operator,        color: '#89dceb' },
    { tag: tags.punctuation,     color: '#cdd6f4' },
    { tag: tags.variableName,    color: '#cdd6f4' },
    { tag: [tags.bool, tags.null], color: '#fab387' },
  ])

  const btn = document.getElementById('analyze-btn')
  const results = document.getElementById('results')

  const editor = new EditorView({
    state: EditorState.create({
      doc: '',
      extensions: [
        lineNumbers(),
        highlightActiveLine(),
        highlightActiveLineGutter(),
        bracketMatching(),
        indentOnInput(),
        keymap.of([
          ...defaultKeymap,
          indentWithTab,
          { key: 'Ctrl-Enter', run: () => { if (!btn.disabled) btn.click(); return true } },
        ]),
        python(),
        syntaxHighlighting(catppuccinHighlight),
        placeholder('def bubble_sort(arr):\n    for i in range(len(arr)):\n        for j in range(len(arr) - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]'),
        catppuccinTheme,
        EditorView.updateListener.of(update => {
          if (update.docChanged) {
            btn.disabled = editor.state.doc.toString().trim() === ''
          }
        }),
      ],
    }),
    parent: document.getElementById('editor'),
  })

  btn.addEventListener('click', async () => {
    btn.disabled = true
    btn.textContent = 'Analyzing...'
    results.innerHTML = ''

    try {
      const resp = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: editor.state.doc.toString() }),
      })

      const data = await resp.json()

      if (!resp.ok) {
        if (resp.status === 400) {
          showBanner('error', `Syntax error on line ${data.detail.line}: ${data.detail.message}`)
        } else {
          showBanner('error', 'An unexpected error occurred. Please try again.')
        }
        return
      }

      if (data.length === 0) {
        showBanner('info', 'No function definitions found. Make sure your code contains at least one def (async def is not supported in this version).')
        return
      }

      const label = document.createElement('div')
      label.className = 'results-label'
      label.textContent = `Results — ${data.length} function${data.length !== 1 ? 's' : ''} found`
      results.appendChild(label)

      data.forEach(fn => results.appendChild(buildCard(fn)))

    } catch {
      showBanner('error', 'Could not reach the server. Is the backend running?')
    } finally {
      btn.disabled = editor.state.doc.toString().trim() === ''
      btn.textContent = 'Analyze →'
    }
  })

  function buildCard(fn) {
    const card = document.createElement('div')
    card.className = 'fn-card'

    const name = document.createElement('div')
    name.className = 'fn-name'
    name.textContent = `def ${fn.name}(...)`

    const badges = document.createElement('div')
    badges.className = 'badges'
    badges.appendChild(buildBadge('time', 'Time', fn.time_complexity))
    badges.appendChild(buildBadge('space', 'Space', fn.space_complexity))

    const explanation = document.createElement('div')
    explanation.className = 'explanation'
    explanation.textContent = fn.explanation

    card.appendChild(name)
    card.appendChild(badges)
    card.appendChild(explanation)
    return card
  }

  function buildBadge(type, label, value) {
    const badge = document.createElement('div')
    badge.className = `badge-complexity badge-${type}`

    const lbl = document.createElement('span')
    lbl.className = 'badge-label'
    lbl.textContent = label

    badge.appendChild(lbl)
    badge.appendChild(document.createTextNode(value))
    return badge
  }

  function showBanner(type, message) {
    const banner = document.createElement('div')
    banner.className = `banner banner-${type}`
    banner.textContent = message
    results.appendChild(banner)
  }
</script>
```

---

- [ ] **Step 5: Start the dev server and open the browser**

```bash
python -m uvicorn main:app --reload --port 8000
```

Open http://127.0.0.1:8000 and verify:

- [ ] Editor renders with dark background (`#181825`) and visible border
- [ ] Placeholder text (bubble_sort example) is visible in muted gray when empty
- [ ] Clicking the editor focuses it and border turns blue (`#89b4fa`)
- [ ] Line numbers appear in the left gutter
- [ ] Analyze button is disabled when editor is empty

---

- [ ] **Step 6: Verify syntax highlighting**

Type (or paste) the following into the editor:

```python
def binary_search(arr, target):
    # find the target
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

Expected colors:
- `def`, `while`, `if`, `elif`, `else`, `return` → mauve/purple (`#cba6f7`)
- `binary_search` (function name after `def`) → blue (`#89b4fa`)
- `len` → blue
- `0`, `1`, `2` → peach (`#fab387`)
- `# find the target` comment → muted gray (`#585b70`) italic
- `==`, `<`, `//` operators → sky (`#89dceb`)
- Line numbers visible, active line subtly highlighted

---

- [ ] **Step 7: Verify indentation and keyboard shortcuts**

- Press Tab on an indented line → 4 spaces inserted (not a tab character)
- Press Enter after `while low <= high:` → next line auto-indents to 8 spaces
- Type any code, then press Ctrl+Enter → analysis triggers (same as clicking Analyze →)

---

- [ ] **Step 8: Verify the full analysis flow**

Paste the bubble_sort + binary_search example and click Analyze →.

Expected: two result cards appear — `bubble_sort` O(n²) / O(1) and `binary_search` O(log n) / O(1).

Then paste invalid Python (e.g. `def foo(:`):

Expected: error banner with line number.

---

- [ ] **Step 9: Stop the server and commit**

Stop the server (`Ctrl+C`), then:

```bash
git add static/index.html
git commit -m "feat: replace textarea with CodeMirror 6 editor (Catppuccin theme, Python highlighting)"
```

---

### Task 2: Update TODO.md and open PR

**Files:**
- Modify: `TODO.md`

- [ ] **Step 1: Mark two items complete in TODO.md**

In `TODO.md`, move these two items from the Planned list to Completed:

Find under `### Features`:
```markdown
- [ ] **Add syntax highlighting to the code editor** — replace the plain `<textarea>` with a code editor component (e.g. CodeMirror or Monaco) that highlights Python syntax in real time
- [ ] **Python indentation in the textarea** — intercept Tab key to insert 4 spaces instead of moving focus; also handle Enter key to auto-indent to the current line's indentation level
```

Replace with:
```markdown
- [x] **Add syntax highlighting to the code editor** — CodeMirror 6 with Catppuccin Mocha theme and Python language support
- [x] **Python indentation in the textarea** — Tab → 4 spaces and Enter auto-indent handled natively by CodeMirror
```

- [ ] **Step 2: Commit TODO update**

```bash
git add TODO.md
git commit -m "chore: mark syntax highlighting and indentation as complete in TODO"
```

- [ ] **Step 3: Push the feature branch and open a PR**

```bash
git push -u origin feature/syntax-highlighting
gh pr create --title "feat: syntax highlighting with CodeMirror 6" --body "$(cat <<'EOF'
## Summary
- Replaces the plain `<textarea>` with a CodeMirror 6 editor loaded from CDN
- Python syntax highlighting using Catppuccin Mocha colors (keywords purple, functions blue, numbers peach, strings green, comments muted)
- Line numbers, active line highlight, bracket matching
- Tab → 4 spaces, Enter auto-indent, Ctrl+Enter to analyze
- Closes TODO items: syntax highlighting + Python indentation

## Test Plan
- [ ] Editor renders with correct Catppuccin Mocha theme (dark bg, blue border on focus)
- [ ] Python keywords, strings, numbers, comments render in correct colors
- [ ] Line numbers visible and scroll in sync
- [ ] Tab inserts 4 spaces; Enter auto-indents to current level
- [ ] Ctrl+Enter triggers analysis
- [ ] Analyze button disabled when editor is empty
- [ ] Full analysis flow works (result cards, error banners unchanged)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```
