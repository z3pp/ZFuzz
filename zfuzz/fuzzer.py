import threading
import sys
import time
import queue
import requests

from .utils import replace_kv_dict
from .utils import get_code_color
from .utils import is_matching
from .cli import ZFuzzCLI


class Fuzz(object):

    """ Used to fuzz an host with multi-threads

        :param url: Url to fuzz
        :param wordlist: Wordlist used
        :param headers: HTTP Headers
        :param data: POST Data
        :param verb: HTTP verb
        :param cookies: HTTP Cookies
        :param threads: Threads numbers
        :param keyword: Fuzzing keyword to use
        :param timeout: Requests timeout
        :param delay: Delay between requests
        :param follow: Follow HTTP Requests
        :param quiet: Do not print additional information
        :param hc: HTTP Code(s) to hide
        :param sc: HTTP Code(s) to show
        :param hs: Hide reponse with the given str
        :param ss: Show reponse with the given str
        :param hr: Hide response with the given regex
        :param sr: Show response with the given regex
        :param hl: Response lenght to hide
        :param sl: Response lenght to show
    """

    def __init__(self, url, wordlist, headers, data, verb, cookies,
                 threads, keyword, timeout, delay, follow, quiet,
                 hc, sc, hs, ss, hr, sr, hl, sl):

        self.cli = ZFuzzCLI()
        self.log = self.cli.log

        self._url = url
        self._wordlist = wordlist
        self._headers = headers
        self._data = data
        self._cookies = cookies
        self._threads = threads
        self._keyword = keyword
        self._timeout = timeout
        self._delay = delay
        self._follow = follow
        self._quiet = quiet
        self._hc = hc
        self._sc = sc
        self._hs = hs
        self._ss = ss
        self._hr = hr
        self._sr = sr
        self._hl = hl
        self._sl = sl

        self._method = (requests.post if data and verb.lower() == "get"
                        else eval("requests." + verb.lower()))

        self.run()

    def fuzz(self, i, q):

        """ Start to fuzz the url

            :param q: Queue instance that contains all words of the wordlist
        """

        while True:
            i = q.get()
            link = self._url.replace(self._keyword, i)
            headers = replace_kv_dict(self._headers.copy(), self._keyword, i)
            data = replace_kv_dict(self._data.copy(), self._keyword, i)
            cookies = replace_kv_dict(self._cookies.copy(), self._keyword, i)
            try:
                res = self._method(link, headers=headers, data=data,
                                   cookies=cookies, timeout=self._timeout,
                                   allow_redirects=self._follow)

                time.sleep(self._delay)
                code = res.status_code
                if is_matching(code, self._hc, self._sc, str(res.content),
                               len(res.text), self._hs, self._ss, self._hr,
                               self._sr, self._hl, self._sl):

                    color = get_code_color(code)
                    if not self._quiet:
                        state = (f"[{color}{code}{self.cli.default}]: {i}\n")
                        self.log.warn(state)
                    else:
                        sys.stdout.write(i + '\n')

            except Exception as e:
                print(e)

            finally:
                q.task_done()

    def run(self):

        """ Start the threads """

        q = queue.Queue()

        lines = self._wordlist.read().splitlines()
        for line in lines:
            q.put(line.rstrip('\n\r'))

        threads = [threading.Thread(target=self.fuzz, args=(i, q))
                   for i in range(int(self._threads))]

        for t in threads:
            t.setDaemon(True)
            t.start()

        q.join()
