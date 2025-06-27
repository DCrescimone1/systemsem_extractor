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
        try:
            df = self.read_csv_safe(file_path)
            if df.empty:
                return
            
            # Extract language pair from filename
            lang1, lang2 = self.extract_language_pair(file_path.name)
            if not lang1 or not lang2:
                self.logger.warning(f"Could not extract language pair from {file_path.name}")
                return
            
            # Process correlation data
            correlation_score = self._calculate_average_correlation(df, file_path.name)
            if correlation_score is not None:
                correlations[f"{lang1}_{lang2}"] = correlation_score
                self.logger.debug(f"Added correlation {lang1}-{lang2}: {correlation_score:.3f}")
        except Exception as e:
            self.logger.warning(f"Failed to process {file_path.name}: {e}")
            return
    
    def _calculate_average_correlation(self, df: pd.DataFrame, filename: str = "") -> float:
        """Calculate average correlation from SYSTEMSEM dataframe"""
        try:
            # Debug: print structure for first few files
            self.logger.debug(f"CSV structure for {filename}: columns={list(df.columns)}, shape={df.shape}")
            if len(df) > 0:
                self.logger.debug(f"First few rows: {df.head(2).to_dict('records')}")
            
            # SYSTEMSEM files should now have proper column names after reading
            if 'correlation' in df.columns:
                # Perfect! Use the correlation column directly
                correlation_values = pd.to_numeric(df['correlation'], errors='coerce').dropna()
                
                if len(correlation_values) > 0:
                    # Filter reasonable correlation range [-1, 1]
                    valid_correlations = correlation_values[(correlation_values >= -1.0) & (correlation_values <= 1.0)]
                    
                    if len(valid_correlations) > 0:
                        avg_correlation = float(valid_correlations.mean())
                        self.logger.debug(f"✅ {filename}: correlation column -> {avg_correlation:.4f} (from {len(valid_correlations)} values)")
                        return avg_correlation
                    else:
                        self.logger.warning(f"❌ {filename}: No correlations in valid range [-1,1]")
                        return None
                else:
                    self.logger.warning(f"❌ {filename}: No numeric values in correlation column")
                    return None
            
            # Fallback: try to find correlation column by position (column index 2 for SYSTEMSEM)
            elif len(df.columns) >= 3:
                correlation_col = df.iloc[:, 2]  # Third column (index 2)
                correlation_values = pd.to_numeric(correlation_col, errors='coerce').dropna()
                
                if len(correlation_values) > 0:
                    # Filter reasonable correlation range
                    valid_correlations = correlation_values[(correlation_values >= -1.0) & (correlation_values <= 1.0)]
                    
                    if len(valid_correlations) > 0:
                        avg_correlation = float(valid_correlations.mean())
                        self.logger.debug(f"✅ {filename}: column[2] -> {avg_correlation:.4f} (from {len(valid_correlations)} values)")
                        return avg_correlation
                    else:
                        self.logger.warning(f"❌ {filename}: Column[2] has no valid correlations in range [-1,1]")
                        return None
                else:
                    self.logger.warning(f"❌ {filename}: Column[2] has no numeric values")
                    return None
            
            else:
                self.logger.warning(f"❌ {filename}: Insufficient columns ({len(df.columns)}). Expected SYSTEMSEM format: cluster,type,correlation,lang1,lang2")
                return None
            
        except Exception as e:
            self.logger.warning(f"❌ Error calculating correlation for {filename}: {e}")
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