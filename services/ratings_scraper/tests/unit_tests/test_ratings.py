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

    @patch('program.ratings.get_text')
    @patch('program.ratings.logger')
    def test_get_rating_success(self, mock_logger, mock_get_text):
        """Test get_rating function with a successful result."""
        driver = MagicMock()
        mock_get_text.side_effect = ["Rating 4.5", "1,234 votes"]

        result = get_rating(driver, "Test Company")
        self.assertEqual(result, ["Test Company", 4.5, 1234])
        driver.get.assert_called_with("https://www.google.com/search?q=Test+Company+glassdoor")
        mock_logger.info.assert_called_with("Rating for Test Company: 4.5 with 1234 votes.")

    @patch('program.ratings.get_text')
    @patch('program.ratings.logger')
    def test_get_rating_no_rating(self, mock_logger, mock_get_text):
        """Test get_rating function with no rating found."""
        driver = MagicMock()
        mock_get_text.side_effect = [None, "1,234 votes"]

        result = get_rating(driver, "Test Company")
        self.assertEqual(result, ["Test Company", 0, 1234])
        driver.get.assert_called_with("https://www.google.com/search?q=Test+Company+glassdoor")
        mock_logger.info.assert_called_with("Rating for Test Company: 0 with 1234 votes.")

    @patch('program.ratings.get_text')
    @patch('program.ratings.logger')
    def test_get_rating_no_votes(self, mock_logger, mock_get_text):
        """Test get_rating function with no votes found."""
        driver = MagicMock()
        mock_get_text.side_effect = ["Rating 4.5", None]

        result = get_rating(driver, "Test Company")
        self.assertEqual(result, ["Test Company", 4.5, 0])
        driver.get.assert_called_with("https://www.google.com/search?q=Test+Company+glassdoor")
        mock_logger.info.assert_called_with("Rating for Test Company: 4.5 with 0 votes.")

if __name__ == '__main__':
    unittest.main()