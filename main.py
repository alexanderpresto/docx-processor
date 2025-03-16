#!/usr/bin/env python3
import os
import argparse
from src.docx_processor.processor import process_document

def main():
    parser = argparse.ArgumentParser(description="Process Word documents into analyzable formats")
    parser.add_argument("input", help="Input Word document path")
    parser.add_argument("output", help="Output directory path")
    parser.add_argument("--image-quality", type=int, default=85, help="Image quality (1-100)")
    parser.add_argument("--max-image-size", type=int, default=1200, help="Maximum image dimension")
    parser.add_argument("--format", choices=["json", "html", "both"], default="both", 
                       help="Output format (json, html, or both)")
    parser.add_argument("--extract-tables", action="store_true", help="Extract tables to CSV files")
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return 1
    
    # Process document
    try:
        process_document(
            args.input, 
            args.output,
            image_quality=args.image_quality,
            max_image_size=args.max_image_size,
            output_format=args.format,
            extract_tables=args.extract_tables
        )
        print(f"Document processed successfully. Output saved to {args.output}")
        return 0
    except Exception as e:
        print(f"Error processing document: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
