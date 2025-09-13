"""
Benchmark Runner and Analysis Tool
==================================

This script compiles and runs the C++ benchmark tests, collecting performance data
for comparison between reflection-based and traditional C++ approaches.

Author: Mohammadreza Alipour
Date: August 24, 2025
"""

import subprocess
import time
import os
import json
import statistics
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

@dataclass
class BenchmarkResult:
    name: str
    compilation_time: float
    execution_time: float
    binary_size: int
    output: str
    success: bool

class BenchmarkRunner:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.benchmark_dir = self.project_root / "benchmarks"
        self.results_dir = self.project_root / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Try to find available compilers
        self.available_compilers = self._detect_compilers()
        
    def _detect_compilers(self):
        """Detect available C++ compilers on the system."""
        compilers = {}
        
        # Test for GCC
        try:
            result = subprocess.run(["g++", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                compilers["gcc"] = {
                    "command": "g++",
                    "flags": ["-std=c++20", "-O2", "-Wall", "-Wextra"]  # Using C++20 for now
                }
        except:
            pass
            
        # Test for Clang
        try:
            result = subprocess.run(["clang++", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                compilers["clang"] = {
                    "command": "clang++",
                    "flags": ["-std=c++20", "-O2", "-Wall", "-Wextra"]
                }
        except:
            pass
            
        # Test for MSVC (Windows)
        try:
            result = subprocess.run(["cl", "/?"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                compilers["msvc"] = {
                    "command": "cl",
                    "flags": ["/std:c++20", "/O2", "/EHsc"]
                }
        except:
            pass
            
        return compilers
    
    def compile_benchmark(self, source_file: str, compiler: str = None) -> BenchmarkResult:
        """Compile a single benchmark file and measure compilation time."""
        
        if not compiler:
            compiler = list(self.available_compilers.keys())[0] if self.available_compilers else None
            
        if not compiler or compiler not in self.available_compilers:
            return BenchmarkResult(
                name=source_file,
                compilation_time=0,
                execution_time=0,
                binary_size=0,
                output="No suitable compiler found",
                success=False
            )
        
        compiler_config = self.available_compilers[compiler]
        source_path = self.benchmark_dir / source_file
        output_name = source_file.replace('.cpp', '.exe' if os.name == 'nt' else '')
        output_path = self.benchmark_dir / output_name
        
        # Build compilation command
        cmd = [compiler_config["command"]] + compiler_config["flags"] + [
            str(source_path), "-o", str(output_path)
        ]
        
        print(f"Compiling {source_file} with {compiler}...")
        
        # Measure compilation time
        start_time = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            compilation_time = time.time() - start_time
            
            if result.returncode == 0:
                # Get binary size
                binary_size = output_path.stat().st_size if output_path.exists() else 0
                
                return BenchmarkResult(
                    name=source_file,
                    compilation_time=compilation_time,
                    execution_time=0,  # Will be filled by run_benchmark
                    binary_size=binary_size,
                    output=result.stdout + result.stderr,
                    success=True
                )
            else:
                return BenchmarkResult(
                    name=source_file,
                    compilation_time=compilation_time,
                    execution_time=0,
                    binary_size=0,
                    output=f"Compilation failed:\\n{result.stderr}",
                    success=False
                )
                
        except subprocess.TimeoutExpired:
            return BenchmarkResult(
                name=source_file,
                compilation_time=30.0,  # Timeout
                execution_time=0,
                binary_size=0,
                output="Compilation timeout",
                success=False
            )
        except Exception as e:
            return BenchmarkResult(
                name=source_file,
                compilation_time=0,
                execution_time=0,
                binary_size=0,
                output=f"Compilation error: {str(e)}",
                success=False
            )
    
    def run_benchmark(self, executable_name: str) -> Tuple[float, str]:
        """Run a compiled benchmark and measure execution time."""
        
        executable_path = self.benchmark_dir / executable_name
        
        if not executable_path.exists():
            return 0.0, f"Executable {executable_name} not found"
        
        print(f"Running {executable_name}...")
        
        try:
            start_time = time.time()
            result = subprocess.run([str(executable_path)], 
                                  capture_output=True, text=True, timeout=10)
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                return execution_time, result.stdout
            else:
                return execution_time, f"Runtime error:\\n{result.stderr}"
                
        except subprocess.TimeoutExpired:
            return 10.0, "Execution timeout"
        except Exception as e:
            return 0.0, f"Execution error: {str(e)}"
    
    def run_all_benchmarks(self) -> Dict[str, List[BenchmarkResult]]:
        """Run all benchmark pairs and collect results."""
        
        benchmark_pairs = [
            ("serialization_reflection.cpp", "serialization_traditional.cpp"),
            ("orm_reflection.cpp", "orm_traditional.cpp"),
            ("binding_reflection.cpp", "binding_traditional.cpp"),
            ("pattern_reflection.cpp", "pattern_traditional.cpp"),
            ("template_reflection.cpp", "template_traditional.cpp")
        ]
        
        results = {}
        
        for reflection_file, traditional_file in benchmark_pairs:
            pair_name = reflection_file.replace("_reflection.cpp", "")
            results[pair_name] = []
            
            print(f"\\n=== Benchmarking {pair_name} ===")
            
            # Compile and run reflection version
            reflection_result = self.compile_benchmark(reflection_file)
            if reflection_result.success:
                exec_time, output = self.run_benchmark(
                    reflection_file.replace('.cpp', '.exe' if os.name == 'nt' else '')
                )
                reflection_result.execution_time = exec_time
                reflection_result.output += "\\n" + output
            
            results[pair_name].append(reflection_result)
            
            # Compile and run traditional version  
            traditional_result = self.compile_benchmark(traditional_file)
            if traditional_result.success:
                exec_time, output = self.run_benchmark(
                    traditional_file.replace('.cpp', '.exe' if os.name == 'nt' else '')
                )
                traditional_result.execution_time = exec_time
                traditional_result.output += "\\n" + output
            
            results[pair_name].append(traditional_result)
        
        return results
    
    def analyze_results(self, results: Dict[str, List[BenchmarkResult]]) -> Dict:
        """Analyze benchmark results and compute comparisons."""
        
        analysis = {
            "summary": {},
            "detailed_results": results,
            "compiler_info": self.available_compilers
        }
        
        for pair_name, pair_results in results.items():
            if len(pair_results) >= 2:
                reflection_result = pair_results[0]
                traditional_result = pair_results[1]
                
                if reflection_result.success and traditional_result.success:
                    # Calculate speedups and ratios
                    compilation_speedup = (traditional_result.compilation_time / 
                                         reflection_result.compilation_time 
                                         if reflection_result.compilation_time > 0 else float('inf'))
                    
                    execution_speedup = (traditional_result.execution_time / 
                                       reflection_result.execution_time 
                                       if reflection_result.execution_time > 0 else float('inf'))
                    
                    size_ratio = (reflection_result.binary_size / 
                                traditional_result.binary_size 
                                if traditional_result.binary_size > 0 else float('inf'))
                    
                    analysis["summary"][pair_name] = {
                        "compilation_speedup": compilation_speedup,
                        "execution_speedup": execution_speedup,
                        "size_ratio": size_ratio,
                        "reflection_compile_time": reflection_result.compilation_time,
                        "traditional_compile_time": traditional_result.compilation_time,
                        "reflection_execution_time": reflection_result.execution_time,
                        "traditional_execution_time": traditional_result.execution_time,
                        "reflection_binary_size": reflection_result.binary_size,
                        "traditional_binary_size": traditional_result.binary_size
                    }
                else:
                    analysis["summary"][pair_name] = {
                        "error": "One or both benchmarks failed",
                        "reflection_success": reflection_result.success,
                        "traditional_success": traditional_result.success
                    }
        
        return analysis
    
    def save_results(self, analysis: Dict, filename: str = "benchmark_results.json"):
        """Save analysis results to JSON file."""
        
        results_file = self.results_dir / filename
        
        # Convert dataclasses to dicts for JSON serialization
        serializable_analysis = {}
        for key, value in analysis.items():
            if key == "detailed_results":
                serializable_analysis[key] = {}
                for pair_name, pair_results in value.items():
                    serializable_analysis[key][pair_name] = [
                        asdict(result) for result in pair_results
                    ]
            else:
                serializable_analysis[key] = value
        
        with open(results_file, 'w') as f:
            json.dump(serializable_analysis, f, indent=2)
        
        print(f"\\nResults saved to {results_file}")
    
    def print_summary(self, analysis: Dict):
        """Print a summary of benchmark results."""
        
        print("\\n" + "="*60)
        print("BENCHMARK RESULTS SUMMARY")
        print("="*60)
        
        if not self.available_compilers:
            print("❌ No C++ compilers detected on this system")
            print("Please install GCC, Clang, or MSVC to run benchmarks")
            return
        
        print(f"Compilers detected: {list(self.available_compilers.keys())}")
        print("")
        
        summary = analysis.get("summary", {})
        
        for pair_name, metrics in summary.items():
            print(f"📊 {pair_name.upper()} BENCHMARK:")
            
            if "error" in metrics:
                print(f"   ❌ {metrics['error']}")
                continue
            
            print(f"   Compilation Time:")
            print(f"     Reflection: {metrics['reflection_compile_time']:.3f}s")
            print(f"     Traditional: {metrics['traditional_compile_time']:.3f}s")
            print(f"     Speedup: {metrics['compilation_speedup']:.2f}x")
            
            print(f"   Execution Time:")
            print(f"     Reflection: {metrics['reflection_execution_time']:.3f}s")
            print(f"     Traditional: {metrics['traditional_execution_time']:.3f}s")
            print(f"     Speedup: {metrics['execution_speedup']:.2f}x")
            
            print(f"   Binary Size:")
            print(f"     Reflection: {metrics['reflection_binary_size']:,} bytes")
            print(f"     Traditional: {metrics['traditional_binary_size']:,} bytes") 
            print(f"     Size Ratio: {metrics['size_ratio']:.2f}x")
            print("")

def main():
    """Main function to run all benchmarks and generate results."""
    
    print("🚀 C++23 Reflection vs Traditional Approaches Benchmark")
    print("=" * 60)
    
    # Initialize benchmark runner
    runner = BenchmarkRunner("C:/Users/P - K/Downloads/cpp prop/reflection_metaclasses_paper/implementation")
    
    if not runner.available_compilers:
        print("❌ No C++ compilers found. Please install GCC, Clang, or MSVC.")
        return
    
    print(f"✅ Found compilers: {list(runner.available_compilers.keys())}")
    
    # Run all benchmarks
    print("\\n🔄 Running benchmarks...")
    results = runner.run_all_benchmarks()
    
    # Analyze results
    print("\\n📊 Analyzing results...")
    analysis = runner.analyze_results(results)
    
    # Print summary
    runner.print_summary(analysis)
    
    # Save results
    runner.save_results(analysis)
    
    print("\\n✅ Benchmark completed successfully!")

if __name__ == "__main__":
    main()
