# docx-processor

A Python application that transforms Microsoft Word documents into structured, analyzable formats while preserving document structure, images, and tables.

> **IMPORTANT**: This project requires virtual environment activation for all development work. See [Development](#development) section for mandatory setup steps.

## Features

- **Document Structure Extraction**: Hierarchical sections based on headers with semantic preservation
- **Intelligent Document Chunking**: ✨ **NEW in v2.0** - Split documents into AI-friendly chunks with token counting and context preservation
- **Enhanced Metadata Extraction**: ✨ **NEW in v2.0 Phase 2** - Comprehensive document properties, style analysis, and comment extraction
- **Image Extraction**: Optimized embedded images with quality and size controls
- **Table Extraction**: Convert document tables to structured data (CSV format)
- **HTML Preview**: Interactive, navigable document preview with all components
- **Style Analysis**: ✨ **NEW in v2.0 Phase 2** - Font, color, layout, and formatting information extraction

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

**CRITICAL**: Always activate the virtual environment before any development work. This is mandatory, not optional.

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Create and activate virtual environment (Windows - Claude Desktop)
python -m venv docx-processor-env
.\docx-processor-env\Scripts\Activate.ps1

# Verify activation (should show virtual environment path)
python -c "import sys; print(sys.prefix)"

# Create and activate virtual environment (Linux/Mac)
python -m venv docx-processor-env
source docx-processor-env/bin/activate

# Create and activate virtual environment (WSL2 - Claude Code)
# Note: Project is on Windows D: drive, accessed via mount point
cd /mnt/d/Users/alexp/dev/docx-processor
python -m venv docx-processor-env
source docx-processor-env/bin/activate

# Install dependencies (all platforms) - ONLY after activation
pip install -r requirements.txt

# Optional: Install as editable package (all platforms)
pip install -e .
```

**Quick Windows Setup**: Run `.\scripts\setup.ps1` from project root for automated setup.

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

# ✨ NEW: Enable intelligent chunking for AI processing
python main.py input.docx output_directory \
    --enable-chunking \
    --max-chunk-tokens 2000 \
    --chunk-overlap 200

# ✨ NEW: Enhanced metadata and style extraction
python main.py input.docx output_directory \
    --extract-metadata \
    --extract-styles \
    --include-comments

# ✨ Combined: Full v2.0 feature set
python main.py input.docx output_directory \
    --enable-chunking \
    --extract-metadata \
    --extract-styles \
    --include-comments \
    --extract-tables

# Using as installed package
docx-processor input.docx output_directory --enable-chunking --extract-metadata
```

### Command Line Options

**Standard Options:**
- `--image-quality`: JPEG quality for extracted images (1-100, default: 85)
- `--max-image-size`: Maximum dimension for resized images in pixels (default: 1200)
- `--format`: Output format - json, html, or both (default: both)
- `--extract-tables`: Extract tables to CSV files

**✨ v2.0 Phase 1 - Intelligent Chunking:**
- `--enable-chunking`: Enable intelligent document chunking for AI processing
- `--max-chunk-tokens`: Maximum tokens per chunk (default: 2000)
- `--chunk-overlap`: Token overlap between chunks for context preservation (default: 200)

**✨ v2.0 Phase 2 - Enhanced Metadata:**
- `--extract-metadata`: Extract comprehensive document metadata including properties, statistics, and revision history
- `--extract-styles`: Extract style and formatting information including fonts, colors, and layout
- `--include-comments`: Include document comments with positional context in extraction
- `--version`: Show version information

**✨ NEW Chunking Options (v2.0):**
- `--enable-chunking`: Enable intelligent document chunking for AI processing
- `--max-chunk-tokens`: Maximum tokens per chunk (default: 2000)
- `--chunk-overlap`: Token overlap between chunks for context preservation (default: 200)

## Output Structure

```
output_directory/
├── document_structure.json  # Complete document structure and content
├── document_chunks.json     # ✨ AI-ready chunks (if --enable-chunking used)
├── metadata.json           # ✨ Comprehensive metadata (if --extract-metadata used)
├── styles.json             # ✨ Style and formatting info (if --extract-styles used)
├── comments.json           # ✨ Comments with context (if --include-comments used)
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

- **✨ document_chunks.json** (NEW): AI-ready document chunks featuring:
  - Token-counted text segments
  - Context preservation with overlap
  - Section metadata and relationships
  - Chunk boundary information

- **✨ metadata.json** (NEW): Comprehensive document metadata including:
  - Document properties (title, author, creation/modification dates)
  - Document statistics (page count, word count, character count)
  - Revision history and version information
  - Custom properties and application metadata

- **✨ styles.json** (NEW): Style and formatting analysis including:
  - Font families, sizes, and styling information
  - Color schemes and theme information
  - Layout settings (margins, headers, footers)
  - Style usage statistics and relationships

- **✨ comments.json** (NEW): Document comments with context including:
  - Comment text and author information
  - Positional context within the document
  - Reply threads and revision tracking
  - Timestamps and metadata

- **index.html**: Interactive preview featuring:
  - Collapsible navigation sidebar
  - Embedded images (optimized)
  - Formatted tables
  - Document hierarchy visualization

## Development

### Working Directory

- **Primary**: `D:\Users\alexp\dev\docx-processor`
- **Archive**: `D:\Users\alexp\dev\docx-processor\archive`

### Development Workflow

1. **Activate Virtual Environment** (mandatory):

   ```bash
   # Windows
   .\docx-processor-env\Scripts\Activate.ps1
   
   # Verify activation
   python -c "import sys; print(sys.prefix)"
   ```

2. **Check Basic-Memory Project Context** (if using Claude):
   - Ensure "dev" project is active
   - See CLAUDE.md for AI assistant guidelines

3. **Archive Before Modifying**:
   - Never overwrite existing files
   - Archive to `archive\filename_YYYY-MM-DD.ext` before changes
   - Use PowerShell for efficient archival:

     ```powershell
     Copy-Item -Path "src\file.py" -Destination "archive\file_2025-06-22.py"
     ```

4. **Document Changes**:
   - Significant changes should be documented in Basic-Memory
   - Use semantic relationships to connect related concepts

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
    ├── setup.ps1         # Windows setup script
    └── setup.sh          # Linux/WSL2 setup script
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
