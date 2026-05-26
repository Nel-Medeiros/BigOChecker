# BigO Checker

A web app that analyzes Python algorithms for **time and space complexity** using static AST inspection. Paste your code, click Analyze, and get the Big O notation for every function — with a plain-English explanation.

## Features

- Analyzes all top-level `def` functions in one paste
- Detects time complexity: O(1), O(log n), O(n), O(n log n), O(n²), O(n³), O(2^n)
- Detects space complexity: O(1), O(n), O(n²)
- Natural language explanation for each result
- Syntax error reporting with line numbers
- No external APIs — pure Python `ast` module

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+ · FastAPI · Uvicorn |
| Analysis | Python `ast` module (static analysis) |
| Frontend | Plain HTML · CSS · JavaScript (no framework) |
| Tests | pytest · httpx |

## Getting Started

**1. Clone and install dependencies**

```bash
git clone https://github.com/Nel-Medeiros/BigOChecker.git
cd BigOChecker
pip install -r requirements.txt
```

**2. Run the server**

```bash
python -m uvicorn main:app --reload
```

**3. Open in browser**

```
http://127.0.0.1:8000
```

## Usage

Paste any Python algorithm into the textarea and click **Analyze →**.

```python
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def binary_search(arr, target):
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

Result:

| Function | Time | Space |
|---|---|---|
| `bubble_sort` | O(n²) | O(1) |
| `binary_search` | O(log n) | O(1) |

## API

`POST /analyze`

```json
// Request
{ "source": "<python source code>" }

// Response
[
  {
    "name": "bubble_sort",
    "time_complexity": "O(n²)",
    "space_complexity": "O(1)",
    "explanation": "Two nested loops each iterate over the input..."
  }
]
```

**Error responses:**
- `400` — syntax error in submitted code (includes message and line number)
- `422` — empty or blank source
- `500` — unexpected server error

## Running Tests

```bash
python -m pytest tests/ -v
```

43 tests covering the parser, AST visitor, analyzer orchestrator, and API endpoints.

## Project Structure

```
BigOChecker/
├── main.py              # FastAPI app + /analyze endpoint
├── analyzer/
│   ├── __init__.py      # analyze() orchestrator
│   ├── models.py        # FunctionResult Pydantic model
│   ├── parser.py        # ast.parse() wrapper
│   ├── patterns.py      # Explanation templates
│   └── visitor.py       # ComplexityVisitor (ast.NodeVisitor)
├── static/
│   └── index.html       # Single-page frontend
└── tests/
    ├── test_parser.py
    ├── test_visitor.py
    ├── test_analyzer.py
    └── test_api.py
```

## Known Limitations (MVP)

- Only analyzes top-level `def` functions (`async def`, class methods, and nested functions are not supported)
- Static analysis cannot detect complexity patterns that depend on runtime values
- Complex or unusual algorithm structures may produce inaccurate results

## Roadmap

See [TODO.md](TODO.md) for planned features.

## License

MIT
