import json
import pynvim


@pynvim.plugin
class JsonToolsPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('JsonToolsPrettify', sync=True)
    def prettify(self, args):
        '''jsonを整形するコマンド'''
        jsontext = self._get_text()
        d = self._to_dict(jsontext)
        self.nvim.current.buffer[:] = self._to_text(d).split('\n')

    @pynvim.function('JsonToolsCheckValidateFormat', sync=True)
    def validate(self, args):
        '''formatチェック'''
        try:
            json.loads(self._get_text())
            self.nvim.out_write('json ok\n')
        except Exception as e:
            self.nvim.err_write('{}\n'.format(str(e)))

    def _get_text(self):
        return '\n'.join(self.nvim.current.buffer[:])

    def _to_dict(self, text):
        return json.loads(text)

    def _to_text(self, d):
        return json.dumps(
            d,
            ensure_ascii=False,
            indent=2
        )
