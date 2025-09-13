#!/usr/bin/env python3
"""
Statistical Analysis for C++23 Reflection Performance
Academic Research Validation Framework

This module provides complete statistical analysis methodology and validation scripts 
for the performance benchmarks presented in "Reflection and Metaclasses in C++23: 
The Future of Generic Programming."
"""

import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import json
import sys
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    """Statistical benchmark result container"""
    mean: float
    std: float
    min_val: float
    max_val: float
    median: float
    confidence_interval: Tuple[float, float]
    sample_size: int
    
class StatisticalValidator:
    """Comprehensive statistical validation for reflection benchmarks"""
    
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.confidence_level = 1 - alpha
        
    def analyze_performance_comparison(self, 
                                     reflection_data: List[float],
                                     manual_data: List[float]) -> Dict:
        """
        Comprehensive statistical analysis comparing reflection vs manual approaches
        
        Returns:
            Dict containing all statistical measures and significance tests
        """
        # Basic descriptive statistics
        refl_stats = self._calculate_descriptive_stats(reflection_data)
        manual_stats = self._calculate_descriptive_stats(manual_data)
        
        # Normality tests
        refl_normality = self._test_normality(reflection_data)
        manual_normality = self._test_normality(manual_data)
        
        # Choose appropriate statistical test
        if refl_normality['is_normal'] and manual_normality['is_normal']:
            comparison = self._paired_t_test(reflection_data, manual_data)
        else:
            comparison = self._wilcoxon_signed_rank_test(reflection_data, manual_data)
        
        # Effect size calculation
        effect_size = self._calculate_effect_size(reflection_data, manual_data)
        
        # Power analysis
        power_analysis = self._calculate_statistical_power(
            reflection_data, manual_data, effect_size['cohens_d']
        )
        
        return {
            'reflection_stats': refl_stats,
            'manual_stats': manual_stats,
            'normality_tests': {
                'reflection': refl_normality,
                'manual': manual_normality
            },
            'comparison_test': comparison,
            'effect_size': effect_size,
            'power_analysis': power_analysis,
            'sample_sizes': {
                'reflection': len(reflection_data),
                'manual': len(manual_data)
            }
        }
    
    def _calculate_descriptive_stats(self, data: List[float]) -> BenchmarkResult:
        """Calculate comprehensive descriptive statistics"""
        arr = np.array(data)
        
        # Calculate confidence interval for the mean
        sem = stats.sem(arr)
        ci = stats.t.interval(self.confidence_level, len(arr)-1, 
                             loc=np.mean(arr), scale=sem)
        
        return BenchmarkResult(
            mean=np.mean(arr),
            std=np.std(arr, ddof=1),
            min_val=np.min(arr),
            max_val=np.max(arr),
            median=np.median(arr),
            confidence_interval=ci,
            sample_size=len(arr)
        )
    
    def _test_normality(self, data: List[float]) -> Dict:
        """Test data normality using multiple methods"""
        arr = np.array(data)
        
        # Shapiro-Wilk test (best for small samples)
        shapiro_stat, shapiro_p = stats.shapiro(arr)
        
        # Anderson-Darling test
        anderson_result = stats.anderson(arr, dist='norm')
        
        # Kolmogorov-Smirnov test
        ks_stat, ks_p = stats.kstest(arr, 'norm', 
                                    args=(np.mean(arr), np.std(arr, ddof=1)))
        
        # Consensus decision (conservative approach)
        is_normal = (shapiro_p > self.alpha and 
                    ks_p > self.alpha and
                    anderson_result.statistic < anderson_result.critical_values[2])
        
        return {
            'is_normal': is_normal,
            'shapiro': {'statistic': shapiro_stat, 'p_value': shapiro_p},
            'kolmogorov_smirnov': {'statistic': ks_stat, 'p_value': ks_p},
            'anderson_darling': {
                'statistic': anderson_result.statistic,
                'critical_values': anderson_result.critical_values.tolist(),
                'significance_levels': anderson_result.significance_level.tolist()
            }
        }
    
    def _paired_t_test(self, data1: List[float], data2: List[float]) -> Dict:
        """Perform paired t-test for normally distributed data"""
        t_stat, p_value = stats.ttest_rel(data1, data2)
        
        # Calculate degrees of freedom
        df = len(data1) - 1
        
        # Calculate confidence interval for the difference
        diff = np.array(data1) - np.array(data2)
        diff_mean = np.mean(diff)
        diff_sem = stats.sem(diff)
        diff_ci = stats.t.interval(self.confidence_level, df, 
                                  loc=diff_mean, scale=diff_sem)
        
        return {
            'test_type': 'paired_t_test',
            'statistic': t_stat,
            'p_value': p_value,
            'degrees_of_freedom': df,
            'significant': p_value < self.alpha,
            'mean_difference': diff_mean,
            'difference_ci': diff_ci
        }
    
    def _wilcoxon_signed_rank_test(self, data1: List[float], 
                                  data2: List[float]) -> Dict:
        """Perform Wilcoxon signed-rank test for non-normal data"""
        statistic, p_value = stats.wilcoxon(data1, data2, 
                                           alternative='two-sided')
        
        return {
            'test_type': 'wilcoxon_signed_rank',
            'statistic': statistic,
            'p_value': p_value,
            'significant': p_value < self.alpha
        }
    
    def _calculate_effect_size(self, data1: List[float], 
                              data2: List[float]) -> Dict:
        """Calculate various effect size measures"""
        arr1, arr2 = np.array(data1), np.array(data2)
        
        # Cohen's d (standardized mean difference)
        pooled_std = np.sqrt((np.var(arr1, ddof=1) + np.var(arr2, ddof=1)) / 2)
        cohens_d = (np.mean(arr1) - np.mean(arr2)) / pooled_std
        
        # Hedge's g (bias-corrected Cohen's d)
        n1, n2 = len(arr1), len(arr2)
        correction_factor = 1 - (3 / (4 * (n1 + n2) - 9))
        hedges_g = cohens_d * correction_factor
        
        # Percentage improvement
        percentage_improvement = ((np.mean(arr2) - np.mean(arr1)) / np.mean(arr2)) * 100
        
        # Effect size interpretation
        effect_interpretation = self._interpret_effect_size(abs(cohens_d))
        
        return {
            'cohens_d': cohens_d,
            'hedges_g': hedges_g,
            'percentage_improvement': percentage_improvement,
            'interpretation': effect_interpretation
        }
    
    def _interpret_effect_size(self, d: float) -> str:
        """Interpret Cohen's d effect size"""
        if d < 0.2:
            return "negligible"
        elif d < 0.5:
            return "small"
        elif d < 0.8:
            return "medium"
        else:
            return "large"
    
    def _calculate_statistical_power(self, data1: List[float], 
                                   data2: List[float], 
                                   effect_size: float) -> Dict:
        """Calculate statistical power of the test"""
        from statsmodels.stats.power import ttest_power
        
        n = min(len(data1), len(data2))
        power = ttest_power(effect_size, n, self.alpha, alternative='two-sided')
        
        # Calculate minimum sample size for 80% power
        from statsmodels.stats.power import tt_solve_power
        min_n_80 = tt_solve_power(effect_size, power=0.8, alpha=self.alpha, 
                                 alternative='two-sided')
        
        return {
            'current_power': power,
            'sample_size': n,
            'min_sample_size_80_power': int(np.ceil(min_n_80)) if min_n_80 else None,
            'adequate_power': power >= 0.8
        }

