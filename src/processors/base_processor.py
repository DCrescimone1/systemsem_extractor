"""
Base processor class for data extraction
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from ..utils.logger import setup_logger

class BaseProcessor(ABC):
    """Abstract base class for data processors"""
    
    def __init__(self, systemsem_path: Path):
        self.systemsem_path = systemsem_path
        self.logger = setup_logger(self.__class__.__name__)
    
    @abstractmethod
    def process(self) -> Dict[str, Any]:
        """Process data and return structured results"""
        pass
    
    def find_files(self, pattern: str, subdirs: List[str] = None) -> List[Path]:
        """Find files matching pattern in specified subdirectories"""
        files = []
        
        if subdirs:
            for subdir in subdirs:
                search_path = self.systemsem_path / subdir
                if search_path.exists():
                    files.extend(search_path.rglob(pattern))
        else:
            files.extend(self.systemsem_path.rglob(pattern))
        
        self.logger.debug(f"Found {len(files)} files matching '{pattern}'")
        return files
    
    def read_csv_safe(self, file_path: Path) -> pd.DataFrame:
        """Safely read CSV file with error handling"""
        try:
            df = pd.read_csv(file_path)
            self.logger.debug(f"Read {len(df)} rows from {file_path.name}")
            return df
        except Exception as e:
            self.logger.warning(f"Failed to read {file_path}: {e}")
            return pd.DataFrame()
    
    def extract_language_pair(self, filename: str) -> tuple:
        """Extract language pair from filename"""
        # Common patterns: "lang1_lang2.csv" or "correlations_lang1_lang2.csv"
        parts = filename.replace('.csv', '').split('_')
        
        # Look for language codes (typically 2-3 characters)
        lang_codes = [part for part in parts if len(part) in [2, 3] and part.isalpha()]
        
        if len(lang_codes) >= 2:
            return lang_codes[-2], lang_codes[-1]  # Last two are usually the languages
        
        return None, None