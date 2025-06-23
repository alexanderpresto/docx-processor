#!/usr/bin/env python3
import os
import argparse
import sys
import traceback

# Import version from dedicated module to avoid circular imports
from .version import __version__
from .processor import process_document

def main():
    """Main entry point for the docx-processor application."""
    parser = argparse.ArgumentParser(description="Process Word documents into analyzable formats")
    parser.add_argument("input", help="Input Word document path")
    parser.add_argument("output", help="Output directory path")
    parser.add_argument("--image-quality", type=int, default=85, help="Image quality (1-100)")
    parser.add_argument("--max-image-size", type=int, default=1200, help="Maximum image dimension")
    parser.add_argument("--format", choices=["json", "html", "both"], default="both", 
                       help="Output format (json, html, or both)")
    parser.add_argument("--extract-tables", action="store_true", help="Extract tables to CSV files")
    parser.add_argument("--enable-chunking", action="store_true", 
                       help="Enable intelligent document chunking for AI processing")
    parser.add_argument("--max-chunk-tokens", type=int, default=2000,
                       help="Maximum tokens per chunk (default: 2000)")
    parser.add_argument("--chunk-overlap", type=int, default=200,
                       help="Token overlap between chunks (default: 200)")
    # Phase 2: Enhanced Metadata and Style Extraction
    parser.add_argument("--extract-metadata", action="store_true",
                       help="Extract comprehensive document metadata")
    parser.add_argument("--extract-styles", action="store_true",
                       help="Extract document style and formatting information")
    parser.add_argument("--include-comments", action="store_true",
                       help="Include comments in metadata extraction (requires --extract-metadata)")
    parser.add_argument("--version", action="version", version=f"docx-processor {__version__}")
    
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
            extract_tables=args.extract_tables,
            enable_chunking=args.enable_chunking,
            max_chunk_tokens=args.max_chunk_tokens,
            chunk_overlap=args.chunk_overlap,
            extract_metadata=args.extract_metadata,
            extract_styles=args.extract_styles,
            include_comments=args.include_comments
        )
        print(f"Document processed successfully. Output saved to {args.output}")
        return 0
    except Exception as e:
        print(f"Error processing document: {e}")
        print("Detailed error information:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