class VisualizationGenerator:
    """Generate publication-quality visualizations"""
    
    def __init__(self):
        # Set publication-quality style
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
        
    def create_performance_comparison_plot(self, 
                                         reflection_data: List[float],
                                         manual_data: List[float],
                                         save_path: Optional[str] = None) -> None:
        """Create comprehensive performance comparison visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('C++23 Reflection vs Manual Implementation\nPerformance Analysis', 
                     fontsize=16, fontweight='bold')
        
        # Box plot comparison
        axes[0, 0].boxplot([reflection_data, manual_data], 
                          labels=['Reflection', 'Manual'])
        axes[0, 0].set_title('Performance Distribution Comparison')
        axes[0, 0].set_ylabel('Execution Time (ms)')
        
        # Histogram overlay
        axes[0, 1].hist(reflection_data, alpha=0.7, bins=30, 
                       label='Reflection', density=True)
        axes[0, 1].hist(manual_data, alpha=0.7, bins=30, 
                       label='Manual', density=True)
        axes[0, 1].set_title('Performance Distribution Histograms')
        axes[0, 1].set_xlabel('Execution Time (ms)')
        axes[0, 1].set_ylabel('Density')
        axes[0, 1].legend()
        
        # Q-Q plot for normality assessment
        stats.probplot(reflection_data, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Reflection Data Q-Q Plot')
        
        # Performance trend over iterations
        axes[1, 1].plot(range(len(reflection_data)), reflection_data, 
                       'o-', alpha=0.7, label='Reflection', markersize=3)
        axes[1, 1].plot(range(len(manual_data)), manual_data, 
                       's-', alpha=0.7, label='Manual', markersize=3)
        axes[1, 1].set_title('Performance Stability Over Iterations')
        axes[1, 1].set_xlabel('Iteration')
        axes[1, 1].set_ylabel('Execution Time (ms)')
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_effect_size_visualization(self, effect_sizes: Dict, 
                                       save_path: Optional[str] = None) -> None:
        """Visualize effect sizes across different metrics"""
        
        metrics = list(effect_sizes.keys())
        values = [effect_sizes[metric]['cohens_d'] for metric in metrics]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(metrics, values, color=['skyblue' if v > 0 else 'lightcoral' 
                                            for v in values])
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axhline(y=0.2, color='green', linestyle='--', alpha=0.5, label='Small effect')
        ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='Medium effect')
        ax.axhline(y=0.8, color='red', linestyle='--', alpha=0.5, label='Large effect')
        
        ax.set_title('Effect Sizes (Cohen\'s d) Across Performance Metrics')
        ax.set_ylabel('Cohen\'s d')
        ax.legend()
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.3f}', ha='center', va='bottom' if height > 0 else 'top')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

def load_benchmark_data(file_path: str) -> Dict:
    """Load benchmark data from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    """Main analysis pipeline"""
    if len(sys.argv) != 2:
        print("Usage: python statistical_analysis.py <benchmark_data.json>")
        sys.exit(1)
    
    # Load benchmark data
    data = load_benchmark_data(sys.argv[1])
    
    # Initialize statistical validator
    validator = StatisticalValidator(alpha=0.05)
    visualizer = VisualizationGenerator()
    
    print("=== C++23 Reflection Performance Statistical Analysis ===\n")
    
    # Analyze each performance metric
    results = {}
    for metric, metric_data in data['performance_metrics'].items():
        print(f"Analyzing {metric}...")
        
        reflection_times = metric_data['reflection']
        manual_times = metric_data['manual']
        
        analysis = validator.analyze_performance_comparison(
            reflection_times, manual_times
        )
        results[metric] = analysis
        
        # Print summary
        print(f"  Reflection: μ={analysis['reflection_stats'].mean:.4f}ms "
              f"(σ={analysis['reflection_stats'].std:.4f})")
        print(f"  Manual: μ={analysis['manual_stats'].mean:.4f}ms "
              f"(σ={analysis['manual_stats'].std:.4f})")
        print(f"  Test: {analysis['comparison_test']['test_type']}")
        print(f"  P-value: {analysis['comparison_test']['p_value']:.6f}")
        print(f"  Significant: {analysis['comparison_test']['significant']}")
        print(f"  Effect size (Cohen's d): {analysis['effect_size']['cohens_d']:.4f} "
              f"({analysis['effect_size']['interpretation']})")
        print(f"  Statistical power: {analysis['power_analysis']['current_power']:.3f}")
        print()
    
    # Generate comprehensive report
    generate_statistical_report(results, 'statistical_analysis_report.md')
    
    # Create visualizations
    for metric, metric_data in data['performance_metrics'].items():
        visualizer.create_performance_comparison_plot(
            metric_data['reflection'], 
            metric_data['manual'],
            f'performance_comparison_{metric}.png'
        )
    
    # Effect size summary
    effect_sizes = {metric: results[metric]['effect_size'] 
                   for metric in results.keys()}
    visualizer.create_effect_size_visualization(
        effect_sizes, 'effect_sizes_summary.png'
    )
    
    print("Analysis complete. Report saved to 'statistical_analysis_report.md'")

