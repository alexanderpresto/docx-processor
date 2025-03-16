import os
import json
import mammoth
from bs4 import BeautifulSoup
from src.docx_processor.image_handler import extract_images
from src.docx_processor.html_generator import create_index_html

def process_document(file_path, output_dir, image_quality=85, max_image_size=1200, 
                     output_format="both", extract_tables=False):
    """Process Word document, extract content and images into structured JSON format."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract raw content with mammoth
    with open(file_path, "rb") as docx_file:
        result = mammoth.convert_to_html(
            docx_file,
            convert_image=mammoth.images.img_element
        )
        html = result.value
        messages = result.messages
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract structure
    document_data = {
        "title": extract_title(soup),
        "sections": extract_sections(soup),
        "tables": extract_tables_from_soup(soup),
        "images": extract_images(soup, output_dir, quality=image_quality, max_size=max_image_size),
        "references": extract_references(soup)
    }
    
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
    
    return document_data

def extract_title(soup):
    """Extract document title."""
    h1 = soup.find('h1')
    if h1:
        return h1.get_text()
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
