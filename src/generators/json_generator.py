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
        """Generate language_correlations.json file with simplified format"""
        output_file = self.output_dir / "language_correlations.json"
        
        # Create simplified flat format with just the global correlation values
        simplified_correlations = {}
        for pair, data in correlations_data.items():
            if isinstance(data, dict) and 'global' in data:
                simplified_correlations[pair] = data['global']
            else:
                simplified_correlations[pair] = data  # In case it's already simplified
        
        output_data = simplified_correlations
        
        self._write_json(output_data, output_file)
        self.logger.info(f"📄 Generated simplified correlations JSON: {output_file}")
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
        """Generate historical_contact.json file with simplified format"""
        output_file = self.output_dir / "historical_contact.json"
        
        # Output simplified flat format
        output_data = contact_data
        
        self._write_json(output_data, output_file)
        self.logger.info(f"📚 Generated simplified contact JSON: {output_file}")
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