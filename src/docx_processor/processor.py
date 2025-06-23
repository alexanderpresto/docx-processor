import os
import json
import sys
import zipfile  # For direct zipfile handling of docx

# Import mammoth with diagnostic information
try:
    import mammoth
except ImportError as e:
    print(f"Failed to import mammoth: {e}")
    sys.exit(1)

from bs4 import BeautifulSoup
from .image_handler import extract_images
from .html_generator import create_index_html
from .fallback_processor import extract_document_text
from .chunking import DocumentChunker
from .metadata_extractor import MetadataExtractor
from .style_extractor import StyleExtractor

# Custom style mappings to handle unsupported document styles
STYLE_MAP = """
p[style-name='toc 1'] => p.toc-1:fresh
p[style-name='TOC1'] => p.toc-1:fresh
p[style-name='toc 2'] => p.toc-2:fresh
p[style-name='TOC2'] => p.toc-2:fresh
p[style-name='toc 3'] => p.toc-3:fresh
p[style-name='TOC3'] => p.toc-3:fresh
p[style-name='Normal Single Spaced'] => p
p[style-name='NormalSingleSpaced'] => p
p[style-name='Normal Indent'] => p.indented
p[style-name='NormalIndent'] => p.indented
p[style-name='CodeBlock'] => pre.code-block
"""

