import getpass
import os
import os.path
import pathlib
import socket
import subprocess
import sys

from pathlib import Path

def which(name):
    "Search the executable path for a command"
    if os.path.isabs(name):
        return name

    for p in os.environ['PATH'].split(os.pathsep):
        candidate = os.path.join(p, name)
        if os.path.exists(candidate):
            return candidate

class Command:
    """Object representing a command that can be executed by creating a new process

Typical operation is to call it with an argument list. A default list of arguments and keyword arguments (typically specifying the name of the command) can be embedded in the object.

Special keyword arguments:
_path_safety -- If True, arguments starting with - will be prefixed with the current directory to prevent relative paths from being erroneously interpreted as switches. On Windows, arguments starting with / will also be prefixed. Defaults to True.
"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        args = [repr(x) for x in self.args]
        args.extend(f'{name}={repr(value)}' for name, value in self.kwargs.items())
        return f'Command({', '.join(args)})'

    def add(self, *args, **kwargs):
        """Create a new command by appending arguments and/or updating keyword arguments"""
        new_args = self.args + args
        new_kwargs = self.kwargs.copy()
        new_kwargs.update(kwargs)
        return Command(*new_args, **new_kwargs)

    def run(self):
        """Run the command as it is"""
        if '_argv' in self.kwargs:
            argv = self.kwargs['_argv']
        else:
            # translate into regular arguments
            path_safety = self.kwargs.get('_path_safety', True)
            argv = []
            for arg in self.args:
                if isinstance(arg, (str, bytes)):
                    pass
                elif hasattr(arg, '__fspath__'):
                    arg = arg.__fspath__()
                else:
                    arg = str(arg)
                if path_safety:
                    if isinstance(arg, str):
                        if (arg.startswith('-') or (os.name == 'nt' and arg.startswith('/'))):
                            arg = os.path.join(os.getcwd(), arg)
                    else:
                        if (arg.startswith(b'-') or (os.name == 'nt' and arg.startswith(b'/'))):
                            arg = os.path.join(os.getcwdb(), arg)
                argv.append(arg)
        popen = subprocess.Popen(argv)
        retval = popen.wait()
        if retval:
            raise subprocess.CalledProcessError(retval, argv)

    def __call__(self, *args, **kwargs):
        return self.add(*args, **kwargs).run()

class CommandSearcher:
    def find(self, name):
        return Command(which(name))

    def __getattr__(self, name):
        return self.find(name)

    def __getitem__(self, name):
        return self.find(name)

cmd = CommandSearcher()

def pwd():
    "Return the currnet working directory."
    return pathlib.Path(os.getcwd())

user = getpass.getuser()

hostname = socket.gethostname()

class _FnString:
    def __init__(self, fn):
        self.fn = fn

    def __str__(self):
        return self.fn()

def setps1(fn):
    """Set the primary shell prompt.

fn is a function taking no arguments and returning a string.

For example, the default prompt is set by:
setps1(lambda: f'{user}@{hostname}:{pwd()} >>> ')"""
    sys.ps1 = _FnString(fn)

def setps2(fn):
    """Set the secondary shell prompt, which displays when entering multi-line strings.

fn is a function taking no arguments and returning a string."""
    sys.ps2 = _FnString(fn)

setps1(lambda: f'{user}@{hostname}:{pwd()} >>> ')

parent = Path('..')
root = Path('/')
home = Path(os.path.expanduser('~'))
devnull = Path(os.devnull)

cd = os.chdir

