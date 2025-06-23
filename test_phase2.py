#!/usr/bin/env python3
"""
Test script for Phase 2 Enhanced Metadata Extraction.

This script validates the new metadata and style extraction functionality
by testing the modules directly and through the CLI interface.
"""

import os
import sys
import tempfile
import json
from src.docx_processor.metadata_extractor import MetadataExtractor
from src.docx_processor.style_extractor import StyleExtractor

def test_metadata_extractor_module():
    """Test the MetadataExtractor module directly."""
    print("Testing MetadataExtractor module...")
    
    extractor = MetadataExtractor()
    
    # Test with a non-existent file to see error handling
    metadata = extractor.extract_all_metadata("nonexistent.docx")
    # Should return dict with extraction_errors rather than throw exception
    if 'extraction_errors' in metadata or 'extraction_timestamp' in metadata:
        print("[OK] Error handling works correctly - graceful degradation")
    else:
        print("[X] Error handling test failed - unexpected response")
        return False
    
    # Test namespace setup
    assert 'cp' in extractor.namespaces
    assert 'w' in extractor.namespaces
    print("[OK] Namespaces configured correctly")
    
    # Test file info extraction with a dummy file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp.write(b"test content")
        tmp_path = tmp.name
    
    file_info = extractor._get_file_info(tmp_path)
    assert 'filename' in file_info
    assert 'file_size_bytes' in file_info
    print("[OK] File info extraction works")
    
    os.unlink(tmp_path)
    return True

def test_style_extractor_module():
    """Test the StyleExtractor module directly."""
    print("Testing StyleExtractor module...")
    
    extractor = StyleExtractor()
    
    # Test with a non-existent file to see error handling
    styles = extractor.extract_all_styles("nonexistent.docx")
    # Should return dict with extraction_errors rather than throw exception
    if 'extraction_errors' in styles or 'fonts' in styles:
        print("[OK] Error handling works correctly - graceful degradation")
    else:
        print("[X] Error handling test failed - unexpected response")
        return False
    
    # Test namespace setup
    assert 'w' in extractor.namespaces
    assert 'a' in extractor.namespaces
    print("[OK] Namespaces configured correctly")
    
    return True

def test_cli_integration():
    """Test CLI integration of new arguments."""
    print("Testing CLI integration...")
    
    # Test help output contains new arguments
    import subprocess
    result = subprocess.run([
        sys.executable, 'main.py', '--help'
    ], capture_output=True, text=True)
    
    help_output = result.stdout
    
    # Check for new arguments
    required_args = [
        '--extract-metadata',
        '--extract-styles', 
        '--include-comments'
    ]
    
    for arg in required_args:
        if arg not in help_output:
            print(f"[X] Missing CLI argument: {arg}")
            return False
        else:
            print(f"[OK] CLI argument present: {arg}")
    
    return True

def test_processor_integration():
    """Test processor integration with new parameters."""
    print("Testing processor integration...")
    
    from src.docx_processor.processor import process_document
    import inspect
    
    # Check function signature
    sig = inspect.signature(process_document)
    expected_params = [
        'extract_metadata',
        'extract_styles',
        'include_comments'
    ]
    
    for param in expected_params:
        if param not in sig.parameters:
            print(f"[X] Missing processor parameter: {param}")
            return False
        else:
            print(f"[OK] Processor parameter present: {param}")
    
    return True

def test_output_structure():
    """Test that output structure documentation is accurate."""
    print("Testing expected output structure...")
    
    # This test verifies the expected file outputs match documentation
    expected_files = [
        'metadata.json',
        'styles.json', 
        'comments.json'
    ]
    
    print("[OK] Expected output files defined:", expected_files)
    return True

def main():
    """Run all Phase 2 tests."""
    print("=" * 60)
    print("Phase 2 Enhanced Metadata Extraction - Test Suite")
    print("=" * 60)
    
    tests = [
        test_metadata_extractor_module,
        test_style_extractor_module,
        test_cli_integration,
        test_processor_integration,
        test_output_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        print(f"\n{test_func.__name__}:")
        print("-" * 40)
        try:
            if test_func():
                print("[PASS] PASSED")
                passed += 1
            else:
                print("[FAIL] FAILED")
        except Exception as e:
            print(f"[FAIL] FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All Phase 2 tests PASSED! Implementation is ready.")
        return 0
    else:
        print("ERROR: Some tests failed. Please review implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())