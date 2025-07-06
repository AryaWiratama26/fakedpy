import unittest
import pandas as pd
import tempfile
import os
from pathlib import Path
from fakedpy import FakedGenerator, faked

class TestFakedGenerator(unittest.TestCase):
    """Test cases for FakedGenerator class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.generator = FakedGenerator()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up after each test"""
        # Remove temporary files
        for file in Path(self.temp_dir).glob("*"):
            if file.is_file():
                file.unlink()
        os.rmdir(self.temp_dir)
    
    def test_initialization(self):
        """Test FakedGenerator initialization"""
        # Test default locale
        generator = FakedGenerator()
        self.assertIsNotNone(generator.fake)
        
        # Test custom locale
        generator_id = FakedGenerator(locale='id_ID')
        self.assertIsNotNone(generator_id.fake)
        
        # Test multiple locales
        generator_multi = FakedGenerator(locale=['en_US', 'id_ID'])
        self.assertIsNotNone(generator_multi.fake)
    
    def test_basic_generation(self):
        """Test basic data generation"""
        df = self.generator.generate(rows=5)
        
        # Check DataFrame properties
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)
        self.assertTrue(all(col in df.columns for col in ["name", "address", "job"]))
        
        # Check data types
        self.assertIsInstance(df.iloc[0]['name'], str)
        self.assertIsInstance(df.iloc[0]['address'], str)
        self.assertIsInstance(df.iloc[0]['job'], str)
    
    def test_custom_fields(self):
        """Test generation with custom fields"""
        fields = ["email", "phone_number", "company"]
        df = self.generator.generate(rows=3, fields=fields)
        
        self.assertEqual(list(df.columns), fields)
        self.assertEqual(len(df), 3)
        
        # Check that all fields contain data
        for field in fields:
            self.assertTrue(all(df[field].notna()))
    
    def test_output_formats(self):
        """Test different output formats"""
        fields = ["name", "email"]
        base_path = Path(self.temp_dir) / "test_output"
        
        # Test CSV
        df_csv = self.generator.generate(
            rows=2,
            fields=fields,
            output_format="csv",
            output_path=str(base_path)
        )
        self.assertTrue((base_path.with_suffix(".csv")).exists())
        
        # Test JSON
        df_json = self.generator.generate(
            rows=2,
            fields=fields,
            output_format="json",
            output_path=str(base_path)
        )
        self.assertTrue((base_path.with_suffix(".json")).exists())
        
        # Test Excel
        df_excel = self.generator.generate(
            rows=2,
            fields=fields,
            output_format="excel",
            output_path=str(base_path)
        )
        self.assertTrue((base_path.with_suffix(".xlsx")).exists())
        
        # Test Parquet
        df_parquet = self.generator.generate(
            rows=2,
            fields=fields,
            output_format="parquet",
            output_path=str(base_path)
        )
        self.assertTrue((base_path.with_suffix(".parquet")).exists())
    
    def test_related_fields(self):
        """Test related fields functionality"""
        related_fields = {
            "user_id": {"type": "counter", "start": 1000},
            "department": {
                "type": "choice",
                "values": ["IT", "HR", "Finance"]
            }
        }
        
        df = self.generator.generate(
            rows=5,
            fields=["user_id", "name", "department"],
            related_fields=related_fields
        )
        
        # Check counter field
        expected_ids = [1000, 1001, 1002, 1003, 1004]
        self.assertEqual(df["user_id"].tolist(), expected_ids)
        
        # Check choice field
        valid_departments = ["IT", "HR", "Finance"]
        self.assertTrue(all(dept in valid_departments for dept in df["department"]))
    
    def test_all_available_fields(self):
        """Test all available fields"""
        all_fields = [
            "name", "first_name", "last_name", "email", "phone_number",
            "date", "gender", "address", "street_address", "city", "state",
            "country", "postcode", "latitude", "longitude", "username",
            "password", "domain_name", "url", "ipv4", "ipv6", "mac_address",
            "company", "job", "credit_card_number", "credit_card_provider",
            "currency_code", "file_name", "file_extension", "mime_type",
            "text", "word", "sentence", "paragraph", "color_name",
            "hex_color", "rgb_color"
        ]
        
        df = self.generator.generate(rows=1, fields=all_fields)
        
        # Check that all fields are present
        self.assertEqual(set(df.columns), set(all_fields))
        
        # Check that no null values exist
        self.assertFalse(df.isnull().any().any())
    
    def test_invalid_fields(self):
        """Test handling of invalid fields"""
        df = self.generator.generate(
            rows=2,
            fields=["name", "invalid_field", "email"]
        )
        
        # Should only contain valid fields
        self.assertEqual(set(df.columns), {"name", "email"})
    
    def test_zero_rows(self):
        """Test generation with zero rows"""
        df = self.generator.generate(rows=0)
        self.assertEqual(len(df), 0)
    
    def test_large_number_of_rows(self):
        """Test generation with large number of rows"""
        df = self.generator.generate(rows=1000)
        self.assertEqual(len(df), 1000)
    
    def test_data_uniqueness(self):
        """Test that generated data is not all identical"""
        df = self.generator.generate(rows=10, fields=["name"])
        
        # Check that names are not all the same
        unique_names = df["name"].nunique()
        self.assertGreater(unique_names, 1)
    
    def test_locale_specific_data(self):
        """Test that locale affects generated data"""
        # Test Indonesian locale
        generator_id = FakedGenerator(locale='id_ID')
        df_id = generator_id.generate(rows=5, fields=["name", "phone_number"])
        
        # Test English locale
        generator_en = FakedGenerator(locale='en_US')
        df_en = generator_en.generate(rows=5, fields=["name", "phone_number"])
        
        self.assertIsInstance(df_id, pd.DataFrame)
        self.assertIsInstance(df_en, pd.DataFrame)

class TestLegacyFunction(unittest.TestCase):
    """Test cases for legacy faked() function"""
    
    def test_legacy_function_basic(self):
        """Test basic usage of legacy function"""
        df = faked(rows=3, req=["name", "email"])
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertTrue(all(col in df.columns for col in ["name", "email"]))
    
    def test_legacy_function_defaults(self):
        """Test legacy function with default parameters"""
        df = faked()
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 10)  # Default rows
        self.assertTrue(all(col in df.columns for col in ["name", "address", "job"]))
    
    def test_legacy_function_custom_fields(self):
        """Test legacy function with custom fields"""
        df = faked(rows=5, req=["email", "phone_number"])
        
        self.assertEqual(len(df), 5)
        self.assertEqual(list(df.columns), ["email", "phone_number"])

class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling"""
    
    def setUp(self):
        self.generator = FakedGenerator()
    
    def test_invalid_output_format(self):
        """Test handling of invalid output format"""
        with self.assertRaises(ValueError):
            self.generator.generate(
                rows=5,
                fields=["name"],
                output_format="invalid_format"
            )
    
    def test_negative_rows(self):
        """Test handling of negative row count"""
        with self.assertRaises(ValueError):
            self.generator.generate(rows=-1)
    
    def test_empty_fields_list(self):
        """Test handling of empty fields list"""
        df = self.generator.generate(rows=5, fields=[])
        self.assertEqual(len(df), 5)
        self.assertEqual(len(df.columns), 0)

if __name__ == '__main__':
    unittest.main() 