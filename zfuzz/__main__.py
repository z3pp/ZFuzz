import sys
from .cli import ZFuzzCLI


def main():
    ZFuzzCLI().main(sys.argv)
