import sys
import time
import argparse
import pwnlib
from colored import fg, attr

from .actions import RangeAction
from .actions import UrlAction
from .actions import DictAction
from .actions import ListAction
from .actions import DataAction


class ZFuzzCLI(object):

    """ Handle zfuzz CLI """

    def __init__(self):

        pwnlib.log.install_default_handler()
        self.log = pwnlib.log.getLogger('pwnlib.exploit')

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

        helpstr = f"""{self.bold}Usage: {sys.argv[0]} [OPTIONS] [WORDLIST] [URL]
\nZFuzz Options:{self.default}
    [-h/--help]      -- Print this help message
    [-u/--url]       -- URL to fuzz
    [-w/--wordlist]  -- wordlist
    [-H/--headers]   -- HTTP headers
    [-d/--data]      -- POST data
    [-X/--verb]      -- HTTP verb. Default get
    [-b/--cookies]   -- Cookie to send
    [-k/--keyword]   -- Fuzzing keyword. Default ^FUZZ^
    [-t/--threads]   -- Number of threads. Default 35
    [-s/--delay]     -- Delay between requests
    [-r/--follow]    -- Follow HTTP redirection
    [--quiet]        -- Do not print additional information
    [--timeout]      -- Requests timeout
    [--hc/sc]        -- HTTP Code(s) to hide/show
    [--hs/ss]        -- Response to hide/show that match with the given str
    [--hr/sr]        -- Response to hide/show that match with the given regex
    [--hl/sl]        -- Response lenght to hide/show
    """

        self.print_banner()
        print(helpstr)

    def parse_args(self, argv):

        """ ZFuzz Argument parser

            :param argv: Command line arguments list
            :returns: Arguments parsed
        """

        parser = argparse.ArgumentParser(add_help=False,
                                         description="Python Web Fuzzer")

        parser.add_argument("-t", "--threads",
                            type=int, default=35, action=RangeAction,
                            mini=0, maxi=100)

        parser.add_argument("-w", "--wordlist",
                            type=argparse.FileType('r', errors='ignore'),
                            required=True)

        parser.add_argument("-u", "--url",
                            type=str, action=UrlAction, required=True)

        parser.add_argument("-H", "--headers",
                            type=str, default={}, nargs='*', action=DictAction)

        parser.add_argument("-d", "--data",
                            type=str, default={}, action=DataAction)

        parser.add_argument("-X", "--verb",
                            choices=["GET", "HEAD", "POST", "OPTIONS", "PUT"],
                            type=str, default="get")

        parser.add_argument("-b", "--cookies",
                            type=str, default={}, nargs='*', action=DictAction)

        parser.add_argument("-k", "--keyword",
                            type=str, default="^FUZZ^")

        parser.add_argument("-s", "--delay",
                            type=float, default=0)

        parser.add_argument("-r", "--follow",
                            action="store_true")

        parser.add_argument("--quiet",
                            action="store_true")

        parser.add_argument("--timeout", type=float)

        parser.add_argument("--hc",
                            type=str, default=[], action=ListAction)

        parser.add_argument("--sc",
                            type=str, default=[], action=ListAction)

        parser.add_argument("--hs", type=str)

        parser.add_argument("--ss", type=str)

        parser.add_argument("--hr", type=str)

        parser.add_argument("--sr", type=str)

        parser.add_argument("--hl", type=int)

        parser.add_argument("--sl", type=int)

        return parser.parse_args(argv)

    def main(self, argv):

        """ ZFuzz main method

            :param argv: Command line arguments list
        """

        from zfuzz.fuzzer import Fuzz

        if len(argv) <= 1 or "--help" in argv or "-h" in argv:
            self.print_help()
            sys.exit(1)

        args = self.parse_args(argv[1:])

        if not args.quiet:
            self.print_banner()
            old_time = time.time()
            self.log.info("Target: {}".format(args.url.replace("^FUZZ^",
                                                               "<fuzz>")))
            print()

        try:
            Fuzz(**vars(args))
        except KeyboardInterrupt:
            sys.exit(1)

        if not args.quiet:
            new_time = time.time()
            print()
            self.log.success(f"Scan completed successfully in "
                             f"{int(new_time - old_time)}s")
            print()
