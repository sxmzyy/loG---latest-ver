"""
numpy_analyzer.py

NumPy-based log analysis module for high-performance operations.
Provides vectorized operations for timestamp analysis, frequency counting, 
and statistical analysis of large log files.
"""

try:
    import numpy as np
    import pandas as pd
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  NumPy/Pandas not available. Install with: pip install numpy pandas")

from datetime import datetime, timedelta
import re
from collections import Counter


def is_available():
    """Check if NumPy is available."""
    return NUMPY_AVAILABLE


def parse_timestamps_vectorized(log_lines, pattern=r'(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'):
    """
    Parse timestamps from log lines using vectorized operations.
    
    Args:
        log_lines: List of log line strings
        pattern: Regex pattern for timestamp matching
    
    Returns:
        numpy array of datetime objects (or None if NumPy unavailable)
    """
    if not NUMPY_AVAILABLE:
        return None
    
    timestamps = []
    current_year = datetime.now().year
    
    for line in log_lines:
        match = re.search(pattern, line)
        if match:
            try:
                ts_str = match.group(1)
                ts = datetime.strptime(f"{current_year}-{ts_str}", "%Y-%m-%d %H:%M:%S")
                
                # Handle year rollover
                if ts > datetime.now():
                    ts = ts.replace(year=current_year - 1)
                
                timestamps.append(ts)
            except:
                timestamps.append(None)
        else:
            timestamps.append(None)
    
    return np.array(timestamps, dtype='datetime64[s]')


def time_series_binning(timestamps, bin_size='1H'):
    """
    Bin timestamps into time intervals for time-series visualization.
    Much faster than Python loops for large datasets.
    
    Args:
        timestamps: numpy array of timestamps
        bin_size: Pandas frequency string ('1H', '30T', '1D', etc.)
    
    Returns:
        tuple: (bin_edges, counts)
    """
    if not NUMPY_AVAILABLE or timestamps is None:
        return None, None
    
    # Convert to pandas Series for easy binning
    ts_series = pd.Series(1, index=pd.to_datetime(timestamps))
    
    # Resample and count
    binned = ts_series.resample(bin_size).count()
    
    return binned.index.to_numpy(), binned.values


def frequency_analysis_vectorized(items):
    """
    Fast frequency analysis using NumPy.
    
    Args:
        items: List of items to count
    
    Returns:
        tuple: (unique_items, counts) sorted by frequency
    """
    if not NUMPY_AVAILABLE:
        # Fallback to Counter
        counter = Counter(items)
        items, counts = zip(*counter.most_common())
        return np.array(items), np.array(counts)
    
    unique, counts = np.unique(items, return_counts=True)
    
    # Sort by frequency (descending)
    sorted_indices = np.argsort(counts)[::-1]
    
    return unique[sorted_indices], counts[sorted_indices]


def statistical_analysis(values):
    """
    Compute statistical metrics on numeric values.
    
    Args:
        values: List or numpy array of numeric values
    
    Returns:
        dict with mean, median, std, min, max, percentiles
    """
    if not NUMPY_AVAILABLE:
        return {
            'error': 'NumPy not available',
            'mean': sum(values) / len(values) if values else 0,
            'min': min(values) if values else 0,
            'max': max(values) if values else 0
        }
    
    arr = np.array(values, dtype=float)
    
    return {
        'mean': np.mean(arr),
        'median': np.median(arr),
        'std': np.std(arr),
        'min': np.min(arr),
        'max': np.max(arr),
        'p25': np.percentile(arr, 25),
        'p75': np.percentile(arr, 75),
        'p95': np.percentile(arr, 95),
        'count': len(arr)
    }


def detect_outliers(values, threshold=3.0):
    """
    Detect outliers using Z-score method.
    
    Args:
        values: List or numpy array of numeric values
        threshold: Z-score threshold (default: 3.0)
    
    Returns:
        tuple: (outlier_indices, outlier_values)
    """
    if not NUMPY_AVAILABLE:
        return [], []
    
    arr = np.array(values, dtype=float)
    
    # Calculate Z-scores
    mean = np.mean(arr)
    std = np.std(arr)
    
    if std == 0:
        return [], []
    
    z_scores = np.abs((arr - mean) / std)
    
    # Find outliers
    outlier_mask = z_scores > threshold
    outlier_indices = np.where(outlier_mask)[0]
    outlier_values = arr[outlier_mask]
    
    return outlier_indices.tolist(), outlier_values.tolist()


