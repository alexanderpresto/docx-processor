#!/usr/bin/env python3
import os
import argparse
import sys

# Import from the new package structure
from src.docx_processor.processor import process_document
from src.docx_processor.version import __version__

def main():
    """Main entry point for the docx-processor application."""
    parser = argparse.ArgumentParser(
        description="Process Word documents into analyzable formats",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input", help="Input Word document path")
    parser.add_argument("output", help="Output directory path")
    parser.add_argument("--image-quality", type=int, default=85, 
                       help="Image quality (1-100)")
    parser.add_argument("--max-image-size", type=int, default=1200, 
                       help="Maximum image dimension in pixels")
    parser.add_argument("--format", choices=["json", "html", "both"], default="both", 
                       help="Output format (json, html, or both)")
    parser.add_argument("--extract-tables", action="store_true", 
                       help="Extract tables to CSV files")
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
    
    # Convert relative paths to absolute paths based on current working directory
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)
    
    # Validate input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
        return 1
    
    # Validate input file is a .docx
    if not input_path.lower().endswith('.docx'):
        print(f"Warning: Input file '{input_path}' does not have .docx extension.", 
              file=sys.stderr)
    
    # Validate image quality range
    if args.image_quality < 1 or args.image_quality > 100:
        print("Error: Image quality must be between 1-100.", file=sys.stderr)
        return 1
    
    # Process document
    try:
        process_document(
            input_path, 
            output_path,
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
        print(f"Document processed successfully. Output saved to {output_path}")
        return 0
    except Exception as e:
        print(f"Error processing document: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
