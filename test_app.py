import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        from app import app
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        """Test that home page loads"""
        response = self.app.get('/')
        self.assertIn(response.status_code, [200, 302])  # 302 if redirect
    
    def test_app_import(self):
        """Test that app can be imported"""
        try:
            from app import app
            self.assertTrue(app is not None)
        except ImportError:
            self.fail("Failed to import app")
    
    def test_environment(self):
        """Test environment setup"""
        self.assertTrue(os.environ.get('MONGO_URI') is not None)

if __name__ == '__main__':
    unittest.main()
