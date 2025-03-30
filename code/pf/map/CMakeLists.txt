cmake_minimum_required(VERSION 3.22)
project(Map LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)

add_library(
  Map INTERFACE
  Map.cpp
)

target_include_directories(
  Map INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_SOURCE_DIR}/include/
)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Eigen3 3.3 REQUIRED)
target_link_libraries(
  Map INTERFACE
  Python3::Python
  Python3::Module
  Eigen3::Eigen
)

