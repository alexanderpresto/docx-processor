# Developer Documentation for docx-processor

This document provides details about the design decisions, implementation details, and potential areas for improvement in the docx-processor project.

## Architecture Overview

The docx-processor package is designed with a modular architecture to separate concerns and improve maintainability:

- **processor.py**: Core processing logic that coordinates the document conversion pipeline
- **image_handler.py**: Handles image extraction and optimization
- **html_generator.py**: Creates HTML preview files from extracted document structure
- **cli.py**: Provides command-line interface
- **fallback_processor.py**: Contains fallback mechanisms for text extraction
- **version.py**: Contains version information (separated to avoid circular imports)

## Key Design Decisions

### 1. Multiple Conversion Strategies

The processor uses multiple strategies to convert Word documents, attempting each in sequence until successful:

1. **HTML with Image Elements**: Using `mammoth.convert_to_html` with `mammoth.images.img_element`
2. **HTML with Data URIs**: Using `mammoth.convert_to_html` with `mammoth.images.data_uri`
3. **Basic HTML**: Simple HTML conversion without special image handling
4. **Plain Text**: Last resort fallback that extracts only text content

This approach ensures maximum compatibility with different document types and versions.

### 2. Custom Style Mappings

Custom style mappings are defined in the `STYLE_MAP` constant in processor.py to handle various Word styles:

```python
STYLE_MAP = """
p[style-name='toc 1'] => p.toc-1:fresh
p[style-name='TOC1'] => p.toc-1:fresh
# ... additional mappings
"""
```

These mappings improve the quality of the HTML output by properly handling document-specific styles.

### 3. Circular Import Prevention

We've implemented a specific structure to avoid circular imports:

- Version information is isolated in `version.py`
- `__init__.py` imports modules in a specific order
- Modules import specific functions rather than entire modules when possible

This ensures that the package can be properly imported and used as both a library and a command-line tool.

### 4. Direct DOCX Inspection

The processor directly inspects DOCX files (which are ZIP archives) to determine if images are present:

```python
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    image_files = [name for name in zip_ref.namelist() if 
                  name.startswith('word/media/') and 
                  name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
```

This provides better diagnostic information when image extraction fails.

### 5. Error Handling and Diagnostics

Comprehensive error handling and diagnostic output are implemented throughout:

- Detailed error messages at each processing stage
- Fallback processing when primary methods fail
- Diagnostic information about document content and structure
- HTML snippet preview for debugging

## Extension and Enhancement Areas

### 1. Style Mapping Extensions

The custom style mappings can be extended to handle additional document styles. Common areas to enhance:

- Additional TOC levels (TOC4, TOC5, etc.)
- Custom heading styles (Heading 1 Alt, etc.)
- Special content blocks (Notes, Warnings, etc.)
- Code blocks and syntax highlighting

### 2. Image Extraction Improvements

Current image extraction could be enhanced by:

- Supporting additional image formats (SVG, WebP, etc.)
- Extracting image metadata (alt text, dimensions, etc.)
- Providing options for image format conversion
- Adding image compression options

### 3. Table Processing Enhancements

Table extraction could be improved with:

- Better handling of merged cells
- Support for table styles and formatting
- Options for table format conversion (Markdown, HTML, etc.)
- Handling of nested tables

### 4. Document Metadata

Additional document metadata could be extracted:

- Author information
- Document properties
- Creation and modification dates
- Custom properties

### 5. Performance Optimization

Potential performance improvements:

- Parallel processing for large documents
- Memory optimization for image handling
- Caching of intermediate results
- Stream processing for large files

## Troubleshooting Common Issues

### Image Extraction Issues

If images aren't being extracted:

1. Check if the document contains embedded images (see diagnostic output)
2. Verify that the mammoth library has image extraction capabilities
3. Try using the `--image-quality` and `--max-image-size` options
4. Examine the HTML output for img tags with src attributes

### Style Mapping Issues

If document styles aren't properly converted:

1. Check the diagnostic output for unrecognized style warnings
2. Add custom style mappings in processor.py
3. Verify that the document uses standard styles or has properly defined custom styles

### Circular Import Errors

If you encounter circular import errors:

1. Ensure imports are in the correct order in __init__.py
2. Check that version.py only contains version information
3. Use function-specific imports rather than module imports where appropriate
4. Be careful when adding new modules to avoid circular dependencies

## Testing Strategy

The project includes a test suite that should be expanded when making changes:

- Unit tests for each module
- Integration tests for the entire processing pipeline
- Test documents covering various edge cases
- Performance tests for large documents

When extending functionality, always add corresponding tests to ensure backward compatibility and proper functioning.
