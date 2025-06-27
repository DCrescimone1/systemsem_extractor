#!/usr/bin/env python3
"""
SYSTEMSEM Data Extractor - Main Entry Point

Extracts correlation data from SYSTEMSEM research for memoria_test integration.
"""

import sys
from pathlib import Path
from src.extractor import SystemsemExtractor
from src.utils.logger import setup_logger
import config

def main():
    """Main extraction process"""
    
    # Setup logging
    logger = setup_logger("main")
    
    logger.info("🚀 Starting SYSTEMSEM data extraction")
    logger.info(f"📁 Source: {config.SYSTEMSEM_PATH}")
    logger.info(f"📂 Output: {config.OUTPUT_DIR}")
    
    # Validate SYSTEMSEM path
    if not Path(config.SYSTEMSEM_PATH).exists():
        logger.error(f"❌ SYSTEMSEM path not found: {config.SYSTEMSEM_PATH}")
        logger.error("Please update SYSTEMSEM_PATH in config.py")
        sys.exit(1)
    
    # Create output directory
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    
    try:
        # Initialize extractor
        extractor = SystemsemExtractor(config.SYSTEMSEM_PATH)
        
        # Run extraction
        results = extractor.extract_all()
        
        # Report results
        logger.info("✅ Extraction completed successfully!")
        logger.info("📊 Generated files:")
        for file_path, record_count in results.items():
            logger.info(f"   📄 {file_path}: {record_count} records")
        
        logger.info("🎯 Ready for memoria_test integration!")
        
    except Exception as e:
        logger.error(f"❌ Extraction failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()