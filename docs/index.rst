.. title:: ZFuzz

ZFuzz Web Fuzzer
=================

.. image:: https://img.shields.io/badge/python-3.7-20d47a?style=flat-square
    :target: https://python.org/
.. image:: https://img.shields.io/badge/license-GPLv3-4ab0d9?style=flat-square
    :target: https://github.com/z3pp/ZFuzz/blob/master/LICENSE
.. image:: https://img.shields.io/badge/release-1.2-lightgrey?style=flat-square
    :target: https://github.com/z3pp/ZFuzz
.. image:: https://img.shields.io/travis/z3pp/ZFuzz/master?style=flat-square
    :target: https://travis-ci.org/z3pp/ZFuzz

ZFuzz is an opensource web fuzzer written in Python
(See `Wfuzz <https://wfuzz.readthedocs.io>`_ for more advanced features)

**Usage exemple**::

    $ ./zfuzz.py -w /mywordlist -u https://example.com/^FUZZ^ --sc 200
         ___
     ___|  _|_ _ ___ ___
    |- _|  _| | |- _|- _|
    |___|_| |___|___|___| v1.2

    [TARGET] https://example.com/<fuzz>

    [27:58] [200]: admin
    [27:58] [200]: robots.txt
    [27:58] [200]: js
    [27:58] [200]: css
    [27:59] [200]: cgi-bin
    [27:59] [200]: about
    [28:00] [200]: accounts

    [28:00] Total time: 3s

**Features**

- Multithreaded
- Allows fuzzing of HTTP headers, POST data, cookies, and different parts of URL
- Very simple architecture/code so you can easily contribute to the project
- Easy to use and a nice interface

ZFuzz needs Python v3 to work, and it must be run on Linux

Documentation
==============
.. toctree::
   :maxdepth: 2

   source/contributing
   source/installation
   source/basicusage
   source/indepth

