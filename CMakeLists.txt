cmake_minimum_required(VERSION 3.10)
project(Project3)

# For LSP servers that need compile commands for auto complete
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set the C++ standard to C++14
set(CMAKE_CXX_STANDARD 14)

# Error on warnings
set(GCC_COVERAGE_COMPILE_FLAGS "-Wall -Werror")

# Find catch2 (unit testing framework)
find_package(Catch2 REQUIRED)

include_directories(src)

# Add the application executable
add_executable(Project3 src/main.cpp)

# Add the Tests executable
add_executable(Tests tests/tests.cpp)
target_link_libraries(Tests PRIVATE Catch2::Catch2WithMain)
