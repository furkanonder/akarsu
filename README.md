<div align="center">
  <img src="https://github.com/furkanonder/akarsu/blob/develop/static/banner.png"/>
  <a href="https://github.com/furkanonder/akarsu/actions"><img alt="Actions Status" src="https://github.com/furkanonder/akarsu/workflows/Test/badge.svg"></a>
  <a href="https://github.com/furkanonder/akarsu/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/furkanonder/akarsu"></a>
  <a href="https://github.com/furkanonder/akarsu/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/furkanonder/akarsu"></a>
  <a href="https://github.com/furkanonder/akarsu/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/furkanonder/akarsu"></a>
  <a href="https://pepy.tech/project/akarsu"><img alt="Downloads" src="https://pepy.tech/badge/akarsu"></a>
</div>

---

_akarsu_ is the New Generation Profiler based on
[PEP 669](https://peps.python.org/pep-0669/). The name of the project, comes from the
surname of a minstrel named `Muhlis Akarsu`, which means `stream`.

## Installation

_akarsu_ can be installed by running `pip install akarsu`. It requires Python 3.12.0+ to
run.

## Usage

```sh
cat example.py
```

Output:

```python
def foo():
    x = 1
    isinstance(x, int)
    return x


def bar():
    foo()


bar()
```

---

```sh
akarsu -f example.py
```

Output:

```
     Count     Event Type     Filename(function)
         1      PY_CALL       example.py(bar)
         1      PY_START      example.py(bar)
         1      PY_CALL       example.py(foo)
         1      PY_START      example.py(foo)
         1       C_CALL       example.py(<built-in function isinstance>)
         1      C_RETURN      example.py(foo)
         1     PY_RETURN      example.py(foo)
         1     PY_RETURN      example.py(bar)

Total number of events: 8
  PY_CALL = 2
  PY_START = 2
  PY_RETURN = 2
  C_CALL = 1
  C_RETURN = 1
```

---

If you want to show only the function calls in the output, you can use the `-c` or
`--calls` argument.

```sh
akarsu -c -f example.py
```

Output:

```
     Count     Event Type     Filename(function)
         1      PY_CALL       example.py(bar)
         1      PY_CALL       example.py(foo)
         1       C_CALL       example.py(<built-in function isinstance>)

Total number of events: 3
  PY_CALL = 2
  C_CALL = 1
```
