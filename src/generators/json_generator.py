"""
JSON file generator for extracted data
"""

import json
from pathlib import Path
from typing import Dict, Any
from ..utils.logger import setup_logger
import config

class JsonGenerator:
    """Generates JSON files from extracted data"""
    
    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)
        self.output_dir = config.OUTPUT_DIR
    
    def generate_correlations_json(self, correlations_data: Dict[str, Any]) -> str:
        """Generate systemsem_correlations.json file"""
        output_file = self.output_dir / "systemsem_correlations.json"
        
        # Add metadata
        output_data = {
            "metadata": {
                "description": "Language semantic similarity correlations from SYSTEMSEM research",
                "source": "SYSTEMSEM project - Local similarity and global variability paper",
                "extracted_by": "systemsem_extractor",
                "language_pairs": len(correlations_data)
            },
            "correlations": correlations_data
        }
        
        self._write_json(output_data, output_file)
        self.logger.info(f"📄 Generated correlations JSON: {output_file}")
        return str(output_file)
    
    def generate_families_json(self, families_data: Dict[str, Any]) -> str:
        """Generate language_families.json file"""
        output_file = self.output_dir / "language_families.json"
        
        output_data = {
            "metadata": {
                "description": "Language family classifications and relationships",
                "languages_count": len(families_data)
            },
            "families": families_data
        }
        
        self._write_json(output_data, output_file)
        self.logger.info(f"🌳 Generated families JSON: {output_file}")
        return str(output_file)
    
    def generate_contact_json(self, contact_data: Dict[str, Any]) -> str:
        """Generate historical_contact.json file"""
        output_file = self.output_dir / "historical_contact.json"
        
        output_data = {
            "metadata": {
                "description": "Historical language contact information",
                "source": "SYSTEMSEM extraction + linguistic fallback",
                "format": "language_code -> [list of contacted languages]",
                "contact_pairs": len(contact_data)
            },
            "contact_data": contact_data
        }
        
        self._write_json(output_data, output_file)
        self.logger.info(f"📚 Generated contact JSON: {output_file}")
        return str(output_file)
    
    def _write_json(self, data: Dict[str, Any], file_path: Path):
        """Write data to JSON file with pretty formatting"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.debug(f"Wrote JSON to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to write JSON to {file_path}: {e}")
            raise