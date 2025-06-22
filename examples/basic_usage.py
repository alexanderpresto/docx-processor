#!/usr/bin/env python3
"""
Basic usage example for the docx-processor library.

This example demonstrates how to use docx-processor as a Python library
to process Word documents programmatically.
"""

import os
import sys

# Add parent directory to path to import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.docx_processor.processor import process_document
from src.docx_processor.version import __version__

def main():
    """Demonstrate basic usage of the docx-processor library."""
    
    print(f"docx-processor version: {__version__}")
    print("-" * 50)
    
    # Example 1: Basic document processing
    print("Example 1: Basic document processing")
    print("=" * 30)
    
    input_file = "example.docx"  # Replace with your document
    output_dir = "output"
    
    if not os.path.exists(input_file):
        print(f"Please provide a valid Word document at: {input_file}")
        print("You can copy any .docx file to this location to test.")
        return
    
    try:
        # Process with default settings
        print(f"Processing {input_file}...")
        process_document(input_file, output_dir)
        print(f"✓ Document processed successfully!")
        print(f"✓ Output saved to: {os.path.abspath(output_dir)}")
    except Exception as e:
        print(f"✗ Error processing document: {e}")
        return
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 2: Processing with custom options
    print("Example 2: Processing with custom options")
    print("=" * 30)
    
    output_dir_custom = "output_custom"
    
    try:
        print(f"Processing with custom settings...")
        process_document(
            input_file,
            output_dir_custom,
            image_quality=95,  # Higher quality images
            max_image_size=1600,  # Larger image size limit
            output_format="json",  # Only JSON output
            extract_tables=True    # Extract tables to CSV
        )
        print(f"✓ Document processed with custom settings!")
        print(f"✓ Output saved to: {os.path.abspath(output_dir_custom)}")
        
        # Show what was created
        if os.path.exists(output_dir_custom):
            print("\nCreated files:")
            for root, dirs, files in os.walk(output_dir_custom):
                level = root.replace(output_dir_custom, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")
                    
    except Exception as e:
        print(f"✗ Error processing document: {e}")
        return
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 3: Programmatic access to results
    print("Example 3: Accessing results programmatically")
    print("=" * 30)
    
    import json
    
    json_file = os.path.join(output_dir, "document_structure.json")
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            doc_data = json.load(f)
        
        print(f"Document title: {doc_data.get('title', 'Untitled')}")
        print(f"Number of sections: {len(doc_data.get('sections', []))}")
        print(f"Number of images: {len(doc_data.get('images', []))}")
        
        # Show first section
        if doc_data.get('sections'):
            first_section = doc_data['sections'][0]
            print(f"\nFirst section:")
            print(f"  Level: {first_section.get('level', 'N/A')}")
            print(f"  Type: {first_section.get('type', 'N/A')}")
            content_preview = first_section.get('content', '')[:100]
            if content_preview:
                print(f"  Content preview: {content_preview}...")
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("\nTip: You can import and use process_document() in your own scripts.")
    print("See the source code for more advanced options and customization.")

if __name__ == "__main__":
    main()
