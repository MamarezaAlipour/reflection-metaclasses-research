# Makefile for C++23 Reflection and Metaclasses Research Paper Examples
# Requires GCC 13+, Clang 16+, or MSVC 2023+ with C++23 support

CXX = g++
CXXFLAGS = -std=c++23 -Wall -Wextra -O2 -g
LDFLAGS = 

# Alternative compilers
CXX_CLANG = clang++
CXX_MSVC = cl.exe

# Source files
SOURCES = example_code.cpp
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = reflection_examples

# Test files
TEST_SOURCES = tests/reflection_tests.cpp tests/metaclass_tests.cpp tests/performance_tests.cpp
TEST_OBJECTS = $(TEST_SOURCES:.cpp=.o)
TEST_TARGET = run_tests

# Benchmark files
BENCH_SOURCES = benchmarks/compilation_time.cpp benchmarks/runtime_performance.cpp
BENCH_OBJECTS = $(BENCH_SOURCES:.cpp=.o)
BENCH_TARGET = run_benchmarks

# Documentation
DOCS = paper_outline.md references.md 01_abstract_introduction.md 02_background_related_work.md
PDF_TARGET = reflection_metaclasses_paper.pdf

.PHONY: all clean test benchmark docs help install-deps

all: $(TARGET) $(TEST_TARGET) $(BENCH_TARGET)

# Main example compilation
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Test compilation and execution
test: $(TEST_TARGET)
	./$(TEST_TARGET)

$(TEST_TARGET): $(TEST_OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS) -lgtest -lgtest_main

# Benchmark compilation and execution
benchmark: $(BENCH_TARGET)
	./$(BENCH_TARGET)

$(BENCH_TARGET): $(BENCH_OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS) -lbenchmark -lbenchmark_main

# Multi-compiler testing
test-all-compilers: test-gcc test-clang test-msvc

test-gcc:
	@echo "Testing with GCC..."
	$(MAKE) CXX=g++ CXXFLAGS="-std=c++23 -Wall -Wextra -O2" all
	
test-clang:
	@echo "Testing with Clang..."
	$(MAKE) CXX=clang++ CXXFLAGS="-std=c++23 -Wall -Wextra -O2" all

test-msvc:
	@echo "Testing with MSVC..."
	cl.exe /std:c++23 /EHsc $(SOURCES) /Fe:$(TARGET).exe

# Performance profiling
profile: $(TARGET)
	perf record -g ./$(TARGET)
	perf report

# Memory analysis
valgrind: $(TARGET)
	valgrind --tool=memcheck --leak-check=full ./$(TARGET)

# Code coverage
coverage: CXXFLAGS += --coverage
coverage: LDFLAGS += --coverage
coverage: test
	gcov $(SOURCES)
	lcov --capture --directory . --output-file coverage.info
	genhtml coverage.info --output-directory coverage_html

# Documentation generation
docs: $(PDF_TARGET)

$(PDF_TARGET): $(DOCS)
	pandoc $(DOCS) -o $@ \
		--pdf-engine=xelatex \
		--template=ieee_template.tex \
		--number-sections \
		--toc \
		--bibliography=references.bib \
		--csl=ieee.csl

# Install dependencies (Ubuntu/Debian)
install-deps:
	sudo apt-get update
	sudo apt-get install -y \
		gcc-13 g++-13 \
		clang-16 \
		libgtest-dev \
		libbenchmark-dev \
		valgrind \
		lcov \
		pandoc \
		texlive-xetex \
		texlive-latex-extra

# Install dependencies (Windows with vcpkg)
install-deps-windows:
	vcpkg install gtest:x64-windows
	vcpkg install benchmark:x64-windows

# Clean build artifacts
clean:
	rm -f $(OBJECTS) $(TEST_OBJECTS) $(BENCH_OBJECTS)
	rm -f $(TARGET) $(TEST_TARGET) $(BENCH_TARGET)
	rm -f *.gcov *.gcda *.gcno coverage.info
	rm -rf coverage_html
	rm -f $(PDF_TARGET)

# Static analysis
static-analysis:
	clang-static-analyzer $(CXXFLAGS) $(SOURCES)
	cppcheck --enable=all --std=c++23 $(SOURCES)

# Format code
format:
	clang-format -i $(SOURCES) $(TEST_SOURCES) $(BENCH_SOURCES)

# Lint code
lint:
	clang-tidy $(SOURCES) -- $(CXXFLAGS)

# Generate compilation database
compile-commands:
	bear -- make all

# Help target
help:
	@echo "Available targets:"
	@echo "  all                 - Build all targets"
	@echo "  test               - Build and run tests"
	@echo "  benchmark          - Build and run benchmarks"
	@echo "  test-all-compilers - Test with GCC, Clang, and MSVC"
	@echo "  profile            - Profile with perf"
	@echo "  valgrind           - Memory analysis with valgrind"
	@echo "  coverage           - Generate code coverage report"
	@echo "  docs               - Generate PDF documentation"
	@echo "  install-deps       - Install required dependencies (Linux)"
	@echo "  install-deps-windows - Install dependencies (Windows)"
	@echo "  static-analysis    - Run static analysis tools"
	@echo "  format             - Format code with clang-format"
	@echo "  lint               - Lint code with clang-tidy"
	@echo "  compile-commands   - Generate compile_commands.json"
	@echo "  clean              - Remove build artifacts"
	@echo "  help               - Show this help message"

# Compiler feature detection
check-cpp23-support:
	@echo "Checking C++23 support..."
	@echo "GCC version:"
	@g++ --version | head -1
	@echo "Clang version:"
	@clang++ --version | head -1
	@echo "Testing reflection support..."
	@echo '#include <experimental/reflect>' > test_reflect.cpp
	@echo 'int main() { return 0; }' >> test_reflect.cpp
	@if $(CXX) $(CXXFLAGS) test_reflect.cpp -o test_reflect 2>/dev/null; then \
		echo "✓ Reflection support detected"; \
	else \
		echo "✗ Reflection support not available"; \
	fi
	@rm -f test_reflect.cpp test_reflect

# Research data collection
collect-data: benchmark
	@mkdir -p research_data
	@echo "Collecting compilation time data..."
	@time $(MAKE) clean all 2>&1 | tee research_data/compilation_times.log
	@echo "Collecting binary size data..."
	@ls -la $(TARGET) > research_data/binary_sizes.log
	@echo "Collecting benchmark results..."
	@./$(BENCH_TARGET) --benchmark_format=json > research_data/benchmark_results.json

# Generate research plots
plots: collect-data
	python3 scripts/generate_plots.py research_data/

# Package for submission
package:
	@mkdir -p submission
	@cp *.md submission/
	@cp $(PDF_TARGET) submission/
	@cp -r research_data submission/ 2>/dev/null || true
	@tar -czf reflection_metaclasses_submission.tar.gz submission/
	@echo "Submission package created: reflection_metaclasses_submission.tar.gz"

# Continuous integration target
ci: install-deps test-all-compilers static-analysis coverage docs package

# Development environment setup
dev-setup: install-deps compile-commands
	@echo "Development environment setup complete"
	@echo "Run 'make help' to see available targets"
