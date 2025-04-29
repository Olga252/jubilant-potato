import pytest
from unittest.mock import patch
import datetime
from tras import edit_note
from tras import save_notes

def test_edit_note_success():
    notes = [
        {'id': '1', 'title': 'Old Title', 'body': 'Old Body',
         'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            ]

    new_title = "New Title"
    new_body = "New Body"

    with patch('tras.save_notes') as mock_save:
        edit_note(notes, 1, new_title, new_body)
        assert notes[0]['title'] == new_title
        assert notes[0]['body'] == new_body
        assert notes[0]['timestamp'] != notes[0]['timestamp']
        mock_save.assert_called_once_with(notes)


def test_edit_note_not_found(capfd):
    notes = [
        {'id': '1', 'title': 'Title1', 'body': 'Body1',
         'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ]

    with patch('tras.save_notes') as mock_save:
        edit_note(notes, 2, "New Title", "New Body")
        out, _ = capfd.readouterr()
        assert "Заметка с указанным идентификатором не найдена." in out
        mock_save.assert_not_called()


