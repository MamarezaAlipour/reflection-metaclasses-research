cmake_minimum_required(VERSION 3.25)
project(ReflectionMetaclassesResearch
    VERSION 1.0.0
    DESCRIPTION "C++23 Reflection and Metaclasses Research Project"
    LANGUAGES CXX
)

# Set C++23 standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Enable testing
enable_testing()

# Compiler-specific options
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS "13.0")
        message(FATAL_ERROR "GCC 13 or higher is required for C++23 reflection support")
    endif()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -DDEBUG")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS "16.0")
        message(FATAL_ERROR "Clang 16 or higher is required for C++23 reflection support")
    endif()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -DDEBUG")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS "19.35")
        message(FATAL_ERROR "MSVC 2023 or higher is required for C++23 reflection support")
    endif()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
    set(CMAKE_CXX_FLAGS_DEBUG "/Zi /Od /DDEBUG")
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /DNDEBUG")
endif()

# Find packages
find_package(PkgConfig QUIET)

# Try to find GTest
find_package(GTest QUIET)
if(NOT GTest_FOUND)
    message(STATUS "GTest not found, building tests will be disabled")
    set(BUILD_TESTS OFF)
else()
    set(BUILD_TESTS ON)
endif()

# Try to find Google Benchmark
find_package(benchmark QUIET)
if(NOT benchmark_FOUND)
    message(STATUS "Google Benchmark not found, benchmarks will be disabled")
    set(BUILD_BENCHMARKS OFF)
else()
    set(BUILD_BENCHMARKS ON)
endif()

# Configuration options
option(BUILD_EXAMPLES "Build example programs" ON)
option(BUILD_TESTS "Build test programs" ${BUILD_TESTS})
option(BUILD_BENCHMARKS "Build benchmark programs" ${BUILD_BENCHMARKS})
option(BUILD_DOCS "Build documentation" ON)
option(ENABLE_COVERAGE "Enable code coverage" OFF)
option(ENABLE_SANITIZERS "Enable sanitizers" OFF)

# Coverage flags
if(ENABLE_COVERAGE)
    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
    endif()
endif()

# Sanitizer flags
if(ENABLE_SANITIZERS)
    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        set(SANITIZER_FLAGS "-fsanitize=address,undefined -fno-omit-frame-pointer")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${SANITIZER_FLAGS}")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${SANITIZER_FLAGS}")
    endif()
endif()

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# ================================
# Main Example Program
# ================================

add_executable(reflection_examples
    example_code.cpp
)

target_compile_features(reflection_examples PRIVATE cxx_std_23)

# Check for experimental reflection support
try_compile(HAS_REFLECTION
    ${CMAKE_BINARY_DIR}/temp
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/check_reflection.cpp
    CMAKE_FLAGS -DCMAKE_CXX_STANDARD=23
)

if(NOT HAS_REFLECTION)
    message(WARNING "Experimental reflection not available, some features may not work")
    target_compile_definitions(reflection_examples PRIVATE NO_REFLECTION)
endif()

# ================================
# Test Programs
# ================================

if(BUILD_TESTS AND GTest_FOUND)
    # Create tests directory
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/tests)
    
    # Test files
    set(TEST_SOURCES
        tests/reflection_tests.cpp
        tests/metaclass_tests.cpp
        tests/performance_tests.cpp
    )
    
    # Create test files if they don't exist
    foreach(TEST_FILE ${TEST_SOURCES})
        if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${TEST_FILE})
            file(WRITE ${CMAKE_CURRENT_SOURCE_DIR}/${TEST_FILE}
                "#include <gtest/gtest.h>\n"
                "\n"
                "// TODO: Implement tests for ${TEST_FILE}\n"
                "\n"
                "TEST(PlaceholderTest, ShouldPass) {\n"
                "    EXPECT_TRUE(true);\n"
                "}\n"
            )
        endif()
    endforeach()
    
    add_executable(run_tests ${TEST_SOURCES})
    target_link_libraries(run_tests GTest::gtest GTest::gtest_main)
    target_compile_features(run_tests PRIVATE cxx_std_23)
    
    # Register tests with CTest
    add_test(NAME ReflectionTests COMMAND run_tests)
    
    # Custom test targets
    add_custom_target(test_verbose
        COMMAND ${CMAKE_CTEST_COMMAND} --verbose
        DEPENDS run_tests
    )
endif()

# ================================
# Benchmark Programs
# ================================

