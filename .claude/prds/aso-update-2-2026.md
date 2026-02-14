---
name: aso-update-2-2026
description: Major ASO system update with 2026 algorithm changes, region targeting, iTunes Review API, and semantic keyword clustering
status: backlog
created: 2026-02-13T23:11:02Z
---

# PRD: aso-update-2-2026

## Executive Summary

This update brings the ASO Agent System from v1.0 (November 2025 knowledge) to v1.1 (February 2026 knowledge) by incorporating critical platform algorithm changes, adding user-defined region/market targeting, integrating the iTunes Review RSS endpoint for review analysis, and shifting to semantic/intent-based keyword strategies. The App Store landscape has undergone significant changes since v1.0 - screenshot captions are now indexed, Custom Product Pages doubled to 70 with organic keyword assignment, Google Play now penalizes poor battery optimization, and both platforms have shifted toward semantic understanding over keyword matching.

## Problem Statement

### What Problem Are We Solving?

The current ASO system (v1.0) was built with November 2025 knowledge. Since then:

1. **Outdated Algorithm Knowledge** - Apple now indexes screenshot captions for ranking (June 2025 change not captured), CPPs expanded from 35→70 with organic keyword assignment, and AI-generated tags were introduced. Google Play now uses battery optimization and Android Vitals as direct ranking factors.

2. **No Region/Market Targeting** - The system generates generic English-language recommendations without asking users about their target market. Different regions have different keyword competition, user behavior, and store dynamics.

3. **No Review Analysis Capability** - Users identified review insights as a key pain point. Reviews are now a direct ranking factor on Google Play, and competitor review mining reveals keyword opportunities and feature gaps.

4. **Keyword Accuracy Issues** - The ±20% accuracy of search volume estimates is too rough. Additionally, the system still uses individual keyword targeting instead of the 2026 best practice of semantic keyword clusters mapped to user intent.

### Why Is This Important Now?

- **Compliance Deadlines:** Apple age rating restructuring (Jan 31, 2026), Google battery optimization (March 1, 2026), Apple SDK requirements (April 28, 2026)
- **Algorithm Shifts:** Both Apple and Google penalize keyword stuffing and reward semantic coherence - the current system's approach needs updating
- **Competitive Advantage:** Screenshot caption indexing and CPP keyword assignment are new organic levers that competitors may already be using
- **User Demand:** Keyword accuracy and review insights were the top 2 pain points reported

## User Stories

### US1: Region-Aware ASO Analysis

**As** an app developer targeting the Japanese market,
**I want** the system to ask me about my target region and adapt its recommendations,
**So that** I get region-specific keyword suggestions, competitor analysis, and metadata tailored to my market.

**Acceptance Criteria:**
- [ ] System prompts for target region if not provided
- [ ] Keyword research considers region-specific competition levels
- [ ] Competitor analysis fetches data from the specified region's App Store
- [ ] Metadata recommendations account for language and cultural nuances
- [ ] iTunes API calls use correct country code parameter

### US2: Screenshot Caption Strategy

**As** an ASO optimizer,
**I want** the system to generate keyword-optimized screenshot caption recommendations,
**So that** I can leverage Apple's screenshot caption indexing for additional keyword ranking.

**Acceptance Criteria:**
- [ ] System generates recommended caption text for each screenshot slot
- [ ] Captions use keywords NOT already in title/subtitle/keyword field (complementary strategy)
- [ ] Caption text reads naturally (not keyword stuffed)
- [ ] Character count guidance provided for caption legibility
- [ ] Integration with existing metadata output files

### US3: Review Analysis & Mining

**As** an app marketer,
**I want** the system to fetch and analyze competitor reviews via iTunes RSS endpoint,
**So that** I can identify keyword opportunities, feature gaps, and common user pain points.

**Acceptance Criteria:**
- [ ] System fetches reviews via iTunes RSS JSON endpoint (up to 500 reviews per app)
- [ ] Sentiment analysis categorizes reviews (positive/negative/neutral)
- [ ] Common themes extracted (feature requests, bugs, praise points)
- [ ] Keywords extracted from positive reviews for metadata incorporation
- [ ] Competitor review comparison highlights differentiation opportunities
- [ ] Support for multiple regions (country code parameter)

