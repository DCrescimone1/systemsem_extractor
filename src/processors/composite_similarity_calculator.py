"""
Composite Language Similarity Calculator for Memoria
Combines SYSTEMSEM semantic data with linguistic family, contact, and cultural factors
"""

from typing import Dict, Tuple, Optional
import pandas as pd
from pathlib import Path
import json

class CompositeSimilarityCalculator:
    """Calculate composite language similarity scores like those in Memoria"""
    
    def __init__(self):
        # Language family baseline similarities (from research)
        self.family_baselines = {
            "Romance": 0.75,  # Spanish-Italian, French-Portuguese, etc.
            "Germanic": 0.60, # English-German, Dutch-German, etc.  
            "Slavic": 0.70,   # Russian-Polish, Czech-Slovak, etc.
            "Indo-Iranian": 0.65,
            "Sino-Tibetan": 0.30,
            "Semitic": 0.60,
            "Niger-Congo": 0.45,
            "Austronesian": 0.50
        }
        
        # Language family mappings
        self.language_families = {
            "Romance": ["es", "it", "fr", "pt", "ro", "ca"],
            "Germanic": ["en", "de", "nl", "sv", "da", "no"],
            "Slavic": ["ru", "pl", "cs", "sk", "bg", "hr"],
            "Indo-Iranian": ["hi", "ur", "fa", "bn", "pa", "gu", "mr", "ne"],
            "Sino-Tibetan": ["zh", "th", "my"],
            "Semitic": ["ar", "he"],
            "Niger-Congo": ["yo", "ig", "sw"],
            "Austronesian": ["tl", "id", "ms"]
        }
        
        # Historical contact bonuses (major known contact pairs)
        self.historical_contact = {
            ("es", "it"): 0.15,  # Roman Empire, Catholic Church
            ("fr", "en"): 0.20,  # Norman conquest, centuries of contact
            ("de", "en"): 0.10,  # Anglo-Saxon heritage
            ("ar", "es"): 0.12,  # Moorish period
            ("zh", "ja"): 0.08,  # Cultural transmission
            ("hi", "ur"): 0.25,  # Shared Hindustani base
            ("pt", "es"): 0.18,  # Iberian Peninsula
        }
        
        # Geographic proximity bonuses
        self.geographic_proximity = {
            ("th", "vi"): 0.05,
            ("ko", "ja"): 0.06,
            ("fi", "et"): 0.08,
            ("hu", "fi"): 0.03,
        }
        
        # Cultural similarity bonuses
        self.cultural_similarity = {
            ("es", "it"): 0.10,  # Catholic, Mediterranean
            ("fr", "it"): 0.08,  # Catholic, Latin culture
            ("de", "nl"): 0.05,  # Similar Protestant traditions
            ("hi", "ne"): 0.06,  # Hindu/Buddhist overlap
        }
    
    def calculate_composite_similarity(self, 
                                     lang1: str, 
                                     lang2: str, 
                                     systemsem_correlation: Optional[float] = None) -> Dict:
        """
        Calculate composite similarity score combining multiple factors
        
        Returns dict with score, confidence, breakdown, and strategy
        """
        
        # Normalize language pair order for lookup
        pair = tuple(sorted([lang1, lang2]))
        reverse_pair = (pair[1], pair[0])
        
        # Base score from SYSTEMSEM research (if available)
        if systemsem_correlation is not None:
            base_score = systemsem_correlation
            base_confidence = "high"
            base_source = "systemsem_research"
        else:
            base_score = 0.02  # Conservative minimum
            base_confidence = "low"
            base_source = "conservative_default"
        
        # Language family bonus
        family_bonus = 0.0
        family_confidence = "none"
        family1 = self._get_language_family(lang1)
        family2 = self._get_language_family(lang2)
        
        if family1 and family2 and family1 == family2:
            family_bonus = self.family_baselines[family1] - base_score
            family_confidence = "high"
            base_confidence = "high"  # Upgrade overall confidence
        
        # Historical contact bonus
        contact_bonus = 0.0
        if pair in self.historical_contact:
            contact_bonus = self.historical_contact[pair]
        elif reverse_pair in self.historical_contact:
            contact_bonus = self.historical_contact[reverse_pair]
        
        # Geographic proximity bonus
        geo_bonus = 0.0
        if pair in self.geographic_proximity:
            geo_bonus = self.geographic_proximity[pair]
        elif reverse_pair in self.geographic_proximity:
            geo_bonus = self.geographic_proximity[reverse_pair]
        
        # Cultural similarity bonus
        cultural_bonus = 0.0
        if pair in self.cultural_similarity:
            cultural_bonus = self.cultural_similarity[pair]
        elif reverse_pair in self.cultural_similarity:
            cultural_bonus = self.cultural_similarity[reverse_pair]
        
        # Calculate composite score (this becomes our "local" - strongest similarity)
        composite_local = min(0.95, base_score + family_bonus + contact_bonus + geo_bonus + cultural_bonus)
        
        # Global is typically 5-8% lower than local (from SYSTEMSEM research)
        local_global_ratio = 1.06 if systemsem_correlation else 1.04  # Higher ratio if we have research data
        composite_global = composite_local / local_global_ratio
        
        # Determine overall confidence
        confidence = self._assess_confidence(
            systemsem_available=systemsem_correlation is not None,
            same_family=family1 == family2 if family1 and family2 else False,
            has_contact=contact_bonus > 0,
            has_cultural=cultural_bonus > 0
        )
        
        # Determine strategy based on local score (highest similarity)
        strategy = self._get_strategy(confidence, composite_local)
        
        return {
            "score": round(composite_local, 3),  # Main score is the local (strongest) similarity
            "global": round(composite_global, 3),  # Global is lower
            "local": round(composite_local, 3),    # Local is the strongest similarity  
            "confidence": confidence,
            "strategy": strategy,
            "breakdown": {
                "semantic_base": round(base_score, 3),
                "family_bonus": round(family_bonus, 3),
                "contact_bonus": round(contact_bonus, 3),
                "geographic_bonus": round(geo_bonus, 3),
                "cultural_bonus": round(cultural_bonus, 3)
            },
            "evidence_sources": {
                "semantic": base_source,
                "family": family1 if family1 == family2 else None,
                "contact": "documented" if contact_bonus > 0 else None,
                "cultural": "traditional" if cultural_bonus > 0 else None
            }
        }
    
    def _get_language_family(self, lang: str) -> Optional[str]:
        """Get language family for a language code"""
        for family, languages in self.language_families.items():
            if lang in languages:
                return family
        return None
    
    def _assess_confidence(self, systemsem_available: bool, same_family: bool, 
                          has_contact: bool, has_cultural: bool) -> str:
        """Assess overall confidence based on available evidence"""
        evidence_count = sum([systemsem_available, same_family, has_contact, has_cultural])
        
        if systemsem_available and same_family:
            return "high"
        elif evidence_count >= 2:
            return "medium"
        elif evidence_count == 1:
            return "low"
        else:
            return "minimal"
    
    def _get_strategy(self, confidence: str, score: float) -> str:
        """Determine learning strategy based on confidence and score"""
        if confidence == "high" and score > 0.7:
            return "etymological_cognates"
        elif confidence in ["high", "medium"] and score > 0.4:
            return "structural_patterns"
        elif score > 0.2:
            return "vocabulary_borrowing"
        else:
            return "conceptual_bridging"
    
    def process_systemsem_data(self, systemsem_correlations: Dict[str, float]) -> Dict[str, Dict]:
        """Process SYSTEMSEM data and generate composite similarities"""
        results = {}
        
        # Process languages with SYSTEMSEM data
        for pair_key, correlation in systemsem_correlations.items():
            if '-' in pair_key:
                lang1, lang2 = pair_key.split('-')
                key = f"{lang1}-{lang2}"
                results[key] = self.calculate_composite_similarity(lang1, lang2, correlation)
        
        # Add high-confidence pairs not in SYSTEMSEM
        high_confidence_pairs = [
            ("es", "it"), ("es", "pt"), ("es", "fr"),
            ("en", "de"), ("en", "nl"), 
            ("ru", "pl"), ("hi", "ur"),
            ("zh", "ja"), ("ar", "he")
        ]
        
        for lang1, lang2 in high_confidence_pairs:
            key = f"{lang1}-{lang2}"
            if key not in results:
                results[key] = self.calculate_composite_similarity(lang1, lang2)
        
        return results


# Example usage and testing
def main():
    calculator = CompositeSimilarityCalculator()
    
    # Test with known SYSTEMSEM correlations
    systemsem_data = {
        "es-it": 0.58,  # Raw semantic correlation from SYSTEMSEM
        "en-de": 0.45,
        "fr-es": 0.52,
        "ar-bn": 0.295,
        "zh-en": 0.325
    }
    
    print("=== Composite Language Similarity Results ===\n")
    
    for pair, semantic_corr in systemsem_data.items():
        lang1, lang2 = pair.split('-')
        result = calculator.calculate_composite_similarity(lang1, lang2, semantic_corr)
        
        print(f"{pair.upper()}: {result['score']:.3f}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Strategy: {result['strategy']}")
        print(f"  Breakdown: {result['breakdown']}")
        print(f"  Evidence: {result['evidence_sources']}")
        print()
    
    # Test high-confidence pair without SYSTEMSEM data
    print("Testing language pair without SYSTEMSEM data:")
    result = calculator.calculate_composite_similarity("pt", "es")
    print(f"PT-ES: {result['score']:.3f} (confidence: {result['confidence']})")


if __name__ == "__main__":
    main()