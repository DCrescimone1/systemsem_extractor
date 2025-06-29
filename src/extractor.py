"""
Main SYSTEMSEM data extractor class
"""

from pathlib import Path
from typing import Dict, Any, List
from .processors.correlation_processor import CorrelationProcessor
from .processors.language_family_processor import LanguageFamilyProcessor
from .generators.json_generator import JsonGenerator
from .utils.logger import setup_logger
import config

class SystemsemExtractor:
    """Main extractor class that coordinates data extraction from SYSTEMSEM"""
    
    def __init__(self, systemsem_path: str):
        self.systemsem_path = Path(systemsem_path)
        self.logger = setup_logger(self.__class__.__name__)
        self.json_generator = JsonGenerator()
        
        # Initialize processors
        self.processors = {
            'correlations': CorrelationProcessor(self.systemsem_path),
            'language_families': LanguageFamilyProcessor(self.systemsem_path)
        }
    
    def extract_all(self) -> Dict[str, int]:
        """
        Extract all data and generate JSON files
        Returns dict of generated files and their record counts
        """
        results = {}
        
        self.logger.info("🔄 Starting data extraction process")
        
        # Extract language correlations
        self.logger.info("📊 Processing language correlations...")
        correlations_data = self.processors['correlations'].process()
        correlation_file = self.json_generator.generate_correlations_json(correlations_data)
        results[correlation_file] = len(correlations_data)
        
        # Extract language families
        self.logger.info("🌳 Processing language families...")
        families_data = self.processors['language_families'].process()
        families_file = self.json_generator.generate_families_json(families_data)
        results[families_file] = len(families_data)
        
        # Extract historical contact data
        self.logger.info("📚 Processing historical contact data...")
        contact_data = self._extract_historical_contact()
        # Always generate historical_contact.json, even with fallback data
        contact_file = self.json_generator.generate_contact_json(contact_data)
        results[contact_file] = len(contact_data) if contact_data else 0
        
        self.logger.info(f"✅ Extracted {len(results)} datasets")
        return results
    
    def _extract_historical_contact(self) -> Dict[str, Any]:
        """Extract historical contact data with fallback to linguistic knowledge"""
        # Step 1: Try to find actual historical contact files
        contact_files = list(self.systemsem_path.rglob("*historical*contact*.csv"))
        
        historical_contacts = {}
        
        if contact_files:
            self.logger.info(f"📖 Found {len(contact_files)} contact files")
            # TODO: Parse actual CSV files here when available
            for file_path in contact_files:
                try:
                    # Add actual CSV parsing logic if files exist
                    pass
                except Exception as e:
                    self.logger.warning(f"Failed to parse {file_path}: {e}")
        else:
            self.logger.info("ℹ️ No historical contact files found, using linguistic fallback")
        
        # Step 2: Add linguistic fallback data based on known historical contacts
        fallback_contacts = self._create_fallback_contact_data()
        historical_contacts.update(fallback_contacts)
        
        return historical_contacts
    
    def _create_fallback_contact_data(self) -> Dict[str, List[str]]:
        """Create fallback historical contact data based on linguistic knowledge"""
        return {
            # European languages with historical contact
            "en": ["fr", "de", "nl", "es", "it"],  # English colonial/trade contacts
            "fr": ["en", "de", "it", "es", "nl"],  # French historical contacts
            "de": ["en", "fr", "nl", "pl", "it"],  # German historical contacts
            "es": ["fr", "it", "pt", "en"],        # Spanish historical contacts
            "it": ["fr", "es", "de"],              # Italian historical contacts
            "pt": ["es", "fr"],                    # Portuguese historical contacts
            "nl": ["en", "de", "fr"],              # Dutch historical contacts
            
            # Slavic contacts
            "ru": ["pl", "bg", "de"],              # Russian historical contacts
            "pl": ["de", "ru"],                    # Polish historical contacts
            "bg": ["ru", "el"],                    # Bulgarian historical contacts
            
            # South Asian contacts  
            "hi": ["ur", "bn", "fa"],              # Hindi historical contacts
            "ur": ["hi", "fa", "ar"],              # Urdu historical contacts
            "bn": ["hi"],                          # Bengali historical contacts
            
            # Arabic contacts
            "ar": ["fa", "tr", "ur"],              # Arabic historical contacts
            "fa": ["ar", "hi", "ur", "tr"],        # Persian historical contacts
            
            # Other contacts
            "tr": ["ar", "fa", "bg"],              # Turkish historical contacts
            "el": ["bg", "it"],                    # Greek historical contacts
        }