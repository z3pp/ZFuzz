import sys
import argparse
from colored import fg, attr

from .actions import RangeAction
from .actions import UrlAction
from .actions import DictAction
from .actions import ListAction
from .actions import DataAction


class ZFuzzCLI(object):

    """ Handle zfuzz CLI """

    def __init__(self):
        self.bold = attr("bold")
        self.red = fg(203)
        self.green = fg(77)
        self.blue = fg(69)
        self.magenta = fg(170) + self.bold
        self.default = attr("reset")

    def print_banner(self):

        """ Print the zfuzz banner """

        bannerstr = f"""     ___
 ___|  _|_ _ ___ ___
|- _|  _| | |- _|- _|
|___|_| |___|___|___| {self.default + self.bold}v1.2
                     """
        print(self.magenta + bannerstr + self.default)

    def print_help(self):

        """ Print the help banner """

        helpstr = """{}Usage: {} [OPTIONS] [WORDLIST] [URL]
\nZFuzz Options:{}
    [-h/--help]      -- Print this help message
    [-u/--url]       -- URL to fuzz
    [-w/--wordlist]  -- wordlist
    [-H/--headers]   -- HTTP headers
    [-d/--data]      -- POST data
    [-b/--cookies]   -- Cookie to send for the requests
    [-k/--keyword]   -- Fuzzing keyword to use. Default ^FUZZ^
    [-t/--threads]   -- Number of threads. Default 35
    [-s/--delay]     -- Delay between requests
    [-r/--follow]    -- Follow HTTP redirection
    [--timeout]      -- Requests timeout
    [--hc/sc]        -- HTTP Code(s) to hide/show
    [--hs/ss]        -- Response to hide/show with the given str
    """.format(self.bold, sys.argv[0], self.default)

        self.print_banner()
        print(helpstr)

    def parse_args(self, argv):

        """ ZFuzz Argument parser

            :param argv: Command line arguments list
            :returns: Arguments parsed
        """

        self.print_banner()

        parser = argparse.ArgumentParser(add_help=False,
                                         description="Python Web Fuzzer")

        parser.add_argument("-t", "--threads",
                            type=int, default=35, action=RangeAction,
                            mini=0, maxi=100)

        parser.add_argument("-w", "--wordlist",
                            type=argparse.FileType('r'), required=True)

        parser.add_argument("-u", "--url",
                            type=str, action=UrlAction, required=True)

        parser.add_argument("-H", "--headers",
                            type=str, default={}, nargs='*', action=DictAction)

        parser.add_argument("-d", "--data",
                            type=str, default={}, action=DataAction)

        parser.add_argument("-b", "--cookies",
                            type=str, default={}, nargs='*', action=DictAction)

        parser.add_argument("-k", "--keyword",
                            type=str, default="^FUZZ^")

        parser.add_argument("-s", "--delay",
                            type=float, default=0)

        parser.add_argument("-r", "--follow",
                            action="store_true")

        parser.add_argument("--timeout",
                            type=float)

        parser.add_argument("--hc",
                            type=str, default=[], action=ListAction)

        parser.add_argument("--sc",
                            type=str, default=[], action=ListAction)

        parser.add_argument("--hs",
                            type=str)

        parser.add_argument("--ss",
                            type=str)

        return parser.parse_args(argv)

    def main(self, argv):

        """ ZFuzz main method

            :param argv: Command line arguments list
        """

        from zfuzz.fuzzer import Fuzz

        if len(argv) <= 1 or "--help" in argv or "-h" in argv:
            self.print_help()
            exit(1)
        args = self.parse_args(argv[1:])
        try:
            Fuzz(**vars(args))
        except KeyboardInterrupt:
            sys.exit(1)
