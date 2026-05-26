# Syntax Highlighting Implementation Design

## Goal

Replace the plain `<textarea>` in `static/index.html` with a CodeMirror 6 editor that highlights Python syntax in real time, using the existing Catppuccin Mocha color scheme.

## Architecture

Only `static/index.html` changes — no backend modifications required. The `<textarea>` is replaced by a `<div id="editor">` that CodeMirror mounts into. CodeMirror 6 and its dependencies are loaded as ES modules from `esm.sh` (a CDN that bundles npm packages as ESM — one `<script type="module">` tag, no build step). The existing `/analyze` fetch logic is updated to read from `editor.state.doc.toString()` instead of `textarea.value`. The button enable/disable logic is updated to listen for CodeMirror `EditorView.updateListener` instead of the `input` event.

## CDN Strategy

All CodeMirror packages are imported via `esm.sh` in a single `<script type="module">`:

```js
import { EditorState } from 'https://esm.sh/@codemirror/state@6'
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, bracketMatching, placeholder } from 'https://esm.sh/@codemirror/view@6'
import { defaultKeymap, indentWithTab } from 'https://esm.sh/@codemirror/commands@6'
import { python } from 'https://esm.sh/@codemirror/lang-python@6'
import { indentOnInput } from 'https://esm.sh/@codemirror/language@6'
```

Total CDN weight: ~200KB (gzipped). Acceptable for this use case.

## Editor Features

- **Python syntax highlighting** — `@codemirror/lang-python`
- **Line numbers** — `lineNumbers()` extension
- **Active line highlight** — `highlightActiveLine()` + `highlightActiveLineGutter()`
- **Bracket matching** — `bracketMatching()`
- **Tab → 4 spaces** — `indentWithTab` keymap (4-space indent width)
- **Enter auto-indent** — `indentOnInput()` matches Python indentation level
- **Ctrl+Enter to analyze** — custom keymap entry dispatched to the analyze button click handler

## Catppuccin Mocha Theme

A custom `EditorView.theme()` defined inline in the JS block. Key mappings:

| Element | Color |
|---|---|
| Editor background | `#181825` |
| Cursor | `#89b4fa` |
| Selection | `#313244` |
| Gutter background | `#1e1e2e` |
| Gutter border | `#313244` |
| Line number text | `#585b70` |
| Active line number | `#a6adc8` |
| Active line background | `#1e1e2e` |

Python token colors:

| Token | Color | Example |
|---|---|---|
| Keywords (`def`, `for`, `if`, `return`, `in`) | `#cba6f7` (mauve) |
| Function names | `#89b4fa` (blue) |
| Built-ins (`range`, `len`, `print`) | `#89b4fa` (blue) |
| Numbers | `#fab387` (peach) |
| Strings | `#a6e3a1` (green) |
| Operators | `#89dceb` (sky) |
| Comments | `#585b70` (muted) |
| Default text | `#cdd6f4` (text) |

## HTML Changes

**Remove:** `<textarea id="code" ...></textarea>`

**Add:** `<div id="editor"></div>` in the same location, with matching height and border-radius via CSS.

**Update hint text:** append `· Ctrl+Enter to analyze`

## JS Changes

1. Remove the `textarea` `input` event listener.
2. Initialize `EditorView` with all extensions and mount to `#editor`.
3. Add `EditorView.updateListener` to enable/disable the analyze button when the document is empty.
4. Replace `textarea.value` with `editor.state.doc.toString()` in the fetch call.
5. After analysis completes, do not clear the editor (keep existing behavior — textarea was never cleared after analysis).
6. Add `placeholder()` extension from `@codemirror/view` with the same `bubble_sort` example text the textarea used. The placeholder is shown only when the editor is empty and does not pre-fill any content.

## TODO Impact

This feature completes two TODO items:
- **Syntax highlighting in the code editor** (top priority)
- **Python indentation in the textarea** — Tab/Enter behavior handled natively by CodeMirror

## Testing

No new backend tests needed. Manual testing checklist:
- Python keywords, strings, numbers, comments render in correct Catppuccin colors
- Line numbers appear and scroll in sync with code
- Tab inserts 4 spaces
- Enter on an indented line auto-indents to the same level
- Ctrl+Enter triggers analysis
- Analyze button is disabled when editor is empty, enabled when it has content
- Existing analysis flow (results cards, error banners) works unchanged
- The placeholder example (`bubble_sort`) is shown on initial load
