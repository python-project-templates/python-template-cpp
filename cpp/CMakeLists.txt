# Builds and installs libpython_template_cpp without Python, for conda, vcpkg, and system packages.
cmake_minimum_required(VERSION 3.20)
project(python_template_cpp VERSION 0.1.0 LANGUAGES CXX)

include(CMakePackageConfigHelpers)

add_library(python_template_cpp SHARED python-template-cpp/c_api.cpp python-template-cpp/example.cpp)
add_library(python_template_cpp::python_template_cpp ALIAS python_template_cpp)
target_compile_features(python_template_cpp PRIVATE cxx_std_17)
target_compile_definitions(python_template_cpp PRIVATE PYTHON_TEMPLATE_CPP_BUILD)
target_include_directories(
  python_template_cpp
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../python_template_cpp/include> $<INSTALL_INTERFACE:include>
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
# SOVERSION is PYTHON_TEMPLATE_CPP_ABI_VERSION.
set_target_properties(
  python_template_cpp
  PROPERTIES VERSION ${PROJECT_VERSION}
             SOVERSION 1
             CXX_VISIBILITY_PRESET hidden
             VISIBILITY_INLINES_HIDDEN ON
             INSTALL_NAME_DIR "@rpath"
)

install(
  TARGETS python_template_cpp
  EXPORT python_template_cppTargets
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
install(DIRECTORY ../python_template_cpp/include/ DESTINATION include)
install(EXPORT python_template_cppTargets NAMESPACE python_template_cpp:: DESTINATION lib/cmake/python_template_cpp)

configure_package_config_file(
  cmake/python_template_cppConfig.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/python_template_cppConfig.cmake
  INSTALL_DESTINATION lib/cmake/python_template_cpp
)
write_basic_package_version_file(${CMAKE_CURRENT_BINARY_DIR}/python_template_cppConfigVersion.cmake COMPATIBILITY SameMinorVersion)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/python_template_cppConfig.cmake ${CMAKE_CURRENT_BINARY_DIR}/python_template_cppConfigVersion.cmake
        DESTINATION lib/cmake/python_template_cpp
)

configure_file(cmake/python_template_cpp.pc.in ${CMAKE_CURRENT_BINARY_DIR}/python_template_cpp.pc @ONLY)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/python_template_cpp.pc DESTINATION lib/pkgconfig)
