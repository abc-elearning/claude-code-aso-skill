---
created: 2026-02-13T14:41:49Z
last_updated: 2026-02-13T14:41:49Z
version: 1.0
author: Claude Code PM System
---

# Project Structure

## Root Directory

```
claude-code-aso-skill/
├── .claude/                          # Claude Code configuration (agents, commands, skills, CCPM)
├── .git/                             # Git repository
├── .github/                          # GitHub workflows, templates, community files
├── app-store-optimization/           # Standalone distributable skill package
├── app-store-optimization.zip        # ZIP package for Claude Desktop/Web App
├── documentation/                    # Implementation plans and workflow docs
├── outputs/                          # Generated ASO outputs (per-app folders)
├── scripts/                          # Project utility scripts
├── CHANGELOG.md                      # Version history
├── CLAUDE.md                         # Claude Code instructions (16KB)
├── LICENSE.md                        # MIT License
├── PROJECT-STATUS.md                 # Completion status document
├── README.md                         # Main documentation (18KB)
└── pyproject.toml                    # Python project configuration
```

## .claude/ Directory (Core Configuration)

```
.claude/
├── ARCHITECTURE.md                   # System architecture docs
├── INSTALL.md                        # Installation guide
├── USAGE.md                          # Usage guide
├── ccpm.config                       # CCPM GitHub repo detection
├── settings.local.json               # Permission allowlists (merged ASO + CCPM)
├── settings.json.example             # CCPM hook configuration example
│
├── agents/                           # AI agent definitions
│   ├── aso/                          # ASO specialist agents (4)
│   │   ├── aso-master.md             # Orchestrator (Opus)
│   │   ├── aso-research.md           # Research agent (Opus)
│   │   ├── aso-optimizer.md          # Metadata agent (Sonnet)
│   │   └── aso-strategist.md         # Strategy agent (Opus)
│   ├── code-analyzer.md             # CCPM: Bug hunting agent
│   ├── file-analyzer.md             # CCPM: File analysis agent
│   ├── parallel-worker.md           # CCPM: Parallel execution agent
│   └── test-runner.md               # CCPM: Test execution agent
│
├── commands/                         # Slash command definitions
│   ├── aso/                          # ASO commands (4)
│   │   ├── aso-full-audit.md
│   │   ├── aso-optimize.md
│   │   ├── aso-prelaunch.md
│   │   └── aso-competitor.md
│   ├── pm/                           # CCPM project management (40+ commands)
│   ├── context/                      # CCPM context management (3 commands)
│   ├── testing/                      # CCPM testing (2 commands)
│   ├── code-rabbit.md               # CCPM: CodeRabbit review
│   ├── prompt.md                    # CCPM: Direct prompt
│   └── re-init.md                   # CCPM: CLAUDE.md update
│
├── context/                          # Project context documentation (this system)
├── epics/                            # CCPM: Epic tracking workspace
├── hooks/                            # CCPM: Git worktree fix hook
├── prds/                             # CCPM: Product requirements documents
├── rules/                            # CCPM: 11 operational rules
├── scripts/                          # CCPM: PM and utility scripts
│
├── skills/aso/                       # Agent-integrated ASO skill
│   ├── *.py                          # 8 Python modules
│   ├── lib/                          # Data fetching utilities
│   │   ├── itunes_api.py
│   │   ├── scraper.py
│   │   └── data_sources.md
│   ├── SKILL.md                     # Skill specification
│   └── sample/expected JSON files
│
└── templates/                        # Output templates (6 action checklists)
    ├── master-action-plan-template.md
    └── action-*-template.md (5 files)
```

## app-store-optimization/ (Standalone Skill)

```
app-store-optimization/
├── keyword_analyzer.py               # 13KB - Keyword analysis
├── metadata_optimizer.py             # 20KB - Metadata generation
├── competitor_analyzer.py            # 21KB - Competitor analysis
├── aso_scorer.py                     # 19KB - Health score calculation
├── ab_test_planner.py                # 23KB - A/B test planning
├── localization_helper.py            # 22KB - Multi-language support
├── review_analyzer.py                # 26KB - Review sentiment analysis
├── launch_checklist.py               # 29KB - Pre-launch validation
├── lib/                              # Data fetching layer
│   ├── itunes_api.py
│   ├── scraper.py
│   └── data_sources.md
├── SKILL.md                          # Skill specification
├── HOW_TO_USE.md                     # Usage guide
├── README.md                         # Skill documentation
├── sample_input.json                 # Example request
└── expected_output.json              # Example response
```

## .github/ (GitHub Configuration)

```
.github/
├── CODEOWNERS                        # Code ownership
├── CODE_OF_CONDUCT.md                # Community guidelines
├── CONTRIBUTING.md                   # Contribution guide
├── FUNDING.yml                       # Sponsorship config
├── PULL_REQUEST_TEMPLATE.md          # PR template
├── SECURITY.md                       # Security policy
├── dependabot.yml                    # Dependency updates
├── ISSUE_TEMPLATE/                   # 5 issue templates
│   ├── bug_report.yml
│   ├── config.yml
│   ├── documentation.yml
│   ├── feature_request.yml
│   └── feedback.yml
└── workflows/                        # 9 GitHub Actions
    ├── auto-pr-dev.yml
    ├── auto-pr-main.yml
    ├── branch-lifecycle.yml
    ├── claude-code-review.yml
    ├── claude-main-check.yml
    ├── claude.yml
    ├── python-quality.yml
    ├── security.yml
    └── wiki-sync.yml
```

## Key Naming Conventions

- **Agent files:** `aso-{role}.md` (lowercase, hyphenated)
- **Command files:** `aso-{action}.md` (lowercase, hyphenated)
- **Python modules:** `{feature}_{type}.py` (snake_case)
- **Templates:** `{type}-template.md` (lowercase, hyphenated)
- **Output folders:** `{number}-{phase}/` (numbered phases 01-05)
- **CCPM rules:** `{topic}.md` (lowercase, hyphenated)
- **CCPM scripts:** `{action}.sh` (lowercase, hyphenated)

## Dual Structure Note

The project maintains two copies of the ASO skill:
1. `app-store-optimization/` - Standalone distributable package
2. `.claude/skills/aso/` - Agent-integrated version

These must be kept in sync: `cp -r app-store-optimization/* .claude/skills/aso/`