def time_range_filter(timestamps, values, start_time=None, end_time=None):
    """
    Filter values by time range using vectorized operations.
    
    Args:
        timestamps: numpy array of datetime objects
        values: corresponding values
        start_time: datetime object (or None for no lower bound)
        end_time: datetime object (or None for no upper bound)
    
    Returns:
        tuple: (filtered_timestamps, filtered_values)
    """
    if not NUMPY_AVAILABLE:
        return timestamps, values
    
    ts_arr = np.array(timestamps, dtype='datetime64[s]')
    val_arr = np.array(values)
    
    mask = np.ones(len(ts_arr), dtype=bool)
    
    if start_time:
        start_np = np.datetime64(start_time, 's')
        mask &= (ts_arr >= start_np)
    
    if end_time:
        end_np = np.datetime64(end_time, 's')
        mask &= (ts_arr <= end_np)
    
    return ts_arr[mask], val_arr[mask]


def rolling_average(values, window_size=10):
    """
    Calculate rolling average for smoothing time series data.
    
    Args:
        values: List or numpy array of numeric values
        window_size: Window size for rolling average
    
    Returns:
        numpy array of smoothed values
    """
    if not NUMPY_AVAILABLE:
        return values
    
    arr = np.array(values, dtype=float)
    
    # Use pandas rolling for cleaner implementation
    series = pd.Series(arr)
    smoothed = series.rolling(window=window_size, center=True).mean()
    
    return smoothed.fillna(arr).values


def activity_heatmap_data(timestamps, bin_by_hour=True):
    """
    Generate heatmap data for activity analysis.
    
    Args:
        timestamps: numpy array of timestamps
        bin_by_hour: If True, bin by hour of day, else by day of week
    
    Returns:
        dict with heatmap data
    """
    if not NUMPY_AVAILABLE or len(timestamps) == 0:
        return {}
    
    df = pd.DataFrame({'timestamp': pd.to_datetime(timestamps)})
    df['count'] = 1
    
    if bin_by_hour:
        df['hour'] = df['timestamp'].dt.hour
        heatmap = df.groupby('hour')['count'].sum().to_dict()
    else:
        df['day'] = df['timestamp'].dt.day_name()
        heatmap = df.groupby('day')['count'].sum().to_dict()
    
    return heatmap


# Example usage and benchmarking
if __name__ == '__main__':
    print("NumPy Analyzer Module\n")
    
    if not NUMPY_AVAILABLE:
        print("❌ NumPy/Pandas not installed.")
        print("   Install with: pip install numpy pandas")
    else:
        print("✅ NumPy/Pandas available!\n")
        
        # Example: Generate sample data
        import random
        sample_times = [(datetime.now() - timedelta(hours=random.randint(0, 24))).strftime("%m-%d %H:%M:%S") 
                       for _ in range(1000)]
        sample_logs = [f"{t} I/Example: Sample log {i}" for i, t in enumerate(sample_times)]
        
        # Test timestamp parsing
        print("Testing timestamp parsing...")
        from performance_utils import timer
        
        @timer
        def test_parsing():
            return parse_timestamps_vectorized(sample_logs)
        
        timestamps = test_parsing()
        print(f"   Parsed {len(timestamps)} timestamps\n")
        
        # Test frequency analysis
        sample_items = [f"Process{random.randint(1, 10)}" for _ in range(1000)]
        
        @timer
        def test_frequency():
            return frequency_analysis_vectorized(sample_items)
        
        items, counts = test_frequency()
        print(f"   Top 5 items: {list(zip(items[:5], counts[:5]))}\n")
        
        # Test statistical analysis
        sample_values = [random.gauss(100, 20) for _ in range(1000)]
        stats = statistical_analysis(sample_values)
        print("Statistical Analysis:")
        for key, value in stats.items():
            print(f"   {key}: {value:.2f}")
        
        print("\n✅ NumPy analyzer ready!")
