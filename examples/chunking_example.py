#!/usr/bin/env python3
"""
Example demonstrating the intelligent document chunking feature.

This example shows how to use the new chunking capabilities added in v2.0
to split documents into AI-friendly chunks with context preservation.
"""

import sys
import os
import json
import tempfile

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from docx_processor.processor import process_document

def main():
    """Demonstrate chunking with a sample document."""
    
    # Check if a DOCX file was provided
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' not found.")
            return 1
    else:
        print("Usage: python chunking_example.py <path_to_docx_file>")
        print("Example: python chunking_example.py ../tests/test_data/sample.docx")
        return 1
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Processing document: {input_file}")
        print(f"Output directory: {temp_dir}")
        print()
        
        # Process document with chunking enabled
        try:
            result = process_document(
                file_path=input_file,
                output_dir=temp_dir,
                image_quality=85,
                max_image_size=1200,
                output_format="json",  # JSON only for cleaner output
                extract_tables=False,
                enable_chunking=True,
                max_chunk_tokens=1000,  # Smaller chunks for demonstration
                chunk_overlap=100
            )
            
            print("Document processed successfully!")
            print()
            
            # Display chunking results
            if "chunks" in result:
                chunks = result["chunks"]
                summary = result["chunk_summary"]
                
                print(f"Chunking Results:")
                print(f"- Total chunks created: {summary['total_chunks']}")
                print(f"- Total tokens: {summary['total_tokens']}")
                print(f"- Average chunk size: {summary['average_chunk_size']} tokens")
                print(f"- Overlap ratio: {summary['overlap_ratio']:.2%}")
                print()
                
                # Show first few chunks
                print("First 3 chunks:")
                for i, chunk in enumerate(chunks[:3]):
                    print(f"\nChunk {chunk['id']}:")
                    print(f"  Tokens: {chunk['token_count']}")
                    print(f"  Characters: {chunk['char_count']}")
                    print(f"  Section: {chunk['metadata'].get('section_title', 'Unknown')}")
                    print(f"  Content preview: {chunk['content'][:200]}...")
                    if chunk['overlap_tokens'] > 0:
                        print(f"  Overlap with previous: {chunk['overlap_tokens']} tokens")
                
                # Show chunk files created
                chunk_file = os.path.join(temp_dir, "document_chunks.json")
                if os.path.exists(chunk_file):
                    with open(chunk_file, 'r') as f:
                        chunk_data = json.load(f)
                    
                    print(f"\nChunk data saved to: {chunk_file}")
                    print(f"File size: {os.path.getsize(chunk_file):,} bytes")
                    
                    # Demonstrate how chunks could be used for AI processing
                    print("\n" + "="*60)
                    print("AI Processing Simulation:")
                    print("="*60)
                    
                    for i, chunk in enumerate(chunk_data["chunks"][:2]):  # Show first 2
                        print(f"\n--- Processing Chunk {i+1} for AI Analysis ---")
                        print(f"Token count: {chunk['token_count']} (fits in most AI context windows)")
                        print(f"Section context: {chunk['metadata'].get('section_title', 'N/A')}")
                        print(f"Chunk content (first 300 chars):")
                        print(f"'{chunk['content'][:300]}...'")
                        print(f"[This chunk would be sent to AI service for analysis]")
                
            else:
                print("No chunks were created (chunking may not have been enabled)")
                
        except Exception as e:
            print(f"Error processing document: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    print(f"\nChunking demonstration completed!")
    print("The chunked document can now be processed by AI systems more efficiently.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())