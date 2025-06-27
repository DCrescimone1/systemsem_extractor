# SYSTEMSEM Data Extractor

A focused Python tool to extract language correlation data from the SYSTEMSEM research project for integration with memoria_test.

## Quick Setup

1. **Update configuration**:
   ```bash
   # Edit config.py and set your SYSTEMSEM path
   SYSTEMSEM_PATH = "/path/to/your/SYSTEMSEM"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run extraction**:
   ```bash
   python main.py
   ```

## Output Files

The tool generates these JSON files in the `output/` directory:

- **`systemsem_correlations.json`** - Language pair semantic correlations
- **`language_families.json`** - Language family classifications  
- **`historical_contact.json`** - Historical contact data (if available)
- **`extraction_log.txt`** - Detailed extraction log

## What it extracts

- Language correlation coefficients from pairwise CSV files
- Language family relationships and classifications
- Linguistic distance metrics
- Historical contact information

## Integration with memoria_test

Copy the generated `systemsem_correlations.json` to your memoria_test project:

```bash
cp output/systemsem_correlations.json /path/to/memoria_test/data/
```

## Project Structure

```
systemsem_extractor/
├── config.py              # Configuration settings
├── main.py                 # Main entry point
├── src/
│   ├── extractor.py        # Main extractor class
│   ├── processors/         # Data processors
│   ├── generators/         # JSON generators
│   └── utils/             # Utilities
└── output/                # Generated files
```

Simple, focused, and ready to use! 🚀