def process_document(file_path, output_dir, image_quality=85, max_image_size=1200, 
                     output_format="both", extract_tables=False, 
                     enable_chunking=False, max_chunk_tokens=2000, chunk_overlap=200,
                     extract_metadata=False, extract_styles=False, include_comments=False):
    """Process Word document, extract content and images into structured JSON format."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Try multiple approaches to extract content
    html = None
    try_count = 0
    error_details = []
    
    # 1. First try: Using convert_to_html with img_element for proper image handling
    try:
        try_count += 1
        print(f"Attempt {try_count}: Converting to HTML with img_element for image extraction")
        with open(file_path, "rb") as docx_file:
            result = mammoth.convert_to_html(
                docx_file, 
                convert_image=mammoth.images.img_element,
                style_map=STYLE_MAP
            )
            html = result.value
            messages = result.messages
            print(f"Conversion messages: {messages}")
    except Exception as e:
        error_details.append(f"Attempt {try_count} failed: {str(e)}")
        print(error_details[-1])
    
    # 2. Second try: Convert to HTML using data_uri
    if html is None:
        try:
            try_count += 1
            print(f"Attempt {try_count}: Converting to HTML with data_uri")
            with open(file_path, "rb") as docx_file:
                result = mammoth.convert_to_html(
                    docx_file, 
                    convert_image=mammoth.images.data_uri,
                    style_map=STYLE_MAP
                )
                html = result.value
                messages = result.messages
                print(f"Conversion messages: {messages}")
        except Exception as e:
            error_details.append(f"Attempt {try_count} failed: {str(e)}")
            print(error_details[-1])
    
    # 3. Third try: Basic HTML conversion without image handling
    if html is None:
        try:
            try_count += 1
            print(f"Attempt {try_count}: Basic HTML conversion without image handling")
            with open(file_path, "rb") as docx_file:
                result = mammoth.convert_to_html(
                    docx_file,
                    style_map=STYLE_MAP
                )
                html = result.value
                messages = result.messages
                print(f"Conversion messages: {messages}")
        except Exception as e:
            error_details.append(f"Attempt {try_count} failed: {str(e)}")
            print(error_details[-1])
    
    # 4. Check if document has any embedded images using zipfile directly
    try:
        # DOCX files are actually ZIP archives, so we can open them directly
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Check if there are any image files in the Word document
            image_files = [name for name in zip_ref.namelist() if 
                          name.startswith('word/media/') and 
                          name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            
            if image_files:
                print(f"Document contains {len(image_files)} embedded images: {', '.join(image_files[:5])}")
                if len(image_files) > 5:
                    print(f"...and {len(image_files) - 5} more")
            else:
                print("Document does not contain any embedded images in the standard location")
                
                # Also check for other potential image locations
                other_images = [name for name in zip_ref.namelist() if 
                               name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) and 
                               not name.startswith('word/media/')]
                if other_images:
                    print(f"Found {len(other_images)} images in non-standard locations: {', '.join(other_images[:5])}")
    except Exception as e:
        print(f"Could not check for embedded images: {str(e)}")
    
    # 5. Last resort: Extract raw text
    if html is None:
        try:
            try_count += 1
            print(f"Attempt {try_count}: Falling back to plain text extraction")
            text = extract_document_text(file_path)
            if text:
                # Convert plain text to simple HTML
                html = f"<html><body>\n"
                for paragraph in text.split("\n\n"):
                    if paragraph.strip():
                        html += f"<p>{paragraph}</p>\n"
                html += "</body></html>"
                print("Successfully extracted text and converted to basic HTML")
        except Exception as e:
            error_details.append(f"Attempt {try_count} failed: {str(e)}")
            print(error_details[-1])
    
    if html is None:
        error_message = "All attempts to extract document content failed:\n" + "\n".join(error_details)
        print(error_message)
        raise RuntimeError(error_message)
    
    # Print HTML snippet for debugging image tags
    print(f"HTML snippet (first 500 chars): {html[:500]}")
    
    # Parse with BeautifulSoup
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Debug: Print all image tags found
        img_tags = soup.find_all('img')
        print(f"BeautifulSoup found {len(img_tags)} image tags")
        for i, img in enumerate(img_tags[:3]):  # Show first 3 images for debugging
            print(f"Image {i} attributes: {img.attrs}")
        
        # Extract structure with error handling
        document_data = {
            "title": extract_title(soup),
            "sections": extract_sections(soup),
            "tables": extract_tables_from_soup(soup),
            "images": [],  # Initialize with empty list
            "references": extract_references(soup)
        }
        
        # Extract images separately with error handling
        try:
            document_data["images"] = extract_images(soup, output_dir, quality=image_quality, max_size=max_image_size)
        except Exception as e:
            print(f"Warning: Failed to extract images: {e}")
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        raise
    
    # Save to JSON if requested
    if output_format in ["json", "both"]:
        output_json = os.path.join(output_dir, "document_structure.json")
        with open(output_json, 'w') as f:
            json.dump(document_data, f, indent=2)
    
    # Create index HTML if requested
    if output_format in ["html", "both"]:
        create_index_html(document_data, output_dir)
    
    # Extract tables to CSV if requested
    if extract_tables and document_data["tables"]:
        save_tables_to_csv(document_data["tables"], output_dir)
    
    # Apply chunking if requested
    if enable_chunking:
        print(f"Applying intelligent chunking with max_tokens={max_chunk_tokens}, overlap={chunk_overlap}")
        chunker = DocumentChunker(
            max_tokens=max_chunk_tokens,
            overlap_tokens=chunk_overlap,
            respect_boundaries=True
        )
        
        # Chunk the document sections
        chunks = chunker.chunk_document_sections(document_data["sections"])
        chunk_summary = chunker.create_chunk_summary(chunks)
        
        # Add chunking results to document data
        document_data["chunks"] = [
            {
                "id": chunk.id,
                "content": chunk.content,
                "token_count": chunk.token_count,
                "char_count": chunk.char_count,
                "start_index": chunk.start_index,
                "end_index": chunk.end_index,
                "overlap_tokens": chunk.overlap_tokens,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]
        document_data["chunk_summary"] = chunk_summary
        
        # Save chunked document as separate JSON file
        if output_format in ["json", "both"]:
            chunked_output = os.path.join(output_dir, "document_chunks.json")
            with open(chunked_output, 'w') as f:
                json.dump({
                    "chunks": document_data["chunks"],
                    "summary": chunk_summary,
                    "source_document": os.path.basename(file_path)
                }, f, indent=2)
            print(f"Saved {len(chunks)} chunks to {chunked_output}")
    
    # Phase 2: Enhanced Metadata Extraction
    if extract_metadata:
        print("Extracting document metadata...")
        metadata_extractor = MetadataExtractor()
        metadata = metadata_extractor.extract_all_metadata(file_path)
        
        # Filter comments if not requested
        if not include_comments:
            metadata['comments'] = []
        
        # Save metadata as separate JSON file
        if output_format in ["json", "both"]:
            metadata_output = os.path.join(output_dir, "metadata.json")
            metadata_extractor.save_metadata(metadata, metadata_output)
        
        # Add metadata summary to main document data
        document_data["metadata_summary"] = metadata_extractor.get_metadata_summary(metadata)
        document_data["metadata"] = metadata
    
    # Phase 2: Style Information Extraction
    if extract_styles:
        print("Extracting document styles...")
        style_extractor = StyleExtractor()
        styles = style_extractor.extract_all_styles(file_path)
        
        # Save styles as separate JSON file
        if output_format in ["json", "both"]:
            styles_output = os.path.join(output_dir, "styles.json")
            style_extractor.save_styles(styles, styles_output)
        
        # Add style summary to main document data
        document_data["style_summary"] = style_extractor.get_style_summary(styles)
        document_data["styles"] = styles
    
    # Save separate comments file if requested and available
    if include_comments and extract_metadata and document_data.get("metadata", {}).get("comments"):
        comments_output = os.path.join(output_dir, "comments.json")
        with open(comments_output, 'w', encoding='utf-8') as f:
            json.dump({
                "comments": document_data["metadata"]["comments"],
                "source_document": os.path.basename(file_path),
                "extraction_timestamp": document_data["metadata"]["extraction_timestamp"]
            }, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(document_data['metadata']['comments'])} comments to {comments_output}")
    
    return document_data

def extract_title(soup):
    """Extract document title."""
    h1 = soup.find('h1')
    if h1:
        return h1.get_text()
    
    # If no h1, try to find the first strong text as title
    strong = soup.find('strong')
    if strong:
        return strong.get_text()
        
    return "Untitled Document"

def extract_sections(soup):
    """Extract document sections based on headers."""
    sections = []
    current_header = None
    current_content = []
    
    for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        if elem.name.startswith('h'):
            # Save previous section
            if current_header:
                sections.append({
                    "level": int(current_header.name[1]),
                    "title": current_header.get_text(),
                    "content": "\n".join(current_content)
                })
            # Start new section
            current_header = elem
            current_content = []
        else:
            if current_header:  # Only append if we have a header
                current_content.append(elem.get_text())
    
    # Add the last section
    if current_header:
        sections.append({
            "level": int(current_header.name[1]),
            "title": current_header.get_text(),
            "content": "\n".join(current_content)
        })
    
    # If no sections found with headers, create a single section from the document
    if not sections and soup.find('p'):
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        if paragraphs:
            first_para = paragraphs[0]
            remaining = "\n".join(paragraphs[1:]) if len(paragraphs) > 1 else ""
            sections.append({
                "level": 1,
                "title": first_para[:50] + ("..." if len(first_para) > 50 else ""),
                "content": remaining
            })
    
    return sections

def extract_tables_from_soup(soup):
    """Extract tables from document."""
    tables = []
    for table_elem in soup.find_all('table'):
        table_data = []
        headers = []
        
        # Extract headers
        header_row = table_elem.find('tr')
        if header_row:
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.get_text().strip())
        
        # Extract rows
        for row in table_elem.find_all('tr')[1:]:  # Skip header row
            row_data = []
            for cell in row.find_all(['td', 'th']):
                row_data.append(cell.get_text().strip())
            if row_data:
                table_data.append(row_data)
        
        tables.append({
            "headers": headers,
            "data": table_data
        })
    
    return tables

def extract_references(soup):
    """Extract links and references."""
    references = []
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text()
        if href:
            references.append({
                "text": text,
                "href": href
            })
    return references

def save_tables_to_csv(tables, output_dir):
    """Save extracted tables to CSV files."""
    import csv
    
    tables_dir = os.path.join(output_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)
    
    for i, table in enumerate(tables):
        filepath = os.path.join(tables_dir, f"table_{i+1}.csv")
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            if table["headers"]:
                writer.writerow(table["headers"])
            writer.writerows(table["data"])
