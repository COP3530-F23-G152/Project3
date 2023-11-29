cmake_minimum_required(VERSION 3.10)
project(Project3)

# For LSP servers that need compile commands for auto complete
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set the C++ standard to C++20
set(CMAKE_CXX_STANDARD 20)

# Error on warnings
set(GCC_COVERAGE_COMPILE_FLAGS "-Wall -Werror")

# Find catch2 (unit testing framework)
find_package(Catch2 REQUIRED)

include(FetchContent)
FetchContent_Declare(SFML
    GIT_REPOSITORY https://github.com/SFML/SFML.git
    GIT_TAG 2.6.x)
FetchContent_MakeAvailable(SFML)

include_directories(src)

# Add the application executable
add_executable(Project3 src/main.cpp)
target_link_libraries(Project3 PRIVATE sfml-graphics)
target_compile_features(Project3 PRIVATE cxx_std_20)

# Whacky windows stuffs
if(WIN32)
    add_custom_command(
        TARGET CMakeSFMLProject
        COMMENT "Copy OpenAL DLL"
        PRE_BUILD COMMAND ${CMAKE_COMMAND} -E copy ${SFML_SOURCE_DIR}/extlibs/bin/$<IF:$<EQUAL:${CMAKE_SIZEOF_VOID_P},8>,x64,x86>/openal32.dll $<TARGET_FILE_DIR:CMakeSFMLProject>
        VERBATIM)
endif()

# Add the Tests executable
add_executable(Tests tests/tests.cpp)
target_link_libraries(Tests PRIVATE Catch2::Catch2WithMain)
