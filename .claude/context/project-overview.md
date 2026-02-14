---
created: 2026-02-13T14:41:49Z
last_updated: 2026-02-13T14:41:49Z
version: 1.0
author: Claude Code PM System
---

# Project Overview

## Feature Summary

### Multi-Agent System (4 Agents)
- **aso-master** (Opus) - Orchestrator coordinating all agents sequentially
- **aso-research** (Opus) - Keyword research + competitor analysis via iTunes API
- **aso-optimizer** (Sonnet) - Metadata generation with character validation
- **aso-strategist** (Opus) - Launch timelines, checklists, review templates

### Slash Commands (4 Workflows)
| Command | Duration | Description |
|---------|----------|-------------|
| `/aso-full-audit` | 30-40 min | Complete ASO audit across all phases |
| `/aso-optimize` | 10-15 min | Quick metadata optimization only |
| `/aso-prelaunch` | 15-20 min | Pre-launch validation checklist |
| `/aso-competitor` | 10-15 min | Competitive intelligence analysis |

### Python Skill Modules (8 Modules)
- `keyword_analyzer.py` - Keyword search volume, competition, relevance analysis
- `metadata_optimizer.py` - Platform-specific metadata generation with validation
- `competitor_analyzer.py` - Competitor strategy analysis and gap identification
- `aso_scorer.py` - ASO health score calculation (0-100)
- `ab_test_planner.py` - A/B test design with statistical significance
- `localization_helper.py` - Multi-language optimization and ROI analysis
- `review_analyzer.py` - Sentiment analysis and response templates
- `launch_checklist.py` - 47-item pre-launch validation

### Data Integration
- **iTunes Search API** (Primary) - Free, official Apple API for competitor metadata
- **WebFetch** (Secondary) - Fallback scraping for additional data
- **User-Provided** (Tertiary) - Manual input when APIs insufficient

### Output Structure (5 Phases)
```
outputs/[app-name]/
├── 00-MASTER-ACTION-PLAN.md
├── 01-research/ (keywords, competitors, action items)
├── 02-metadata/ (Apple + Google copy-paste ready)
├── 03-testing/ (A/B test configuration)
├── 04-launch/ (checklist, timeline, submission guide)
└── 05-optimization/ (review responses, ongoing schedule)
```

## Current State

- **Version:** 1.0.0 (Production Ready)
- **Release:** November 7, 2025
- **Status:** Stable, actively maintained
- **License:** MIT
- **Author:** Alireza Rezvani

## Integration Points

- **Claude Code CLI** - Full agent system with slash commands
- **Claude Desktop/Web App** - Standalone skill via ZIP upload
- **GitHub** - Issue templates, workflows, code review automation
- **iTunes Search API** - Real-time competitor data
- **CCPM** - Project management integration (recently added)

## Distribution Methods

1. **Git Clone** - Full repository with agents + skill
2. **ZIP Upload** - `app-store-optimization.zip` for Claude Desktop
3. **Manual Copy** - Install agents/commands to `~/.claude/`
