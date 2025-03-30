cmake_minimum_required(VERSION 3.22)
project(Plotter LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)

add_library(
  Plotter 
  Plotter.cpp
)

target_include_directories (
  Plotter PUBLIC
  ${CMAKE_SOURCE_DIR}/util/
  ${CMAKE_CURRENT_SOURCE_DIR}
)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Eigen3 3.3 REQUIRED)
target_link_libraries(
  Plotter PRIVATE
  Python3::Python
  Python3::Module
  Eigen3::Eigen
  Map
  Bot
)

