/* C ABI of libpython_template_cpp. Every exported function is declared here. */
#pragma once

#include <stdint.h>

#define PYTHON_TEMPLATE_CPP_ABI_VERSION 1

#if defined(_WIN32) && defined(PYTHON_TEMPLATE_CPP_BUILD)
#define PYTHON_TEMPLATE_CPP_API __declspec(dllexport)
#elif defined(_WIN32)
#define PYTHON_TEMPLATE_CPP_API __declspec(dllimport)
#else
#define PYTHON_TEMPLATE_CPP_API __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* The ABI version the library was built with. Compare it with PYTHON_TEMPLATE_CPP_ABI_VERSION. */
PYTHON_TEMPLATE_CPP_API uint32_t python_template_cpp_abi_version(void);

/* Adds two numbers. */
PYTHON_TEMPLATE_CPP_API int32_t python_template_cpp_add(int32_t i, int32_t j);

#ifdef __cplusplus
}
#endif
