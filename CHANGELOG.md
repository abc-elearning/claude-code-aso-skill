# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-02-14

### Added

#### Keyword Analysis
- Semantic keyword clustering with 12 intent categories (navigate, compare, learn, manage, track, plan, create, discover, buy, fix, share, general)
- Natural language query generation for voice and AI search readiness ("how to...", "best app for...")
- Combined intent scoring per cluster

#### Metadata Optimization
- Screenshot caption optimizer generating complementary keyword captions (avoids title/subtitle duplication)
- Custom Product Page (CPP) strategy planning for up to 70 CPPs with audience segmentation
- Per-platform caption style (Apple: benefit-focused; Google: feature-focused)

#### Review Analysis
- `load_from_itunes_rss()` adapter for ingesting real reviews from iTunes RSS feed
- Integration with iTunesAPI `fetch_reviews()` for automated review fetching

#### iTunes API
- `fetch_reviews()` method with configurable rate limiting
- RSS feed parsing for real user review data
- Retry logic and error handling for API calls

#### ASO Scoring
- Technical performance scoring: crash rate, ANR rate, battery impact
- Visual optimization scoring: screenshot captions, CPP count, app preview video
- Platform-specific weight profiles (Google weights technical metrics higher; Apple weights visual/editorial)

#### Launch Checklist
- 6 real 2026 compliance deadlines tracked:
  - Google Age Signals API Restrictions (Jan 1, 2026)
  - Apple Age Rating Restructuring (Jan 31, 2026)
  - Google US Billing Policy Changes (Jan 28, 2026)
  - Google Battery Optimization Compliance (Mar 1, 2026)
  - Apple Promo Code Discontinuation (Mar 26, 2026)
  - Apple iOS 26 SDK Requirement (Apr 28, 2026)
- `check_compliance_deadlines()` with status-aware alerts (passed/warning/upcoming/future)
- Days-until-deadline and days-from-launch calculations

#### Agent System
- All 4 agent definitions updated with 2026 platform knowledge
- Region targeting support across all agents and slash commands
- Updated compliance awareness in aso-strategist agent

#### Slash Commands
- `/aso-full-audit` - Added region targeting parameter
- `/aso-optimize` - Added region targeting parameter
- `/aso-prelaunch` - Added region targeting parameter
- `/aso-competitor` - Added region targeting parameter

### Changed
- ASO scorer now uses platform-specific weight profiles instead of uniform weights
- Agent definitions reference 2026 compliance deadlines and platform updates
- Slash commands accept optional region/country parameter for localized analysis

### Technical Details
- All modules maintain zero external dependencies (Python 3.7+ standard library only)
- Both skill copies synchronized (app-store-optimization/ and .claude/skills/aso/)
- All 10 Python modules pass syntax validation
- End-to-end smoke tests pass for all new features

---

## [1.0.0] - 2025-11-07

### 🎉 Initial Release - Production Ready

First stable release of the ASO Agent System for Claude Code. Complete multi-agent framework for App Store Optimization with real data integration.

### Added

#### Core Agent System
- **aso-master** agent - Orchestrator coordinating all specialist agents (500 lines)
- **aso-research** agent - Keyword research with iTunes API integration (700 lines)
- **aso-optimizer** agent - Metadata generation with character validation (600 lines)
- **aso-strategist** agent - Launch timelines and ongoing optimization (700 lines)
- Total agent code: 2,500+ lines with comprehensive workflows

#### Slash Commands
- `/aso-full-audit [AppName]` - Complete ASO audit (30-40 min workflow)
- `/aso-optimize [AppName]` - Quick metadata optimization (10-15 min)
- `/aso-prelaunch [AppName]` - Pre-launch validation (15-20 min)
- `/aso-competitor [AppName] "Competitors"` - Competitive intelligence (10-15 min)

#### Data Integration
- iTunes Search API wrapper (`itunes_api.py`) - Tested and working
- WebFetch utilities (`scraper.py`) - Additional data scraping
- Real competitor data fetching (no generic recommendations)
- Character limit validation (Apple: 30/30/100, Google: 50/80/4000)

#### Output Structure
- `00-MASTER-ACTION-PLAN.md` - Complete roadmap with ASO health score
- `01-research/` - Keyword research (20 keywords, tiered strategy)
- `02-metadata/` - Copy-paste ready metadata for both platforms
- `03-testing/` - A/B test configuration and monitoring
- `04-launch/` - 47-item pre-launch checklist with timeline
- `05-optimization/` - Review response templates and task schedule
- `FINAL-REPORT.md` - Executive summary

#### Templates
- 6 action checklist templates for all workflow phases
- Master action plan template with ASO scoring
- Platform-specific metadata templates
- A/B testing configuration templates
- Pre-launch validation checklist (47 items)

#### Documentation
- `README.md` - Comprehensive project documentation (540+ lines)
- `LICENSE.md` - MIT License with third-party attributions
- `CHANGELOG.md` - Version history (this file)
- `.claude/ARCHITECTURE.md` - Complete system architecture (509 lines)
- `.claude/INSTALL.md` - Installation guide for 3 scenarios
- `.claude/USAGE.md` - Usage guide with 5 workflows
- `CLAUDE.md` - Quick reference for Claude instances (+280 lines)
- `documentation/implementation/aso-agents-implementation-plan.md` - Development plan (400+ lines)

