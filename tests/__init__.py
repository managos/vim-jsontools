import os
import unittest
from pynvim import attach
from rplugin.python3.vimjsontools import JsonToolsPlugin

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


class TestSomething(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.nvim = attach('socket', path='/tmp/nvim')
        self.nvim.command('tabnew {}/tests/data.json'.format(BASE_DIR))
        self.plugin = JsonToolsPlugin(self.nvim)

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
