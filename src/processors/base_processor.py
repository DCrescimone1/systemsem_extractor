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
            # SYSTEMSEM correlation files have NO HEADERS
            # Format: cluster_count,type,correlation,lang1,lang2
            # Example: 10,global,0.364,en,tr
            
            read_strategies = [
                # Strategy 1: No header (correct for SYSTEMSEM files)
                {'header': None, 'encoding': 'utf-8'},
                # Strategy 2: Different separators without header
                {'header': None, 'encoding': 'utf-8', 'sep': ','},
                {'header': None, 'encoding': 'utf-8', 'sep': '\t'},
                # Strategy 3: Different encodings without header
                {'header': None, 'encoding': 'latin-1'},
                {'header': None, 'encoding': 'cp1252'},
                # Strategy 4: Skip problematic lines without header
                {'header': None, 'encoding': 'utf-8', 'on_bad_lines': 'skip'},
            ]
            
            for i, strategy in enumerate(read_strategies):
                try:
                    df = pd.read_csv(file_path, **strategy)
                    if not df.empty and len(df.columns) >= 3:
                        # Assign proper column names for SYSTEMSEM format
                        df.columns = ['n_clusters', 'type', 'correlation', 'lang1', 'lang2'][:len(df.columns)]
                        self.logger.debug(f"✅ Read {file_path.name} with strategy {i+1}: {len(df)} rows, {len(df.columns)} cols")
                        return df
                except (UnicodeDecodeError, pd.errors.ParserError) as e:
                    self.logger.debug(f"Strategy {i+1} failed for {file_path.name}: {e}")
                    continue
                except Exception as e:
                    self.logger.debug(f"Strategy {i+1} error for {file_path.name}: {e}")
                    continue
            
            # Last resort: read with maximum error tolerance
            try:
                df = pd.read_csv(file_path, header=None, encoding='utf-8', errors='ignore', 
                               on_bad_lines='skip', engine='python')
                if not df.empty and len(df.columns) >= 3:
                    df.columns = ['n_clusters', 'type', 'correlation', 'lang1', 'lang2'][:len(df.columns)]
                self.logger.warning(f"⚠️ Read {file_path.name} with error tolerance: {len(df)} rows")
                return df
            except Exception as e:
                self.logger.error(f"❌ All strategies failed for {file_path.name}: {e}")
                return pd.DataFrame()
            
        except Exception as e:
            self.logger.warning(f"❌ Completely failed to read {file_path}: {e}")
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