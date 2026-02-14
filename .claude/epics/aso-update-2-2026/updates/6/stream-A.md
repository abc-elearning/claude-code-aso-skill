# Issue #6: Add screenshot caption optimizer and CPP strategy to metadata optimizer

## Status: COMPLETED

## Summary
Extended `metadata_optimizer.py` with two new methods: `generate_screenshot_captions()` for Apple screenshot caption optimization (indexed since June 2025) and `generate_cpp_metadata()` for Custom Product Page strategy generation.

## Implementation Details

### 1. `generate_screenshot_captions(keywords, existing_metadata, num_captions, max_caption_length)`

**Location:** `MetadataOptimizer` class in `app-store-optimization/metadata_optimizer.py`

**Purpose:** Since June 2025, Apple indexes screenshot captions for keyword ranking. This method generates natural-sounding captions using complementary keywords NOT already present in title/subtitle/keyword field.

**Algorithm:**
1. Collects all words already used in existing metadata (title, subtitle, keyword_field)
2. Filters input keywords to only complementary (unused) ones - a keyword is "already covered" if ALL its words appear in existing metadata
3. Generates natural captions from 15 rotating templates (e.g., "Easily {kw} in seconds", "{kw} made simple")
4. Classifies each caption by readability tier: short (<=40 chars), medium (<=70 chars), long (<=100 chars)

**Return structure:**
```python
{
    'platform': 'apple',
    'captions': [
        {
            'caption': 'Goal setting made simple',
            'keywords_used': ['goal setting'],
            'char_count': 24,
            'readability': 'excellent',
            'readability_note': 'Short and punchy - great readability on all devices',
        }
    ],
    'caption_count': 6,
    'keyword_coverage': {
        'total_input_keywords': 12,
        'already_in_metadata': 6,
        'complementary_available': 6,
        'used_in_captions': 6,
        'already_covered_keywords': [...],
        'complementary_keywords': [...],
    },
    'character_guidance': {...},
    'best_practices': [...],
}
```

**Supporting constants:**
- `CAPTION_CHAR_GUIDANCE` - Readability tiers (short/medium/long) with max char counts
- `_CAPTION_TEMPLATES` - 15 natural language templates for caption generation

### 2. `generate_cpp_metadata(segments, keywords, keyword_clusters=None)`

**Location:** `MetadataOptimizer` class in `app-store-optimization/metadata_optimizer.py`

**Purpose:** Generates per-segment Custom Product Page configurations for both organic search and paid (Apple Search Ads) CPPs.

**Algorithm:**
1. Calculates total CPPs needed (organic + paid per segment)
2. Validates count <= 70 (raises `ValueError` if exceeded)
3. If `keyword_clusters` provided (from `keyword_analyzer.cluster_by_intent()`), maps clusters to segments by intent
4. Otherwise, distributes keywords round-robin across segments
5. Generates organic CPPs with keyword-focused titles and segment-specific subtitles
6. Generates paid CPPs with CTA-oriented titles and urgency-driven subtitles
7. Validates all metadata against Apple character limits (30/30 for title/subtitle)

**Return structure:**
```python
{
    'platform': 'apple',
    'total_cpps': 6,
    'max_allowed': 70,
    'remaining_slots': 64,
    'organic_cpps': [
        {
            'segment': 'beginners',
            'cpp_type': 'organic',
            'title_variant': 'Task Manager',
            'title_char_count': 12,
            'title_limit': 30,
            'subtitle_variant': 'Made for beginners',
            'subtitle_char_count': 18,
            'subtitle_limit': 30,
            'keyword_assignment': ['task manager', ...],
            'keyword_count': 4,
            'dominant_intent': 'manage',
            'screenshot_focus': ['Onboarding simplicity', ...],
        }
    ],
    'paid_cpps': [...],
    'segment_keyword_distribution': {...},
    'validation': {'is_valid': True, ...},
    'strategy_notes': {...},
}
```

