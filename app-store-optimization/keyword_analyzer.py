"""
Keyword analysis module for App Store Optimization.
Analyzes keyword search volume, competition, and relevance for app discovery.
"""

from typing import Dict, List, Any, Optional, Tuple
import re
from collections import Counter


class KeywordAnalyzer:
    """Analyzes keywords for ASO effectiveness."""

    # Competition level thresholds (based on number of competing apps)
    COMPETITION_THRESHOLDS = {
        'low': 1000,
        'medium': 5000,
        'high': 10000
    }

    # Search volume categories (monthly searches estimate)
    VOLUME_CATEGORIES = {
        'very_low': 1000,
        'low': 5000,
        'medium': 20000,
        'high': 100000,
        'very_high': 500000
    }

    # Intent categories for semantic clustering
    INTENT_CATEGORIES = {
        'track': ['track', 'tracking', 'monitor', 'log', 'record', 'measure', 'count', 'diary'],
        'manage': ['manage', 'management', 'organize', 'organizer', 'control', 'handle', 'coordinate'],
        'plan': ['plan', 'planner', 'planning', 'schedule', 'scheduler', 'calendar', 'agenda', 'timeline'],
        'create': ['create', 'creator', 'make', 'maker', 'build', 'builder', 'design', 'designer', 'edit', 'editor'],
        'learn': ['learn', 'learning', 'study', 'education', 'course', 'tutorial', 'teach', 'training'],
        'find': ['find', 'finder', 'search', 'discover', 'locate', 'lookup', 'browse', 'explore'],
        'compare': ['compare', 'comparison', 'versus', 'review', 'rate', 'rating', 'rank', 'ranking'],
        'share': ['share', 'sharing', 'social', 'connect', 'collaborate', 'collaboration', 'team', 'group'],
        'save': ['save', 'saving', 'budget', 'budgeting', 'money', 'finance', 'financial', 'expense', 'cost'],
        'health': ['health', 'healthy', 'fitness', 'workout', 'exercise', 'diet', 'nutrition', 'wellness', 'meditation'],
        'communicate': ['chat', 'message', 'messaging', 'call', 'calling', 'video', 'voice', 'talk'],
        'automate': ['automate', 'automation', 'automatic', 'auto', 'smart', 'ai', 'intelligent', 'reminder'],
    }

    def __init__(self):
        """Initialize keyword analyzer."""
        self.analyzed_keywords = {}

    def analyze_keyword(
        self,
        keyword: str,
        search_volume: int = 0,
        competing_apps: int = 0,
        relevance_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        Analyze a single keyword for ASO potential.

        Args:
            keyword: The keyword to analyze
            search_volume: Estimated monthly search volume
            competing_apps: Number of apps competing for this keyword
            relevance_score: Relevance to your app (0.0-1.0)

        Returns:
            Dictionary with keyword analysis
        """
        competition_level = self._calculate_competition_level(competing_apps)
        volume_category = self._categorize_search_volume(search_volume)
        difficulty_score = self._calculate_keyword_difficulty(
            search_volume,
            competing_apps
        )

        # Calculate potential score (0-100)
        potential_score = self._calculate_potential_score(
            search_volume,
            competing_apps,
            relevance_score
        )

        analysis = {
            'keyword': keyword,
            'search_volume': search_volume,
            'volume_category': volume_category,
            'competing_apps': competing_apps,
            'competition_level': competition_level,
            'relevance_score': relevance_score,
            'difficulty_score': difficulty_score,
            'potential_score': potential_score,
            'recommendation': self._generate_recommendation(
                potential_score,
                difficulty_score,
                relevance_score
            ),
            'keyword_length': len(keyword.split()),
            'is_long_tail': len(keyword.split()) >= 3
        }

        self.analyzed_keywords[keyword] = analysis
        return analysis

    def compare_keywords(self, keywords_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple keywords and rank by potential.

        Args:
            keywords_data: List of dicts with keyword, search_volume, competing_apps, relevance_score

        Returns:
            Comparison report with ranked keywords
        """
        analyses = []
        for kw_data in keywords_data:
            analysis = self.analyze_keyword(
                keyword=kw_data['keyword'],
                search_volume=kw_data.get('search_volume', 0),
                competing_apps=kw_data.get('competing_apps', 0),
                relevance_score=kw_data.get('relevance_score', 0.0)
            )
            analyses.append(analysis)

        # Sort by potential score (descending)
        ranked_keywords = sorted(
            analyses,
            key=lambda x: x['potential_score'],
            reverse=True
        )

        # Categorize keywords
        primary_keywords = [
            kw for kw in ranked_keywords
            if kw['potential_score'] >= 70 and kw['relevance_score'] >= 0.8
        ]

        secondary_keywords = [
            kw for kw in ranked_keywords
            if 50 <= kw['potential_score'] < 70 and kw['relevance_score'] >= 0.6
        ]

        long_tail_keywords = [
            kw for kw in ranked_keywords
            if kw['is_long_tail'] and kw['relevance_score'] >= 0.7
        ]

        return {
            'total_keywords_analyzed': len(analyses),
            'ranked_keywords': ranked_keywords,
            'primary_keywords': primary_keywords[:5],  # Top 5
            'secondary_keywords': secondary_keywords[:10],  # Top 10
            'long_tail_keywords': long_tail_keywords[:10],  # Top 10
            'summary': self._generate_comparison_summary(
                primary_keywords,
                secondary_keywords,
                long_tail_keywords
            )
        }

    def find_long_tail_opportunities(
        self,
        base_keyword: str,
        modifiers: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate long-tail keyword variations.

        Args:
            base_keyword: Core keyword (e.g., "task manager")
            modifiers: List of modifiers (e.g., ["free", "simple", "team"])

        Returns:
            List of long-tail keyword suggestions
        """
        long_tail_keywords = []

        # Generate combinations
        for modifier in modifiers:
            # Modifier + base
            variation1 = f"{modifier} {base_keyword}"
            long_tail_keywords.append({
                'keyword': variation1,
                'pattern': 'modifier_base',
                'estimated_competition': 'low',
                'rationale': f"Less competitive variation of '{base_keyword}'"
            })

            # Base + modifier
            variation2 = f"{base_keyword} {modifier}"
            long_tail_keywords.append({
                'keyword': variation2,
                'pattern': 'base_modifier',
                'estimated_competition': 'low',
                'rationale': f"Specific use-case variation of '{base_keyword}'"
            })

        # Add question-based long-tail
        question_words = ['how', 'what', 'best', 'top']
        for q_word in question_words:
            question_keyword = f"{q_word} {base_keyword}"
            long_tail_keywords.append({
                'keyword': question_keyword,
                'pattern': 'question_based',
                'estimated_competition': 'very_low',
                'rationale': f"Informational search query"
            })

        return long_tail_keywords

    def extract_keywords_from_text(
        self,
        text: str,
        min_word_length: int = 3
    ) -> List[Tuple[str, int]]:
        """
        Extract potential keywords from text (descriptions, reviews).

        Args:
            text: Text to analyze
            min_word_length: Minimum word length to consider

        Returns:
            List of (keyword, frequency) tuples
        """
        # Clean and normalize text
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)

        # Extract words
        words = text.split()

        # Filter by length
        words = [w for w in words if len(w) >= min_word_length]

        # Remove common stop words
        stop_words = {
            'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have',
            'but', 'not', 'you', 'all', 'can', 'are', 'was', 'were', 'been'
        }
        words = [w for w in words if w not in stop_words]

        # Count frequency
        word_counts = Counter(words)

        # Extract 2-word phrases
        phrases = []
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrases.append(phrase)

        phrase_counts = Counter(phrases)

        # Combine and sort
        all_keywords = list(word_counts.items()) + list(phrase_counts.items())
        all_keywords.sort(key=lambda x: x[1], reverse=True)

        return all_keywords[:50]  # Top 50

    def calculate_keyword_density(
        self,
        text: str,
        target_keywords: List[str]
    ) -> Dict[str, float]:
        """
        Calculate keyword density in text.

        Args:
            text: Text to analyze (title, description)
            target_keywords: Keywords to check density for

        Returns:
            Dictionary of keyword: density (percentage)
        """
        text_lower = text.lower()
        total_words = len(text_lower.split())

        densities = {}
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            occurrences = text_lower.count(keyword_lower)
            density = (occurrences / total_words) * 100 if total_words > 0 else 0
            densities[keyword] = round(density, 2)

        return densities

    def cluster_by_intent(
        self,
        keywords: List[str],
        keyword_data: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Group keywords into intent-based semantic clusters.

        Args:
            keywords: List of keyword strings to cluster
            keyword_data: Optional dict mapping keyword to its analysis data
                         (search_volume, competition, relevance_score)

        Returns:
            List of cluster dicts with keys:
            {name, intent, keywords, natural_queries, combined_score, keyword_count}
        """
        clusters = {}
        unclustered = []

        for keyword in keywords:
            words = set(re.findall(r'\w+', keyword.lower()))
            matched_intent = None
            best_overlap = 0

            for intent, intent_words in self.INTENT_CATEGORIES.items():
                overlap = len(words.intersection(set(intent_words)))
                if overlap > best_overlap:
                    best_overlap = overlap
                    matched_intent = intent

            if matched_intent and best_overlap > 0:
                if matched_intent not in clusters:
                    clusters[matched_intent] = []
                clusters[matched_intent].append(keyword)
            else:
                unclustered.append(keyword)

        # Build cluster results
        result = []
        for intent, cluster_keywords in clusters.items():
            cluster = {
                'name': f"{intent.title()} Intent",
                'intent': intent,
                'keywords': cluster_keywords,
                'keyword_count': len(cluster_keywords),
                'natural_queries': self.generate_natural_queries(intent, cluster_keywords),
                'combined_score': self.score_cluster(cluster_keywords, keyword_data),
            }
            result.append(cluster)

        # Add unclustered keywords as "General" cluster
        if unclustered:
            result.append({
                'name': 'General',
                'intent': 'general',
                'keywords': unclustered,
                'keyword_count': len(unclustered),
                'natural_queries': [],
                'combined_score': self.score_cluster(unclustered, keyword_data),
            })

        # Sort by combined score descending
        result.sort(key=lambda x: x['combined_score'], reverse=True)
        return result

    def generate_natural_queries(
        self,
        intent: str,
        keywords: List[str],
        max_queries: int = 5
    ) -> List[str]:
        """
        Generate natural language query variants for voice/AI search optimization.

        Args:
            intent: The intent category name
            keywords: Keywords in this cluster
            max_queries: Maximum queries to generate

        Returns:
            List of natural language query strings
        """
        templates = {
            'track': [
                "apps to help me track {obj}",
                "best {obj} tracking app",
                "how to track my {obj} on my phone",
            ],
            'manage': [
                "apps to help me manage {obj}",
                "best {obj} management app",
                "how to organize my {obj}",
            ],
            'plan': [
                "apps to help me plan {obj}",
                "best {obj} planner app",
                "how to schedule my {obj}",
            ],
            'create': [
                "apps to create {obj}",
                "best {obj} creator app",
                "easy way to make {obj}",
            ],
            'learn': [
                "apps to learn {obj}",
                "best {obj} learning app",
                "how to study {obj} on my phone",
            ],
            'find': [
                "apps to find {obj}",
                "best app for finding {obj}",
                "where to find {obj}",
            ],
            'compare': [
                "apps to compare {obj}",
                "best {obj} comparison app",
                "how to compare {obj}",
            ],
            'share': [
                "apps to share {obj}",
                "best {obj} sharing app",
                "how to collaborate on {obj}",
            ],
            'save': [
                "apps to save {obj}",
                "best {obj} budgeting app",
                "how to manage my {obj}",
            ],
            'health': [
                "apps for {obj}",
                "best {obj} app",
                "how to improve my {obj}",
            ],
            'communicate': [
                "apps for {obj}",
                "best {obj} app",
                "how to {obj} for free",
            ],
            'automate': [
                "apps to automate {obj}",
                "best smart {obj} app",
                "how to automate {obj}",
            ],
        }

        queries = []
        intent_templates = templates.get(intent, [
            "apps for {obj}",
            "best {obj} app",
        ])

        # Extract object nouns from keywords (remove intent words)
        intent_words = set(self.INTENT_CATEGORIES.get(intent, []))
        objects = set()
        for kw in keywords:
            words = re.findall(r'\w+', kw.lower())
            obj_words = [w for w in words if w not in intent_words and len(w) > 2]
            if obj_words:
                objects.add(' '.join(obj_words))

        # Generate queries from templates
        for obj in list(objects)[:max_queries]:
            for template in intent_templates:
                query = template.format(obj=obj)
                if query not in queries:
                    queries.append(query)
                    if len(queries) >= max_queries:
                        return queries

        return queries

    def score_cluster(
        self,
        keywords: List[str],
        keyword_data: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> float:
        """
        Calculate combined potential score for a keyword cluster.

        Args:
            keywords: List of keywords in the cluster
            keyword_data: Optional analysis data per keyword

        Returns:
            Combined cluster score (0.0 - 100.0)
        """
        if not keywords:
            return 0.0

        if not keyword_data:
            # Without data, score based on keyword count and diversity
            return min(len(keywords) * 10.0, 50.0)

        total_volume = 0
        total_relevance = 0.0
        total_opportunity = 0.0
        count = 0

        for keyword in keywords:
            data = keyword_data.get(keyword, {})
            volume = data.get('search_volume', 0)
            competition = data.get('competing_apps', 5000)
            relevance = data.get('relevance_score', 0.5)

            total_volume += volume
            total_relevance += relevance

            # Opportunity = high volume + low competition
            if competition > 0:
                opportunity = (volume / competition) * relevance
            else:
                opportunity = volume * relevance
            total_opportunity += opportunity
            count += 1

        if count == 0:
            return 0.0

        # Normalize scores
        volume_score = min(total_volume / 10000, 30.0)  # Max 30 points
        relevance_score = (total_relevance / count) * 30.0  # Max 30 points
        opportunity_score = min(total_opportunity * 10, 30.0)  # Max 30 points
        diversity_score = min(count * 2.0, 10.0)  # Max 10 points (keyword count)

        return round(volume_score + relevance_score + opportunity_score + diversity_score, 1)

    def _calculate_competition_level(self, competing_apps: int) -> str:
        """Determine competition level based on number of competing apps."""
        if competing_apps < self.COMPETITION_THRESHOLDS['low']:
            return 'low'
        elif competing_apps < self.COMPETITION_THRESHOLDS['medium']:
            return 'medium'
        elif competing_apps < self.COMPETITION_THRESHOLDS['high']:
            return 'high'
        else:
            return 'very_high'

    def _categorize_search_volume(self, search_volume: int) -> str:
        """Categorize search volume."""
        if search_volume < self.VOLUME_CATEGORIES['very_low']:
            return 'very_low'
        elif search_volume < self.VOLUME_CATEGORIES['low']:
            return 'low'
        elif search_volume < self.VOLUME_CATEGORIES['medium']:
            return 'medium'
        elif search_volume < self.VOLUME_CATEGORIES['high']:
            return 'high'
        else:
            return 'very_high'

    def _calculate_keyword_difficulty(
        self,
        search_volume: int,
        competing_apps: int
    ) -> float:
        """
        Calculate keyword difficulty score (0-100).
        Higher score = harder to rank.
        """
        if competing_apps == 0:
            return 0.0

        # Competition factor (0-1)
        competition_factor = min(competing_apps / 50000, 1.0)

        # Volume factor (0-1) - higher volume = more difficulty
        volume_factor = min(search_volume / 1000000, 1.0)

        # Difficulty score (weighted average)
        difficulty = (competition_factor * 0.7 + volume_factor * 0.3) * 100

        return round(difficulty, 1)

    def _calculate_potential_score(
        self,
        search_volume: int,
        competing_apps: int,
        relevance_score: float
    ) -> float:
        """
        Calculate overall keyword potential (0-100).
        Higher score = better opportunity.
        """
        # Volume score (0-40 points)
        volume_score = min((search_volume / 100000) * 40, 40)

        # Competition score (0-30 points) - inverse relationship
        if competing_apps > 0:
            competition_score = max(30 - (competing_apps / 500), 0)
        else:
            competition_score = 30

        # Relevance score (0-30 points)
        relevance_points = relevance_score * 30

        total_score = volume_score + competition_score + relevance_points

        return round(min(total_score, 100), 1)

    def _generate_recommendation(
        self,
        potential_score: float,
        difficulty_score: float,
        relevance_score: float
    ) -> str:
        """Generate actionable recommendation for keyword."""
        if relevance_score < 0.5:
            return "Low relevance - avoid targeting"

        if potential_score >= 70:
            return "High priority - target immediately"
        elif potential_score >= 50:
            if difficulty_score < 50:
                return "Good opportunity - include in metadata"
            else:
                return "Competitive - use in description, not title"
        elif potential_score >= 30:
            return "Secondary keyword - use for long-tail variations"
        else:
            return "Low potential - deprioritize"

    def _generate_comparison_summary(
        self,
        primary_keywords: List[Dict[str, Any]],
        secondary_keywords: List[Dict[str, Any]],
        long_tail_keywords: List[Dict[str, Any]]
    ) -> str:
        """Generate summary of keyword comparison."""
        summary_parts = []

        summary_parts.append(
            f"Identified {len(primary_keywords)} high-priority primary keywords."
        )

        if primary_keywords:
            top_keyword = primary_keywords[0]['keyword']
            summary_parts.append(
                f"Top recommendation: '{top_keyword}' (potential score: {primary_keywords[0]['potential_score']})."
            )

        summary_parts.append(
            f"Found {len(secondary_keywords)} secondary keywords for description and metadata."
        )

        summary_parts.append(
            f"Discovered {len(long_tail_keywords)} long-tail opportunities with lower competition."
        )

        return " ".join(summary_parts)


def analyze_keyword_set(keywords_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convenience function to analyze a set of keywords.

    Args:
        keywords_data: List of keyword data dictionaries

    Returns:
        Complete analysis report
    """
    analyzer = KeywordAnalyzer()
    return analyzer.compare_keywords(keywords_data)
