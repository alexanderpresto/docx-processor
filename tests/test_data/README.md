# Test Data Directory

This directory contains test documents for the docx-processor test suite.

## Structure

```
test_data/
├── fixtures/       # Small test fixtures for unit tests
│   ├── simple.docx
│   ├── with_images.docx
│   └── with_tables.docx
└── samples/        # Larger sample documents for integration tests
    ├── complex_document.docx
    └── edge_cases.docx
```

## Test Document Types

### Fixtures (Unit Tests)
Small, focused documents testing specific features:
- **simple.docx**: Basic document with headers and paragraphs
- **with_images.docx**: Document containing various image types
- **with_tables.docx**: Document with different table structures

### Samples (Integration Tests)
Larger documents for comprehensive testing:
- **complex_document.docx**: Multi-section document with mixed content
- **edge_cases.docx**: Documents with unusual formatting or structures

## Adding Test Documents

When adding new test documents:
1. Keep fixture files small (<100KB)
2. Name files descriptively
3. Document any special characteristics
4. Ensure no sensitive data is included

## Note

Test documents are not included in the repository by default. Create your own test documents or use the provided examples as templates.
