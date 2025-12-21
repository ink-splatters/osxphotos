# OSXPhotos Performance Benchmarks

This directory contains benchmarking scripts to measure performance of osxphotos.

## Running Benchmarks

### Import Time Benchmark
Measures the cold-start time for importing osxphotos and running CLI commands:

```bash
python3 benchmarks/import_time.py
```

### CLI Commands Benchmark
Measures execution time for common CLI commands:

```bash
python3 benchmarks/cli_commands.py
```

### Using Python's Import Profiler
To see detailed import time breakdown:

```bash
PYTHONPROFILEIMPORTTIME=1 python -c "import osxphotos" 2>&1 | head -20
```

## Baseline Results

Run these benchmarks before and after optimizations to measure improvements.
Store baseline results in `BASELINE.md` for comparison.

