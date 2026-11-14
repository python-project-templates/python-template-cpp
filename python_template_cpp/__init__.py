import os
import os.path

if os.name == "nt" and os.path.isdir(os.path.join(os.path.dirname(__file__), "lib")):
    # Windows has no rpath, so the extension finds libpython_template_cpp.dll through this directory.
    _DLL_DIRECTORY = os.add_dll_directory(os.path.join(os.path.dirname(__file__), "lib"))

from .extension import *

__version__ = "0.1.0"


def include_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "include"))


def bin_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "bin"))


def lib_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "lib"))


def get_prefix() -> str:
    """The installed package directory, which holds ``include`` and ``lib`` for libpython_template_cpp."""
    return os.path.abspath(os.path.dirname(__file__))


def get_include() -> str:
    """The directory holding ``python_template_cpp/python_template_cpp.h``."""
    return include_path()


def get_library_dirs() -> list[str]:
    """Directories holding the bundled libpython_template_cpp shared library."""
    return [lib_path()]


def get_libraries() -> list[str]:
    """Link names for libpython_template_cpp, for ``-l`` or ``target_link_libraries``."""
    return ["libpython_template_cpp" if os.name == "nt" else "python_template_cpp"]
