---
name: aso-update-2-2026
status: backlog
created: 2026-02-13T23:34:45Z
progress: 0%
prd: .claude/prds/aso-update-2-2026.md
github: https://github.com/abc-elearning/aso-agents/issues/1
---

# Epic: aso-update-2-2026

## Overview

Update the ASO Agent System from v1.0 (Nov 2025 knowledge) to v1.1 (Feb 2026 knowledge). This involves updating existing Python modules and agent definitions with 25 platform changes, adding review fetching capability, introducing region targeting, and shifting to semantic keyword strategies. The approach prioritizes extending existing code over creating new modules.

## Architecture Decisions

### AD1: Extend existing modules, don't create new ones
- **Decision:** Add review fetching to `itunes_api.py` (not a new module), add semantic clustering to `keyword_analyzer.py`, add screenshot captions to `metadata_optimizer.py`
- **Rationale:** The existing 8-module architecture is solid. Adding a `review_fetcher.py` would fragment the codebase. The iTunes RSS endpoint is just another iTunes API call - it belongs in `itunes_api.py`.

### AD2: Rule-based sentiment analysis (no NLP libraries)
- **Decision:** Use the existing `ReviewAnalyzer` class with enhanced keyword lists for sentiment analysis of fetched reviews
- **Rationale:** Zero external dependencies constraint. The existing `review_analyzer.py` already has sentiment analysis, positive/negative keyword lists, and theme extraction. Just needs to consume real data from the RSS endpoint.

### AD3: Semantic clustering via keyword co-occurrence
- **Decision:** Implement intent-based clustering using keyword overlap scoring and manual intent categories, not ML
- **Rationale:** Standard library constraint prevents using NLP clustering (no sklearn, spaCy). Co-occurrence analysis + predefined intent categories (track, manage, plan, learn, etc.) is practical and maintainable.

### AD4: Region as a first-class parameter across all commands
- **Decision:** Add `region` parameter to all 4 slash commands and pass it through to iTunes API calls
- **Rationale:** `iTunesAPI.__init__` already accepts `country` parameter. The plumbing exists - just need to prompt users and pass it through. No architectural changes needed.

### AD5: Agent knowledge as inline updates, not separate files
- **Decision:** Update agent Markdown files directly with 2026 knowledge rather than creating separate reference files
- **Rationale:** Agents are already 500-1100 lines. Adding 2026 knowledge sections is simpler than managing cross-file references. Keeps agents self-contained.

## Technical Approach

### Python Module Changes

**`itunes_api.py` (extend)**
- Add `fetch_reviews(app_id, country, pages=10)` method using RSS JSON endpoint
- Add `REVIEW_RSS_URL` constant: `https://itunes.apple.com/{code}/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json`
- Add rate limiting (20 calls/min) with `time.sleep()` between pagination calls
- Add review JSON parsing (extract: author, rating, title, body, version, date)

**`keyword_analyzer.py` (extend)**
- Add `cluster_by_intent(keywords)` method grouping keywords into intent themes
- Add `generate_natural_queries(cluster)` for voice/AI search variants
- Add `INTENT_CATEGORIES` dict (track, manage, plan, create, learn, find, compare, etc.)
- Add `score_cluster(cluster)` for combined cluster potential scoring

**`metadata_optimizer.py` (extend)**
- Add `generate_screenshot_captions(keywords, existing_metadata)` method
- Captions use complementary keywords (not duplicating title/subtitle/keyword field)
- Add `generate_cpp_metadata(segments, keywords)` for Custom Product Page variants
- Validate CPP count <= 70

**`aso_scorer.py` (extend)**
- Reweight categories: metadata (20%), ratings (20%), keywords (20%), conversion (20%), technical (15%), screenshot/CPP (5%)
- Add `score_technical_performance(crash_rate, anr_rate, battery_impact)` method
- Add `score_visual_optimization(has_captions, cpp_count)` sub-score
- Platform-specific weighting (Google weighs technical higher)

