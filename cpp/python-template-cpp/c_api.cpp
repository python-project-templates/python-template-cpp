#include "python_template_cpp/python_template_cpp.h"

#include "python-template-cpp/example.hpp"

uint32_t python_template_cpp_abi_version(void) { return PYTHON_TEMPLATE_CPP_ABI_VERSION; }

int32_t python_template_cpp_add(int32_t i, int32_t j) { return python_template_cpp::add(i, j); }
