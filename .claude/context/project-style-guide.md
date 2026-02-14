---
created: 2026-02-13T14:41:49Z
last_updated: 2026-02-13T14:41:49Z
version: 1.0
author: Claude Code PM System
---

# Project Style Guide

## Python Code Style

### General
- **Target:** Python 3.8+ (backward compatibility)
- **Line Length:** 100 characters max
- **Indent:** 4 spaces
- **Quotes:** Double quotes preferred
- **Linter:** Ruff (configured in `pyproject.toml`)

### Naming Conventions
- **Files:** `snake_case.py` (e.g., `keyword_analyzer.py`, `launch_checklist.py`)
- **Functions:** `snake_case()` (e.g., `analyze_keyword()`, `optimize_title()`)
- **Classes:** `PascalCase` (e.g., `KeywordAnalyzer`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `APPLE_TITLE_LIMIT`)
- **Variables:** `snake_case` (e.g., `search_volume`, `keyword_list`)

### Module Structure
Each Python module follows this pattern:
```python
# Standard library imports
import json
import urllib.request

# Module-level constants
APPLE_TITLE_LIMIT = 30
GOOGLE_TITLE_LIMIT = 50

# Core functions (public API)
def analyze_keyword():
    ...

def compare_keywords():
    ...

# Helper functions (internal)
def _calculate_score():
    ...

# Main block (for testing)
if __name__ == "__main__":
    ...
```

### Dependencies
- **Zero external dependencies** - Standard library only
- No pip install required
- All modules self-contained

## Markdown Style

### Agent Definitions
- YAML frontmatter with metadata
- Structured sections: Role, Protocol, Tools, Outputs
- Detailed step-by-step instructions

### Command Definitions
- YAML frontmatter with `description`, `user_invocable`
- Preflight checklist section
- Clear instructions with code blocks

### Documentation Files
- H1 title matching filename purpose
- Table of contents for files > 100 lines
- Code blocks with language identifiers
- Tables for structured data

### Output Files
- YAML frontmatter with creation date
- Character count validation displayed as `count/limit`
- Checkbox format for action items: `- [ ] Task description`
- Pass/fail indicators with emoji

## Git Conventions

### Commit Messages
- Format: `type: description`
- Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`
- Examples:
  - `feat: add complete ASO multi-agent system`
  - `fix: correct mermaid diagram syntax in CONTRIBUTING.md`
  - `docs: update README title for clarity`

### Branch Naming
- Feature: `feature/description`
- Fix: `fix/description`
- Docs: `docs/description`

## File Organization

### Agent Files
- Location: `.claude/agents/aso/`
- Naming: `aso-{role}.md`
- Size: 500-700 lines per agent

### Command Files
- Location: `.claude/commands/aso/`
- Naming: `aso-{action}.md`
- Include preflight checks and error handling

### Template Files
- Location: `.claude/templates/`
- Naming: `{type}-template.md`
- Include placeholder sections for agent-generated content

### Output Files
- Location: `outputs/[app-name]/`
- Numbered folders: `01-research/`, `02-metadata/`, etc.
- Action files: `action-{phase}.md` in each folder
- Entry point: `00-MASTER-ACTION-PLAN.md`

## Comment Style

- **Python:** Docstrings for public functions, inline comments for complex logic
- **Markdown:** Section headers serve as documentation
- **Shell Scripts:** Header comment block, inline comments for non-obvious logic
- Avoid over-commenting obvious code

## Character Limit Display Format

Always display character counts as:
```
Title: "FitFlow: Fitness Tracker"
Character Count: 25/30 ✅
```
Or for failures:
```
Title: "FitFlow: The Ultimate Fitness Tracker App"
Character Count: 42/30 ❌ (12 chars over limit)
```
