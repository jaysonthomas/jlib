cmake_minimum_required(VERSION 3.22)
project(pf LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)

add_executable(
  pf 
  main.cpp 
  map/Map.cpp
  bot/Bot.cpp
)

target_include_directories(
  pf PUBLIC
  util/
  map/
  bot/
  include/
  matrix/
)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Eigen3 3.3 REQUIRED)
target_link_libraries(
  pf PRIVATE
  Python3::Python
  Python3::Module
  Eigen3::Eigen
)

