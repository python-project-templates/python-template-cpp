# python template cpp

A C++-Python project template

[![Build Status](https://github.com/python-project-templates/python-template-cpp/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/python-project-templates/python-template-cpp/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/python-project-templates/python-template-cpp/branch/main/graph/badge.svg)](https://codecov.io/gh/python-project-templates/python-template-cpp)
[![License](https://img.shields.io/github/license/python-project-templates/python-template-cpp)](https://github.com/python-project-templates/python-template-cpp)
[![PyPI](https://img.shields.io/pypi/v/python-template-cpp.svg)](https://pypi.python.org/pypi/python-template-cpp)

## Overview

## C ABI

`cpp/python-template-cpp` builds `libpython_template_cpp`, a C ABI over the C++ code, declared in
`python_template_cpp/include/python_template_cpp/python_template_cpp.h`. Wheels ship the library under `python_template_cpp/lib` and
the header under `python_template_cpp/include/python_template_cpp`, and the pybind11 extension in `cpp/python` links
against the library. The tests compile a C program against the installed package. Other
projects build against the installed wheel with `python_template_cpp.get_include()`,
`get_library_dirs()`, `get_libraries()`, and `get_prefix()`.

`HATCH_CPP_LIBRARY_SOURCE` chooses where the library comes from at build time:
`bundled` (the default, for wheels), `external` (a prebuilt library found
through `HATCH_CPP_LIBRARY_ROOT`, pkg-config, or the conda prefix), or `direct`
(compile the library sources into the extension).

`cpp/CMakeLists.txt` builds and installs the library without Python, with a CMake
package config and a pkg-config file, for conda, vcpkg, and system packages:

```bash
cmake -S cpp -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cmake --install build --prefix /path/to/prefix
```

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
