"""
Processor for language correlation data
"""

from pathlib import Path
from typing import Dict, Any
import pandas as pd
from .base_processor import BaseProcessor
import config

class CorrelationProcessor(BaseProcessor):
    """Processes language correlation data from SYSTEMSEM CSV files"""
    
    def process(self) -> Dict[str, Any]:
        """
        Extract and process language correlation data
        Returns: Dict with language pairs and their correlation scores
        """
        correlations = {}
        
        # Find correlation files
        correlation_files = self.find_files(
            config.FILE_PATTERNS["pairwise_correlations"],
            [config.DATA_PATHS["correlations"]]
        )
        
        self.logger.info(f"📊 Processing {len(correlation_files)} correlation files")
        
        for file_path in correlation_files:
            self._process_correlation_file(file_path, correlations)
        
        # Convert to standard language codes
        standardized_correlations = self._standardize_language_codes(correlations)
        
        self.logger.info(f"✅ Processed correlations for {len(standardized_correlations)} language pairs")
        return standardized_correlations
    
    def _process_correlation_file(self, file_path: Path, correlations: Dict):
        """Process a single correlation CSV file"""
        df = self.read_csv_safe(file_path)
        if df.empty:
            return
        
        # Extract language pair from filename
        lang1, lang2 = self.extract_language_pair(file_path.name)
        if not lang1 or not lang2:
            self.logger.warning(f"Could not extract language pair from {file_path.name}")
            return
        
        # Process correlation data
        correlation_score = self._calculate_average_correlation(df)
        if correlation_score is not None:
            correlations[f"{lang1}_{lang2}"] = correlation_score
            self.logger.debug(f"Added correlation {lang1}-{lang2}: {correlation_score:.3f}")
    
    def _calculate_average_correlation(self, df: pd.DataFrame) -> float:
        """Calculate average correlation from dataframe"""
        # Look for correlation columns (different CSV formats)
        correlation_columns = [col for col in df.columns if 
                             any(keyword in col.lower() for keyword in 
                                 ['correlation', 'cor', 'pearson', 'r'])]
        
        if not correlation_columns:
            # Try numeric columns (exclude cluster numbers)
            numeric_cols = df.select_dtypes(include=['float64', 'float32']).columns
            correlation_columns = [col for col in numeric_cols if col not in ['cluster', 'n_clusters']]
        
        if correlation_columns:
            # Take the first correlation column and average it
            correlation_values = df[correlation_columns[0]].dropna()
            if len(correlation_values) > 0:
                return float(correlation_values.mean())
        
        self.logger.warning(f"No correlation data found in dataframe columns: {list(df.columns)}")
        return None
    
    def _standardize_language_codes(self, correlations: Dict) -> Dict[str, Dict[str, float]]:
        """Convert ETS language codes to standard codes and create nested structure"""
        standardized = {}
        
        for pair_key, correlation in correlations.items():
            lang1, lang2 = pair_key.split('_')
            
            # Convert to standard codes
            std_lang1 = config.LANGUAGE_MAPPING.get(lang1.upper(), lang1.lower())
            std_lang2 = config.LANGUAGE_MAPPING.get(lang2.upper(), lang2.lower())
            
            # Create nested structure
            if std_lang1 not in standardized:
                standardized[std_lang1] = {}
            if std_lang2 not in standardized:
                standardized[std_lang2] = {}
            
            # Add bidirectional mapping
            standardized[std_lang1][std_lang2] = correlation
            standardized[std_lang2][std_lang1] = correlation
        
        return standardized