#### Example Outputs
- Complete FitFlow example workflow (`outputs/FitFlow-example/`)
- Demonstrates all quality standards and deliverables
- ASO health score: 58/100
- 20 priority keywords with implementation guide
- Copy-paste ready metadata with character validation
- Timeline: November 7 - December 1, 2025 (real dates)

#### Distribution
- Standalone skill package (`app-store-optimization/`)
- Agent-integrated version (`.claude/skills/aso/`)
- Distributable ZIP file (`app-store-optimization.zip`)
- Dual structure supporting both direct skill usage and agent coordination

### Technical Details

#### Quality Standards Implemented
- ✅ Character limits validated for both platforms
- ✅ Natural language checking (no keyword stuffing)
- ✅ Real calendar dates (not placeholders)
- ✅ Copy-paste ready content (no formatting needed)
- ✅ Actionable tasks with success criteria
- ✅ Data-backed recommendations (iTunes API)

#### Testing
- iTunes API integration tested successfully
- Test apps: Todoist (4.8★, 120K ratings), Any.do (4.6★, 49K ratings), Microsoft To Do (4.7★, 250K ratings)
- Example workflow validated for quality standards
- All deliverables verified for character counts and actionability

#### Project Statistics
- Total files: 59
- Lines of code: 26,526+
- Agents: 4 (2,500+ lines)
- Python modules: 8 (800+ lines)
- Templates: 6 action checklists
- Slash commands: 4 workflows
- Documentation: 1,500+ lines

### Known Limitations

#### iTunes Search API
- No keyword search volumes (estimated using benchmarks)
- No keyword rankings (must be checked manually)
- No download numbers (estimated only)
- No historical data (current state only)

#### WebFetch
- Slower than API calls (10-30 seconds per page)
- Structure-dependent extraction
- Self-imposed rate limiting

#### User Data Required
- Search volumes should be verified with Apple Search Ads
- Keyword rankings must be tracked manually initially
- Conversion rates tracked via App Store Connect

### Migration Notes

This is the initial release - no migration needed.

### Installation

```bash
# Clone repository
git clone https://github.com/alirezarezvani/claude-code-aso-skill.git
cd claude-code-aso-skill

# Install agents (user-level)
cp .claude/agents/aso/*.md ~/.claude/agents/

# Install slash commands (optional)
cp .claude/commands/aso/*.md ~/.claude/commands/

# Verify
claude --list-agents | grep aso
```

### Upgrade Notes

First release - no upgrade needed.

---

## [Unreleased]

### Planned for v1.2

#### Features
- [ ] Historical tracking database for keyword rankings
- [ ] Enhanced A/B test analytics with statistical significance
- [ ] Multi-language support (Spanish, German, French)
- [ ] App preview video script templates
- [ ] Automated metadata refresh scheduling

#### Improvements
- [ ] Faster data fetching with concurrent API calls
- [ ] Enhanced competitor analysis with pricing trends
- [ ] ASO score improvement recommendations

#### Documentation
- [ ] Video tutorials for common workflows
- [ ] Advanced customization guide
- [ ] Translation of documentation to Spanish, German, French

### Planned for v2.0

#### Major Features
- [ ] Paid ASO API integration (AppTweak, Sensor Tower)
- [ ] Web dashboard for tracking and visualization
- [ ] Automated reporting via email/Slack
- [ ] Team collaboration features
- [ ] Keyword ranking tracking over time
- [ ] Conversion funnel analysis
- [ ] Review sentiment analysis with ML

#### Breaking Changes
- None currently planned

---

## Version History

### [1.1.0] - 2026-02-14
- Region targeting across all commands
- iTunes Review API, semantic keyword clustering, screenshot captions, CPP strategy
- Technical/visual scoring, platform-specific weights, 2026 compliance deadlines
- All agents and slash commands updated for 2026

### [1.0.0] - 2025-11-07
- Initial production release
- Multi-agent system with 4 specialized agents
- iTunes API integration tested
- Complete documentation and examples
- 26,526+ lines of code

---

## Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0) - Incompatible API changes
- **MINOR** version (0.X.0) - Backward-compatible functionality additions
- **PATCH** version (0.0.X) - Backward-compatible bug fixes

---

## Support

For questions about this changelog:
- Open an issue: https://github.com/alirezarezvani/claude-code-aso-skill/issues
- Read documentation: `.claude/INSTALL.md` and `.claude/USAGE.md`

---

## Links

- [Homepage](https://github.com/alirezarezvani/claude-code-aso-skill)
- [Documentation](.claude/)
- [Issues](https://github.com/alirezarezvani/claude-code-aso-skill/issues)
- [Releases](https://github.com/alirezarezvani/claude-code-aso-skill/releases)

---

**Maintained by:** Alireza Rezvani
**License:** MIT
**Last Updated:** February 14, 2026