**`launch_checklist.py` (extend)**
- Add 2026 compliance items: Apple age rating (Jan 31), Google battery (Mar 1), Apple SDK (Apr 28), Apple promo codes (Mar 26), Google US billing (Jan 28)
- Add dynamic deadline warnings (compare item deadline vs user's launch date)

**`review_analyzer.py` (minor update)**
- No structural changes - already has sentiment analysis, theme extraction, response templates
- Update keyword lists with 2026-relevant terms
- Add method to accept reviews from `itunes_api.fetch_reviews()` output format

### Agent Definition Changes

**`aso-research.md` (update)**
- Add region prompt at start of workflow
- Add review fetching step using `itunes_api.fetch_reviews()`
- Feed fetched reviews into `review_analyzer.py`
- Add competitor review mining for keyword opportunities

**`aso-optimizer.md` (update)**
- Add screenshot caption generation section
- Add CPP strategy section (segment-based, up to 70 pages)
- Update algorithm knowledge: semantic coherence, no keyword stuffing
- Add CPP keyword assignment guidance

**`aso-strategist.md` (update)**
- Add 2026 compliance deadlines to checklist generation
- Update timeline templates with new platform requirements
- Add technical performance recommendations

**`aso-master.md` (update)**
- Add region collection at orchestration start
- Pass region to all agent invocations
- Add 2026 platform changes to synthesis knowledge
- Update master action plan template with new sections (screenshots, CPPs, technical)

### Slash Command Changes

**All 4 commands** (`aso-full-audit.md`, `aso-optimize.md`, `aso-prelaunch.md`, `aso-competitor.md`):
- Add region prompt: "What is your target market/region? (e.g., us, jp, de, kr)"
- Default to "us" if not specified
- Pass region through to agent invocations

## Implementation Strategy

### Development approach
- Work task-by-task in dependency order
- Each task produces testable changes
- Sync both skill copies after each Python module change (`app-store-optimization/` ↔ `.claude/skills/aso/`)
- Test with FitFlow example after all changes

### Risk mitigation
- iTunes RSS endpoint: test early in Task 2; if broken, implement WebFetch fallback
- Semantic clustering quality: validate with manual review of 3-5 sample clusters
- Agent prompt length: monitor token count; trim redundant sections if needed

### Testing approach
- Each Python module: run `python3 module.py` for basic syntax/import check
- Review fetching: test with known app IDs (Todoist: 585829637, Headspace: 493145008)
- End-to-end: run `/aso-full-audit FitFlow` and verify new sections appear in outputs

## Task Breakdown

- [ ] **Task 1: Update agent and command definitions with 2026 knowledge + region targeting**
  Update all 4 agent MDs with 2026 algorithm knowledge (25 platform changes), add region prompt to all 4 slash commands, update `aso-master` to collect and pass region parameter. This is the foundational knowledge update.

- [ ] **Task 2: Add review fetching to `itunes_api.py` and wire to `review_analyzer.py`**
  Add `fetch_reviews()` method to iTunesAPI class using RSS JSON endpoint. Add rate limiting. Update `review_analyzer.py` to accept fetched review format. Test with real app IDs across multiple regions.

- [ ] **Task 3: Add semantic keyword clustering to `keyword_analyzer.py`**
  Add intent categories, `cluster_by_intent()`, `generate_natural_queries()`, and `score_cluster()` methods. Shift from individual keyword targeting to intent-based clusters.

- [ ] **Task 4: Add screenshot caption + CPP strategy to `metadata_optimizer.py`**
  Add `generate_screenshot_captions()` with complementary keyword strategy. Add `generate_cpp_metadata()` for up to 70 Custom Product Pages with keyword assignments. Validate character limits.

- [ ] **Task 5: Update `aso_scorer.py` weights + add technical performance scoring**
  Reweight scoring categories to include technical performance (15%) and visual optimization (5%). Add `score_technical_performance()` and `score_visual_optimization()` methods. Platform-specific weighting.

- [ ] **Task 6: Update `launch_checklist.py` with 2026 compliance deadlines**
  Add 6 new compliance items with specific dates. Add dynamic deadline comparison against user's launch date. Update compliance validation logic.

- [ ] **Task 7: Sync skill copies + end-to-end testing + documentation update**
  Sync `app-store-optimization/` ↔ `.claude/skills/aso/`. Run full audit with FitFlow example. Update README, CLAUDE.md, CHANGELOG with v1.1 changes. Update FitFlow example outputs.

## Dependencies

### Task Dependencies
```
Task 1 (knowledge + region) → all other tasks depend on updated agent definitions
Task 2 (reviews) → independent after Task 1
Task 3 (semantic keywords) → independent after Task 1
Task 4 (screenshots + CPP) → depends on Task 3 (uses keyword clusters)
Task 5 (scorer) → depends on Task 4 (scores screenshot/CPP usage)
Task 6 (compliance) → independent after Task 1
Task 7 (integration) → depends on all tasks (2-6)
```

### External Dependencies
- iTunes RSS JSON endpoint must be available (test in Task 2)
- Apple App Store territory list for region validation (can hardcode common ones)

## Success Criteria (Technical)

| Criteria | Measurement |
|----------|-------------|
| All 8 Python modules pass syntax check | `python3 module.py` exits 0 |
| Review fetching works for 3+ regions | Test US, JP, DE with known app IDs |
| Semantic clusters group related keywords | Manual review: >80% coherence |
| Screenshot captions don't duplicate existing metadata | Automated check in method |
| CPP count validated ≤ 70 | Assertion in `generate_cpp_metadata()` |
| ASO scorer weights sum to 100 | Unit assertion |
| Compliance items have specific dates | No placeholder dates in output |
| Region flows through all 4 commands | Test each command with `region=jp` |
| Both skill copies identical | `diff -r` shows no differences |
| Zero external dependencies maintained | No `import` outside standard library |

## Estimated Effort

| Task | Effort | Critical Path |
|------|--------|---------------|
| Task 1: Knowledge + region | 3-4 days | YES (blocks all) |
| Task 2: Review fetching | 2-3 days | No |
| Task 3: Semantic keywords | 2-3 days | No |
| Task 4: Screenshots + CPP | 2-3 days | Depends on Task 3 |
| Task 5: Scorer update | 1-2 days | Depends on Task 4 |
| Task 6: Compliance update | 1 day | No |
| Task 7: Integration + docs | 2-3 days | YES (final gate) |
| **Total** | **~14-19 days** | |

**Critical path:** Task 1 → Task 3 → Task 4 → Task 5 → Task 7

**Parallelizable:** Tasks 2, 3, 6 can run in parallel after Task 1 completes.

## Tasks Created
- [ ] #2 - Update agent definitions and commands with 2026 ASO knowledge and region targeting (parallel: false)
- [ ] #3 - Add iTunes review fetching and wire to review analyzer (parallel: true)
- [ ] #5 - Add semantic keyword clustering to keyword analyzer (parallel: true)
- [ ] #6 - Add screenshot caption optimizer and CPP strategy to metadata optimizer (parallel: false)
- [ ] #4 - Update ASO scorer with technical performance and visual optimization scoring (parallel: false)
- [ ] #7 - Update launch checklist with 2026 compliance deadlines (parallel: true)
- [ ] #9 - Sync skill copies, end-to-end testing, and documentation update (parallel: false)

Total tasks: 7
Parallel tasks: 3 (#3, #5, #7 — can run simultaneously after #2)
Sequential tasks: 4 (#2, #6, #4, #9)
Estimated total effort: 104-152 hours (~14-19 days)
