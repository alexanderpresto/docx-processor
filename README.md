# docx-processor

Convert Word documents into analyzable formats while preserving structure and images.

## Features

- **Document Structure Extraction:** Hierarchical sections based on headers
- **Image Extraction:** Optimized embedded images with quality and size controls
- **Table Extraction:** Convert document tables to structured data
- **HTML Preview:** Navigable document preview with all components

## Installation

### Using pip

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Install dependencies
pip install -r requirements.txt

# Install as package (development mode)
pip install -e .
```

### Using Conda

```bash
# Clone the repository
git clone https://github.com/alexanderpresto/docx-processor.git
cd docx-processor

# Create and activate conda environment
conda env create -f environment.yml
conda activate docx-processor

# Install as package (development mode)
pip install -e .
```

## Usage

### Basic Usage

```bash
docx-processor input.docx output_directory
```

### Advanced Options

```bash
docx-processor input.docx output_directory \
    --image-quality 90 \
    --max-image-size 800 \
    --format html \
    --extract-tables
```

## Output

The processor generates the following outputs:

- `document_structure.json`: Complete document structure
- `index.html`: Interactive document preview
- `images/`: Extracted and optimized document images
- `tables/`: CSV files of extracted tables (optional)

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Input Word document path | (required) |
| `output` | Output directory path | (required) |
| `--image-quality` | Image quality (1-100) | 85 |
| `--max-image-size` | Maximum image dimension in pixels | 1200 |
| `--format` | Output format (json, html, or both) | both |
| `--extract-tables` | Extract tables to CSV files | False |

## Project Structure

```
docx-processor/
├── src/
│   └── docx_processor/       # Core package
│       ├── __init__.py
│       ├── processor.py      # Document processing functionality
│       ├── image_handler.py  # Image extraction and optimization
│       ├── html_generator.py # HTML preview creation
│       ├── cli.py            # Command-line interface
│       └── utils.py          # Helper functions and utilities
├── tests/
│   ├── __init__.py
│   ├── test_processor.py     # Unit tests for processor module
│   └── test_data/
│       └── sample.docx       # Test document for validation
├── requirements.txt          # Project dependencies
├── setup.py                  # Package installation configuration
├── pyproject.toml           # Modern Python packaging configuration
└── README.md                 # Project documentation
```

## Requirements

- Python 3.8+
- Dependencies:
  - mammoth (>=1.5.0)
  - beautifulsoup4 (>=4.11.0)
  - Pillow (>=9.0.0)
  - lxml (>=4.9.0)

## Development

For development and testing:

```bash
# Create development environment
conda env create -f environment.yml
conda activate docx-processor

# Install in development mode
pip install -e .

# Run tests
pytest
```

### Development Notes

- Package configuration is handled in both setup.py and pyproject.toml
- The CLI is implemented in src/docx_processor/cli.py
- Make sure to run unit tests when making changes to core functionality
- Running in development mode allows changes to be reflected immediately

## Contributing

Contributions are welcome! Please see [CONTRIBUTION.md](CONTRIBUTION.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.