### US4: Semantic Keyword Clustering

**As** an ASO specialist,
**I want** the system to group keywords into intent-based semantic clusters,
**So that** I can optimize for how users actually search in 2026 (conversational, intent-driven queries).

**Acceptance Criteria:**
- [ ] Keywords grouped by user intent (e.g., "track expenses" cluster vs "save money" cluster)
- [ ] Natural language query suggestions generated (e.g., "apps to help me budget")
- [ ] Cluster priority scoring based on combined search potential
- [ ] Metadata recommendations map clusters to specific metadata fields
- [ ] Voice search optimization guidance included

### US5: Custom Product Page Strategy

**As** an app developer with multiple user segments,
**I want** the system to recommend CPP strategies with keyword assignments,
**So that** I can leverage Apple's new organic CPP search visibility.

**Acceptance Criteria:**
- [ ] System recommends number of CPPs based on identified user segments
- [ ] Each CPP has assigned keywords for organic search targeting
- [ ] CPP metadata (title, subtitle, screenshots) generated per segment
- [ ] Strategy differentiates between organic CPPs and paid CPPs
- [ ] Maximum 70 CPPs documented

### US6: Updated Compliance Checklists

**As** an app developer preparing for submission,
**I want** the pre-launch checklist to include all 2026 compliance requirements,
**So that** I don't miss critical deadlines and get rejected.

**Acceptance Criteria:**
- [ ] Apple age rating restructuring (5 categories) included
- [ ] Google battery optimization compliance check included
- [ ] Apple SDK requirements (iOS 26) documented
- [ ] Promo code discontinuation (March 26, 2026) noted
- [ ] US billing policy changes (Google) documented
- [ ] Each item has specific deadline and action steps

### US7: Technical Performance ASO Scoring

**As** an app developer,
**I want** the ASO health score to include technical performance factors,
**So that** my score reflects the 2026 reality where Android Vitals and app performance directly affect rankings.

**Acceptance Criteria:**
- [ ] ASO scorer includes technical performance category
- [ ] Crash rate, ANR rate, battery impact assessed (user-provided data)
- [ ] Score weights updated: technical performance = 15-20% of total
- [ ] Recommendations include technical improvement suggestions
- [ ] Google Play and Apple treated differently (Google weights tech more heavily)

## Requirements

### Functional Requirements

#### FR1: Region/Market Targeting System
- Add region selection prompt to all slash commands
- Support any App Store territory (175+ regions)
- iTunes API calls use `country` parameter for region-specific data
- Region stored in app profile for consistent use across commands
- Default to US if not specified (with prompt to confirm)

