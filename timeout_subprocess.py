import subprocess
import threading


def checkout_output(*popenargs, **kwargs):
    command = Command()
    command.run(func_type='checkout_output', *popenargs, **kwargs)
    return command.output


def call(*popenargs, **kwargs):
    command = Command()
    command.run(func_type='call', *popenargs, **kwargs)
    return command.returncode


def check_call(*popenargs, **kwargs):
    retcode = call(*popenargs, **kwargs)
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd)
    return 0


def popen(*popenargs, **kwargs):
    command = Command()
    command.run(func_type='popen', *popenargs, **kwargs)
    return command.process



class Command(object):
    def __init__(self):
        self.process = None
        self.output = None
        self.unused_err = None
        self.returncode = None

    def run(self, *popenargs, **kwargs):
        def target_checkout_output():
            print 'Thread started'
            if 'stdout' in kwargs:
                raise ValueError('stdout argument not allowed, it will be overridden.')
            self.process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
            self.output, self.unused_err = self.process.communicate()
            retcode = self.process.poll()
            if retcode:
                cmd = kwargs.get("args")
                if cmd is None:
                    cmd = popenargs[0]
                raise subprocess.CalledProcessError(retcode, cmd, output=self.output)
            print 'Thread finished'

        def target_call():
            self.process = subprocess.Popen(*popenargs, **kwargs)
            self.returncode = self.process.wait()

        def popen():
            self.process = subprocess.Popen(*popenargs, **kwargs)

        timeout = kwargs.get('timeout')
        if timeout:
            kwargs.pop('timeout')

        func_type = kwargs.get('func_type')
        if func_type:
            kwargs.pop('func_type')

        if func_type == 'checkout_output':
            thread = threading.Thread(target=target_checkout_output)
        elif func_type == 'call':
            thread = threading.Thread(target=target_call)
        elif func_type == 'popen':
            thread = threading.Thread(target=popen)
        else:
            raise GllueSubProcessError(func_type)

        thread.start()

        if timeout:
            thread.join(timeout)
        else:
            thread.join()
        if thread.is_alive():

            self.process.terminate()
            thread.join()


class GllueSubProcessError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "timeout_subprocess has no function named %s" % self.msg


# print check_call("pwd; sleep 2; pwd;", shell=True, timeout=4)
