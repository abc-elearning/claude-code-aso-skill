---
created: 2026-02-13T14:41:49Z
last_updated: 2026-02-13T14:41:49Z
version: 1.0
author: Claude Code PM System
---

# Technology Context

## Primary Language

- **Python 3.8+** (backward compatible target)
- **Zero external dependencies** - Standard library only
- Configured via `pyproject.toml` with setuptools build backend

## AI Framework

- **Claude Code** - CLI tool for AI-powered development
- **Agent Models:**
  - Opus - For complex orchestration and research (aso-master, aso-research, aso-strategist)
  - Sonnet - For focused generation tasks (aso-optimizer)
- **Agent Definitions:** Markdown files in `.claude/agents/`
- **Slash Commands:** Markdown files in `.claude/commands/`

## Data Sources

### iTunes Search API (Primary)
- **Endpoint:** `https://itunes.apple.com/search`
- **Auth:** None required (free, public API)
- **Rate Limit:** Self-imposed respectful delays
- **Provides:** App metadata, ratings, categories, screenshots
- **Limitations:** No search volumes, no keyword rankings, no download counts

### WebFetch (Secondary)
- **Usage:** Fallback when iTunes API insufficient
- **Implementation:** `.claude/skills/aso/lib/scraper.py`
- **Speed:** 10-30 seconds per page
- **Reliability:** Structure-dependent, can break with page changes

## Development Tools

### Code Quality
- **Ruff** (>=0.1.0) - Linting and formatting
  - Target: Python 3.8
  - Line length: 100
  - Rules: E, F, W, C90, I, N, UP, B, A, C4 and more
- **mypy** (>=1.0.0) - Optional type checking
  - Gradual typing (untyped defs allowed)
  - Strict equality and return checking

### Project Management (CCPM)
- **GitHub CLI (gh)** - Issue and PR management
- **gh-sub-issue extension** - Issue hierarchy support
- **Git worktrees** - Parallel agent execution
- **CCPM scripts** - PM automation (init, status, standup, etc.)

## GitHub Automation (9 Workflows)

| Workflow | Purpose |
|----------|---------|
| `auto-pr-dev.yml` | Auto-create PR to dev branch |
| `auto-pr-main.yml` | Auto-create PR to main branch |
| `branch-lifecycle.yml` | Branch cleanup and management |
| `claude-code-review.yml` | AI-powered code review |
| `claude-main-check.yml` | Main branch validation |
| `claude.yml` | Claude integration workflow |
| `python-quality.yml` | Ruff linting + quality checks |
| `security.yml` | Security scanning |
| `wiki-sync.yml` | Wiki synchronization |

## Output Format

- **Markdown** with YAML frontmatter
- **Structured folders** (numbered phases 01-05)
- **Character-validated** metadata sections
- **Checkbox format** for action items

## Platform Constraints (Critical)

### Apple App Store
| Field | Limit |
|-------|-------|
| Title | 30 chars |
| Subtitle | 30 chars |
| Promotional Text | 170 chars |
| Description | 4,000 chars |
| Keywords | 100 chars (comma-separated, no spaces) |

### Google Play Store
| Field | Limit |
|-------|-------|
| Title | 50 chars |
| Short Description | 80 chars |
| Full Description | 4,000 chars |
| Keywords | Extracted from title/description (no field) |

## Repository Info

- **Remote:** `https://github.com/abc-elearning/claude-code-aso-skill`
- **Default Branch:** `main`
- **License:** MIT
- **Build System:** setuptools (>=61.0)
