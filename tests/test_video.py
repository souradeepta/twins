import os
import hashlib
import unittest
import sys

# Get the parent directory (assuming the test file is one level deep in the "tests" folder)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.insert(0, parent_dir)

# Now, you can import the video code from the "twins" folder
from twins.video import video_file_hash, find_duplicate_video_files

class TestDuplicateVideoFileFinder(unittest.TestCase):
    def test_video_file_hash_valid_file(self):
        # Test with a valid video file
        test_file = "test_video.mp4"
        with open(test_file, "wb") as f:
            f.write(b"test video data")  # Create a sample video file
        expected_hash = hashlib.md5(b"test video data").hexdigest()
        self.assertEqual(video_file_hash(test_file), expected_hash)

        os.remove(test_file)  # Remove the test video file

    def test_video_file_hash_invalid_file(self):
        # Test with an invalid video file
        test_file = "invalid_file.txt"
        with open(test_file, "w") as f:
            f.write("invalid file data")  # Create a sample non-video file
        self.assertIsNone(video_file_hash(test_file))

        os.remove(test_file)  # Remove the test file

    def test_find_duplicate_video_files_no_duplicates(self):
        # Test with a directory containing no video files
        test_dir = "test_dir_no_duplicates"
        os.makedirs(test_dir)
        self.assertEqual(find_duplicate_video_files([test_dir]), {})
        os.rmdir(test_dir)  # Remove the test directory

    def test_find_duplicate_video_files_with_duplicates(self):
        # Test with a directory containing multiple duplicate video files
        test_dir = "test_dir_with_duplicates"
        os.makedirs(test_dir)

        # Create two duplicate video files
        video_data = b"test video data"
        with open(os.path.join(test_dir, "video1.mp4"), "wb") as f:
            f.write(video_data)
        with open(os.path.join(test_dir, "video2.mp4"), "wb") as f:
            f.write(video_data)

        expected_duplicates = {hashlib.md5(video_data).hexdigest(): [os.path.join(test_dir, "video1.mp4"), os.path.join(test_dir, "video2.mp4")]}
        self.assertEqual(find_duplicate_video_files([test_dir]), expected_duplicates)

        os.remove(os.path.join(test_dir, "video1.mp4"))  # Remove the test video files
        os.remove(os.path.join(test_dir, "video2.mp4"))
        os.rmdir(test_dir)  # Remove the test directory

if __name__ == "__main__":
    unittest.main()
