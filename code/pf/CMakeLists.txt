cmake_minimum_required(VERSION 3.22)
project(pf LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)

add_subdirectory(plotter)
add_subdirectory(map)
add_subdirectory(bot)

add_executable(
  pf 
  main.cpp 
)

target_include_directories(
  pf PUBLIC
  include/
  util/
)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Eigen3 3.3 REQUIRED)
target_link_libraries(
  pf PRIVATE
  Python3::Python
  Python3::Module
  Eigen3::Eigen
  Map
  Bot
  Plotter
)