if(BUILD_BENCHMARKS AND benchmark_FOUND)
    # Create benchmarks directory
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/benchmarks)
    
    # Benchmark files
    set(BENCHMARK_SOURCES
        benchmarks/compilation_time.cpp
        benchmarks/runtime_performance.cpp
        benchmarks/memory_usage.cpp
    )
    
    # Create benchmark files if they don't exist
    foreach(BENCH_FILE ${BENCHMARK_SOURCES})
        if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${BENCH_FILE})
            file(WRITE ${CMAKE_CURRENT_SOURCE_DIR}/${BENCH_FILE}
                "#include <benchmark/benchmark.h>\n"
                "\n"
                "// TODO: Implement benchmarks for ${BENCH_FILE}\n"
                "\n"
                "static void BM_Placeholder(benchmark::State& state) {\n"
                "    for (auto _ : state) {\n"
                "        // Benchmark implementation here\n"
                "        benchmark::DoNotOptimize(42);\n"
                "    }\n"
                "}\n"
                "BENCHMARK(BM_Placeholder);\n"
                "\n"
                "BENCHMARK_MAIN();\n"
            )
        endif()
    endforeach()
    
    add_executable(run_benchmarks ${BENCHMARK_SOURCES})
    target_link_libraries(run_benchmarks benchmark::benchmark benchmark::benchmark_main)
    target_compile_features(run_benchmarks PRIVATE cxx_std_23)
    
    # Custom benchmark targets
    add_custom_target(benchmark_json
        COMMAND run_benchmarks --benchmark_format=json --benchmark_out=benchmark_results.json
        DEPENDS run_benchmarks
    )
    
    add_custom_target(benchmark_all
        COMMAND run_benchmarks
        DEPENDS run_benchmarks
    )
endif()

# ================================
# Documentation
# ================================

if(BUILD_DOCS)
    find_program(PANDOC_EXECUTABLE pandoc)
    find_program(PDFLATEX_EXECUTABLE pdflatex)
    
    if(PANDOC_EXECUTABLE AND PDFLATEX_EXECUTABLE)
        set(PAPER_SOURCES
            paper_outline.md
            01_abstract_introduction.md
            02_background_related_work.md
            references.md
        )
        
        add_custom_target(docs
            COMMAND ${PANDOC_EXECUTABLE} ${PAPER_SOURCES}
                -o reflection_metaclasses_paper.pdf
                --pdf-engine=pdflatex
                --number-sections
                --toc
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            DEPENDS ${PAPER_SOURCES}
            COMMENT "Generating PDF documentation"
        )
    else()
        message(STATUS "Pandoc or PDFLaTeX not found, documentation target disabled")
    endif()
endif()

# ================================
# Installation
# ================================

install(TARGETS reflection_examples
    RUNTIME DESTINATION bin
)

if(BUILD_TESTS AND TARGET run_tests)
    install(TARGETS run_tests
        RUNTIME DESTINATION bin
    )
endif()

if(BUILD_BENCHMARKS AND TARGET run_benchmarks)
    install(TARGETS run_benchmarks
        RUNTIME DESTINATION bin
    )
endif()

# Install documentation
install(FILES
    paper_outline.md
    01_abstract_introduction.md
    02_background_related_work.md
    references.md
    DESTINATION share/doc/reflection_metaclasses
)

# ================================
# Custom Targets
# ================================

# Format code with clang-format
find_program(CLANG_FORMAT_EXECUTABLE clang-format)
if(CLANG_FORMAT_EXECUTABLE)
    file(GLOB_RECURSE ALL_CXX_SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/*.h
        ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp
    )
    
    add_custom_target(format
        COMMAND ${CLANG_FORMAT_EXECUTABLE} -i ${ALL_CXX_SOURCE_FILES}
        COMMENT "Formatting code with clang-format"
    )
endif()

# Static analysis with clang-tidy
find_program(CLANG_TIDY_EXECUTABLE clang-tidy)
if(CLANG_TIDY_EXECUTABLE)
    add_custom_target(tidy
        COMMAND ${CLANG_TIDY_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/example_code.cpp
            -- -std=c++23
        COMMENT "Running static analysis with clang-tidy"
    )
endif()

# Generate compile commands
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Coverage report
if(ENABLE_COVERAGE)
    find_program(LCOV_EXECUTABLE lcov)
    find_program(GENHTML_EXECUTABLE genhtml)
    
    if(LCOV_EXECUTABLE AND GENHTML_EXECUTABLE)
        add_custom_target(coverage
            COMMAND ${LCOV_EXECUTABLE} --capture --directory . --output-file coverage.info
            COMMAND ${GENHTML_EXECUTABLE} coverage.info --output-directory coverage_html
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
            COMMENT "Generating coverage report"
        )
    endif()
endif()

# Package creation
set(CPACK_PACKAGE_NAME "ReflectionMetaclassesResearch")
set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PROJECT_DESCRIPTION}")
set(CPACK_PACKAGE_CONTACT "research@example.com")
set(CPACK_GENERATOR "TGZ;ZIP")

include(CPack)

# ================================
# Status Report
# ================================

message(STATUS "")
message(STATUS "Configuration Summary:")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  Build Examples: ${BUILD_EXAMPLES}")
message(STATUS "  Build Tests: ${BUILD_TESTS}")
message(STATUS "  Build Benchmarks: ${BUILD_BENCHMARKS}")
message(STATUS "  Build Documentation: ${BUILD_DOCS}")
message(STATUS "  Enable Coverage: ${ENABLE_COVERAGE}")
message(STATUS "  Enable Sanitizers: ${ENABLE_SANITIZERS}")
message(STATUS "  Reflection Support: ${HAS_REFLECTION}")
message(STATUS "")
