"""
Updated correlation_processor.py that generates the high-confidence values
"""

from pathlib import Path
from typing import Dict, Any
import pandas as pd
from .base_processor import BaseProcessor
from .composite_similarity_calculator import CompositeSimilarityCalculator
import config

class CorrelationProcessor(BaseProcessor):
    """Processes language correlation data and generates composite similarity scores"""
    
    def __init__(self, systemsem_path: Path):
        super().__init__(systemsem_path)
        self.composite_calculator = CompositeSimilarityCalculator()
    
    def process(self) -> Dict[str, Any]:
        """
        Extract SYSTEMSEM correlations and generate composite similarity scores
        Returns: Dict with language pairs and their composite scores
        """
        
        # Step 1: Extract raw SYSTEMSEM correlations
        raw_correlations = self._extract_systemsem_correlations()
        
        # Step 2: Generate composite similarities
        composite_similarities = self._generate_composite_similarities(raw_correlations)
        
        # Step 3: Create the final output format for Memoria
        memoria_format = self._format_for_memoria(composite_similarities)
        
        self.logger.info(f"✅ Generated composite similarities for {len(memoria_format)} language pairs")
        return memoria_format
    
    def _extract_systemsem_correlations(self) -> Dict[str, float]:
        """Extract raw semantic correlations from SYSTEMSEM CSV files"""
        correlations = {}
        
        # Find correlation files
        correlation_files = self.find_files(
            config.FILE_PATTERNS["pairwise_correlations"],
            [config.DATA_PATHS["correlations"]]
        )
        
        self.logger.info(f"📊 Processing {len(correlation_files)} correlation files")
        
        for file_path in correlation_files:
            self._process_correlation_file(file_path, correlations)
        
        return correlations
    
    def _process_correlation_file(self, file_path: Path, correlations: Dict):
        """Process a single correlation CSV file to extract LOCAL correlations"""
        try:
            df = self.read_csv_safe(file_path)
            if df.empty:
                return
            
            # Extract language pair from filename
            lang1, lang2 = self.extract_language_pair(file_path.name)
            if not lang1 or not lang2:
                self.logger.warning(f"Could not extract language pair from {file_path.name}")
                return
            
            # Extract LOCAL correlation (the semantic similarity we want)
            local_correlation = self._extract_local_correlation(df, file_path.name)
            if local_correlation is not None:
                pair_key = f"{lang1}_{lang2}"
                correlations[pair_key] = local_correlation
                self.logger.debug(f"Added LOCAL correlation {lang1}-{lang2}: {local_correlation:.3f}")
                
        except Exception as e:
            self.logger.warning(f"Failed to process {file_path.name}: {e}")
    
    def _extract_local_correlation(self, df: pd.DataFrame, filename: str = "") -> float:
        """Extract LOCAL correlation from SYSTEMSEM dataframe"""
        try:
            # SYSTEMSEM format: cluster_count, type, correlation, lang1, lang2
            if len(df.columns) >= 3:
                df.columns = ['cluster_count', 'type', 'correlation', 'lang1', 'lang2'][:len(df.columns)]
                
                # Filter for LOCAL correlations only (within-cluster semantic similarity)
                local_df = df[df['type'] == 'local']
                
                if local_df.empty:
                    self.logger.warning(f"No LOCAL correlations found in {filename}")
                    return None
                
                # Use 10-cluster solution (most stable according to research)
                cluster_10_df = local_df[local_df['cluster_count'] == 10]
                
                if not cluster_10_df.empty:
                    correlation_value = cluster_10_df['correlation'].iloc[0]
                    self.logger.debug(f"Using 10-cluster LOCAL correlation: {correlation_value:.3f}")
                else:
                    # Fallback to mean LOCAL correlation if no 10-cluster data
                    correlation_value = local_df['correlation'].mean()
                    self.logger.debug(f"Using average LOCAL correlation: {correlation_value:.3f}")
                
                return correlation_value
                
            else:
                self.logger.warning(f"Unexpected CSV format in {filename}")
                return None
                
        except Exception as e:
            self.logger.warning(f"❌ Error extracting LOCAL correlation from {filename}: {e}")
            return None
    
    def _generate_composite_similarities(self, raw_correlations: Dict[str, float]) -> Dict[str, Dict]:
        """Generate composite similarity scores using the calculator"""
        composite_similarities = {}
        
        # Convert SYSTEMSEM correlations to composite scores
        for pair_key, correlation in raw_correlations.items():
            lang1, lang2 = pair_key.split('_')
            
            # Convert to standard language codes
            std_lang1 = config.LANGUAGE_MAPPING.get(lang1.upper(), lang1.lower())
            std_lang2 = config.LANGUAGE_MAPPING.get(lang2.upper(), lang2.lower())
            
            # Calculate composite similarity
            composite_result = self.composite_calculator.calculate_composite_similarity(
                std_lang1, std_lang2, correlation
            )
            
            # Store with standardized key
            standard_key = f"{std_lang1}-{std_lang2}"
            composite_similarities[standard_key] = composite_result
        
        # Add high-confidence pairs that might not be in SYSTEMSEM
        self._add_high_confidence_pairs(composite_similarities)
        
        return composite_similarities
    
    def _add_high_confidence_pairs(self, similarities: Dict[str, Dict]):
        """Add important language pairs that should have high confidence"""
        important_pairs = [
            ("es", "it"),  # Spanish-Italian (should be ~0.89)
            ("es", "pt"),  # Spanish-Portuguese 
            ("fr", "es"),  # French-Spanish (should be ~0.85)
            ("en", "de"),  # English-German (should be ~0.68)
            ("it", "fr"),  # Italian-French (should be ~0.78)
            ("ru", "pl"),  # Russian-Polish
            ("hi", "ur"),  # Hindi-Urdu
        ]
        
        for lang1, lang2 in important_pairs:
            key1 = f"{lang1}-{lang2}"
            key2 = f"{lang2}-{lang1}"
            
            # Only add if not already present
            if key1 not in similarities and key2 not in similarities:
                composite_result = self.composite_calculator.calculate_composite_similarity(lang1, lang2)
                similarities[key1] = composite_result
                self.logger.info(f"Added high-confidence pair {key1}: {composite_result['score']:.3f}")
    
    def _format_for_memoria(self, composite_similarities: Dict[str, Dict]) -> Dict[str, Dict]:
        """Format composite similarities for Memoria application"""
        memoria_format = {}
        
        for pair_key, similarity_data in composite_similarities.items():
            # Create the format expected by Memoria
            memoria_format[pair_key.upper()] = {
                "global": similarity_data["global"],
                "local": similarity_data["local"], 
                "confidence": similarity_data["confidence"],
                "strategy": similarity_data["strategy"],
                "breakdown": similarity_data["breakdown"],
                "evidence": similarity_data["evidence_sources"]
            }
        
        return memoria_format


