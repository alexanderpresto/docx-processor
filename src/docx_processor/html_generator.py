import os

def create_index_html(document_data, output_dir):
    """Create an HTML index for easy navigation."""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{document_data['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin-bottom: 10px; }}
        .section-1 {{ font-size: 24px; font-weight: bold; }}
        .section-2 {{ font-size: 20px; font-weight: bold; margin-left: 20px; }}
        .section-3 {{ font-size: 16px; font-weight: bold; margin-left: 40px; }}
        .section-4 {{ font-size: 14px; font-weight: bold; margin-left: 60px; }}
        .image-gallery {{ display: flex; flex-wrap: wrap; }}
        .image-item {{ margin: 10px; text-align: center; }}
        table {{ border-collapse: collapse; margin-bottom: 20px; }}
        td, th {{ border: 1px solid #ddd; padding: 8px; }}
    </style>
</head>
<body>
    <h1>{document_data['title']}</h1>
    
    <h2>Document Sections</h2>
    <div class="toc">
"""
    
    # Add sections to TOC
    for section in document_data['sections']:
        level = section['level']
        html_content += f"""        <div class="section section-{level}">
            {section['title']}
        </div>
"""
    
    # Add image gallery
    if document_data['images']:
        html_content += """
    <h2>Images</h2>
    <div class="image-gallery">
"""
        for img in document_data['images']:
            html_content += f"""        <div class="image-item">
            <img src="{img['path']}" style="max-width: 200px; max-height: 200px;">
            <div>{img['caption'] or 'No caption'}</div>
        </div>
"""
        html_content += "    </div>\n"
    
    # Add tables preview
    if document_data['tables']:
        html_content += """
    <h2>Tables</h2>
"""
        for i, table in enumerate(document_data['tables']):
            html_content += f"""    <h3>Table {i+1}</h3>
    <table>
        <tr>
"""
            for header in table['headers']:
                html_content += f"            <th>{header}</th>\n"
            html_content += "        </tr>\n"
            
            # Add up to 5 rows for preview
            for row in table['data'][:5]:
                html_content += "        <tr>\n"
                for cell in row:
                    html_content += f"            <td>{cell}</td>\n"
                html_content += "        </tr>\n"
            
            html_content += "    </table>\n"
    
    html_content += """
</body>
</html>"""
    
    # Write HTML file
    with open(os.path.join(output_dir, "index.html"), 'w') as f:
        f.write(html_content)
