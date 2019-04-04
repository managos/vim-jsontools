import io
import json
import csv
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

    @pynvim.function('JsonToolsCsvToJson')
    def csv_to_json(self, args):
        self.nvim.out_write("params={}\n".format(str(args)))
        keyname = args[0] if len(args) > 0 else None
        stream = io.StringIO(self._get_text())
        text = self._to_text(
            self._stream_to_items(stream, keyname)
        )
        self.nvim.current.buffer[:] = text.split('\n')

    def _stream_to_items(self, stream, keyname=None):
        reader = csv.DictReader(
            stream,
            skipinitialspace=True,
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        if keyname is None:
            rows = [row for row in reader]
        else:
            rows = {}
            for row in reader:
                key = row.pop(keyname)
                rows.setdefault(key, row)
        return rows

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
