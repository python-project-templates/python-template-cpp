import os
from ctypes import CDLL, c_uint32
from pathlib import Path
from shutil import which
from subprocess import run
from sys import platform

import pytest

from python_template_cpp import add, get_include, get_libraries, get_library_dirs

C_CONSUMER = """
#include <stdio.h>
#include <python_template_cpp/python_template_cpp.h>

int main(void) {
    printf("%u %d", python_template_cpp_abi_version(), python_template_cpp_add(1, 2));
    return 0;
}
"""

CMAKE_CONSUMER = """
cmake_minimum_required(VERSION 3.20)
project(consumer LANGUAGES C)
find_package(python_template_cpp CONFIG REQUIRED)
add_executable(consumer consumer.c)
target_link_libraries(consumer PRIVATE python_template_cpp::python_template_cpp)
"""


def _library_filename(name: str) -> str:
    return f"{name}.dll" if platform == "win32" else f"lib{name}.dylib" if platform == "darwin" else f"lib{name}.so"


def _cmake_build(cmake: str, source: Path, build: Path, option: str) -> None:
    run([cmake, "-S", str(source), "-B", str(build), option, "-DCMAKE_BUILD_TYPE=Release"], check=True)
    run([cmake, "--build", str(build), "--config", "Release"], check=True)


def test_all():
    assert 3 == add(1, 2)


def test_c_library_and_header_are_installed():
    if platform == "emscripten":
        pytest.skip("Pyodide wheels compile the library in")
    header = Path(get_include()) / "python_template_cpp" / "python_template_cpp.h"
    assert "#define PYTHON_TEMPLATE_CPP_ABI_VERSION 1" in header.read_text()
    (name,) = get_libraries()
    library = CDLL(str(Path(get_library_dirs()[0]) / _library_filename(name)))
    library.python_template_cpp_abi_version.restype = c_uint32
    assert library.python_template_cpp_abi_version() == 1


def test_c_consumer_builds_against_the_installed_package(tmp_path):
    if platform == "emscripten":
        pytest.skip("Pyodide wheels compile the library in")
    compiler = next((path for path in map(which, ("cc", "gcc", "clang", "cl")) if path), None)
    if compiler is None:
        pytest.skip("no C compiler on PATH")
    (library,) = get_libraries()
    (library_dir,) = get_library_dirs()
    source = tmp_path / "consumer.c"
    source.write_text(C_CONSUMER)
    executable = tmp_path / ("consumer.exe" if platform == "win32" else "consumer")
    env = dict(os.environ)
    if platform == "win32":
        # Windows has no rpath, so the program finds the DLL through PATH whichever compiler built it.
        env["PATH"] = library_dir + os.pathsep + env["PATH"]
    if Path(compiler).stem.lower() == "cl":
        command = [compiler, "/nologo", f"/I{get_include()}", str(source), f"/Fe:{executable}", "/link", f"/LIBPATH:{library_dir}", f"{library}.lib"]
    else:
        command = [
            compiler,
            f"-I{get_include()}",
            str(source),
            f"-L{library_dir}",
            f"-l{library}",
            f"-Wl,-rpath,{library_dir}",
            "-o",
            str(executable),
        ]
    run(command, check=True, cwd=tmp_path)
    assert run([str(executable)], check=True, capture_output=True, text=True, env=env).stdout == "1 3"


def test_cmake_project_installs_a_package_that_find_package_locates(tmp_path):
    cmake = which("cmake")
    project = Path(__file__).resolve().parents[2] / "cpp"
    if cmake is None or not (project / "CMakeLists.txt").is_file():
        pytest.skip("needs cmake and the source tree")
    prefix = tmp_path / "prefix"
    _cmake_build(cmake, project, tmp_path / "build", f"-DCMAKE_INSTALL_PREFIX={prefix}")
    run([cmake, "--install", str(tmp_path / "build"), "--config", "Release"], check=True)
    assert (prefix / "lib" / "pkgconfig" / "python_template_cpp.pc").is_file()

    consumer = tmp_path / "consumer"
    consumer.mkdir()
    (consumer / "CMakeLists.txt").write_text(CMAKE_CONSUMER)
    (consumer / "consumer.c").write_text(C_CONSUMER)
    _cmake_build(cmake, consumer, consumer / "build", f"-DCMAKE_PREFIX_PATH={prefix}")
    (executable,) = [path for path in (consumer / "build").rglob("consumer*") if path.name in ("consumer", "consumer.exe") and path.is_file()]
    env = {**os.environ, "PATH": str(prefix / "bin") + os.pathsep + os.environ["PATH"]}
    assert run([str(executable)], check=True, capture_output=True, text=True, env=env).stdout == "1 3"
