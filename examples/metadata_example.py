#!/usr/bin/env python3
"""
Example script demonstrating Phase 2 Enhanced Metadata Extraction features.

This script shows how to use the docx-processor v2.0 Phase 2 features:
- Comprehensive metadata extraction
- Style and formatting analysis
- Comment extraction with context

Requirements:
- docx-processor v2.0.0-beta or higher
- Sample DOCX file for testing

Usage:
    python metadata_example.py sample.docx output_dir
"""

import sys
import os
import json
from pathlib import Path

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from docx_processor.processor import DocxProcessor
from docx_processor.metadata_extractor import MetadataExtractor
from docx_processor.style_extractor import StyleExtractor


def demonstrate_metadata_extraction(docx_path: str, output_dir: str):
    """
    Demonstrate Phase 2 metadata extraction capabilities.
    
    Args:
        docx_path: Path to input DOCX file
        output_dir: Directory for output files
    """
    print(f"🚀 Phase 2 Metadata Extraction Demo")
    print(f"📄 Input: {docx_path}")
    print(f"📁 Output: {output_dir}")
    print("-" * 50)
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize processor with Phase 2 features enabled
    processor = DocxProcessor(
        extract_metadata=True,
        extract_styles=True,
        include_comments=True
    )
    
    try:
        # Process the document
        print("📖 Processing document...")
        result = processor.process_document(docx_path, output_dir)
        
        if result:
            print("✅ Processing completed successfully!")
            
            # Display summary of extracted metadata
            print("\n📊 Extraction Summary:")
            print(f"  • Document structure: {'✅' if 'structure' in result else '❌'}")
            print(f"  • Metadata: {'✅' if 'metadata' in result else '❌'}")
            print(f"  • Styles: {'✅' if 'styles' in result else '❌'}")
            print(f"  • Comments: {'✅' if 'comments' in result else '❌'}")
            
            # Show specific metadata if available
            if 'metadata' in result and result['metadata']:
                metadata = result['metadata']
                print(f"\n📋 Document Properties:")
                print(f"  • Title: {metadata.get('title', 'N/A')}")
                print(f"  • Author: {metadata.get('author', 'N/A')}")
                print(f"  • Created: {metadata.get('created', 'N/A')}")
                print(f"  • Modified: {metadata.get('modified', 'N/A')}")
                print(f"  • Pages: {metadata.get('pages', 'N/A')}")
                print(f"  • Words: {metadata.get('words', 'N/A')}")
            
            # Show style information
            if 'styles' in result and result['styles']:
                styles = result['styles']
                font_info = styles.get('fonts', {})
                if font_info:
                    print(f"\n🎨 Style Information:")
                    print(f"  • Font families used: {len(font_info.get('families', []))}")
                    if font_info.get('families'):
                        print(f"  • Primary fonts: {', '.join(list(font_info['families'].keys())[:3])}")
            
            # Show comment count
            if 'comments' in result and result['comments']:
                comments = result['comments']
                print(f"\n💬 Comments: {len(comments.get('comments', []))} found")
            
            # List output files
            print(f"\n📄 Output Files:")
            output_path = Path(output_dir)
            for file_path in sorted(output_path.glob("*.json")):
                size_kb = file_path.stat().st_size / 1024
                print(f"  • {file_path.name} ({size_kb:.1f} KB)")
            
        else:
            print("❌ Processing failed!")
            
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return False
    
    return True


def demonstrate_direct_extraction(docx_path: str):
    """
    Demonstrate direct use of metadata and style extractors.
    
    Args:
        docx_path: Path to input DOCX file
    """
    print(f"\n🔧 Direct Extractor Demo")
    print("-" * 30)
    
    # Direct metadata extraction
    print("📋 Testing MetadataExtractor...")
    metadata_extractor = MetadataExtractor()
    metadata = metadata_extractor.extract_all_metadata(docx_path)
    
    if metadata and not metadata.get('extraction_errors'):
        print("✅ Metadata extraction successful")
        core_props = metadata.get('core_properties', {})
        if core_props:
            print(f"  • Document title: {core_props.get('title', 'N/A')}")
            print(f"  • Last author: {core_props.get('last_modified_by', 'N/A')}")
    else:
        print("❌ Metadata extraction had issues")
        if metadata.get('extraction_errors'):
            for error in metadata['extraction_errors'][:3]:  # Show first 3 errors
                print(f"  • Error: {error}")
    
    # Direct style extraction
    print("\n🎨 Testing StyleExtractor...")
    style_extractor = StyleExtractor()
    styles = style_extractor.extract_all_styles(docx_path)
    
    if styles and not styles.get('extraction_errors'):
        print("✅ Style extraction successful")
        fonts = styles.get('fonts', {})
        if fonts.get('families'):
            print(f"  • Font families found: {len(fonts['families'])}")
    else:
        print("❌ Style extraction had issues")
        if styles.get('extraction_errors'):
            for error in styles['extraction_errors'][:3]:  # Show first 3 errors
                print(f"  • Error: {error}")


def main():
    """Main demonstration function."""
    if len(sys.argv) != 3:
        print("Usage: python metadata_example.py <input.docx> <output_directory>")
        print("\nExample:")
        print("  python metadata_example.py sample.docx ./output")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Verify input file exists
    if not os.path.exists(docx_path):
        print(f"❌ Error: Input file '{docx_path}' not found")
        sys.exit(1)
    
    # Run demonstrations
    success = demonstrate_metadata_extraction(docx_path, output_dir)
    
    if success:
        demonstrate_direct_extraction(docx_path)
        
        print(f"\n🎉 Demo completed!")
        print(f"Check the output directory '{output_dir}' for generated files:")
        print("  • metadata.json - Comprehensive document metadata")
        print("  • styles.json - Style and formatting information")
        print("  • comments.json - Document comments with context")
        print("  • document_structure.json - Complete document structure")
        print("  • index.html - Interactive preview")
    else:
        print("\n❌ Demo failed. Check error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