**Supporting methods (private):**
- `_distribute_keywords_to_segments()` - Intent-aware keyword distribution using clusters
- `_build_cpp_for_segment()` - Builds single CPP configuration
- `_generate_cpp_title()` / `_generate_cpp_title_paid()` - Title generation for organic/paid
- `_generate_cpp_subtitle()` / `_generate_cpp_subtitle_paid()` - Subtitle generation for organic/paid
- `_determine_screenshot_focus()` - Maps segment types to screenshot theme recommendations
- `_validate_cpp_metadata()` - Validates all CPPs against character limits

**Supporting constants:**
- `MAX_CPP_COUNT = 70` - Apple's maximum CPP limit

### 3. Synced to agent-integrated skill location

File copied to `.claude/skills/aso/metadata_optimizer.py` and verified identical with `diff`.

## Testing Results

### Test 1: Syntax check
```bash
python3 app-store-optimization/metadata_optimizer.py
```
**Result:** Passes with no errors.

### Test 2: Screenshot caption generation
- 12 input keywords, 6 already in metadata, 6 complementary
- 6 captions generated (clamped to available complementary keywords)
- All captions use natural language templates
- All readability classifications correct (excellent/good/acceptable)
- Complementary keyword filtering verified - no caption uses keywords already in title/subtitle/keyword field

### Test 3: CPP metadata generation (basic)
- 3 segments, 12 keywords, no clusters
- 6 CPPs generated (3 organic + 3 paid)
- All title variants within 30 chars
- All subtitle variants within 30 chars
- Round-robin keyword distribution verified
- Screenshot focus areas match segment types (beginner/power user/enterprise)

### Test 4: CPP count validation
- 36 segments (72 CPPs) correctly raises `ValueError`
- Error message includes current count, limit, and max segments suggestion

### Test 5: Google platform rejection
- `generate_cpp_metadata()` on Google platform returns error dict
- Suggests Google Play Store Listing Experiments as alternative

### Test 6: CPP with keyword_clusters
- 3 mock clusters (manage/plan/track intents)
- Keywords distributed by intent: beginners=manage, power users=track, enterprise=plan
- Dominant intent correctly identified per segment
- Unclustered keywords distributed round-robin

## Files Modified

1. `/Users/truongnguyen/workspace/claude-code-aso-skill/app-store-optimization/metadata_optimizer.py`
   - Added `CAPTION_CHAR_GUIDANCE` class constant
   - Added `_CAPTION_TEMPLATES` class constant
   - Added `MAX_CPP_COUNT = 70` class constant
   - Added `generate_screenshot_captions()` method (~100 lines)
   - Added `generate_cpp_metadata()` method (~80 lines)
   - Added 8 private helper methods (~200 lines)

2. `/Users/truongnguyen/workspace/claude-code-aso-skill/.claude/skills/aso/metadata_optimizer.py`
   - Synced copy (verified identical with diff)

## Acceptance Criteria Verification

- [x] `generate_screenshot_captions(keywords, existing_metadata)` method added
- [x] Captions use complementary keywords (automatically excludes keywords already in title/subtitle/keyword field)
- [x] 5-10 caption recommendations generated per call (clamped to range)
- [x] Each caption reads naturally (no keyword stuffing) - uses 15 natural templates
- [x] Character count guidance for caption legibility provided (short/medium/long tiers)
- [x] `generate_cpp_metadata(segments, keywords)` method added
- [x] Per-CPP metadata includes: title variant, subtitle variant, keyword assignment, screenshot focus
- [x] CPP count validated <= 70 (raises ValueError if exceeded)
- [x] Strategy differentiates organic CPPs vs paid CPPs
- [x] Output format integrates with existing metadata output structure
- [x] Apple character limits enforced (30/30 for title/subtitle)
- [x] Both skill copies synced
- [x] Zero external dependencies maintained
- [x] `python3 metadata_optimizer.py` passes syntax check

## Dependencies

- Task 5 (cluster_by_intent) output format supported via `keyword_clusters` parameter
- Method works without clusters (falls back to round-robin distribution)

## Completion Date
2026-02-14

## Time Spent
~20 minutes (implementation + testing + documentation)
