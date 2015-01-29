import os
import sys


def configure():
    os.system("export LANG='en_US.UTF-8'")
    os.system("export LC_ALL='en_US.UTF-8'")
    sys.setrecursionlimit(10000)

