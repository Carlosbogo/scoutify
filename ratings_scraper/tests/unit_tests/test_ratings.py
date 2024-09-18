import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from program.ratings import get_text, get_rating

class TestRatings(unittest.TestCase):
    @patch('program.ratings.logger')
    def test_get_text_success(self, mock_logger):
        """Test get_text function with a successful result."""
        driver = MagicMock()
        driver.find_element.return_value.text = "Rating 4.5"

        result = get_text(driver, "Rating")
        self.assertEqual(result, "Rating 4.5")
        driver.find_element.assert_called_with(By.XPATH, '//span[text()[contains(., "Rating")]]')
        mock_logger.error.assert_not_called()

    @patch('program.ratings.logger')
    def test_get_text_failure(self, mock_logger):
        """Test get_text function with an unsuccessful result."""
        driver = MagicMock()
        driver.find_element.side_effect = Exception("Element not found")

        result = get_text(driver, "Rating")
        self.assertEqual(result, 0)
        self.assertEqual(driver.find_element.call_count, 5)
        self.assertEqual(mock_logger.error.call_count, 5)

if __name__ == '__main__':
    unittest.main()