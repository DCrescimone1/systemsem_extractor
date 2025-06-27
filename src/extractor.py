"""
Main SYSTEMSEM data extractor class
"""

from pathlib import Path
from typing import Dict, Any
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
        
        # Extract historical contact (if available)
        self.logger.info("📚 Processing historical contact data...")
        contact_data = self._extract_historical_contact()
        if contact_data:
            contact_file = self.json_generator.generate_contact_json(contact_data)
            results[contact_file] = len(contact_data)
        
        self.logger.info(f"✅ Extracted {len(results)} datasets")
        return results
    
    def _extract_historical_contact(self) -> Dict[str, Any]:
        """Extract historical contact data if available"""
        # Look for historical contact files
        contact_files = list(self.systemsem_path.rglob("*historical*contact*.csv"))
        
        if not contact_files:
            self.logger.info("ℹ️ No historical contact data found")
            return {}
        
        # Simple extraction - can be expanded later
        self.logger.info(f"📖 Found {len(contact_files)} contact files")
        return {"files_found": len(contact_files)}  # Placeholder