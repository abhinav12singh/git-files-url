import unittest
from app.services import URLShortenerService

class TestURLShortenerService(unittest.TestCase):
    """Unit tests for URLShortenerService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.service = URLShortenerService()
    
    def test_shorten_url_creation(self):
        """Test that a shortened URL is created"""
        test_url = "https://example.com/very/long/url"
        result = self.service.shorten_url(test_url)
        
        self.assertIsNotNone(result)
        self.assertIn('short_code', result)
        self.assertIn('original_url', result)
        self.assertEqual(result['original_url'], test_url)
    
    def test_get_original_url(self):
        """Test retrieving original URL by short code"""
        test_url = "https://example.com/test"
        result = self.service.shorten_url(test_url)
        
        if result:
            short_code = result['short_code']
            retrieved_url = self.service.get_original_url(short_code)
            self.assertEqual(retrieved_url, test_url)
    
    def test_get_invalid_short_code(self):
        """Test that invalid short code returns None"""
        result = self.service.get_original_url('invalid123')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
