"""
docx-processor - Convert Word documents into analyzable formats while preserving structure.

This package provides functionality to process Microsoft Word (.docx) files
and convert them into structured JSON and HTML formats. It preserves document
structure, extracts and optimizes images, and handles document tables.

The package can be used as a library or via its command-line interface.

Modules:
    processor: Core document processing functionality
    image_handler: Image extraction and optimization
    html_generator: HTML preview creation
    cli: Command-line interface
    fallback_processor: Fallback text extraction when primary methods fail
    version: Version information (isolated to prevent circular imports)

Important: Imports in this file are ordered specifically to prevent circular imports.
The version is imported first, followed by processing modules, and finally the CLI.
"""

# Version information
from .version import __version__

# Make modules available at package level
from . import processor
from . import image_handler
from . import html_generator
from . import fallback_processor

# Import CLI last to avoid circular imports
from . import cli
