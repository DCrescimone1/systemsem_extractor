#!/usr/bin/env python3
"""
Convert SYSTEMSEM web_correlations.json to memoria_test format
Simple, direct, efficient.
"""

import json
import os

# Language code mapping (3-letter to 2-letter ISO)
LANGUAGE_MAPPING = {
    "ARA": "ar", "BEN": "bn", "BUL": "bg", "CHI": "zh", "DUT": "nl",
    "ENG": "en", "FAS": "fa", "FRE": "fr", "GER": "de", "GRE": "el", 
    "GUJ": "gu", "HIN": "hi", "IBO": "ig", "IND": "id", "ITA": "it",
    "JPN": "ja", "KAN": "kn", "KOR": "ko", "MAL": "ml", "MAR": "mr",
    "NEP": "ne", "PAN": "pa", "POL": "pl", "POR": "pt", "RUM": "ro",
    "RUS": "ru", "SPA": "es", "TAM": "ta", "TEL": "te", "TGL": "tl",
    "THA": "th"
}

def convert_correlations():
    """Convert correlations to memoria_test format"""
    
    # Input file
    input_file = "output/web_correlations.json"
    
    # Output file for memoria_test  
    output_file = "output/language_correlations.json"
    
    print(f"🔄 Converting {input_file} to {output_file}")
    
    # Read input
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found")
        return False
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {input_file}")
        return False
    
    # Extract correlations
    correlations = data.get("correlations", {})
    if not correlations:
        print("❌ Error: No 'correlations' found in input file")
        return False
    
    print(f"📊 Found {len(correlations)} language pairs")
    
    # Convert format
    converted = {}
    skipped = 0
    
    for pair_key, correlation in correlations.items():
        try:
            # Parse language codes (e.g., "ARA_BEN" -> ["ARA", "BEN"])
            lang1, lang2 = pair_key.split("_")
            
            # Convert to 2-letter codes
            iso1 = LANGUAGE_MAPPING.get(lang1)
            iso2 = LANGUAGE_MAPPING.get(lang2)
            
            if not iso1 or not iso2:
                print(f"⚠️  Skipping unknown language codes: {pair_key}")
                skipped += 1
                continue
            
            # Create new key format (e.g., "ar-bn")
            new_key = f"{iso1}-{iso2}"
            
            # Store just the correlation value
            converted[new_key] = correlation
            
        except ValueError:
            print(f"⚠️  Skipping malformed pair: {pair_key}")
            skipped += 1
            continue
    
    print(f"✅ Converted {len(converted)} pairs")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} pairs")
    
    # Create output directory if needed
    os.makedirs("data", exist_ok=True)
    
    # Write output
    try:
        with open(output_file, 'w') as f:
            json.dump(converted, f, indent=2)
        print(f"💾 Saved to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error writing output: {e}")
        return False

def main():
    """Main function"""
    print("🚀 SYSTEMSEM Data Converter")
    print("=" * 40)
    
    success = convert_correlations()
    
    if success:
        print("\n🎉 Conversion complete!")
        print("\n📋 Next steps:")
        print("1. Copy the generated data/systemsem_correlations.json")
        print("2. Place it in your memoria_test/data/ folder")
        print("3. Test with: python main.py <word>")
    else:
        print("\n❌ Conversion failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())