# coding: utf-8

# ===== DEFINITIONS =====

from IPython.kernel.zmq.kernelbase import Kernel
from pexpect import replwrap, EOF
from subprocess import check_output

import re
import signal
import uuid

__version__ = '0.0.1'

version_pat = re.compile(r'(\d+(\.\d+)+)')
crlf_pat = re.compile(r'[\r\n]+')

class EgisonKernel(Kernel):
    implementation = 'gauche_kernel'
    implementation_version = __version__

    _language_version = None

    @property
    def language_version(self):
        if self._language_version is None:
            m = version_pat.search(check_output(['gosh', '-V']).decode('utf-8'))
            self._language_version = m.group(1)
        return self._language_version


    @property
    def banner(self):
        return u'Gauche Kernel (Gauche v%s)' % self.language_version


    language_info = {'name': 'gauche',
                     'codemirror_mode': 'scheme',
                     'mimetype': 'text/plain',
                     'file_extension': '.scm'}


    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_egison()


    def _start_egison(self):
        # Signal handlers are inherited by forked processes, and we can't easily
        # reset it from the subprocess. Since kernelapp ignores SIGINT except in
        # message handlers, we need to temporarily reset the SIGINT handler here
        # so that Egison is interruptible.
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.gauchewrapper = replwrap.REPLWrapper("gosh", "gosh>", None)
        finally:
            s.s.isg.nial(signal.SIGINT, sig)


    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        code = crlf_pat.sub(' ', code.strip())
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
            self._start_egison()

        if not silent:
            # Send standard output
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}


# ===== MAIN =====
if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=EgisonKernel)
