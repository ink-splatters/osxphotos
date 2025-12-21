#!/usr/bin/env python3
"""Benchmark common CLI commands."""

import subprocess
import sys
import time
from statistics import mean, stdev


def measure_cli_command(command: list[str], iterations: int = 3) -> list[float]:
    """Measure time to execute a CLI command."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = subprocess.run(
            [sys.executable, "-m", "osxphotos"] + command,
            capture_output=True,
            text=True,
        )
        end = time.perf_counter()
        if result.returncode == 0:
            times.append(end - start)
    return times


def main():
    """Run CLI benchmarks and print results."""
    print("Running CLI command benchmarks...")
    print("=" * 60)
    
    commands = [
        (["--help"], "Help"),
        (["--version"], "Version"),
        (["docs", "--help"], "Docs Help"),
        (["about"], "About"),
    ]
    
    for cmd, name in commands:
        times = measure_cli_command(cmd, iterations=3)
        if times:
            avg = mean(times)
            std = stdev(times) if len(times) > 1 else 0
            print(f"\n{name}:")
            print(f"  Mean: {avg:.4f}s")
            print(f"  Stdev: {std:.4f}s")
            print(f"  Min: {min(times):.4f}s")
            print(f"  Max: {max(times):.4f}s")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

