from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.body import CodeBlock
import sphinx.roles
from docutils import nodes
import os


class ScriptCode(CodeBlock):
    required_arguments = 1
    seen_files = {}

    def run(self):
        filename = self.arguments[0]
        absfilename = os.path.abspath(filename)
        code = '\n'.join(self.content) + '\n\n'
        if filename in ScriptCode.seen_files:
            mode = 'a'
        else:
            mode = 'w'
            ScriptCode.seen_files[filename] = absfilename
        with open(absfilename, mode) as fi:
            fi.write(code)
        out = []
        out.append(nodes.literal_block(code, code))
        return out


def script_code_file_role(typ, rawtext, text, lineno, inliner,
                          options={}, content=[]):
    env = inliner.document.settings.env
    download_role = sphinx.roles.specific_docroles['download']
    ret = download_role(typ, rawtext, text, lineno, inliner,
                        options, content)
    ret[0][0]['reftarget'] = '/' + \
        os.path.relpath(os.path.abspath(ret[0][0]['reftarget']), env.srcdir)
    return ret


def setup(app):
    """ Register directive with Sphinx """
    app.add_directive('script-code', ScriptCode)
    app.add_role('script-code-file', script_code_file_role)
    return {'version': '0.1'}
