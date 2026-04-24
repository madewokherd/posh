import getpass
import os
import pathlib
import socket
import sys

from pathlib import Path

def pwd():
    return pathlib.Path(os.getcwd())

user = getpass.getuser()

hostname = socket.gethostname()

class _FnString:
    def __init__(self, fn):
        self.fn = fn

    def __str__(self):
        return self.fn()

def setps1(fn):
    sys.ps1 = _FnString(fn)

def setps2(fn):
    sys.ps2 = _FnString(fn)

setps1(lambda: f'{user}@{hostname}:{pwd()} >>> ')