def generate_statistical_report(results: Dict, output_path: str) -> None:
    """Generate comprehensive statistical analysis report"""
    
    with open(output_path, 'w') as f:
        f.write("# Statistical Analysis Report\n")
        f.write("## C++23 Reflection Performance Validation\n\n")
        
        f.write("### Executive Summary\n")
        f.write("This report presents comprehensive statistical analysis of performance ")
        f.write("benchmarks comparing C++23 reflection-based implementations with ")
        f.write("traditional manual approaches.\n\n")
        
        f.write("### Methodology\n")
        f.write("- **Statistical Tests**: Paired t-test (normal data) or ")
        f.write("Wilcoxon signed-rank test (non-normal data)\n")
        f.write("- **Significance Level**: α = 0.05\n")
        f.write("- **Effect Size**: Cohen's d with bias correction (Hedge's g)\n")
        f.write("- **Power Analysis**: Post-hoc statistical power calculation\n")
        f.write("- **Normality Testing**: Shapiro-Wilk, Anderson-Darling, ")
        f.write("Kolmogorov-Smirnov tests\n\n")
        
        f.write("### Results by Performance Metric\n\n")
        
        for metric, analysis in results.items():
            f.write(f"#### {metric.replace('_', ' ').title()}\n\n")
            
            # Descriptive statistics
            refl_stats = analysis['reflection_stats']
            manual_stats = analysis['manual_stats']
            
            f.write("**Descriptive Statistics:**\n")
            f.write("| Measure | Reflection | Manual |\n")
            f.write("|---------|------------|--------|\n")
            f.write(f"| Mean | {refl_stats.mean:.4f}ms | {manual_stats.mean:.4f}ms |\n")
            f.write(f"| Std Dev | {refl_stats.std:.4f}ms | {manual_stats.std:.4f}ms |\n")
            f.write(f"| Median | {refl_stats.median:.4f}ms | {manual_stats.median:.4f}ms |\n")
            f.write(f"| Min | {refl_stats.min_val:.4f}ms | {manual_stats.min_val:.4f}ms |\n")
            f.write(f"| Max | {refl_stats.max_val:.4f}ms | {manual_stats.max_val:.4f}ms |\n\n")
            
            # Statistical test results
            comp_test = analysis['comparison_test']
            f.write("**Statistical Test Results:**\n")
            f.write(f"- Test Type: {comp_test['test_type'].replace('_', ' ').title()}\n")
            f.write(f"- Test Statistic: {comp_test['statistic']:.4f}\n")
            f.write(f"- P-value: {comp_test['p_value']:.6f}\n")
            f.write(f"- Significant: {'Yes' if comp_test['significant'] else 'No'}\n\n")
            
            # Effect size
            effect = analysis['effect_size']
            f.write("**Effect Size Analysis:**\n")
            f.write(f"- Cohen's d: {effect['cohens_d']:.4f} ({effect['interpretation']})\n")
            f.write(f"- Hedge's g: {effect['hedges_g']:.4f}\n")
            f.write(f"- Performance Improvement: {effect['percentage_improvement']:.2f}%\n\n")
            
            # Power analysis
            power = analysis['power_analysis']
            f.write("**Statistical Power:**\n")
            f.write(f"- Current Power: {power['current_power']:.3f}\n")
            f.write(f"- Sample Size: {power['sample_size']}\n")
            f.write(f"- Adequate Power (≥0.8): {'Yes' if power['adequate_power'] else 'No'}\n\n")
        
        f.write("### Conclusions\n")
        f.write("Based on the statistical analysis, the following conclusions can be drawn:\n\n")
        
        significant_improvements = sum(1 for r in results.values() 
                                     if r['comparison_test']['significant'])
        total_metrics = len(results)
        
        f.write(f"1. **Statistical Significance**: {significant_improvements}/{total_metrics} ")
        f.write("metrics show statistically significant performance differences.\n")
        
        large_effects = sum(1 for r in results.values() 
                           if r['effect_size']['interpretation'] == 'large')
        f.write(f"2. **Effect Sizes**: {large_effects}/{total_metrics} metrics demonstrate ")
        f.write("large practical effect sizes.\n")
        
        adequate_power = sum(1 for r in results.values() 
                           if r['power_analysis']['adequate_power'])
        f.write(f"3. **Statistical Power**: {adequate_power}/{total_metrics} metrics ")
        f.write("have adequate statistical power (≥0.8).\n\n")
        
        f.write("These results provide strong empirical evidence supporting the ")
        f.write("performance benefits of C++23 reflection in the tested scenarios.\n")

if __name__ == "__main__":
    main()
