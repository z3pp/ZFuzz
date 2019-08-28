import sys
import threading
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
        :param headers: HTTP Headerss
        :param data: POST Data
        :param cookies: HTTP Cookies
        :param threads: Threads numbers
        :param keyword: Fuzzing keyword to use
        :param timeout: Requests timeout
        :param delay: Delay between requests
        :param hc: HTTP Code(s) to hide
        :param sc: HTTP Code(s) to show
        :param hs: Hide reponse with the given str
        :param ss: Show reponse with the given str
    """

    def __init__(self, url, wordlist, headers, data, cookies, threads,
                 keyword, timeout, delay, hc, sc, hs, ss):

        self.colors = ZFuzzCLI()

        self._url = url
        self._wordlist = wordlist
        self._headers = headers
        self._data = data
        self._cookies = cookies
        self._threads = threads
        self._keyword = keyword
        self._timeout = timeout
        self._delay = delay
        self._hc = hc
        self._sc = sc
        self._hs = hs
        self._ss = ss

        self._method = requests.post if data else requests.get

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
                                   cookies=cookies, timeout=self._timeout)

                time.sleep(self._delay)
                code = res.status_code
                if is_matching(code, self._hc, self._sc, str(res.content),
                               self._hs, self._ss):

                    color = get_code_color(code)
                    sys.stdout.write(f"{self.colors.blue}["
                                     f"{time.strftime('%M:%S', time.gmtime())}"
                                     f"]{self.colors.default} "
                                     f"[{color}{code}"
                                     f"{self.colors.default}]: {i}\n")

            except Exception:
                pass

            finally:
                q.task_done()

    def run(self):

        """ Start the threads """

        q = queue.Queue()

        lines = self._wordlist.read().splitlines()
        for line in lines:
            q.put(line.rstrip('\n\r'))

        print(f"{self.colors.magenta}[TARGET] "
              f"{self.colors.default}"
              f"{self._url.replace(self._keyword, '<fuzz>')}")
        print()

        # Start Fuzzing :)
        old_time = time.time()
        threads = [threading.Thread(target=self.fuzz, args=(i, q))
                   for i in range(int(self._threads))]

        for t in threads:
            t.setDaemon(True)
            t.start()

        q.join()
        new_time = time.time()
        print()
        print(f"{self.colors.blue}"
              f"[{time.strftime('%M:%S', time.gmtime())}]"
              f"{self.colors.default} Total time: {int(new_time - old_time)}s")
        print()