#### FR2: iTunes Review RSS Integration
- New module: `review_fetcher.py` wrapping the RSS JSON endpoint
- Endpoint: `https://itunes.apple.com/{CODE}/rss/customerreviews/page={PAGE}/id={APPID}/sortby=mostrecent/json`
- Pagination support (pages 1-10, ~500 reviews max)
- Rate limiting: max 20 calls/minute (Apple's limit)
- Error handling for invalid app IDs, unavailable regions
- JSON parsing and structured output

#### FR3: Screenshot Caption Optimizer
- New section in metadata output: "Screenshot Caption Strategy"
- Generate 5-10 caption recommendations per app
- Complementary keyword strategy (avoid duplicating title/subtitle/keywords)
- Natural language validation (no keyword stuffing)
- Integration with `metadata_optimizer.py`

#### FR4: Semantic Keyword Engine
- Upgrade `keyword_analyzer.py` with intent clustering
- Group keywords by user intent themes
- Generate natural language query variants
- Score clusters by combined search potential
- Voice search optimization recommendations

#### FR5: Custom Product Page Module
- New section in metadata output: "CPP Strategy"
- Segment identification based on keyword clusters
- Per-CPP metadata generation (title, subtitle, screenshots)
- Organic keyword assignment per CPP
- Maximum 70 CPPs limit enforced

#### FR6: Updated ASO Scorer
- Add technical performance category (15-20% weight)
- Add screenshot optimization sub-score
- Add CPP utilization sub-score
- Update algorithm knowledge to reflect 2026 ranking factors
- Platform-specific scoring (Apple vs Google weights differ)

#### FR7: Updated Compliance Module
- Add 2026 compliance deadlines to `launch_checklist.py`
- Apple: age rating restructuring, SDK requirements, promo code changes
- Google: battery optimization, age-restricted content, US billing policy
- Dynamic deadline checking (warn if deadline is approaching)

#### FR8: Agent Prompt Updates
- Update all 4 agent definitions with 2026 knowledge
- Add screenshot caption analysis to aso-optimizer
- Add review fetching to aso-research
- Add CPP strategy to aso-strategist
- Add compliance deadlines to aso-master synthesis

### Non-Functional Requirements

#### NFR1: Performance
- Review fetching: < 30 seconds for 500 reviews (10 pages)
- Region-specific API calls: same latency as current (< 5s per call)
- Semantic clustering: < 10 seconds for 50 keywords
- No degradation to existing workflow timing

#### NFR2: Compatibility
- Python 3.8+ (no new external dependencies)
- All new modules use standard library only
- Backward compatible with existing output structures
- Existing slash commands continue to work unchanged

#### NFR3: Data Quality
- Review sentiment accuracy: > 80% agreement with manual labeling
- Keyword cluster coherence: semantically related keywords score > 0.7 similarity
- Screenshot caption quality: natural language, no keyword stuffing
- Region data: correct country codes validated against Apple's territory list

#### NFR4: Reliability
- Graceful fallback when iTunes RSS endpoint is unavailable
- Handle apps with < 10 reviews (insufficient data warning)
- Handle regions with no reviews (suggest alternative regions)
- Rate limiting prevents API throttling

## Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Algorithm knowledge currency | Feb 2026 | All 15 major changes documented and integrated |
| Screenshot caption coverage | 100% of audits | Caption recommendations in every metadata output |
| Review fetching success rate | > 95% | Successful RSS API calls for valid app IDs |
| Region support | 175+ territories | All Apple App Store territories supported |
| Keyword cluster quality | > 80% coherence | Manual review of cluster groupings |
| Compliance checklist completeness | 100% | All 6 deadline items included |
| CPP strategy generation | Yes/No | CPP recommendations in full audit output |
| Technical ASO score accuracy | Validated | Score correlates with actual ranking performance |
| Backward compatibility | 100% | Existing commands work without changes |
| Zero external dependencies | Maintained | No pip install required |

## Constraints & Assumptions

### Constraints
- **No paid APIs** - Must continue using free data sources only (iTunes Search API, RSS endpoint)
- **Python standard library only** - No external packages (no NLTK, spaCy for NLP)
- **iTunes RSS limitations** - Max ~500 reviews per app, no historical data
- **No real search volumes** - Continue using industry benchmarks for estimation
- **Agent definition format** - Must use existing Markdown agent format

### Assumptions
- iTunes RSS JSON endpoint remains available and stable
- Apple's screenshot caption indexing continues to be a ranking factor
- Google's battery optimization enforcement proceeds as announced (March 1, 2026)
- Users can provide Android Vitals data for technical scoring
- CPP keyword assignment feature is available to all developers (not limited rollout)

## Out of Scope

- **Paid API integration** (AppTweak, Sensor Tower) - Deferred to v2.0
- **Web dashboard** - No UI development
- **Automated screenshot generation** - Only caption text recommendations
- **Translation/localization** - Region targeting is about market selection, not language translation (deferred to v1.2)
- **Apple Search Ads integration** - Paid acquisition out of scope
- **Real-time ranking monitoring** - No persistent tracking database
- **Google Play review API** - Focus on iTunes RSS first; Google Play reviews require scraping

## Dependencies

### Internal Dependencies
- Existing `keyword_analyzer.py` must be refactored (not rewritten) for semantic clustering
- Existing `metadata_optimizer.py` extended with screenshot caption section
- Existing `launch_checklist.py` updated with 2026 deadlines
- Existing `aso_scorer.py` scoring weights adjusted
- All 4 agent definitions updated with new knowledge

### External Dependencies
- iTunes RSS JSON endpoint availability (unofficial, could change)
- Apple App Store territory list (for region validation)
- 2026 compliance deadline confirmations from Apple/Google official docs

### Data Dependencies
- Users must provide Android Vitals data for technical scoring (Google Play)
- Users must provide target region (prompted if not given)
- Review analysis requires apps with at least 10 reviews for meaningful results

## Implementation Phases

### Phase 1: Research & Algorithm Update (Weeks 1-3)
- Update all agent definitions with 2026 algorithm knowledge
- Update compliance checklists with new deadlines
- Document all 15 major platform changes in knowledge base
- Update ASO scorer weights

### Phase 2: Region Targeting (Weeks 4-5)
- Add region prompt to all slash commands
- Update iTunes API wrapper with country parameter
- Validate against Apple territory list
- Test with JP, KR, DE, BR markets

### Phase 3: Review Integration (Weeks 6-8)
- Build `review_fetcher.py` module
- Implement RSS JSON endpoint wrapper
- Add sentiment analysis (rule-based, no external deps)
- Add review mining for keyword extraction
- Integrate into aso-research agent

### Phase 4: Semantic Keywords & Screenshots (Weeks 9-11)
- Refactor `keyword_analyzer.py` for intent clustering
- Add screenshot caption optimizer to `metadata_optimizer.py`
- Add natural language query generation
- Integrate into aso-optimizer agent

### Phase 5: CPP Strategy & Scoring (Weeks 12-14)
- Add CPP strategy module
- Update ASO scorer with technical performance category
- Update aso-strategist agent
- End-to-end testing with example app

### Phase 6: Integration Testing & Documentation (Weeks 15-16)
- Full workflow testing with sample apps
- Update all documentation (CLAUDE.md, README, USAGE, ARCHITECTURE)
- Create migration guide from v1.0 to v1.1
- Update FitFlow example with new features

## Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| iTunes RSS endpoint deprecated | HIGH | LOW | Document alternative scraping approach; monitor endpoint status |
| Semantic clustering without NLP libraries | MEDIUM | MEDIUM | Use TF-IDF approximation with standard library; keyword co-occurrence analysis |
| Google battery enforcement delayed | LOW | MEDIUM | Keep as optional check; update deadline when confirmed |
| Agent prompts too long with new knowledge | MEDIUM | HIGH | Modularize agent knowledge into separate reference files |
| Review sentiment accuracy without ML | MEDIUM | HIGH | Use rule-based approach with keyword lists; document accuracy limitations |

## Appendix: Platform Changes Reference (Nov 2025 → Feb 2026)

### Apple App Store
1. Screenshot captions now indexed for keyword ranking (June 2025)
2. Custom Product Pages expanded from 35 to 70
3. CPP keyword assignment for organic search visibility
4. AI-generated tags introduced (iOS 26)
5. Visual Intelligence screenshot interaction
6. Age rating restructured (2→5 categories, deadline: Jan 31, 2026)
7. 100+ new App Store Connect analytics metrics
8. Accessibility nutrition labels on product pages
9. Promo codes discontinued (March 26, 2026), replaced by expanded offer codes
10. SDK requirements: iOS 26 SDK required (April 28, 2026)
11. In-app events can be submitted separately from app versions
12. App Store Ads expansion (December 18, 2025)

### Google Play Store
13. Battery optimization as direct ranking factor (March 1, 2026)
14. Android Vitals (crash rate, ANR, wake locks) as primary signals
15. Semantic coherence over keyword stuffing (NLP spam detection)
16. Reviews as direct ranking factor (not just trust signal)
17. Hero content carousel and YouTube playlist carousel
18. Topic browse pages for enhanced discovery
19. Age Signals API restrictions (January 1, 2026)
20. US billing policy changes (January 28, 2026)

### Industry Shifts
21. ASO as strategy, not just optimization (Phiture)
22. Semantic keyword clusters over individual keywords (AppTweak)
23. Intent-driven algorithm transformation (Google)
24. Connected decision-making: ASO + paid synergy (SplitMetrics)
25. Community-led organic growth emphasis (Reddit/industry)

### Sources
- Apple Developer News, WWDC 2025 announcements
- Google Play Console Help announcements
- Phiture / The ASO Stack
- AppTweak Blog, MobileAction Blog
- SplitMetrics Blog
- Appfigures, ASOWorld
- Reddit r/AppStoreOptimization
