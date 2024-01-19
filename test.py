import unittest
from unittest.mock import patch, mock_open, MagicMock
from file_sorter import log_movement, move_file, undo_last_organization
from pathlib import Path


class TestFileOrganizer(unittest.TestCase):

    def setUp(self):
        self.test_log_path = "test_log.json"
        self.test_file = Path("test.txt")
        self.test_dir = Path("test_dir")
        self.test_target = self.test_dir / self.test_file.name

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("os.path.exists", return_value=False)
    @patch("json.dump")
    def test_log_movement_new_log(self, mock_json_dump, mock_exists, mock_file):
        log_movement(self.test_file, self.test_target, self.test_log_path)
        mock_exists.assert_called_with(self.test_log_path)
        mock_file.assert_called_with(self.test_log_path, "w")
        mock_json_dump.assert_called()

    @patch("os.path.exists", return_value=True)
    @patch("shutil.move")
    @patch("os.remove")
    @patch("pathlib.Path.exists", MagicMock(return_value=True))
    def test_undo_last_organization(self, mock_os_path_exists, mock_shutil_move, os_remove):
        log_data = '[{"original": "test.txt", "new": "test_dir/test.txt"}]'
        with patch("builtins.open", new_callable=mock_open, read_data=log_data):
            undo_last_organization(self.test_log_path)
            mock_shutil_move.assert_called_with("test_dir\\test.txt", "test.txt")
            os_remove.assert_called_with(self.test_log_path)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"original": "old_path", "new": "new_path"}]')
    @patch("os.path.exists", return_value=True)
    @patch("json.dump")
    def test_log_movement_existing_log(self, mock_json_dump, mock_exists, mock_file):
        log_movement(self.test_file, self.test_target, self.test_log_path)
        mock_exists.assert_called_with(self.test_log_path)
        mock_file.assert_called_with(self.test_log_path, "w")
        mock_json_dump.assert_called()

    @patch("pathlib.Path.mkdir")
    @patch("shutil.move")
    def test_move_file(self, mock_shutil_move, mock_mkdir):
        move_file(self.test_file, self.test_dir, False, self.test_log_path)
        mock_mkdir.assert_called_with(exist_ok=True)
        mock_shutil_move.assert_called_with(str(self.test_file), str(self.test_target))

    @patch("pathlib.Path.mkdir")
    @patch("shutil.move")
    def test_move_file_simulate(self, mock_shutil_move, mock_mkdir):
        move_file(self.test_file, self.test_dir, True, self.test_log_path)
        assert not  mock_mkdir.assert_not_called()
        assert not mock_shutil_move.assert_not_called()


if __name__ == '__main__':
    unittest.main()
