#from unit import dievn

#def test_ope_good( ):
 #   assert dievn(10, 2) ==5

import pytest
from  unittest.mock import patch
import  datetime

from tras import delete_note
from tras import add_note
from tras import edit_note
from tras import save_notes
from io import StringIO
from  tras import main



def test_add_note():
    notes = []
    title = 'Test Title'
    body = 'Test Body'

    with patch('tras.save_notes') as mock_save:
        add_note(notes, title, body)
        assert len(notes) == 1
        assert notes[0]['title'] == title
        assert notes[0]['body'] == body
        assert 'timestamp' in notes[0]
        assert notes[0]['id'] == 1
        mock_save.assert_called_once_with(notes)


def test_delete_note():
    notes = [{'id': '1', 'title': 'Title1', 'body': 'Body1',
              'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]

    with patch('tras.save_notes') as mock_save:
        delete_note(notes, 1)
        assert len(notes) == 0
        mock_save.assert_called_once_with(notes)


def test_delete_note_not_found(capfd):
    notes = []
    with patch('tras.save_notes') as mock_save:
        delete_note(notes, 1)
        out, _ = capfd.readouterr()
        assert 'не найдена' in out.lower()
        mock_save.assert_not_called()


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


def test_invalid_choice():
    user_input = "6\n1\n5\n"
    with patch('builtins.input', side_effect=user_input.splitlines()), \
            patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        main()

        output = mock_stdout.getvalue()
        assert "Некорректный ввод. Пожалуйста, введите число от 1 до 5." in output

