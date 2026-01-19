"""
performance_utils.py

Performance profiling and monitoring utilities for the Android Forensic Tool.
Provides decorators and functions for timing, profiling, and performance analysis.
"""

import time
import cProfile
import pstats
import io
import functools
from datetime import datetime


def timer(func):
    """
    Decorator to measure execution time of a function.
    
    Usage:
        @timer
        def my_function():
            # code here
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"⏱️  {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper


def profile(output_file=None):
    """
    Decorator to profile a function with cProfile.
    
    Usage:
        @profile("output.prof")
        def my_function():
            # code here
    
    Args:
        output_file: Optional file to save profiling stats
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            
            result = func(*args, **kwargs)
            
            profiler.disable()
            
            # Print stats to console
            s = io.StringIO()
            ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
            ps.print_stats(20)  # Top 20 functions
            print(f"\n📊 Profile for {func.__name__}:")
            print(s.getvalue())
            
            # Save to file if requested
            if output_file:
                profiler.dump_stats(output_file)
                print(f"💾 Profile saved to {output_file}")
            
            return result
        return wrapper
    return decorator


class PerformanceMonitor:
    """
    Context manager for monitoring performance of code blocks.
    
    Usage:
        with PerformanceMonitor("Log Extraction"):
            # code to monitor
    """
    
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        print(f"🚀 Starting: {self.operation_name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"✅ Completed: {self.operation_name} in {elapsed:.4f} seconds")
        return False
    
    def elapsed(self):
        """Get elapsed time."""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time


def run_performance_test(func, iterations=100, *args, **kwargs):
    """
    Run a function multiple times and collect performance statistics.
    
    Args:
        func: Function to test
        iterations: Number of times to run
        *args, **kwargs: Arguments to pass to function
    
    Returns:
        dict with min, max, mean, median times
    """
    times = []
    
    print(f"🔬 Running performance test: {func.__name__} ({iterations} iterations)")
    
    for i in range(iterations):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        times.append(end - start)
    
    times.sort()
    mean_time = sum(times) / len(times)
    median_time = times[len(times) // 2]
    min_time = times[0]
    max_time = times[-1]
    
    stats = {
        'min': min_time,
        'max': max_time,
        'mean': mean_time,
        'median': median_time,
        'iterations': iterations
    }
    
    print(f"📈 Results for {func.__name__}:")
    print(f"   Min:    {min_time:.4f}s")
    print(f"   Max:    {max_time:.4f}s")
    print(f"   Mean:   {mean_time:.4f}s")
    print(f"   Median: {median_time:.4f}s")
    
    return stats


def benchmark_comparison(func1, func2, iterations=100, *args, **kwargs):
    """
    Compare performance of two functions.
    
    Args:
        func1: First function
        func2: Second function
        iterations: Number of iterations
        *args, **kwargs: Arguments for both functions
    
    Returns:
        dict with comparison results
    """
    print(f"⚔️  Benchmarking: {func1.__name__} vs {func2.__name__}")
    
    stats1 = run_performance_test(func1, iterations, *args, **kwargs)
    stats2 = run_performance_test(func2, iterations, *args, **kwargs)
    
    improvement = ((stats1['mean'] - stats2['mean']) / stats1['mean']) * 100
    
    print(f"\n🏆 Comparison:")
    if improvement > 0:
        print(f"   {func2.__name__} is {improvement:.1f}% faster")
    else:
        print(f"   {func1.__name__} is {abs(improvement):.1f}% faster")
    
    return {
        'func1': stats1,
        'func2': stats2,
        'improvement_percent': improvement
    }


def generate_performance_report(log_file="performance_report.txt"):
    """
    Generate a performance report from profiling data.
    
    Args:
        log_file: File to save the report
    """
    with open(log_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("Android Forensic Tool - Performance Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write("Use @timer and @profile decorators to collect data.\n")
    
    print(f"📄 Performance report template created: {log_file}")


if __name__ == '__main__':
    # Example usage
    print("Performance Utils - Example Usage\n")
    
    @timer
    def example_function():
        time.sleep(0.1)
        return "Done"
    
    # Test timer decorator
    result = example_function()
    
    # Test context manager
    with PerformanceMonitor("Example Operation"):
        time.sleep(0.05)
    
    print("\n✅ Performance utils ready to use!")
