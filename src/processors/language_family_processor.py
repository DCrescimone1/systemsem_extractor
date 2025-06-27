"""
Processor for language family and linguistic data
"""

from pathlib import Path
from typing import Dict, Any
from .base_processor import BaseProcessor
import config

class LanguageFamilyProcessor(BaseProcessor):
    """Processes language family and linguistic metadata"""
    
    def process(self) -> Dict[str, Any]:
        """
        Extract language family and related linguistic data
        Returns: Dict with language family information
        """
        families_data = {}
        
        # Look for language family files
        family_files = self.find_files("*language*family*.csv")
        family_files.extend(self.find_files("*linguistic*.csv"))
        
        self.logger.info(f"🌳 Processing {len(family_files)} language family files")
        
        for file_path in family_files:
            self._process_family_file(file_path, families_data)
        
        # If no specific family files found, create basic structure from language mapping
        if not families_data:
            families_data = self._create_basic_family_structure()
        
        self.logger.info(f"✅ Processed family data for {len(families_data)} languages")
        return families_data
    
    def _process_family_file(self, file_path: Path, families_data: Dict):
        """Process a language family CSV file"""
        df = self.read_csv_safe(file_path)
        if df.empty:
            return
        
        # Look for relevant columns
        lang_col = self._find_column(df, ['language', 'lang', 'code'])
        family_col = self._find_column(df, ['family', 'group', 'branch'])
        
        if lang_col and family_col:
            for _, row in df.iterrows():
                lang_code = str(row[lang_col]).lower()
                family = str(row[family_col])
                families_data[lang_code] = {
                    'family': family,
                    'source': file_path.name
                }
    
    def _find_column(self, df, possible_names):
        """Find column with any of the possible names"""
        for col in df.columns:
            if any(name in col.lower() for name in possible_names):
                return col
        return None
    
    def _create_basic_family_structure(self) -> Dict[str, Any]:
        """Create basic language family structure from known language codes"""
        # Basic language families for the languages in memoria_test
        basic_families = {
            'en': {'family': 'Germanic', 'branch': 'West Germanic'},
            'es': {'family': 'Romance', 'branch': 'Ibero-Romance'},
            'fr': {'family': 'Romance', 'branch': 'Gallo-Romance'},
            'de': {'family': 'Germanic', 'branch': 'West Germanic'},
            'it': {'family': 'Romance', 'branch': 'Italo-Western'},
            'pt': {'family': 'Romance', 'branch': 'Ibero-Romance'},
            'ru': {'family': 'Slavic', 'branch': 'East Slavic'},
            'zh': {'family': 'Sino-Tibetan', 'branch': 'Chinese'},
            'ja': {'family': 'Japonic', 'branch': 'Japanese'},
            'ar': {'family': 'Semitic', 'branch': 'Central Semitic'},
            'hi': {'family': 'Indo-European', 'branch': 'Indo-Aryan'},
        }
        
        # Add all languages from mapping
        for ets_code, std_code in config.LANGUAGE_MAPPING.items():
            if std_code not in basic_families:
                basic_families[std_code] = {
                    'family': 'Unknown',
                    'branch': 'Unknown',
                    'ets_code': ets_code
                }
        
        return basic_families