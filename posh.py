import getpass
import os
import os.path
import pathlib
import socket
import sys

from pathlib import Path

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

