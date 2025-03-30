cmake_minimum_required(VERSION 3.22)
project(Bot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)

add_library(
  Bot 
  Bot.cpp
)

target_include_directories(
  Bot PUBLIC
  ${CMAKE_SOURCE_DIR}/include/
  ${CMAKE_CURRENT_SOURCE_DIR}
)