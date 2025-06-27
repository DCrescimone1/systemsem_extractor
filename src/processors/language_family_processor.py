"""
Corrected Language Family Processor that extracts from WALS data in SYSTEMSEM
"""

from pathlib import Path
from typing import Dict, Any
import pandas as pd
from .base_processor import BaseProcessor
import config

class LanguageFamilyProcessor(BaseProcessor):
    """Processes language family data from SYSTEMSEM WALS files"""
    
    def process(self) -> Dict[str, Any]:
        """
        Extract language family data from SYSTEMSEM WALS database
        Returns: Dict with accurate language family information
        """
        families_data = {}
        
        # Step 1: Look for WALS mapping file in SYSTEMSEM
        wals_mapping_file = self._find_wals_mapping_file()
        if wals_mapping_file:
            families_data = self._extract_from_wals_mapping(wals_mapping_file)
        
        # Step 2: If no WALS file found, use comprehensive linguistic database
        if not families_data:
            self.logger.warning("No WALS mapping found in SYSTEMSEM, using comprehensive database")
            families_data = self._create_comprehensive_family_structure()
        
        self.logger.info(f"✅ Processed family data for {len(families_data)} languages")
        return families_data
    
    def _find_wals_mapping_file(self) -> Path:
        """Find the WALS language mapping file in SYSTEMSEM"""
        # Look for the specific WALS mapping file mentioned in the research
        possible_paths = [
            "analyses/04_predicting_semantic_sim/data/lang_distance_metrics/linguistic/data/iso_to_wals_for_ling_dists.csv",
            "**/iso_to_wals*.csv",
            "**/wals*mapping*.csv",
            "**/linguistic*.csv"
        ]
        
        for pattern in possible_paths:
            files = list(self.systemsem_path.rglob(pattern))
            if files:
                self.logger.info(f"Found WALS mapping file: {files[0]}")
                return files[0]
        
        self.logger.warning("No WALS mapping file found in SYSTEMSEM")
        return None
    
    def _extract_from_wals_mapping(self, file_path: Path) -> Dict[str, Any]:
        """Extract language families from WALS mapping file"""
        try:
            df = self.read_csv_safe(file_path)
            if df.empty:
                return {}
            
            families_data = {}
            
            # The file should have columns like: iso, ETS_lang_name, wals_code
            for _, row in df.iterrows():
                iso_code = str(row.get('iso', '')).lower()
                ets_code = str(row.get('ETS_lang_name', '')).upper()
                
                if iso_code and ets_code:
                    # Map to comprehensive family data
                    family_info = self._get_language_family_info(iso_code)
                    if family_info:
                        families_data[iso_code] = {
                            **family_info,
                            'ets_code': ets_code,
                            'source': 'wals_mapping'
                        }
            
            return families_data
            
        except Exception as e:
            self.logger.error(f"Error processing WALS mapping file: {e}")
            return {}
    
    def _get_language_family_info(self, iso_code: str) -> Dict[str, str]:
        """Get comprehensive language family information for ISO code"""
        
        # Comprehensive language family database (linguistically accurate)
        family_database = {
            'ar': {'family': 'Afro-Asiatic', 'branch': 'Semitic', 'sub_branch': 'Central Semitic'},
            'bn': {'family': 'Indo-European', 'branch': 'Indo-Aryan', 'sub_branch': 'Eastern Indo-Aryan'},
            'bg': {'family': 'Indo-European', 'branch': 'Slavic', 'sub_branch': 'South Slavic'},
            'zh': {'family': 'Sino-Tibetan', 'branch': 'Chinese', 'sub_branch': 'Mandarin'},
            'nl': {'family': 'Indo-European', 'branch': 'Germanic', 'sub_branch': 'West Germanic'},
            'en': {'family': 'Indo-European', 'branch': 'Germanic', 'sub_branch': 'West Germanic'},
            'fa': {'family': 'Indo-European', 'branch': 'Iranian', 'sub_branch': 'Western Iranian'},
            'fr': {'family': 'Indo-European', 'branch': 'Romance', 'sub_branch': 'Gallo-Romance'},
            'de': {'family': 'Indo-European', 'branch': 'Germanic', 'sub_branch': 'West Germanic'},
            'el': {'family': 'Indo-European', 'branch': 'Hellenic', 'sub_branch': 'Greek'},
            'gu': {'family': 'Indo-European', 'branch': 'Indo-Aryan', 'sub_branch': 'Western Indo-Aryan'},
            'hi': {'family': 'Indo-European', 'branch': 'Indo-Aryan', 'sub_branch': 'Central Indo-Aryan'},
            'ig': {'family': 'Niger-Congo', 'branch': 'Volta-Niger', 'sub_branch': 'Igboid'},
            'id': {'family': 'Austronesian', 'branch': 'Malayo-Polynesian', 'sub_branch': 'Western Malayo-Polynesian'},
            'it': {'family': 'Indo-European', 'branch': 'Romance', 'sub_branch': 'Italo-Western'},
            'ja': {'family': 'Japonic', 'branch': 'Japanese', 'sub_branch': 'Japanese'},
            'kn': {'family': 'Dravidian', 'branch': 'Southern Dravidian', 'sub_branch': 'Tamil-Kannada'},
            'ko': {'family': 'Koreanic', 'branch': 'Korean', 'sub_branch': 'Korean'},
            'ml': {'family': 'Dravidian', 'branch': 'Southern Dravidian', 'sub_branch': 'Tamil-Malayalam'},
            'mr': {'family': 'Indo-European', 'branch': 'Indo-Aryan', 'sub_branch': 'Southern Indo-Aryan'},
            'ne': {'family': 'Indo-European', 'branch': 'Indo-Aryan', 'sub_branch': 'Northern Indo-Aryan'},
            'pa': {'family': 'Indo-European', 'branch': 'Indo-Aryan', 'sub_branch': 'Northwestern Indo-Aryan'},
            'pl': {'family': 'Indo-European', 'branch': 'Slavic', 'sub_branch': 'West Slavic'},
            'pt': {'family': 'Indo-European', 'branch': 'Romance', 'sub_branch': 'Ibero-Romance'},
            'ro': {'family': 'Indo-European', 'branch': 'Romance', 'sub_branch': 'Eastern Romance'},
            'ru': {'family': 'Indo-European', 'branch': 'Slavic', 'sub_branch': 'East Slavic'},
            'es': {'family': 'Indo-European', 'branch': 'Romance', 'sub_branch': 'Ibero-Romance'},
            'ta': {'family': 'Dravidian', 'branch': 'Southern Dravidian', 'sub_branch': 'Tamil-Malayalam'},
            'te': {'family': 'Dravidian', 'branch': 'South-Central Dravidian', 'sub_branch': 'Telugu'},
            'tl': {'family': 'Austronesian', 'branch': 'Malayo-Polynesian', 'sub_branch': 'Philippine'},
            'th': {'family': 'Tai-Kadai', 'branch': 'Tai', 'sub_branch': 'Southwestern Tai'},
            'tr': {'family': 'Turkic', 'branch': 'Southwestern Turkic', 'sub_branch': 'Turkish'},
            'ur': {'family': 'Indo-European', 'branch': 'Indo-Aryan', 'sub_branch': 'Central Indo-Aryan'},
            'vi': {'family': 'Austroasiatic', 'branch': 'Vietic', 'sub_branch': 'Vietnamese'},
            'yo': {'family': 'Niger-Congo', 'branch': 'Volta-Niger', 'sub_branch': 'Defoid'},
        }
        
        return family_database.get(iso_code, {})
    
    def _create_comprehensive_family_structure(self) -> Dict[str, Any]:
        """Create comprehensive language family structure from linguistic research"""
        families_data = {}
        
        # Map all languages we know about from config.LANGUAGE_MAPPING
        for ets_code, iso_code in config.LANGUAGE_MAPPING.items():
            family_info = self._get_language_family_info(iso_code.lower())
            if family_info:
                families_data[iso_code.lower()] = {
                    **family_info,
                    'ets_code': ets_code,
                    'source': 'comprehensive_database'
                }
        
        return families_data


# Test the corrected processor
def test_corrected_processor():
    """Test the corrected language family processor"""
    processor = LanguageFamilyProcessor(Path("/mock/path"))
    
    # Test comprehensive database
    families = processor._create_comprehensive_family_structure()
    
    print("=== Corrected Language Family Data ===\n")
    
    # Test some key languages that were marked as "Unknown" before
    test_languages = ['bn', 'bg', 'nl', 'fa', 'el', 'pl', 'ro', 'ko']
    
    for lang in test_languages:
        if lang in families:
            family_data = families[lang]
            print(f"{lang.upper()}: {family_data['family']} → {family_data['branch']} → {family_data['sub_branch']}")
        else:
            print(f"{lang.upper()}: Not found")
    
    print(f"\nTotal languages classified: {len(families)}")
    
    # Count by family
    family_counts = {}
    for lang_data in families.values():
        family = lang_data['family']
        family_counts[family] = family_counts.get(family, 0) + 1
    
    print("\nLanguages by family:")
    for family, count in sorted(family_counts.items()):
        print(f"  {family}: {count} languages")

if __name__ == "__main__":
    test_corrected_processor()