#!/usr/bin/env python3
"""Benchmark import time for osxphotos module."""

import subprocess
import sys
import time
from statistics import mean, stdev


def measure_import_time(iterations: int = 5) -> dict:
    """Measure time to import osxphotos."""
    results = {
        "simple_import": [],
        "help_command": [],
    }
    
    # Test 1: Simple import
    for _ in range(iterations):
        start = time.perf_counter()
        result = subprocess.run(
            [sys.executable, "-c", "import osxphotos"],
            capture_output=True,
            text=True,
        )
        end = time.perf_counter()
        if result.returncode == 0:
            results["simple_import"].append(end - start)
    
    # Test 2: CLI help (cold start)
    for _ in range(iterations):
        start = time.perf_counter()
        result = subprocess.run(
            [sys.executable, "-m", "osxphotos", "--help"],
            capture_output=True,
            text=True,
        )
        end = time.perf_counter()
        if result.returncode == 0:
            results["help_command"].append(end - start)
    
    return results


def main():
    """Run benchmarks and print results."""
    print("Running import time benchmarks...")
    print("=" * 60)
    
    results = measure_import_time(iterations=5)
    
    for test_name, times in results.items():
        if times:
            avg = mean(times)
            std = stdev(times) if len(times) > 1 else 0
            print(f"\n{test_name.replace('_', ' ').title()}:")
            print(f"  Mean: {avg:.4f}s")
            print(f"  Stdev: {std:.4f}s")
            print(f"  Min: {min(times):.4f}s")
            print(f"  Max: {max(times):.4f}s")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

