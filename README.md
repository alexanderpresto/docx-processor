# docx-processor

A Python application that transforms Microsoft Word documents into structured, analyzable formats while preserving document structure, images, and tables.

## Features

- **Document Structure Extraction**: Hierarchical sections based on headers with semantic preservation
- **Image Extraction**: Optimized embedded images with quality and size controls
- **Table Extraction**: Convert document tables to structured data (CSV format)
- **HTML Preview**: Interactive, navigable document preview with all components
- **Metadata Preservation**: Document properties and structure maintained

## Why Use docx-processor?

Despite AI advancements, language models still cannot:
- Extract images embedded in Word documents
- Preserve complex document structure reliably
- Handle very large documents efficiently
- Export tables to analyzable formats

This tool bridges that gap, making Word documents truly AI-friendly.

## Installation

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Setup with Virtual Environment

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Create and activate virtual environment (Windows)
python -m venv docx-processor-env
.\docx-processor-env\Scripts\Activate.ps1

# Create and activate virtual environment (Linux/Mac)
python -m venv docx-processor-env
source docx-processor-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install as editable package
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Basic usage
python main.py input.docx output_directory

# With options
python main.py input.docx output_directory \
    --image-quality 90 \
    --max-image-size 800 \
    --format both \
    --extract-tables

# Using as installed package
docx-processor input.docx output_directory
```

### Command Line Options

- `--image-quality`: JPEG quality for extracted images (1-100, default: 85)
- `--max-image-size`: Maximum dimension for resized images in pixels (default: 1200)
- `--format`: Output format - json, html, or both (default: both)
- `--extract-tables`: Extract tables to CSV files
- `--version`: Show version information

## Output Structure

```
output_directory/
├── document_structure.json  # Complete document structure and content
├── index.html              # Interactive HTML preview
├── images/                 # Extracted and optimized images
│   ├── image_0.png
│   ├── image_1.jpg
│   └── ...
└── tables/                 # Extracted tables (if --extract-tables used)
    ├── table_1.csv
    └── ...
```

### Output Files

- **document_structure.json**: Complete document data including:
  - Hierarchical document structure
  - Text content with formatting
  - Image references and metadata
  - Table data

- **index.html**: Interactive preview featuring:
  - Collapsible navigation sidebar
  - Embedded images (optimized)
  - Formatted tables
  - Document hierarchy visualization

## Development

### Project Structure

```
docx-processor/
├── src/
│   ├── docx_processor/       # Main package
│   │   ├── processor.py      # Core processing logic
│   │   ├── image_handler.py  # Image extraction
│   │   ├── html_generator.py # HTML generation
│   │   ├── cli.py           # CLI interface
│   │   └── version.py       # Version info
│   └── __main__.py          # Package entry point
├── docs/                    # Documentation
│   └── requirements/        # v2.0 planning docs
├── tests/                   # Test suite
├── examples/               # Usage examples
└── scripts/               # Development scripts
```

### Version 2.0 Development

Currently planning version 2.0 with enhanced features:
- Intelligent chunking for large documents
- Enhanced metadata extraction
- API framework with AI service integration
- Advanced processing (OCR, formulas)

See `docs/requirements/` for detailed specifications.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes (ensure virtual environment is active)
4. Run tests
5. Submit a pull request

## Requirements

Core dependencies:
- `mammoth` - DOCX parsing
- `beautifulsoup4` - HTML manipulation
- `Pillow` - Image processing
- `lxml` - XML processing

## License

See LICENSE file for details.

## Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/alexanderpresto/docx-processor/issues)
- **Developer**: Alexander Presto
- **Repository**: <https://github.com/alexanderpresto/docx-processor>
