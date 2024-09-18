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

    def test_parse(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as temp_file:
            temp_file.write("col1,col2\nval1,val2\nval3,val4")
            temp_file_path = temp_file.name

        expected_output = [['col1', 'col2'], ['val1', 'val2'], ['val3', 'val4']]
        result = parse(temp_file_path)
        self.assertEqual(result, expected_output)

        os.remove(temp_file_path)

    def test_write_csv(self):
        data = [['col1', 'col2'], ['val1', 'val2'], ['val3', 'val4']]
        with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as temp_file:
            temp_file_path = temp_file.name

        write_csv(data, temp_file_path)

        with open(temp_file_path, newline='') as f:
            reader = csv.reader(f)
            result = list(reader)

        self.assertEqual(result, data)

        os.remove(temp_file_path)

if __name__ == '__main__':
    unittest.main()