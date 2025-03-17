"""
Fallback processor module for simple text extraction when image handling fails.
"""
import os
import mammoth

def extract_document_text(file_path):
    """Extract plain text from a Word document using mammoth.
    
    Args:
        file_path: Path to the Word document
        
    Returns:
        A string containing the document's text content
    """
    try:
        with open(file_path, "rb") as docx_file:
            # Use extract_raw_text which doesn't attempt image handling
            result = mammoth.extract_raw_text(docx_file)
            text = result.value
            return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
