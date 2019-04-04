import io
import os
import unittest
from pynvim import attach
from rplugin.python3.vimjsontools import JsonToolsPlugin

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


class TestSomething(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nvim = attach('socket', path='/tmp/nvim')
        cls.nvim.command('tabnew {}/tests/data.json'.format(BASE_DIR))
        cls.bufnr = cls.nvim.funcs.bufnr('%')
        cls.plugin = JsonToolsPlugin(cls.nvim)

    @classmethod
    def tearDownClass(cls):
        cls.nvim.command('u')
        cls.nvim.command('bdelete {}'.format(cls.bufnr))

    def test_get_text(self):
        self.assertEqual(
            self.plugin._get_text(),
            '''{"key": "value"
}'''
        )

    def test_to_dict(self):
        text = self.plugin._get_text()
        d = self.plugin._to_dict(text)
        self.assertEqual(d['key'], 'value')

    def test_validate(self):
        self.plugin.validate(None)

    def test_prettify(self):
        self.plugin.prettify(None)


class TestCSV(unittest.TestCase):
    def setUp(self):
        self.nvim = attach('socket', path='/tmp/nvim')
        self.nvim.command('tabnew {}/tests/data.csv'.format(BASE_DIR))
        self.bufnr = self.nvim.funcs.bufnr('%')
        self.plugin = JsonToolsPlugin(self.nvim)

    def tearDown(self):
        self.nvim.command('u')
        self.nvim.command('bdelete {}'.format(self.bufnr))

    def test_csv_to_json(self):
        self.plugin.csv_to_json([])

    def test_csv_to_json_with_key(self):
        self.plugin.csv_to_json(['a'])

    def test_stream_ti_items(self):
        obj = self.plugin._stream_to_items(io.StringIO('''1, 2, 3
4, 5, 6
7, 8, "テキスト"'''), keyname=None)
        self.assertEqual(len(obj), 2)
        self.assertEqual(obj[0]["1"], '4')
        self.assertEqual(obj[0]["2"], '5')
        self.assertEqual(obj[0]["3"], '6')
        self.assertEqual(obj[1]["3"], "テキスト")

    def test_stream_ti_items2(self):
        obj = self.plugin._stream_to_items(io.StringIO('''1, 2, 3
4, 5, 6
7, 8, "テキスト"'''), keyname='1')
        self.assertIsInstance(obj, dict)
        self.assertFalse("4" not in obj)
        self.assertEqual(obj["4"]["2"], '5')
        self.assertEqual(obj["4"]["3"], '6')
