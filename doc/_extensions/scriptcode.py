from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.body import CodeBlock
import sphinx.roles
from docutils import nodes
import os
import re


class ScriptCode(CodeBlock):
    required_arguments = 1
    seen_files = {}

    def run(self):
        filename = self.arguments[0]
        code = '\n'.join(self.content) + '\n\n'
        code_test = code.replace("#TEST ", "")
        code_test = re.sub(r"\n\s*#NOTEST[^\n]*", "", code_test)
        code_test = re.sub(r"^\s*#NOTEST[^\n]*\n", "", code_test)
        code = code.replace("#NOTEST ", "")
        code = re.sub(r"\n\s*#TEST[^\n]*", "", code)
        code = re.sub(r"^\s*#TEST[^\n]*\n", "", code)
        if filename in ScriptCode.seen_files:
            mode = 'a'
        else:
            mode = 'w'
            ScriptCode.seen_files[filename] = filename
            try:
                os.mkdir('scripts')
            except OSError:
                pass
        with open('scripts/' + filename, mode) as fi:
            fi.write(code)
        with open("scripts/test_" + filename, mode) as fi:
            fi.write(code_test)
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
        os.path.relpath(os.path.abspath('scripts/' + ret[0][0]['reftarget']), env.srcdir)
    return ret


def setup(app):
    """ Register directive with Sphinx """
    app.add_directive('script-code', ScriptCode)
    app.add_role('script-code-file', script_code_file_role)
    return {'version': '0.1'}
