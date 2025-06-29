"""Test script to verify language similarity calculations"""
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from processors.composite_similarity_calculator import FixedSimilarityCalculator

def test_romance_languages():
    """Test similarity between Romance languages"""
    calculator = FixedSimilarityCalculator()
    
    # Test ES-IT (Spanish-Italian)
    result = calculator.calculate_composite_similarity("es", "it", 0.58)
    print(f"ES-IT Similarity: {result['global']:.3f}")
    print(f"  Family: {result['breakdown']['family_similarity']:.3f}")
    print(f"  Contact: {result['breakdown']['contact_similarity']:.3f}")
    print(f"  Confidence: {result['confidence']}")
    print()
    
    # Test ES-PT (Spanish-Portuguese)
    result = calculator.calculate_composite_similarity("es", "pt", 0.62)
    print(f"ES-PT Similarity: {result['global']:.3f}")
    print(f"  Family: {result['breakdown']['family_similarity']:.3f}")
    print(f"  Contact: {result['breakdown']['contact_similarity']:.3f}")
    print(f"  Confidence: {result['confidence']}")

def test_germanic_languages():
    """Test similarity between Germanic languages"""
    calculator = FixedSimilarityCalculator()
    
    # Test EN-DE (English-German)
    result = calculator.calculate_composite_similarity("en", "de", 0.45)
    print(f"EN-DE Similarity: {result['global']:.3f}")
    print(f"  Family: {result['breakdown']['family_similarity']:.3f}")
    print(f"  Contact: {result['breakdown']['contact_similarity']:.3f}")
    print(f"  Confidence: {result['confidence']}")

def test_cross_family():
    """Test similarity between languages from different families"""
    calculator = FixedSimilarityCalculator()
    
    # Test EN-ES (English-Spanish)
    result = calculator.calculate_composite_similarity("en", "es", 0.38)
    print(f"EN-ES Similarity: {result['global']:.3f}")
    print(f"  Family: {result['breakdown']['family_similarity']:.3f}")
    print(f"  Contact: {result['breakdown']['contact_similarity']:.3f}")
    print(f"  Confidence: {result['confidence']}")

if __name__ == "__main__":
    print("=== Testing Romance Languages ===")
    test_romance_languages()
    
    print("\n=== Testing Germanic Languages ===")
    test_germanic_languages()
    
    print("\n=== Testing Cross-Family Similarity ===")
    test_cross_family()
