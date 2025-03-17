import unittest
import os
import shutil
import json
from docx_processor.processor import process_document

class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = os.path.join(self.test_dir, "test_data")
        self.output_dir = os.path.join(self.test_dir, "test_output")
        
        # Create output dir if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def tearDown(self):
        # Clean up output directory after tests
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
    
    def test_sample_document_processing(self):
        # Skip if sample.docx doesn't exist
        sample_path = os.path.join(self.test_data_dir, "sample.docx")
        if not os.path.exists(sample_path):
            self.skipTest("sample.docx not found in test_data directory")
        
        # Process the document
        result = process_document(
            sample_path,
            self.output_dir,
            image_quality=85,
            max_image_size=800,
            output_format="both",
            extract_tables=True
        )
        
        # Check that output files were created
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "document_structure.json")))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "index.html")))
        
        # Check that the result contains expected keys
        self.assertIn("title", result)
        self.assertIn("sections", result)
        self.assertIn("tables", result)
        self.assertIn("images", result)
        self.assertIn("references", result)

if __name__ == "__main__":
    unittest.main()
