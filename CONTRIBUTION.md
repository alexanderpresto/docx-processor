# Contributing to docx-processor

Thank you for your interest in contributing to docx-processor! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and collaborative environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue in the GitHub repository with the following information:

1. A clear, descriptive title
2. A detailed description of the bug, including steps to reproduce
3. Expected behavior vs. actual behavior
4. Any relevant screenshots or error messages
5. Your environment (OS, Python version, package versions)

### Suggesting Enhancements

We welcome suggestions for enhancing the project. Please create an issue with:

1. A clear, descriptive title
2. A detailed description of the proposed enhancement
3. Any specific use cases or examples that would benefit from this enhancement
4. Any implementation ideas you might have

### Pull Requests

We encourage you to contribute directly to the codebase through pull requests:

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request with a clear description of your changes

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/alexanderpresto/docx-processor.git
   cd docx-processor
   ```

2. Set up your development environment:

   ```bash
   # Using conda (recommended)
   conda env create -f environment.yml
   conda activate docx-processor
   
   # OR using pip
   pip install -r requirements.txt
   ```

3. Install the package in development mode:

   ```bash
   pip install -e .
   ```

## Coding Standards

- Follow PEP 8 style guide for Python code
- Use docstrings for all functions, classes, and modules
- Write unit tests for new functionality
- Keep functions focused and modular
- Use descriptive variable and function names

## Testing

Run tests using pytest:

```bash
pytest
```

Please ensure all tests pass before submitting a pull request. Add new tests for new functionality.

## Documentation

Update documentation for any changes to APIs or functionality:

- Update docstrings in the code
- Update the README.md if necessary
- Add examples for new features

## Versioning

We use semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR version for incompatible API changes
- MINOR version for backward-compatible functionality additions
- PATCH version for backward-compatible bug fixes

## Pull Request Process

1. Update tests and documentation as necessary
2. Update the README.md with details of changes if appropriate
3. The PR should work on Python 3.8 and above
4. The PR will be merged once it receives approval from maintainers

## Questions?

If you have any questions or need clarification on these guidelines, please open an issue in the repository.

Thank you for contributing to docx-processor!
