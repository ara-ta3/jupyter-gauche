# coding: utf-8

# ===== DEFINITIONS =====

from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
from subprocess import check_output

import re
import signal

__version__ = '0.0.4'

def parse_commands(code):
    codes = []
    tmp = ""
    for c in code.splitlines():
        comment_out_removed = remove_comment_out(c.strip())
        tmp += (" " + comment_out_removed)
        tmp = tmp.strip()
        start = tmp.count("(")
        end = tmp.count(")")
        if tmp and start == end:
            codes.append(tmp)
            tmp = ""
    return codes

def remove_comment_out(code):
    comment_out_idx = code.find(";")
    if comment_out_idx > -1:
        return code[:comment_out_idx]
    else:
        return code

class GaucheKernel(Kernel):
    implementation = 'gauche_kernel'
    implementation_version = __version__

    @property
    def banner(self):
        return u'Gauche Kernel'


    language_info = {'name': 'gauche',
                     'codemirror_mode': 'scheme',
                     'mimetype': 'text/plain',
                     'file_extension': '.scm'}


    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_gauche()


    def _start_gauche(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.gauchewrapper = replwrap.REPLWrapper("gosh", "gosh>", None)
        finally:
            signal.signal(signal.SIGINT, sig)


    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        code = "\n".join(parse_commands(code))
        if not code:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            output = self.gauchewrapper.run_command(code, timeout=None)
        except KeyboardInterrupt:
            self.gauchewrapper.child.sendintr()
            interrupted = True
            self.gauchewrapper._expect_prompt()
            output = self.gauchewrapper.child.before
        except EOF:
            output = self.gauchewrapper.child.before + 'Restarting Gauche'
            self._start_gauche()

        if not silent:
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}


