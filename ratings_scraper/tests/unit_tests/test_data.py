import unittest
from unittest.mock import patch
import csv
import tempfile
import os
from program.data import download_from_bucket, parse, write_csv, upload_to_bucket

class TestDataFunctions(unittest.TestCase):

    @patch('google.cloud.storage.Client')
    def test_download_from_bucket(self, MockClient):
        mock_client = MockClient.return_value
        mock_bucket = mock_client.bucket.return_value
        mock_blob = mock_bucket.blob.return_value

        download_from_bucket('test_bucket', 'test_blob', 'test_file')

        mock_client.bucket.assert_called_with('test_bucket')
        mock_bucket.blob.assert_called_with('test_blob')
        mock_blob.download_to_filename.assert_called_with('test_file')

if __name__ == '__main__':
    unittest.main()