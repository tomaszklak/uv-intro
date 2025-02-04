---
title:
- UV introduction
author:
- Tomasz Kłak
theme:
- Copenhagen
date:
- Febuary 7, 2025
---

# What's UV?

Small and fast, all-in-one solution for managing python projects big and small - [cargo for python](https://astral.sh/blog/uv-unified-python-packaging).

# Running scripts

```python
import sys
print("Hello from python:", sys.version)
```

```
$ python 01.py
Hello from python: 3.10.14 (main, May  8 2024, 13:05:03) [Clang 15.0.0 (clang-1500.0.40.1)]  
```

To run a script with `uv` replace `python` with `uv run`:

```
$ uv run 01.py
Hello from python: 3.13.1 (main, Dec 19 2024, 14:22:59) [Clang 18.1.8 ]  
```

# Managing dependencies

```python
import requests
r = requests.get('https://nordvpn.com')
print("requests:", requests.__version__,
    "status:", r.status_code)
```

```bash
$ uv run 02.py
Traceback (most recent call last):
  File "/Users/tomaszklak/Development/uv-tutorial/02.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

# Managing dependencies (`--with`)

It's easy to use dependencies to with any script using `--with`:

```bash
$ uv run --with requests 02.py
requests: 2.32.3 status: 200
```
And to experiment with different versions:
```bash
$ uv run --with 'requests<2.30' 02.py
Installed 5 packages in 13ms
requests: 2.29.0 status: 200  
$ uv run --with 'requests<2.30' 02.py
requests: 2.29.0 status: 200
```

# Managing dependencies inline

It's possible to encode dependencies in python scripts directly (see [PEP-723](https://peps.python.org/pep-0723/)):
```python
# /// script
# dependencies = [
#     "requests<2.30",
# ]
# ///
import requests
r = requests.get('https://nordvpn.com')
print("requests:", requests.__version__,
    "status:", r.status_code)
```
```bash
$ uv run 03.py
Reading inline script metadata from `03.py`
requests: 2.29.0 status: 200
```

# Managing dependencies inline

It's still easy to override versions:
```bash
$ uv run --with 'requests==2.30' 03.py
Reading inline script metadata from `03.py`
requests: 2.30.0 status: 200    
```

# Managing dependencies - reproducibility

```python
# /// script
# dependencies = [
#     "requests",
# ]
# [tool.uv]
# exclude-newer = "2023-04-27T00:00:00Z"
# ///
import requests
r = requests.get('https://nordvpn.com')
print("requests:", requests.__version__,
    "status:", r.status_code)
```

```bash
$ uv run 04.py
Reading inline script metadata from `04.py`
requests: 2.29.0 status: 200
```

# Managing dependencies with lock files

Adding a lockfile is a as simple as `uv lock --script`:

```bash
$ uv lock --script 05.py
$ head 05.py.lock
version = 1
requires-python = ">=3.13"

[manifest]
requirements = [{ name = "requests" }]

[[package]]
name = "certifi"
version = "2025.1.31"
source = { registry = "https://pypi.org/simple" }
```

# Managing python

```bash
$ uv python list
cpython-3.13.1+freethreaded-macos-aarch64-none    <download available>
cpython-3.13.1-macos-aarch64-none                 /Users/tomaszklak/.local/share/uv/python/cpython-3.13.1-macos-aarch64-none/bin/python3.13
cpython-3.12.8-macos-aarch64-none                 <download available>
cpython-3.12.6-macos-aarch64-none                 /opt/homebrew/opt/python@3.12/bin/python3.12 -> ../Frameworks/Python.framework/Versions/3.12/bin/python3.12
cpython-3.11.11-macos-aarch64-none                <download available>
cpython-3.11.9-macos-aarch64-none                 /opt/homebrew/opt/python@3.11/bin/python3.11 -> ../Frameworks/Python.framework/Versions/3.11/bin/python3.11
cpython-3.10.16-macos-aarch64-none                /Users/tomaszklak/.local/bin/python3.10 -> /Users/tomaszklak/.local/share/uv/python/cpython-3.10.16-macos-aarch64-none/bin/python3.10
cpython-3.10.16-macos-aarch64-none                /Users/tomaszklak/.local/share/uv/python/cpython-3.10.16-macos-aarch64-none/bin/python3.10
cpython-3.10.14-macos-aarch64-none                /Users/tomaszklak/.pyenv/versions/3.10.14/bin/python3.10
cpython-3.10.14-macos-aarch64-none                /Users/tomaszklak/.pyenv/versions/3.10.14/bin/python3 -> python3.10
cpython-3.10.14-macos-aarch64-none                /Users/tomaszklak/.pyenv/versions/3.10.14/bin/python -> python3.10
cpython-3.9.21-macos-aarch64-none                 <download available>
cpython-3.9.6-macos-aarch64-none                  /Applications/Xcode.app/Contents/Developer/usr/bin/python3 -> ../../Library/Frameworks/Python3.framework/Versions/3.9/bin/python3
cpython-3.8.20-macos-aarch64-none                 <download available>
pypy-3.10.14-macos-aarch64-none                   /Users/tomaszklak/.local/share/uv/python/pypy-3.10.14-macos-aarch64-none/bin/pypy3.10
pypy-3.9.19-macos-aarch64-none                    <download available>
pypy-3.8.16-macos-aarch64-none                    <download available>
```

# Managing python

```bash
$ uv run --python cpython-3.13 python --version
Python 3.13.1

$ uv run --python cpython-3.13 which python
/Users/tomaszklak/.local/share/uv/python/cpython-3.13.1-macos-aarch64-none/bin/python

$ uv run --python pypy-3.10 python --version
Python 3.10.14 (39dc8d3c85a7, Aug 27 2024, 20:40:24)
[PyPy 7.3.17 with GCC Apple LLVM 15.0.0 (clang-1500.3.9.4)]

$ uv run --python pypy-3.10 which python
/Users/tomaszklak/.local/share/uv/python/pypy-3.10.14-macos-aarch64-none/bin/python
```

# Managing python - `requires-python`

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import requests
import sys
r = requests.get('https://nordvpn.com')
print("python:", sys.version,
    "version:", requests.__version__,
    "status:", r.status_code)
```

```bash
$ uv run 06.py
python: 3.13.1 (main, Dec 19 2024, 14:22:59)\
    [Clang 18.1.8] version: 2.32.3 status: 200
```

# Managing python - `--python`

```bash
$ uv run --python cpython-3.12 06.py
python: 3.12.6 (main, Sep  6 2024, 19:03:47)\
    [Clang 15.0.0 (clang-1500.1.0.2.5)] version: 2.32.3\
    status: 200
$ uv run --python pypy-3.10 06.py
python: 3.10.14 (39dc8d3c85a7, Aug 27 2024, 20:40:24)
[PyPy 7.3.17 with GCC Apple LLVM 15.0.0\
    (clang-1500.3.9.4 )] requests: 2.32.3 status: 200
```
# UV shebang

```python
#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
import requests
import sys
r = requests.get('https://nordvpn.com')
print("python:", sys.version, "requests:", requests.__version__, "status:", r.status_code)
```

```bash
$ chmod +x 07.py
$ ./07.py
python: 3.13.1 (main, Dec 19 2024, 14:22:59)\
    [Clang 18.1.8 ] requests: 2.32.3 status: 200
```

# Projects

```bash
$ uv init hello
Initialized project `hello` at `/Users/tomaszklak/Development/uv-tutorial/hello`
$ cat hello/pyproject.toml
[project]
name = "hello"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []
$ cat hello/.python-version
3.13
```

# Projects

```bash
$ cat hello.py
import requests
import sys
r = requests.get('https://nordvpn.com')
print("python:", sys.version,
    "requests:", requests.__version__,
    "status:", r.status_code)
$ uv add requests
Using CPython 3.13.1
Creating virtual environment at: .venv
Resolved 6 packages in 0.64ms
Installed 5 packages in 9ms
 + certifi==2025.1.31
 + charset-normalizer==3.4.1
 + idna==3.10
 + requests==2.32.3
 + urllib3==2.3.0
```

# Projects

```bash
$ cat hello/pyproject.toml
[project]
name = "hello"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "requests>=2.32.3",
]
$ head hello/uv.lock
version = 1
requires-python = ">=3.13"

[[package]]
name = "certifi"
version = "2025.1.31"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/1c/ab/c9f1e32b7b1bf505bf26f0ef697775960db7932abeb7b516de930ba2705f/certifi-2025.1.31.tar.gz", hash = "sha256:3d5da6925056f6f18f119200434a4780a94263f10d1c21d032a6f6b2baa20651", size = 167577 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/38/fc/bce832fd4fd99766c04d1ee0eead6b0ec6486fb100ae5e74c1d91292b982/certifi-2025.1.31-py3-none-any.whl", hash = "sha256:ca78db4565a652026a4db2bcdf68f2fb589ea80d0be70e03929ed730746b84fe", size = 166393 },
```

# Projects

```bash
$ uv run hello.py
python: 3.13.1 (main, Dec 19 2024, 14:22:59)\
    [Clang 18.1.8 ] requests: 2.32.3 status: 200
```
