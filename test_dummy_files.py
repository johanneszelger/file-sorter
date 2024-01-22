import os
import shutil
import unittest
from unittest.mock import patch, mock_open, MagicMock
from file_sorter import log_movement, move_file, undo_last_organization, organize_by_type, organize_by_size, \
    organize_by_date
from pathlib import Path


class TestFileOrganizer(unittest.TestCase):

    def setUp(self):
        self.test_file = "test.txt"
        self.test_dir = "test_dir"
        shutil.rmtree(self.test_dir, ignore_errors=True)
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_target = os.path.join(self.test_dir, self.test_file)
        self.log_file = "testlog.json"

        with open(os.path.join(self.test_dir, "binary.exe"), "w") as f:
            f.write("a" * int(1e5))
        os.utime(os.path.join(self.test_dir, "binary.exe"), (0, 0))

        with open(os.path.join(self.test_dir, "image.jpg"), "w") as f:
            f.write("a" * int(1e6))
        os.utime(os.path.join(self.test_dir, "image.jpg"), (2 * 3600 * 24, 3600 * 24))

        with open(os.path.join(self.test_dir, "video.mp4"), "w") as f:
            f.write("a" * int(1e7))
        os.utime(os.path.join(self.test_dir, "video.mp4"), (2 * 3600 * 24, 2 * 3600 * 24))

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_undo_last_organization(self):
        organize_by_type(self.test_dir, False, self.log_file)
        undo_last_organization(self.log_file)

        assert not os.path.exists(os.path.join(self.test_dir, "exe", "binary.exe"))
        assert not os.path.exists(os.path.join(self.test_dir, "jpg", "image.jpg"))
        assert not os.path.exists(os.path.join(self.test_dir, "mp4", "video.mp4"))

        assert os.path.exists(os.path.join(self.test_dir, "binary.exe"))
        assert os.path.exists(os.path.join(self.test_dir, "image.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "video.mp4"))

    def test_sort_by_type(self):
        organize_by_type(self.test_dir, False, self.log_file)

        assert os.path.exists(os.path.join(self.test_dir, "exe", "binary.exe"))
        assert os.path.exists(os.path.join(self.test_dir, "jpg", "image.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "mp4", "video.mp4"))

        assert not os.path.exists(os.path.join(self.test_dir, "binary.exe"))
        assert not os.path.exists(os.path.join(self.test_dir, "image.jpg"))
        assert not os.path.exists(os.path.join(self.test_dir, "video.mp4"))

    def test_sort_by_type_sim(self):
        organize_by_type(self.test_dir, True, self.log_file)

        assert not os.path.exists(os.path.join(self.test_dir, "exe", "binary.exe"))
        assert not os.path.exists(os.path.join(self.test_dir, "jpg", "image.jpg"))
        assert not os.path.exists(os.path.join(self.test_dir, "mp4", "video.mp4"))

        assert os.path.exists(os.path.join(self.test_dir, "binary.exe"))
        assert os.path.exists(os.path.join(self.test_dir, "image.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "video.mp4"))

    def test_sort_by_size(self):
        organize_by_size(self.test_dir, False, self.log_file, int(1e6), int(1e7), int(1e8))

        assert os.path.exists(os.path.join(self.test_dir, "small", "binary.exe"))
        assert os.path.exists(os.path.join(self.test_dir, "medium", "image.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "large", "video.mp4"))

        assert not os.path.exists(os.path.join(self.test_dir, "binary.exe"))
        assert not os.path.exists(os.path.join(self.test_dir, "image.jpg"))
        assert not os.path.exists(os.path.join(self.test_dir, "video.mp4"))

    def test_sort_by_size_sim(self):
        organize_by_size(self.test_dir, True, self.log_file, int(1e6), int(1e7), int(1e8))

        assert not os.path.exists(os.path.join(self.test_dir, "small", "binary.exe"))
        assert not os.path.exists(os.path.join(self.test_dir, "medium", "image.jpg"))
        assert not os.path.exists(os.path.join(self.test_dir, "large", "video.mp4"))

        assert os.path.exists(os.path.join(self.test_dir, "binary.exe"))
        assert os.path.exists(os.path.join(self.test_dir, "image.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "video.mp4"))

    def test_sort_by_date(self):
        organize_by_date(self.test_dir, False, self.log_file)

        assert os.path.exists(os.path.join(self.test_dir, "1970-01-01", "binary.exe"))
        assert os.path.exists(os.path.join(self.test_dir, "1970-01-02", "image.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "1970-01-03", "video.mp4"))

        assert not os.path.exists(os.path.join(self.test_dir, "binary.exe"))
        assert not os.path.exists(os.path.join(self.test_dir, "image.jpg"))
        assert not os.path.exists(os.path.join(self.test_dir, "video.mp4"))

    def test_sort_by_date_sim(self):
        organize_by_date(self.test_dir, True, self.log_file)

        assert not os.path.exists(os.path.join(self.test_dir, "1970-01-01", "binary.exe"))
        assert not os.path.exists(os.path.join(self.test_dir, "1970-01-02", "image.jpg"))
        assert not os.path.exists(os.path.join(self.test_dir, "1970-01-03", "video.mp4"))

        assert os.path.exists(os.path.join(self.test_dir, "binary.exe"))
        assert os.path.exists(os.path.join(self.test_dir, "image.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "video.mp4"))


if __name__ == '__main__':
    unittest.main()
