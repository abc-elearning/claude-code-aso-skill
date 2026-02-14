---
created: 2026-02-13T14:41:49Z
last_updated: 2026-02-13T14:41:49Z
version: 1.0
author: Claude Code PM System
---

# Product Context

## Product Requirements

### Core Functionality
1. **Keyword Research** - Analyze and prioritize keywords by search volume, competition, and relevance
2. **Metadata Optimization** - Generate platform-compliant titles, descriptions, and keyword fields
3. **Competitor Analysis** - Fetch real competitor data and identify strategic gaps
4. **ASO Health Scoring** - Calculate 0-100 health score across multiple dimensions
5. **A/B Test Planning** - Design tests with proper sample size and significance calculations
6. **Launch Planning** - Generate 47-item pre-launch checklist with specific dates
7. **Review Management** - Analyze sentiment and generate response templates
8. **Localization** - Multi-language optimization with ROI analysis

### Platform Support
- Apple App Store (App Store Connect)
- Google Play Store (Play Console)

## User Personas

### Persona 1: Indie Developer (Primary)
- **Profile:** Solo developer building their first/second app
- **Pain Points:** No ASO budget, limited marketing knowledge, overwhelmed by app store requirements
- **Needs:** Step-by-step guidance, copy-paste metadata, clear checklists
- **Usage:** `/aso-full-audit` for initial setup, `/aso-optimize` for updates

### Persona 2: App Marketer
- **Profile:** Marketing professional managing multiple apps
- **Pain Points:** Repetitive metadata creation, keeping up with competitors, manual keyword tracking
- **Needs:** Automated analysis, competitive intelligence, A/B test plans
- **Usage:** `/aso-competitor` for competitive analysis, `/aso-optimize` for metadata refreshes

### Persona 3: ASO Specialist
- **Profile:** Professional ASO consultant serving multiple clients
- **Pain Points:** Time-consuming research, need for standardized deliverables
- **Needs:** Structured outputs, data-backed recommendations, professional reports
- **Usage:** Full audit workflow, customized per client

### Persona 4: Development Team
- **Profile:** Small team launching apps regularly
- **Pain Points:** ASO not integrated into development workflow, forgotten pre-launch steps
- **Needs:** Checklist integration, automated validation, consistent process
- **Usage:** `/aso-prelaunch` before every release

## Core Use Cases

### UC1: New App Launch
**Trigger:** Developer has a new app ready for submission
**Flow:** `/aso-full-audit AppName` → Complete 5-phase output
**Output:** Master action plan, keywords, metadata, checklists, timeline
**Success:** App submitted with optimized metadata and clear plan

### UC2: Metadata Refresh
**Trigger:** Quarterly optimization cycle or keyword performance drop
**Flow:** `/aso-optimize AppName` → Updated metadata
**Output:** New Apple + Google metadata variants
**Success:** Updated character-validated metadata ready to paste

### UC3: Competitive Intelligence
**Trigger:** New competitor enters market or ranking changes
**Flow:** `/aso-competitor AppName "Comp1,Comp2"` → Gap analysis
**Output:** Competitor comparison, keyword gaps, opportunity areas
**Success:** Actionable insights for competitive positioning

### UC4: Pre-Launch Validation
**Trigger:** App update or new version ready for submission
**Flow:** `/aso-prelaunch AppName` → Validation checklist
**Output:** 47-item checklist, submission guide, timeline
**Success:** No rejection, optimized submission timing

## Quality Standards

- All metadata character-validated against platform limits
- Real calendar dates in all timelines (never "Week 1")
- Copy-paste ready content (no additional formatting needed)
- Checkbox format for all action items with success criteria
- Data sources documented (API vs estimated vs user-provided)
