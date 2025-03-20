# docx-processor

Convert Word documents into analyzable formats while preserving structure and images.

## Features

- **Document Structure Extraction:** Hierarchical sections based on headers
- **Image Extraction:** Optimized embedded images with quality and size controls
- **Table Extraction:** Convert document tables to structured data
- **HTML Preview:** Navigable document preview with all components

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/docx-processor.git
cd docx-processor

# Install dependencies
pip install -r requirements.txt

# Optional: Install as package
pip install -e .
```

## Usage

### Basic Usage

```bash
python main.py input.docx output_directory
```

### Advanced Options

```bash
python main.py input.docx output_directory \
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

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Development

For development-related information and progress tracking, see:
- [Project Journal](JOURNAL.md): Chronological record of development decisions and progress
- [GitHub Issues](https://github.com/alexanderpresto/docx-processor/issues): Current tasks and bug reports

Contributors should review the Project Journal to understand recent decisions before submitting pull requests.