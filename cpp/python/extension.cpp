#include <pybind11/pybind11.h>

#include "python_template_cpp/python_template_cpp.h"

PYBIND11_MODULE(extension, m) {
  m.doc() = "pybind11 example plugin";

  m.def("add", &python_template_cpp_add, "A function that adds two numbers");
}
