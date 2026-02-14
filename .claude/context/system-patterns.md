---
created: 2026-02-13T14:41:49Z
last_updated: 2026-02-13T14:41:49Z
version: 1.0
author: Claude Code PM System
---

# System Patterns

## Architectural Style

### Multi-Agent Orchestration Pattern
The system uses a **coordinator/specialist** pattern:
- **aso-master** acts as orchestrator, invoking specialists sequentially
- Each specialist agent has a focused domain (research, optimization, strategy)
- Data flows unidirectionally: Research → Optimization → Strategy → Synthesis
- Quality gates validate outputs between phases

### Dual Structure Pattern
The skill exists in two locations for different use cases:
- `app-store-optimization/` - Standalone distributable package
- `.claude/skills/aso/` - Agent-integrated version for workflow automation
- Kept synchronized via manual copy (`cp -r`)

### Layered Architecture
```
Layer 1: Standalone Skill (Python modules)
Layer 2: Agent-Integrated Skill (same modules, different location)
Layer 3: Agent Definitions (Markdown with protocols)
Layer 4: Slash Commands (user-facing entry points)
Layer 5: Output Structure (deliverable files)
```

## Design Patterns

### Input → Process → Output (All Modules)
Every Python module follows:
```
Input (JSON/dict) → Analysis Functions → Output (JSON/dict)
```
- `sample_input.json` documents expected input structure
- `expected_output.json` documents response format

### Universal Agent Protocol
All agents follow the same lifecycle:
1. **Pre-work** - Validate inputs, check dependencies
2. **Execution** - Perform primary task
3. **Verification** - Self-assess quality (must be >= 4/5)
4. **Handoff** - Write outputs for next agent

### Template-Driven Output
- 6 action checklist templates in `.claude/templates/`
- Each phase generates files following template structure
- Templates ensure consistency across different app analyses

### Data Source Fallback Chain
```
iTunes Search API (preferred)
    ↓ (if insufficient)
WebFetch Scraping (fallback)
    ↓ (if unreliable)
User-Provided Data (last resort)
```
Each data point documents its source and confidence level.

### Character Limit Validation
All metadata generation includes:
1. Generate content
2. Count characters
3. Validate against platform limits
4. Display `count/limit` with pass/fail indicator
5. Reject non-compliant output

## Data Flow

### Full Audit Workflow
```
User Request
    → aso-master (parse request, gather app details)
        → aso-research (iTunes API → keywords, competitors, gaps)
            → writes: 01-research/*.md
        → aso-optimizer (reads research → generates metadata)
            → writes: 02-metadata/*.md, 03-testing/*.md
        → aso-strategist (reads all → creates timeline, checklists)
            → writes: 04-launch/*.md, 05-optimization/*.md
    → aso-master (synthesize → 00-MASTER-ACTION-PLAN.md)
```

### Quick Optimize Workflow
```
User Request
    → aso-optimizer (user input → metadata)
        → writes: 02-metadata/*.md
```

## Error Handling Patterns

- **API Failure:** Fall back to WebFetch, then user-provided data
- **Character Overflow:** Truncate intelligently, re-validate
- **Missing Data:** Use "Unknown" placeholder, document limitation
- **Quality Gate Failure:** Agent retries with refined approach (max 2 retries)

## File Organization Conventions

- **Numbered phases:** `01-research/`, `02-metadata/`, etc. for execution order
- **Action files:** `action-{phase}.md` in each phase folder for tasks
- **Master plan:** `00-MASTER-ACTION-PLAN.md` as entry point
- **Per-app isolation:** All outputs in `outputs/[app-name]/`

## CCPM Integration Patterns

- **GitHub Issues as Database** - Epics and tasks tracked via GitHub Issues
- **Worktree Parallelism** - Git worktrees enable parallel agent work
- **Sequential PM Commands** - `/pm:prd-new` → `/pm:prd-parse` → `/pm:epic-oneshot`
- **Context Management** - `/context:create` → `/context:prime` → `/context:update`
- **Rule-Based Guardrails** - 11 rules in `.claude/rules/` enforce standards
