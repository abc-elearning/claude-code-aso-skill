---
issue: 2
analyzed: 2026-02-13T23:51:21Z
streams: 2
---

# Analysis: Issue #2 - Update agent definitions and commands with 2026 ASO knowledge and region targeting

## Work Streams

### Stream A: Agent Definitions (4 files, can start immediately)
Update all 4 agent Markdown files with 2026 algorithm knowledge and region parameter handling.

**Files:**
- `.claude/agents/aso/aso-master.md` (576 lines) - Add region collection, 2026 synthesis knowledge, pass region to agents
- `.claude/agents/aso/aso-research.md` (670 lines) - Add review fetching step, region-aware API calls, 2026 research knowledge
- `.claude/agents/aso/aso-optimizer.md` (821 lines) - Add screenshot caption section, CPP strategy, semantic coherence, 2026 optimization knowledge
- `.claude/agents/aso/aso-strategist.md` (1114 lines) - Add 2026 compliance deadlines, technical performance, updated strategy knowledge

**Agent type:** general-purpose

### Stream B: Slash Commands (4 files, can start immediately)
Add region prompt to all 4 slash commands. Independent from Stream A (different files).

**Files:**
- `.claude/commands/aso/aso-full-audit.md` (203 lines) - Add region prompt to workflow
- `.claude/commands/aso/aso-optimize.md` (80 lines) - Add region prompt
- `.claude/commands/aso/aso-prelaunch.md` (85 lines) - Add region prompt
- `.claude/commands/aso/aso-competitor.md` (107 lines) - Add region prompt

**Agent type:** general-purpose

## Dependencies
- Stream A and B are independent (different files, no conflicts)
- Both can run in parallel

## Risks
- Agent prompt length may increase significantly with 25 platform changes
- Keep additions focused and concise to avoid bloating agent definitions
