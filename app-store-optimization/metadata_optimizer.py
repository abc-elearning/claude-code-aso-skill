"""
Metadata optimization module for App Store Optimization.
Optimizes titles, descriptions, and keyword fields with platform-specific character limit validation.
"""

from typing import Dict, List, Any, Optional, Tuple
import re


class MetadataOptimizer:
    """Optimizes app store metadata for maximum discoverability and conversion."""

    # Platform-specific character limits
    CHAR_LIMITS = {
        'apple': {
            'title': 30,
            'subtitle': 30,
            'promotional_text': 170,
            'description': 4000,
            'keywords': 100,
            'whats_new': 4000
        },
        'google': {
            'title': 50,
            'short_description': 80,
            'full_description': 4000
        }
    }

    def __init__(self, platform: str = 'apple'):
        """
        Initialize metadata optimizer.

        Args:
            platform: 'apple' or 'google'
        """
        if platform not in ['apple', 'google']:
            raise ValueError("Platform must be 'apple' or 'google'")

        self.platform = platform
        self.limits = self.CHAR_LIMITS[platform]

    def optimize_title(
        self,
        app_name: str,
        target_keywords: List[str],
        include_brand: bool = True
    ) -> Dict[str, Any]:
        """
        Optimize app title with keyword integration.

        Args:
            app_name: Your app's brand name
            target_keywords: List of keywords to potentially include
            include_brand: Whether to include brand name

        Returns:
            Optimized title options with analysis
        """
        max_length = self.limits['title']

        title_options = []

        # Option 1: Brand name only
        if include_brand:
            option1 = app_name[:max_length]
            title_options.append({
                'title': option1,
                'length': len(option1),
                'remaining_chars': max_length - len(option1),
                'keywords_included': [],
                'strategy': 'brand_only',
                'pros': ['Maximum brand recognition', 'Clean and simple'],
                'cons': ['No keyword targeting', 'Lower discoverability']
            })

        # Option 2: Brand + Primary Keyword
        if target_keywords:
            primary_keyword = target_keywords[0]
            option2 = self._build_title_with_keywords(
                app_name,
                [primary_keyword],
                max_length
            )
            if option2:
                title_options.append({
                    'title': option2,
                    'length': len(option2),
                    'remaining_chars': max_length - len(option2),
                    'keywords_included': [primary_keyword],
                    'strategy': 'brand_plus_primary',
                    'pros': ['Targets main keyword', 'Maintains brand identity'],
                    'cons': ['Limited keyword coverage']
                })

        # Option 3: Brand + Multiple Keywords (if space allows)
        if len(target_keywords) > 1:
            option3 = self._build_title_with_keywords(
                app_name,
                target_keywords[:2],
                max_length
            )
            if option3:
                title_options.append({
                    'title': option3,
                    'length': len(option3),
                    'remaining_chars': max_length - len(option3),
                    'keywords_included': target_keywords[:2],
                    'strategy': 'brand_plus_multiple',
                    'pros': ['Multiple keyword targets', 'Better discoverability'],
                    'cons': ['May feel cluttered', 'Less brand focus']
                })

        # Option 4: Keyword-first approach (for new apps)
        if target_keywords and not include_brand:
            option4 = " ".join(target_keywords[:2])[:max_length]
            title_options.append({
                'title': option4,
                'length': len(option4),
                'remaining_chars': max_length - len(option4),
                'keywords_included': target_keywords[:2],
                'strategy': 'keyword_first',
                'pros': ['Maximum SEO benefit', 'Clear functionality'],
                'cons': ['No brand recognition', 'Generic appearance']
            })

        return {
            'platform': self.platform,
            'max_length': max_length,
            'options': title_options,
            'recommendation': self._recommend_title_option(title_options)
        }

    def optimize_description(
        self,
        app_info: Dict[str, Any],
        target_keywords: List[str],
        description_type: str = 'full'
    ) -> Dict[str, Any]:
        """
        Optimize app description with keyword integration and conversion focus.

        Args:
            app_info: Dict with 'name', 'key_features', 'unique_value', 'target_audience'
            target_keywords: List of keywords to integrate naturally
            description_type: 'full', 'short' (Google), 'subtitle' (Apple)

        Returns:
            Optimized description with analysis
        """
        if description_type == 'short' and self.platform == 'google':
            return self._optimize_short_description(app_info, target_keywords)
        elif description_type == 'subtitle' and self.platform == 'apple':
            return self._optimize_subtitle(app_info, target_keywords)
        else:
            return self._optimize_full_description(app_info, target_keywords)

    def optimize_keyword_field(
        self,
        target_keywords: List[str],
        app_title: str = "",
        app_description: str = ""
    ) -> Dict[str, Any]:
        """
        Optimize Apple's 100-character keyword field.

        Rules:
        - No spaces between commas
        - No plural forms if singular exists
        - No duplicates
        - Keywords in title/subtitle are already indexed

        Args:
            target_keywords: List of target keywords
            app_title: Current app title (to avoid duplication)
            app_description: Current description (to check coverage)

        Returns:
            Optimized keyword field (comma-separated, no spaces)
        """
        if self.platform != 'apple':
            return {'error': 'Keyword field optimization only applies to Apple App Store'}

        max_length = self.limits['keywords']

        # Extract words already in title (these don't need to be in keyword field)
        title_words = set(app_title.lower().split()) if app_title else set()

        # Process keywords
        processed_keywords = []
        for keyword in target_keywords:
            keyword_lower = keyword.lower().strip()

            # Skip if already in title
            if keyword_lower in title_words:
                continue

            # Remove duplicates and process
            words = keyword_lower.split()
            for word in words:
                if word not in processed_keywords and word not in title_words:
                    processed_keywords.append(word)

        # Remove plurals if singular exists
        deduplicated = self._remove_plural_duplicates(processed_keywords)

        # Build keyword field within 100 character limit
        keyword_field = self._build_keyword_field(deduplicated, max_length)

        # Calculate keyword density in description
        density = self._calculate_coverage(target_keywords, app_description)

        return {
            'keyword_field': keyword_field,
            'length': len(keyword_field),
            'remaining_chars': max_length - len(keyword_field),
            'keywords_included': keyword_field.split(','),
            'keywords_count': len(keyword_field.split(',')),
            'keywords_excluded': [kw for kw in target_keywords if kw.lower() not in keyword_field],
            'description_coverage': density,
            'optimization_tips': [
                'Keywords in title are auto-indexed - no need to repeat',
                'Use singular forms only (Apple indexes plurals automatically)',
                'No spaces between commas to maximize character usage',
                'Update keyword field with each app update to test variations'
            ]
        }

    def validate_character_limits(
        self,
        metadata: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Validate all metadata fields against platform character limits.

        Args:
            metadata: Dictionary of field_name: value

        Returns:
            Validation report with errors and warnings
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'field_status': {}
        }

        for field_name, value in metadata.items():
            if field_name not in self.limits:
                validation_results['warnings'].append(
                    f"Unknown field '{field_name}' for {self.platform} platform"
                )
                continue

            max_length = self.limits[field_name]
            actual_length = len(value)
            remaining = max_length - actual_length

            field_status = {
                'value': value,
                'length': actual_length,
                'limit': max_length,
                'remaining': remaining,
                'is_valid': actual_length <= max_length,
                'usage_percentage': round((actual_length / max_length) * 100, 1)
            }

            validation_results['field_status'][field_name] = field_status

            if actual_length > max_length:
                validation_results['is_valid'] = False
                validation_results['errors'].append(
                    f"'{field_name}' exceeds limit: {actual_length}/{max_length} chars"
                )
            elif remaining > max_length * 0.2:  # More than 20% unused
                validation_results['warnings'].append(
                    f"'{field_name}' under-utilizes space: {remaining} chars remaining"
                )

        return validation_results

    def calculate_keyword_density(
        self,
        text: str,
        target_keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Calculate keyword density in text.

        Args:
            text: Text to analyze
            target_keywords: Keywords to check

        Returns:
            Density analysis
        """
        text_lower = text.lower()
        total_words = len(text_lower.split())

        keyword_densities = {}
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            count = text_lower.count(keyword_lower)
            density = (count / total_words * 100) if total_words > 0 else 0

            keyword_densities[keyword] = {
                'occurrences': count,
                'density_percentage': round(density, 2),
                'status': self._assess_density(density)
            }

        # Overall assessment
        total_keyword_occurrences = sum(kw['occurrences'] for kw in keyword_densities.values())
        overall_density = (total_keyword_occurrences / total_words * 100) if total_words > 0 else 0

        return {
            'total_words': total_words,
            'keyword_densities': keyword_densities,
            'overall_keyword_density': round(overall_density, 2),
            'assessment': self._assess_overall_density(overall_density),
            'recommendations': self._generate_density_recommendations(keyword_densities)
        }

    def _build_title_with_keywords(
        self,
        app_name: str,
        keywords: List[str],
        max_length: int
    ) -> Optional[str]:
        """Build title combining app name and keywords within limit."""
        separators = [' - ', ': ', ' | ']

        for sep in separators:
            for kw in keywords:
                title = f"{app_name}{sep}{kw}"
                if len(title) <= max_length:
                    return title

        return None

    def _optimize_short_description(
        self,
        app_info: Dict[str, Any],
        target_keywords: List[str]
    ) -> Dict[str, Any]:
        """Optimize Google Play short description (80 chars)."""
        max_length = self.limits['short_description']

        # Focus on unique value proposition with primary keyword
        unique_value = app_info.get('unique_value', '')
        primary_keyword = target_keywords[0] if target_keywords else ''

        # Template: [Primary Keyword] - [Unique Value]
        short_desc = f"{primary_keyword.title()} - {unique_value}"[:max_length]

        return {
            'short_description': short_desc,
            'length': len(short_desc),
            'remaining_chars': max_length - len(short_desc),
            'keywords_included': [primary_keyword] if primary_keyword in short_desc.lower() else [],
            'strategy': 'keyword_value_proposition'
        }

    def _optimize_subtitle(
        self,
        app_info: Dict[str, Any],
        target_keywords: List[str]
    ) -> Dict[str, Any]:
        """Optimize Apple App Store subtitle (30 chars)."""
        max_length = self.limits['subtitle']

        # Very concise - primary keyword or key feature
        primary_keyword = target_keywords[0] if target_keywords else ''
        key_feature = app_info.get('key_features', [''])[0] if app_info.get('key_features') else ''

        options = [
            primary_keyword[:max_length],
            key_feature[:max_length],
            f"{primary_keyword} App"[:max_length]
        ]

        return {
            'subtitle_options': [opt for opt in options if opt],
            'max_length': max_length,
            'recommendation': options[0] if options else ''
        }

    def _optimize_full_description(
        self,
        app_info: Dict[str, Any],
        target_keywords: List[str]
    ) -> Dict[str, Any]:
        """Optimize full app description (4000 chars for both platforms)."""
        max_length = self.limits.get('description', self.limits.get('full_description', 4000))

        # Structure: Hook → Features → Benefits → Social Proof → CTA
        sections = []

        # Hook (with primary keyword)
        primary_keyword = target_keywords[0] if target_keywords else ''
        unique_value = app_info.get('unique_value', '')
        hook = f"{unique_value} {primary_keyword.title()} that helps you achieve more.\n\n"
        sections.append(hook)

        # Features (with keywords naturally integrated)
        features = app_info.get('key_features', [])
        if features:
            sections.append("KEY FEATURES:\n")
            for i, feature in enumerate(features[:5], 1):
                # Integrate keywords naturally
                feature_text = f"• {feature}"
                if i <= len(target_keywords):
                    keyword = target_keywords[i-1]
                    if keyword.lower() not in feature.lower():
                        feature_text = f"• {feature} with {keyword}"
                sections.append(f"{feature_text}\n")
            sections.append("\n")

        # Benefits
        target_audience = app_info.get('target_audience', 'users')
        sections.append(f"PERFECT FOR:\n{target_audience}\n\n")

        # Social proof placeholder
        sections.append("WHY USERS LOVE US:\n")
        sections.append("Join thousands of satisfied users who have transformed their workflow.\n\n")

        # CTA
        sections.append("Download now and start experiencing the difference!")

        # Combine and validate length
        full_description = "".join(sections)
        if len(full_description) > max_length:
            full_description = full_description[:max_length-3] + "..."

        # Calculate keyword density
        density = self.calculate_keyword_density(full_description, target_keywords)

        return {
            'full_description': full_description,
            'length': len(full_description),
            'remaining_chars': max_length - len(full_description),
            'keyword_analysis': density,
            'structure': {
                'has_hook': True,
                'has_features': len(features) > 0,
                'has_benefits': True,
                'has_cta': True
            }
        }

    def _remove_plural_duplicates(self, keywords: List[str]) -> List[str]:
        """Remove plural forms if singular exists."""
        deduplicated = []
        singular_set = set()

        for keyword in keywords:
            if keyword.endswith('s') and len(keyword) > 1:
                singular = keyword[:-1]
                if singular not in singular_set:
                    deduplicated.append(singular)
                    singular_set.add(singular)
            else:
                if keyword not in singular_set:
                    deduplicated.append(keyword)
                    singular_set.add(keyword)

        return deduplicated

    def _build_keyword_field(self, keywords: List[str], max_length: int) -> str:
        """Build comma-separated keyword field within character limit."""
        keyword_field = ""

        for keyword in keywords:
            test_field = f"{keyword_field},{keyword}" if keyword_field else keyword
            if len(test_field) <= max_length:
                keyword_field = test_field
            else:
                break

        return keyword_field

    def _calculate_coverage(self, keywords: List[str], text: str) -> Dict[str, int]:
        """Calculate how many keywords are covered in text."""
        text_lower = text.lower()
        coverage = {}

        for keyword in keywords:
            coverage[keyword] = text_lower.count(keyword.lower())

        return coverage

    def _assess_density(self, density: float) -> str:
        """Assess individual keyword density."""
        if density < 0.5:
            return "too_low"
        elif density <= 2.5:
            return "optimal"
        else:
            return "too_high"

    def _assess_overall_density(self, density: float) -> str:
        """Assess overall keyword density."""
        if density < 2:
            return "Under-optimized: Consider adding more keyword variations"
        elif density <= 5:
            return "Optimal: Good keyword integration without stuffing"
        elif density <= 8:
            return "High: Approaching keyword stuffing - reduce keyword usage"
        else:
            return "Too High: Keyword stuffing detected - rewrite for natural flow"

    def _generate_density_recommendations(
        self,
        keyword_densities: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations based on keyword density analysis."""
        recommendations = []

        for keyword, data in keyword_densities.items():
            if data['status'] == 'too_low':
                recommendations.append(
                    f"Increase usage of '{keyword}' - currently only {data['occurrences']} times"
                )
            elif data['status'] == 'too_high':
                recommendations.append(
                    f"Reduce usage of '{keyword}' - appears {data['occurrences']} times (keyword stuffing risk)"
                )

        if not recommendations:
            recommendations.append("Keyword density is well-balanced")

        return recommendations

    def _recommend_title_option(self, options: List[Dict[str, Any]]) -> str:
        """Recommend best title option based on strategy."""
        if not options:
            return "No valid options available"

        # Prefer brand_plus_primary for established apps
        for option in options:
            if option['strategy'] == 'brand_plus_primary':
                return f"Recommended: '{option['title']}' (Balance of brand and SEO)"

        # Fallback to first option
        return f"Recommended: '{options[0]['title']}' ({options[0]['strategy']})"

    # -------------------------------------------------------------------------
    # Screenshot Caption Optimizer (Apple indexes captions since June 2025)
    # -------------------------------------------------------------------------

    # Caption legibility guidance: recommended max characters for readability
    # on device screens at standard screenshot dimensions.
    CAPTION_CHAR_GUIDANCE = {
        'short': {'max_chars': 40, 'description': 'Best for small screenshots / compact layouts'},
        'medium': {'max_chars': 70, 'description': 'Standard caption length for most screenshots'},
        'long': {'max_chars': 100, 'description': 'Use sparingly; only for landscape or large display'},
    }

    # Natural caption templates that read well while incorporating keywords.
    # {kw} is replaced with a keyword or short keyword phrase.
    _CAPTION_TEMPLATES = [
        "Easily {kw} in seconds",
        "{kw} made simple",
        "Your personal {kw} assistant",
        "Smart {kw} at your fingertips",
        "Track and {kw} effortlessly",
        "Powerful {kw} tools",
        "Beautiful {kw} experience",
        "All your {kw} in one place",
        "{kw} with confidence",
        "Discover better {kw}",
        "Simplify your {kw}",
        "The smarter way to {kw}",
        "Master your {kw}",
        "{kw} like a pro",
        "Instant {kw} insights",
    ]

    def generate_screenshot_captions(
        self,
        keywords: List[str],
        existing_metadata: Dict[str, str],
        num_captions: int = 10,
        max_caption_length: int = 70
    ) -> Dict[str, Any]:
        """
        Generate screenshot caption recommendations using complementary keywords.

        Since June 2025, Apple indexes screenshot captions for keyword ranking.
        This method generates natural captions using keywords that are NOT already
        present in title, subtitle, or keyword field to maximize keyword coverage.

        Args:
            keywords: Full list of target keywords to consider
            existing_metadata: Dict with optional keys 'title', 'subtitle',
                              'keyword_field' containing current metadata text
            num_captions: Number of caption recommendations (5-10 recommended)
            max_caption_length: Maximum caption character count for readability

        Returns:
            Dict with caption recommendations, keyword coverage analysis,
            and legibility guidance
        """
        # Clamp num_captions to 5-10 range
        num_captions = max(5, min(10, num_captions))

        # Step 1: Collect all words already used in existing metadata
        used_words = set()
        for field in ['title', 'subtitle', 'keyword_field']:
            value = existing_metadata.get(field, '')
            if value:
                # For keyword_field, split on commas; for others, split on whitespace
                if field == 'keyword_field':
                    tokens = [w.strip().lower() for w in value.split(',')]
                else:
                    tokens = value.lower().split()
                used_words.update(tokens)

        # Step 2: Filter keywords to only complementary (unused) ones
        complementary_keywords = []
        already_covered = []
        for kw in keywords:
            kw_lower = kw.lower().strip()
            kw_words = set(kw_lower.split())
            # A keyword is "already covered" if ALL its words appear in used metadata
            if kw_words.issubset(used_words):
                already_covered.append(kw)
            else:
                complementary_keywords.append(kw)

        # Step 3: Generate natural captions from complementary keywords
        captions = []
        templates_used = 0
        for kw in complementary_keywords:
            if len(captions) >= num_captions:
                break

            template = self._CAPTION_TEMPLATES[templates_used % len(self._CAPTION_TEMPLATES)]
            caption_text = template.format(kw=kw.lower())

            # Capitalize first letter
            caption_text = caption_text[0].upper() + caption_text[1:]

            char_count = len(caption_text)

            # Determine readability tier
            if char_count <= self.CAPTION_CHAR_GUIDANCE['short']['max_chars']:
                readability = 'excellent'
                readability_note = 'Short and punchy - great readability on all devices'
            elif char_count <= self.CAPTION_CHAR_GUIDANCE['medium']['max_chars']:
                readability = 'good'
                readability_note = 'Standard length - readable on most screenshot layouts'
            elif char_count <= self.CAPTION_CHAR_GUIDANCE['long']['max_chars']:
                readability = 'acceptable'
                readability_note = 'Long - consider only for landscape or hero screenshots'
            else:
                # Truncate to max and re-evaluate
                caption_text = caption_text[:max_caption_length]
                char_count = len(caption_text)
                readability = 'truncated'
                readability_note = f'Truncated to {max_caption_length} chars for legibility'

            # Extract which keywords from our list appear in this caption
            keywords_used = [
                k for k in complementary_keywords
                if k.lower() in caption_text.lower()
            ]

            captions.append({
                'caption': caption_text,
                'keywords_used': keywords_used,
                'char_count': char_count,
                'readability': readability,
                'readability_note': readability_note,
            })
            templates_used += 1

        # Step 4: Build summary
        all_keywords_in_captions = set()
        for c in captions:
            for k in c['keywords_used']:
                all_keywords_in_captions.add(k.lower())

        return {
            'platform': self.platform,
            'captions': captions,
            'caption_count': len(captions),
            'keyword_coverage': {
                'total_input_keywords': len(keywords),
                'already_in_metadata': len(already_covered),
                'complementary_available': len(complementary_keywords),
                'used_in_captions': len(all_keywords_in_captions),
                'already_covered_keywords': already_covered,
                'complementary_keywords': complementary_keywords,
            },
            'character_guidance': self.CAPTION_CHAR_GUIDANCE,
            'best_practices': [
                'Screenshot captions are indexed by Apple for keyword ranking (June 2025)',
                'Use keywords NOT already in title/subtitle/keyword field for maximum coverage',
                'Keep captions natural and readable - avoid keyword stuffing',
                'Shorter captions (under 40 chars) have best readability on small devices',
                'Each screenshot should highlight a different feature or keyword theme',
                'Test caption readability at actual screenshot size before submission',
                'Captions should complement the visual content of each screenshot',
            ],
        }

    # -------------------------------------------------------------------------
    # Custom Product Page (CPP) Strategy
    # -------------------------------------------------------------------------

    # Maximum number of Custom Product Pages allowed by Apple
    MAX_CPP_COUNT = 70

    def generate_cpp_metadata(
        self,
        segments: List[str],
        keywords: List[str],
        keyword_clusters: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate metadata for Apple Custom Product Pages (CPPs).

        Creates per-segment CPP configurations with tailored title variants,
        subtitle variants, keyword assignments, and screenshot focus areas.
        Supports both organic search CPPs and paid acquisition CPPs.

        Args:
            segments: User segments to create CPPs for
                     (e.g., ["beginners", "power users", "enterprise"])
            keywords: Full keyword list to distribute across CPPs
            keyword_clusters: Optional list of cluster dicts from
                            keyword_analyzer.cluster_by_intent(). Each cluster
                            has keys: {name, intent, keywords, keyword_count,
                            natural_queries, combined_score}

        Returns:
            Dict with CPP configurations, validation results, and strategy notes

        Raises:
            ValueError: If total CPP count exceeds 70 (Apple limit)
        """
        if self.platform != 'apple':
            return {
                'error': 'Custom Product Pages are only available on Apple App Store',
                'suggestion': 'Use Google Play Store Listing Experiments for A/B testing on Google'
            }

        # Calculate total CPPs needed: organic + paid variants per segment
        # Organic: 1 per segment, Paid: 1 per segment (for Apple Search Ads)
        organic_count = len(segments)
        paid_count = len(segments)
        total_cpps = organic_count + paid_count

        if total_cpps > self.MAX_CPP_COUNT:
            raise ValueError(
                f"Total CPP count ({total_cpps}) exceeds Apple limit of "
                f"{self.MAX_CPP_COUNT}. Reduce segments from {len(segments)} "
                f"to at most {self.MAX_CPP_COUNT // 2}."
            )

        # Build keyword-to-cluster mapping if clusters are provided
        keyword_cluster_map = {}
        if keyword_clusters:
            for cluster in keyword_clusters:
                for kw in cluster.get('keywords', []):
                    keyword_cluster_map[kw.lower()] = {
                        'cluster_name': cluster.get('name', 'General'),
                        'intent': cluster.get('intent', 'general'),
                        'combined_score': cluster.get('combined_score', 0),
                    }

        # Distribute keywords across segments
        segment_keywords = self._distribute_keywords_to_segments(
            segments, keywords, keyword_cluster_map
        )

        # Generate CPP metadata for each segment
        organic_cpps = []
        paid_cpps = []

        for segment in segments:
            seg_kws = segment_keywords.get(segment, [])

            # --- Organic CPP ---
            organic_cpp = self._build_cpp_for_segment(
                segment=segment,
                assigned_keywords=seg_kws,
                cpp_type='organic',
                keyword_cluster_map=keyword_cluster_map,
            )
            organic_cpps.append(organic_cpp)

            # --- Paid CPP (Apple Search Ads) ---
            paid_cpp = self._build_cpp_for_segment(
                segment=segment,
                assigned_keywords=seg_kws,
                cpp_type='paid',
                keyword_cluster_map=keyword_cluster_map,
            )
            paid_cpps.append(paid_cpp)

        # Validation pass
        validation = self._validate_cpp_metadata(organic_cpps + paid_cpps)

        return {
            'platform': 'apple',
            'total_cpps': total_cpps,
            'max_allowed': self.MAX_CPP_COUNT,
            'remaining_slots': self.MAX_CPP_COUNT - total_cpps,
            'organic_cpps': organic_cpps,
            'paid_cpps': paid_cpps,
            'segment_keyword_distribution': {
                seg: kws for seg, kws in segment_keywords.items()
            },
            'validation': validation,
            'strategy_notes': {
                'organic': (
                    'Organic CPPs appear in App Store search results based on '
                    'keyword relevance. Tailor each page to a specific user intent '
                    'so Apple can match the right page to the right query.'
                ),
                'paid': (
                    'Paid CPPs are used with Apple Search Ads. Each paid CPP should '
                    'have messaging aligned to the ad keyword theme. Use strong CTAs '
                    'and social proof specific to the target segment.'
                ),
                'best_practices': [
                    'Create separate CPPs for distinct user segments (beginners vs experts)',
                    'Align screenshot order with segment priorities',
                    'Use segment-specific language in title and subtitle variants',
                    'Test CPP performance monthly and retire underperformers',
                    'Organic CPPs should focus on different keyword themes',
                    'Paid CPPs should mirror the ad copy messaging',
                    'Apple allows up to 70 CPPs - start with 3-5 and expand based on data',
                    'Each CPP can have unique screenshots, app previews, and promotional text',
                ],
            },
        }

    def _distribute_keywords_to_segments(
        self,
        segments: List[str],
        keywords: List[str],
        keyword_cluster_map: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """
        Distribute keywords across segments using intent clusters when available.

        Strategy:
        - If keyword_clusters provided, match cluster intents to segments
        - Otherwise, round-robin distribute keywords evenly
        """
        segment_keywords: Dict[str, List[str]] = {seg: [] for seg in segments}

        if keyword_cluster_map:
            # Group keywords by intent
            intent_groups: Dict[str, List[str]] = {}
            unclustered: List[str] = []
            for kw in keywords:
                info = keyword_cluster_map.get(kw.lower())
                if info:
                    intent = info['intent']
                    intent_groups.setdefault(intent, []).append(kw)
                else:
                    unclustered.append(kw)

            # Map intent groups to segments in order
            intent_list = list(intent_groups.items())
            for idx, segment in enumerate(segments):
                # Assign primary intent cluster
                if idx < len(intent_list):
                    _, cluster_kws = intent_list[idx]
                    segment_keywords[segment].extend(cluster_kws)
                # Distribute unclustered keywords round-robin
                for j, kw in enumerate(unclustered):
                    if j % len(segments) == idx:
                        segment_keywords[segment].append(kw)
        else:
            # Simple round-robin distribution
            for i, kw in enumerate(keywords):
                target_segment = segments[i % len(segments)]
                segment_keywords[target_segment].append(kw)

        return segment_keywords

    def _build_cpp_for_segment(
        self,
        segment: str,
        assigned_keywords: List[str],
        cpp_type: str,
        keyword_cluster_map: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build a single CPP configuration for a segment."""
        title_limit = self.limits['title']      # 30 chars
        subtitle_limit = self.limits['subtitle']  # 30 chars

        # Determine primary keyword for this segment
        primary_kw = assigned_keywords[0] if assigned_keywords else segment

        # Generate title variant
        if cpp_type == 'organic':
            title_variant = self._generate_cpp_title(
                segment, primary_kw, title_limit
            )
            subtitle_variant = self._generate_cpp_subtitle(
                segment, assigned_keywords, subtitle_limit
            )
        else:
            # Paid CPPs use more direct, CTA-oriented language
            title_variant = self._generate_cpp_title_paid(
                segment, primary_kw, title_limit
            )
            subtitle_variant = self._generate_cpp_subtitle_paid(
                segment, assigned_keywords, subtitle_limit
            )

        # Determine screenshot focus based on segment
        screenshot_focus = self._determine_screenshot_focus(segment, assigned_keywords)

        # Determine dominant intent from assigned keywords
        dominant_intent = 'general'
        if keyword_cluster_map and assigned_keywords:
            intent_counts: Dict[str, int] = {}
            for kw in assigned_keywords:
                info = keyword_cluster_map.get(kw.lower())
                if info:
                    intent = info['intent']
                    intent_counts[intent] = intent_counts.get(intent, 0) + 1
            if intent_counts:
                dominant_intent = max(intent_counts, key=intent_counts.get)

        return {
            'segment': segment,
            'cpp_type': cpp_type,
            'title_variant': title_variant,
            'title_char_count': len(title_variant),
            'title_limit': title_limit,
            'subtitle_variant': subtitle_variant,
            'subtitle_char_count': len(subtitle_variant),
            'subtitle_limit': subtitle_limit,
            'keyword_assignment': assigned_keywords[:10],  # Top 10 per CPP
            'keyword_count': min(len(assigned_keywords), 10),
            'dominant_intent': dominant_intent,
            'screenshot_focus': screenshot_focus,
        }

    def _generate_cpp_title(
        self, segment: str, primary_kw: str, limit: int
    ) -> str:
        """Generate an organic CPP title variant within character limit."""
        # Try keyword-focused title first
        candidates = [
            f"{primary_kw.title()}",
            f"{primary_kw.title()} App",
            f"Best {primary_kw.title()}",
            f"{segment.title()} {primary_kw.title()}",
        ]
        for candidate in candidates:
            if len(candidate) <= limit:
                return candidate
        # Fallback: truncate primary keyword
        return primary_kw.title()[:limit]

    def _generate_cpp_title_paid(
        self, segment: str, primary_kw: str, limit: int
    ) -> str:
        """Generate a paid CPP title variant with CTA focus."""
        candidates = [
            f"Try {primary_kw.title()} Free",
            f"Get {primary_kw.title()} Now",
            f"{primary_kw.title()} - Free",
            f"Start {primary_kw.title()}",
        ]
        for candidate in candidates:
            if len(candidate) <= limit:
                return candidate
        return primary_kw.title()[:limit]

    def _generate_cpp_subtitle(
        self, segment: str, keywords: List[str], limit: int
    ) -> str:
        """Generate an organic CPP subtitle variant."""
        seg_lower = segment.lower()
        secondary_kw = keywords[1] if len(keywords) > 1 else ''

        candidates = [
            f"Made for {seg_lower}",
            f"Perfect for {seg_lower}",
            f"{secondary_kw.title()} for {seg_lower}" if secondary_kw else '',
            f"Built for {seg_lower}",
        ]
        candidates = [c for c in candidates if c]
        for candidate in candidates:
            if len(candidate) <= limit:
                return candidate
        return f"For {seg_lower}"[:limit]

    def _generate_cpp_subtitle_paid(
        self, segment: str, keywords: List[str], limit: int
    ) -> str:
        """Generate a paid CPP subtitle variant with urgency/CTA."""
        seg_lower = segment.lower()
        candidates = [
            f"Join millions of {seg_lower}",
            f"#1 app for {seg_lower}",
            f"Loved by {seg_lower}",
            f"Top rated for {seg_lower}",
        ]
        for candidate in candidates:
            if len(candidate) <= limit:
                return candidate
        return f"For {seg_lower}"[:limit]

    def _determine_screenshot_focus(
        self, segment: str, keywords: List[str]
    ) -> List[str]:
        """Determine screenshot focus areas based on segment and keywords."""
        seg_lower = segment.lower()

        # Map common segment types to recommended screenshot themes
        segment_screenshot_map = {
            'beginner': [
                'Onboarding simplicity',
                'Getting started flow',
                'Simple UI overview',
                'Quick start guide visual',
            ],
            'power user': [
                'Advanced features showcase',
                'Customization options',
                'Keyboard shortcuts / power tools',
                'Workflow automation examples',
            ],
            'enterprise': [
                'Team collaboration features',
                'Admin dashboard / controls',
                'Security and compliance badges',
                'Integration ecosystem',
            ],
            'professional': [
                'Productivity metrics',
                'Professional templates',
                'Export and sharing options',
                'Cross-device sync',
            ],
            'student': [
                'Study tools and features',
                'Affordable pricing',
                'Collaboration with classmates',
                'Offline access capability',
            ],
        }

        # Find best matching segment focus
        for key, focus in segment_screenshot_map.items():
            if key in seg_lower:
                return focus

        # Default: generic focus areas incorporating keywords
        focus = ['Key feature highlight', 'User interface overview']
        for kw in keywords[:2]:
            focus.append(f"Showcase {kw.lower()} capability")
        return focus

    def _validate_cpp_metadata(
        self, all_cpps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate all CPP metadata against Apple character limits."""
        errors = []
        warnings = []

        for cpp in all_cpps:
            label = f"{cpp['cpp_type'].upper()} CPP [{cpp['segment']}]"

            if cpp['title_char_count'] > cpp['title_limit']:
                errors.append(
                    f"{label}: Title exceeds {cpp['title_limit']} chars "
                    f"({cpp['title_char_count']} chars): '{cpp['title_variant']}'"
                )
            if cpp['subtitle_char_count'] > cpp['subtitle_limit']:
                errors.append(
                    f"{label}: Subtitle exceeds {cpp['subtitle_limit']} chars "
                    f"({cpp['subtitle_char_count']} chars): '{cpp['subtitle_variant']}'"
                )
            if cpp['keyword_count'] == 0:
                warnings.append(
                    f"{label}: No keywords assigned - CPP may not rank for any queries"
                )

        return {
            'is_valid': len(errors) == 0,
            'error_count': len(errors),
            'warning_count': len(warnings),
            'errors': errors,
            'warnings': warnings,
        }


def optimize_app_metadata(
    platform: str,
    app_info: Dict[str, Any],
    target_keywords: List[str]
) -> Dict[str, Any]:
    """
    Convenience function to optimize all metadata fields.

    Args:
        platform: 'apple' or 'google'
        app_info: App information dictionary
        target_keywords: Target keywords list

    Returns:
        Complete metadata optimization package
    """
    optimizer = MetadataOptimizer(platform)

    return {
        'platform': platform,
        'title': optimizer.optimize_title(
            app_info['name'],
            target_keywords
        ),
        'description': optimizer.optimize_description(
            app_info,
            target_keywords,
            'full'
        ),
        'keyword_field': optimizer.optimize_keyword_field(
            target_keywords
        ) if platform == 'apple' else None
    }
