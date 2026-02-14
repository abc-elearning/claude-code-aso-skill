"""
ASO scoring module for App Store Optimization.
Calculates comprehensive ASO health score across multiple dimensions.
Supports platform-specific weighting for Apple App Store and Google Play Store.
"""

from typing import Dict, List, Any, Optional, Tuple


class ASOScorer:
    """Calculates overall ASO health score and provides recommendations."""

    # Default score weights for different components (total = 100)
    WEIGHTS = {
        'metadata_quality': 20,
        'ratings_reviews': 20,
        'keyword_performance': 20,
        'conversion_metrics': 20,
        'technical_performance': 15,
        'visual_optimization': 5
    }

    # Google Play Store weights - technical performance weighted higher
    # due to Android Vitals visibility and ranking impact
    GOOGLE_WEIGHTS = {
        'metadata_quality': 20,
        'ratings_reviews': 20,
        'keyword_performance': 20,
        'conversion_metrics': 15,
        'technical_performance': 20,
        'visual_optimization': 5
    }

    # Apple App Store weights - visual optimization weighted higher
    # due to CPP (Custom Product Pages) and editorial feature consideration
    APPLE_WEIGHTS = {
        'metadata_quality': 20,
        'ratings_reviews': 20,
        'keyword_performance': 20,
        'conversion_metrics': 20,
        'technical_performance': 10,
        'visual_optimization': 10
    }

    # Assert all weight configurations sum to 100
    assert sum(WEIGHTS.values()) == 100, f"Default WEIGHTS must sum to 100, got {sum(WEIGHTS.values())}"
    assert sum(GOOGLE_WEIGHTS.values()) == 100, f"GOOGLE_WEIGHTS must sum to 100, got {sum(GOOGLE_WEIGHTS.values())}"
    assert sum(APPLE_WEIGHTS.values()) == 100, f"APPLE_WEIGHTS must sum to 100, got {sum(APPLE_WEIGHTS.values())}"

    # Benchmarks for scoring
    BENCHMARKS = {
        'title_keyword_usage': {'min': 1, 'target': 2},
        'description_length': {'min': 500, 'target': 2000},
        'keyword_density': {'min': 2, 'optimal': 5, 'max': 8},
        'average_rating': {'min': 3.5, 'target': 4.5},
        'ratings_count': {'min': 100, 'target': 5000},
        'keywords_top_10': {'min': 2, 'target': 10},
        'keywords_top_50': {'min': 5, 'target': 20},
        'conversion_rate': {'min': 0.02, 'target': 0.10}
    }

    # Technical performance benchmarks
    TECHNICAL_BENCHMARKS = {
        'crash_rate': {'good': 1.0, 'acceptable': 2.0},      # percentage
        'anr_rate': {'good': 0.5, 'acceptable': 1.0},         # percentage (Android)
        'battery_impact': {'good': 5.0, 'acceptable': 10.0}   # percentage
    }

    def __init__(self, platform: Optional[str] = None):
        """
        Initialize ASO scorer.

        Args:
            platform: Optional platform identifier ('apple', 'google', or None for default).
                      When set, platform-specific weights are used automatically.
        """
        self.score_breakdown = {}
        self.platform = platform.lower() if platform else None
        self._active_weights = self._resolve_weights()

    def _resolve_weights(self) -> Dict[str, int]:
        """Resolve which weight configuration to use based on platform."""
        if self.platform == 'google':
            return dict(self.GOOGLE_WEIGHTS)
        elif self.platform == 'apple':
            return dict(self.APPLE_WEIGHTS)
        return dict(self.WEIGHTS)

    def calculate_overall_score(
        self,
        metadata: Dict[str, Any],
        ratings: Dict[str, Any],
        keyword_performance: Dict[str, Any],
        conversion: Dict[str, Any],
        technical_data: Optional[Dict[str, Any]] = None,
        visual_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive ASO score (0-100).

        Args:
            metadata: Title, description quality metrics
            ratings: Rating average and count
            keyword_performance: Keyword ranking data
            conversion: Impression-to-install metrics
            technical_data: Optional technical performance data
                           (crash_rate, anr_rate, battery_impact).
                           Defaults to neutral score (50) when not provided.
            visual_data: Optional visual optimization data
                        (has_captions, cpp_count, has_video).
                        Defaults to neutral score (50) when not provided.

        Returns:
            Overall score with detailed breakdown
        """
        weights = self._active_weights

        # Calculate component scores
        metadata_score = self.score_metadata_quality(metadata)
        ratings_score = self.score_ratings_reviews(ratings)
        keyword_score = self.score_keyword_performance(keyword_performance)
        conversion_score = self.score_conversion_metrics(conversion)

        # Technical and visual scores default to neutral (50) for backward compatibility
        if technical_data is not None:
            technical_score = self.score_technical_performance(**technical_data)
        else:
            technical_score = 50.0

        if visual_data is not None:
            visual_score = self.score_visual_optimization(**visual_data)
        else:
            visual_score = 50.0

        # Calculate weighted overall score
        overall_score = (
            metadata_score * (weights['metadata_quality'] / 100) +
            ratings_score * (weights['ratings_reviews'] / 100) +
            keyword_score * (weights['keyword_performance'] / 100) +
            conversion_score * (weights['conversion_metrics'] / 100) +
            technical_score * (weights['technical_performance'] / 100) +
            visual_score * (weights['visual_optimization'] / 100)
        )

        # Store breakdown
        self.score_breakdown = {
            'metadata_quality': {
                'score': metadata_score,
                'weight': weights['metadata_quality'],
                'weighted_contribution': round(metadata_score * (weights['metadata_quality'] / 100), 1)
            },
            'ratings_reviews': {
                'score': ratings_score,
                'weight': weights['ratings_reviews'],
                'weighted_contribution': round(ratings_score * (weights['ratings_reviews'] / 100), 1)
            },
            'keyword_performance': {
                'score': keyword_score,
                'weight': weights['keyword_performance'],
                'weighted_contribution': round(keyword_score * (weights['keyword_performance'] / 100), 1)
            },
            'conversion_metrics': {
                'score': conversion_score,
                'weight': weights['conversion_metrics'],
                'weighted_contribution': round(conversion_score * (weights['conversion_metrics'] / 100), 1)
            },
            'technical_performance': {
                'score': technical_score,
                'weight': weights['technical_performance'],
                'weighted_contribution': round(technical_score * (weights['technical_performance'] / 100), 1),
                'data_provided': technical_data is not None
            },
            'visual_optimization': {
                'score': visual_score,
                'weight': weights['visual_optimization'],
                'weighted_contribution': round(visual_score * (weights['visual_optimization'] / 100), 1),
                'data_provided': visual_data is not None
            }
        }

        # Generate recommendations
        recommendations = self.generate_recommendations(
            metadata_score,
            ratings_score,
            keyword_score,
            conversion_score,
            technical_score,
            visual_score
        )

        # Assess overall health
        health_status = self._assess_health_status(overall_score)

        return {
            'overall_score': round(overall_score, 1),
            'health_status': health_status,
            'platform': self.platform or 'default',
            'weights_used': weights,
            'score_breakdown': self.score_breakdown,
            'recommendations': recommendations,
            'priority_actions': self._prioritize_actions(recommendations),
            'strengths': self._identify_strengths(self.score_breakdown),
            'weaknesses': self._identify_weaknesses(self.score_breakdown)
        }

    def score_metadata_quality(self, metadata: Dict[str, Any]) -> float:
        """
        Score metadata quality (0-100).

        Evaluates:
        - Title optimization
        - Description quality
        - Keyword usage
        """
        scores = []

        # Title score (0-35 points)
        title_keywords = metadata.get('title_keyword_count', 0)
        title_length = metadata.get('title_length', 0)

        title_score = 0
        if title_keywords >= self.BENCHMARKS['title_keyword_usage']['target']:
            title_score = 35
        elif title_keywords >= self.BENCHMARKS['title_keyword_usage']['min']:
            title_score = 25
        else:
            title_score = 10

        # Adjust for title length usage
        if title_length > 25:  # Using most of available space
            title_score += 0
        else:
            title_score -= 5

        scores.append(min(title_score, 35))

        # Description score (0-35 points)
        desc_length = metadata.get('description_length', 0)
        desc_quality = metadata.get('description_quality', 0.0)  # 0-1 scale

        desc_score = 0
        if desc_length >= self.BENCHMARKS['description_length']['target']:
            desc_score = 25
        elif desc_length >= self.BENCHMARKS['description_length']['min']:
            desc_score = 15
        else:
            desc_score = 5

        # Add quality bonus
        desc_score += desc_quality * 10
        scores.append(min(desc_score, 35))

        # Keyword density score (0-30 points)
        keyword_density = metadata.get('keyword_density', 0.0)

        if self.BENCHMARKS['keyword_density']['min'] <= keyword_density <= self.BENCHMARKS['keyword_density']['optimal']:
            density_score = 30
        elif keyword_density < self.BENCHMARKS['keyword_density']['min']:
            # Too low - proportional scoring
            density_score = (keyword_density / self.BENCHMARKS['keyword_density']['min']) * 20
        else:
            # Too high (keyword stuffing) - penalty
            excess = keyword_density - self.BENCHMARKS['keyword_density']['optimal']
            density_score = max(30 - (excess * 5), 0)

        scores.append(density_score)

        return round(sum(scores), 1)

    def score_ratings_reviews(self, ratings: Dict[str, Any]) -> float:
        """
        Score ratings and reviews (0-100).

        Evaluates:
        - Average rating
        - Total ratings count
        - Review velocity
        """
        average_rating = ratings.get('average_rating', 0.0)
        total_ratings = ratings.get('total_ratings', 0)
        recent_ratings = ratings.get('recent_ratings_30d', 0)

        # Rating quality score (0-50 points)
        if average_rating >= self.BENCHMARKS['average_rating']['target']:
            rating_quality_score = 50
        elif average_rating >= self.BENCHMARKS['average_rating']['min']:
            # Proportional scoring between min and target
            proportion = (average_rating - self.BENCHMARKS['average_rating']['min']) / \
                        (self.BENCHMARKS['average_rating']['target'] - self.BENCHMARKS['average_rating']['min'])
            rating_quality_score = 30 + (proportion * 20)
        elif average_rating >= 3.0:
            rating_quality_score = 20
        else:
            rating_quality_score = 10

        # Rating volume score (0-30 points)
        if total_ratings >= self.BENCHMARKS['ratings_count']['target']:
            rating_volume_score = 30
        elif total_ratings >= self.BENCHMARKS['ratings_count']['min']:
            # Proportional scoring
            proportion = (total_ratings - self.BENCHMARKS['ratings_count']['min']) / \
                        (self.BENCHMARKS['ratings_count']['target'] - self.BENCHMARKS['ratings_count']['min'])
            rating_volume_score = 15 + (proportion * 15)
        else:
            # Very low volume
            rating_volume_score = (total_ratings / self.BENCHMARKS['ratings_count']['min']) * 15

        # Rating velocity score (0-20 points)
        if recent_ratings > 100:
            velocity_score = 20
        elif recent_ratings > 50:
            velocity_score = 15
        elif recent_ratings > 10:
            velocity_score = 10
        else:
            velocity_score = 5

        total_score = rating_quality_score + rating_volume_score + velocity_score

        return round(min(total_score, 100), 1)

    def score_keyword_performance(self, keyword_performance: Dict[str, Any]) -> float:
        """
        Score keyword ranking performance (0-100).

        Evaluates:
        - Top 10 rankings
        - Top 50 rankings
        - Ranking trends
        """
        top_10_count = keyword_performance.get('top_10', 0)
        top_50_count = keyword_performance.get('top_50', 0)
        top_100_count = keyword_performance.get('top_100', 0)
        improving_keywords = keyword_performance.get('improving_keywords', 0)

        # Top 10 score (0-50 points) - most valuable rankings
        if top_10_count >= self.BENCHMARKS['keywords_top_10']['target']:
            top_10_score = 50
        elif top_10_count >= self.BENCHMARKS['keywords_top_10']['min']:
            proportion = (top_10_count - self.BENCHMARKS['keywords_top_10']['min']) / \
                        (self.BENCHMARKS['keywords_top_10']['target'] - self.BENCHMARKS['keywords_top_10']['min'])
            top_10_score = 25 + (proportion * 25)
        else:
            top_10_score = (top_10_count / self.BENCHMARKS['keywords_top_10']['min']) * 25

        # Top 50 score (0-30 points)
        if top_50_count >= self.BENCHMARKS['keywords_top_50']['target']:
            top_50_score = 30
        elif top_50_count >= self.BENCHMARKS['keywords_top_50']['min']:
            proportion = (top_50_count - self.BENCHMARKS['keywords_top_50']['min']) / \
                        (self.BENCHMARKS['keywords_top_50']['target'] - self.BENCHMARKS['keywords_top_50']['min'])
            top_50_score = 15 + (proportion * 15)
        else:
            top_50_score = (top_50_count / self.BENCHMARKS['keywords_top_50']['min']) * 15

        # Coverage score (0-10 points) - based on top 100
        coverage_score = min((top_100_count / 30) * 10, 10)

        # Trend score (0-10 points) - are rankings improving?
        if improving_keywords > 5:
            trend_score = 10
        elif improving_keywords > 0:
            trend_score = 5
        else:
            trend_score = 0

        total_score = top_10_score + top_50_score + coverage_score + trend_score

        return round(min(total_score, 100), 1)

    def score_conversion_metrics(self, conversion: Dict[str, Any]) -> float:
        """
        Score conversion performance (0-100).

        Evaluates:
        - Impression-to-install conversion rate
        - Download velocity
        """
        conversion_rate = conversion.get('impression_to_install', 0.0)
        downloads_30d = conversion.get('downloads_last_30_days', 0)
        downloads_trend = conversion.get('downloads_trend', 'stable')  # 'up', 'stable', 'down'

        # Conversion rate score (0-70 points)
        if conversion_rate >= self.BENCHMARKS['conversion_rate']['target']:
            conversion_score = 70
        elif conversion_rate >= self.BENCHMARKS['conversion_rate']['min']:
            proportion = (conversion_rate - self.BENCHMARKS['conversion_rate']['min']) / \
                        (self.BENCHMARKS['conversion_rate']['target'] - self.BENCHMARKS['conversion_rate']['min'])
            conversion_score = 35 + (proportion * 35)
        else:
            conversion_score = (conversion_rate / self.BENCHMARKS['conversion_rate']['min']) * 35

        # Download velocity score (0-20 points)
        if downloads_30d > 10000:
            velocity_score = 20
        elif downloads_30d > 1000:
            velocity_score = 15
        elif downloads_30d > 100:
            velocity_score = 10
        else:
            velocity_score = 5

        # Trend bonus (0-10 points)
        if downloads_trend == 'up':
            trend_score = 10
        elif downloads_trend == 'stable':
            trend_score = 5
        else:
            trend_score = 0

        total_score = conversion_score + velocity_score + trend_score

        return round(min(total_score, 100), 1)

    def score_technical_performance(
        self,
        crash_rate: float = 0.0,
        anr_rate: float = 0.0,
        battery_impact: float = 0.0
    ) -> float:
        """
        Score technical performance (0-100).

        Evaluates app stability and resource usage against industry benchmarks.
        Android Vitals data is the primary source for Google Play; Apple does not
        publicly expose equivalent metrics, so data is typically user-provided.

        Args:
            crash_rate: Crash rate percentage (e.g. 0.8 means 0.8% of sessions crash).
                        Benchmark: <1% good, <2% acceptable.
            anr_rate: Application Not Responding rate percentage (Android).
                      Benchmark: <0.5% good, <1% acceptable.
            battery_impact: Excessive battery usage percentage.
                           Benchmark: <5% good, <10% acceptable.

        Returns:
            Score from 0 to 100.
        """
        benchmarks = self.TECHNICAL_BENCHMARKS

        # Crash rate score (0-40 points) - most impactful metric
        if crash_rate <= benchmarks['crash_rate']['good']:
            crash_score = 40.0
        elif crash_rate <= benchmarks['crash_rate']['acceptable']:
            # Linear interpolation between good and acceptable
            proportion = (crash_rate - benchmarks['crash_rate']['good']) / \
                        (benchmarks['crash_rate']['acceptable'] - benchmarks['crash_rate']['good'])
            crash_score = 40.0 - (proportion * 20.0)  # 40 -> 20
        else:
            # Above acceptable threshold - steep penalty
            excess = crash_rate - benchmarks['crash_rate']['acceptable']
            crash_score = max(20.0 - (excess * 10.0), 0.0)

        # ANR rate score (0-35 points) - critical for Google Play ranking
        if anr_rate <= benchmarks['anr_rate']['good']:
            anr_score = 35.0
        elif anr_rate <= benchmarks['anr_rate']['acceptable']:
            proportion = (anr_rate - benchmarks['anr_rate']['good']) / \
                        (benchmarks['anr_rate']['acceptable'] - benchmarks['anr_rate']['good'])
            anr_score = 35.0 - (proportion * 17.5)  # 35 -> 17.5
        else:
            excess = anr_rate - benchmarks['anr_rate']['acceptable']
            anr_score = max(17.5 - (excess * 8.75), 0.0)

        # Battery impact score (0-25 points)
        if battery_impact <= benchmarks['battery_impact']['good']:
            battery_score = 25.0
        elif battery_impact <= benchmarks['battery_impact']['acceptable']:
            proportion = (battery_impact - benchmarks['battery_impact']['good']) / \
                        (benchmarks['battery_impact']['acceptable'] - benchmarks['battery_impact']['good'])
            battery_score = 25.0 - (proportion * 12.5)  # 25 -> 12.5
        else:
            excess = battery_impact - benchmarks['battery_impact']['acceptable']
            battery_score = max(12.5 - (excess * 2.5), 0.0)

        total_score = crash_score + anr_score + battery_score
        return round(min(total_score, 100.0), 1)

    def score_visual_optimization(
        self,
        has_captions: bool = False,
        cpp_count: int = 0,
        has_video: bool = False
    ) -> float:
        """
        Score visual optimization (0-100).

        Evaluates screenshot and visual asset optimization. Points are awarded
        on a 5-point scale then mapped to 0-100.

        Scoring breakdown (5 points max):
        - has_captions: 3 points (captions on screenshots significantly boost conversion)
        - cpp_count > 0: 1 point (Custom Product Pages for Apple / Store Listing Experiments)
        - has_video: 1 point (app preview video)

        Args:
            has_captions: Whether screenshots include text captions/overlays.
            cpp_count: Number of Custom Product Pages (Apple) or custom listings (Google).
            has_video: Whether an app preview video is present.

        Returns:
            Score from 0 to 100.
        """
        points = 0

        # Screenshot captions (3 points) - highest impact visual element
        if has_captions:
            points += 3

        # Custom Product Pages / custom listings (1 point)
        if cpp_count > 0:
            points += 1

        # Video preview (1 point)
        if has_video:
            points += 1

        # Map 0-5 points to 0-100 scale
        score = (points / 5.0) * 100.0
        return round(score, 1)

    def generate_recommendations(
        self,
        metadata_score: float,
        ratings_score: float,
        keyword_score: float,
        conversion_score: float,
        technical_score: float = 50.0,
        visual_score: float = 50.0
    ) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations based on scores."""
        recommendations = []

        # Metadata recommendations
        if metadata_score < 60:
            recommendations.append({
                'category': 'metadata_quality',
                'priority': 'high',
                'action': 'Optimize app title and description',
                'details': 'Add more keywords to title, expand description to 1500-2000 characters, improve keyword density to 3-5%',
                'expected_impact': 'Improve discoverability and ranking potential'
            })
        elif metadata_score < 80:
            recommendations.append({
                'category': 'metadata_quality',
                'priority': 'medium',
                'action': 'Refine metadata for better keyword targeting',
                'details': 'Test variations of title/subtitle, optimize keyword field for Apple',
                'expected_impact': 'Incremental ranking improvements'
            })

        # Ratings recommendations
        if ratings_score < 60:
            recommendations.append({
                'category': 'ratings_reviews',
                'priority': 'high',
                'action': 'Improve rating quality and volume',
                'details': 'Address top user complaints, implement in-app rating prompts, respond to negative reviews',
                'expected_impact': 'Better conversion rates and trust signals'
            })
        elif ratings_score < 80:
            recommendations.append({
                'category': 'ratings_reviews',
                'priority': 'medium',
                'action': 'Increase rating velocity',
                'details': 'Optimize timing of rating requests, encourage satisfied users to rate',
                'expected_impact': 'Sustained rating quality'
            })

        # Keyword performance recommendations
        if keyword_score < 60:
            recommendations.append({
                'category': 'keyword_performance',
                'priority': 'high',
                'action': 'Improve keyword rankings',
                'details': 'Target long-tail keywords with lower competition, update metadata with high-potential keywords, build backlinks',
                'expected_impact': 'Significant improvement in organic visibility'
            })
        elif keyword_score < 80:
            recommendations.append({
                'category': 'keyword_performance',
                'priority': 'medium',
                'action': 'Expand keyword coverage',
                'details': 'Target additional related keywords, test seasonal keywords, localize for new markets',
                'expected_impact': 'Broader reach and more discovery opportunities'
            })

        # Conversion recommendations
        if conversion_score < 60:
            recommendations.append({
                'category': 'conversion_metrics',
                'priority': 'high',
                'action': 'Optimize store listing for conversions',
                'details': 'Improve screenshots and icon, strengthen value proposition in description, add video preview',
                'expected_impact': 'Higher impression-to-install conversion'
            })
        elif conversion_score < 80:
            recommendations.append({
                'category': 'conversion_metrics',
                'priority': 'medium',
                'action': 'Test visual asset variations',
                'details': 'A/B test different icon designs and screenshot sequences',
                'expected_impact': 'Incremental conversion improvements'
            })

        # Technical performance recommendations
        if technical_score < 40:
            recommendations.append({
                'category': 'technical_performance',
                'priority': 'high',
                'action': 'Address critical stability issues',
                'details': (
                    'Crash rate and/or ANR rate exceed acceptable thresholds. '
                    'Prioritize crash fixes, reduce ANR by moving heavy work off the main thread, '
                    'and optimize battery usage. Google Play penalizes apps with poor Android Vitals.'
                ),
                'expected_impact': 'Improved ranking on Google Play, reduced uninstalls, better user retention'
            })
        elif technical_score < 70:
            recommendations.append({
                'category': 'technical_performance',
                'priority': 'medium',
                'action': 'Improve app stability and performance',
                'details': (
                    'Technical metrics are acceptable but not optimal. '
                    'Target crash rate below 1%, ANR rate below 0.5%, '
                    'and battery impact below 5% to reach top-tier performance.'
                ),
                'expected_impact': 'Better Android Vitals standing, improved store ranking signals'
            })
        elif technical_score < 90:
            recommendations.append({
                'category': 'technical_performance',
                'priority': 'low',
                'action': 'Fine-tune technical performance',
                'details': (
                    'Technical metrics are good. Consider further optimizing startup time, '
                    'reducing memory footprint, and monitoring for regressions in new releases.'
                ),
                'expected_impact': 'Marginal ranking improvement, sustained app quality'
            })

        # Visual optimization recommendations
        if visual_score < 40:
            recommendations.append({
                'category': 'visual_optimization',
                'priority': 'high',
                'action': 'Add captions and video to screenshots',
                'details': (
                    'Screenshots lack captions and no video preview is present. '
                    'Add descriptive text overlays to screenshots highlighting key features, '
                    'create an app preview video, and set up Custom Product Pages (Apple) '
                    'or custom store listings (Google) for targeted campaigns.'
                ),
                'expected_impact': 'Significant improvement in conversion rate (captions can boost CVR 15-30%)'
            })
        elif visual_score < 80:
            recommendations.append({
                'category': 'visual_optimization',
                'priority': 'medium',
                'action': 'Enhance visual assets for better conversion',
                'details': (
                    'Some visual elements are missing. Ensure all screenshots have captions, '
                    'add a video preview if missing, and create at least one Custom Product Page '
                    'to target specific user segments.'
                ),
                'expected_impact': 'Incremental conversion improvement through better visual storytelling'
            })

        return recommendations

    def _assess_health_status(self, overall_score: float) -> str:
        """Assess overall ASO health status."""
        if overall_score >= 80:
            return "Excellent - Top-tier ASO performance"
        elif overall_score >= 65:
            return "Good - Competitive ASO with room for improvement"
        elif overall_score >= 50:
            return "Fair - Needs strategic improvements"
        else:
            return "Poor - Requires immediate ASO overhaul"

    def _prioritize_actions(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prioritize actions by impact and urgency."""
        # Sort by priority (high first) and expected impact
        priority_order = {'high': 0, 'medium': 1, 'low': 2}

        sorted_recommendations = sorted(
            recommendations,
            key=lambda x: priority_order[x['priority']]
        )

        return sorted_recommendations[:3]  # Top 3 priority actions

    def _identify_strengths(self, score_breakdown: Dict[str, Any]) -> List[str]:
        """Identify areas of strength (scores >= 75)."""
        strengths = []

        for category, data in score_breakdown.items():
            if data['score'] >= 75:
                strengths.append(
                    f"{category.replace('_', ' ').title()}: {data['score']}/100"
                )

        return strengths if strengths else ["Focus on building strengths across all areas"]

    def _identify_weaknesses(self, score_breakdown: Dict[str, Any]) -> List[str]:
        """Identify areas needing improvement (scores < 60)."""
        weaknesses = []

        for category, data in score_breakdown.items():
            if data['score'] < 60:
                weaknesses.append(
                    f"{category.replace('_', ' ').title()}: {data['score']}/100 - needs improvement"
                )

        return weaknesses if weaknesses else ["All areas performing adequately"]


def calculate_aso_score(
    metadata: Dict[str, Any],
    ratings: Dict[str, Any],
    keyword_performance: Dict[str, Any],
    conversion: Dict[str, Any],
    technical_data: Optional[Dict[str, Any]] = None,
    visual_data: Optional[Dict[str, Any]] = None,
    platform: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to calculate ASO score.

    Args:
        metadata: Metadata quality metrics
        ratings: Ratings data
        keyword_performance: Keyword ranking data
        conversion: Conversion metrics
        technical_data: Optional technical performance data
                       (crash_rate, anr_rate, battery_impact)
        visual_data: Optional visual optimization data
                    (has_captions, cpp_count, has_video)
        platform: Optional platform ('apple', 'google', or None for default weights)

    Returns:
        Complete ASO score report
    """
    scorer = ASOScorer(platform=platform)
    return scorer.calculate_overall_score(
        metadata,
        ratings,
        keyword_performance,
        conversion,
        technical_data=technical_data,
        visual_data=visual_data
    )