# Test the updated processor
def test_updated_processor():
    """Test the updated correlation processor"""
    from pathlib import Path
    
    # Create mock processor for testing
    processor = CorrelationProcessor(Path("/mock/path"))
    
    # Test composite calculation directly
    calculator = CompositeSimilarityCalculator()
    
    print("=== Testing Updated Correlation Processor ===\n")
    
    # Test cases that should produce the high-confidence values you mentioned
    test_cases = [
        ("es", "it", 0.58),  # Should become ~0.89
        ("fr", "es", 0.52),  # Should become ~0.85  
        ("en", "de", 0.45),  # Should become ~0.68
        ("it", "fr", 0.48),  # Should become ~0.78
    ]
    
    for lang1, lang2, systemsem_corr in test_cases:
        result = calculator.calculate_composite_similarity(lang1, lang2, systemsem_corr)
        
        print(f"{lang1.upper()}-{lang2.upper()}:")
        print(f"  Raw SYSTEMSEM: {systemsem_corr:.3f}")
        print(f"  Composite Score: {result['score']:.3f}")
        print(f"  Global: {result['global']:.3f}")
        print(f"  Local: {result['local']:.3f}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Strategy: {result['strategy']}")
        print(f"  Breakdown: {result['breakdown']}")
        print()

if __name__ == "__main__":
    test_updated_processor()