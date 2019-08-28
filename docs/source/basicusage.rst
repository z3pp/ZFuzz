Basic Usage
============

ZFuzz Options
--------------

* -h/--help -- Print the help banner
* -u/--url -- URL to fuzz
* -w/--wordlist -- wordlist
* -H/--headers -- HTTP headers
* -d/--data -- POST data
* -b/--cookies -- Cookie to send for the requests
* -k/--keyword -- Fuzzing keyword to use. Default ^FUZZ^
* -t/--threads -- Number of threads. Default 35
* -s/--delay -- Delay between requests
* --timeout -- Requests timeout
* --hc/sc -- HTTP Code(s) to hide/show
* --hs/ss -- Response to hide/show with the given str

Fuzzing keyword
----------------

By default, the fuzzing keyword is ^FUZZ^ but you can change it by using the  [-k/--keyword] option::

    $ ./zfuzz.py -k #FUZZ# ...

To fuzz something, just add the ^FUZZ^ keyword in the options that you would like to fuzz,
And zfuzz will replace this keyword by each word of the wordlist specified::

    $ ./zfuzz.py -w /mywordlist -u https://example.com/^FUZZ^
    $ ./zfuzz.py -w /mywordlist -u https://example.com/ -d "username=admin&password=^FUZZ^"
    $ ./zfuzz.py -w /mywordlist -u https://example.com/ -H "User-agent: ^FUZZ^" "Content-Type: application/json"
    $ ./zfuzz.py -w /mywordlist -u https://example.com/ -b cookie:^FUZZ^

Limiting requests
------------------

The fuzzer is multi-threaded and by default, has 35 threads, you can change this by using the [-t/--threads] option
You also can specify a delay between the requests

* Safe mode (Sending requests each 0.2s)::

    $ ./zfuzz.py -w /mywordlist -u http://example.com/^FUZZ^ -t 1 --delay 0.2

Filters
--------

You can easily filter the requests result with these filters:

Hide reponse
^^^^^^^^^^^^^

The following options can be used to hide certain HTTP responses

--hc (HTTP Code(s) to hide)::

    $ ./zfuzz.py -w /mywordlist -u http://example.com/^FUZZ^ --hc 500,404

--hs (Response to hide with the given str)::

    $ ./zfuzz.py -w /mywordlist -u http://example.com/^FUZZ^ --hs "home page"


Show reponse
^^^^^^^^^^^^^

The following options can be used to show certain HTTP responses

--sc (HTTP Code(s) to show)::

    $ ./zfuzz.py -w /mywordlist -u http://example.com/^FUZZ^ --sc 200,301

--hs (Response to show with the given str)::

    $ ./zfuzz.py -w /mywordlist -u http://example.com/^FUZZ^ --hs "home page"

