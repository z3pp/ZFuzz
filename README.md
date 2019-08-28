# ZFuzz
[![Python](https://img.shields.io/badge/python-3.7-20d47a?style=flat-square)](https://python.org/) [![License](https://img.shields.io/badge/license-GPLv3-4ab0d9?style=flat-square)](https://github.com/z3pp/ZFuzz/blob/master/LICENSE) [![Release](https://img.shields.io/badge/release-1.2-lightgrey?style=flat-square)](https://github.com/z3pp/ZFuzz/) [![Build Status](https://img.shields.io/travis/z3pp/ZFuzz/master?style=flat-square)](https://travis-ci.org/z3pp/ZFuzz)

ZFuzz is an opensource web fuzzer written in Python (See [Wfuzz](https://wfuzz.readthedocs.io/) for more advanced features)

### Usage exemple:
```
$ zfuzz.py -w /mywordlist -u https://example.com/^FUZZ^ --sc 200
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

```

### Installation
You can easily install zfuzz by following these commands:
```
$ git clone https://github.com/z3pp/ZFuzz.git
$ cd ZFuzz
$ python setup.py install
```
ZFuzz needs Python v3 to work, and it must be run on Linux

### Documentation
The documentation is available at http://zfuzz.readthedocs.io

Enjoy ;)
