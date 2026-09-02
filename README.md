# Multi-Level Cache Simulator

## Project Overview

This project presents a **Multi-Level Cache Simulator** designed to model the behavior of a computer memory hierarchy consisting of **L1, L2, and L3 cache levels**.

The simulator evaluates cache performance using different replacement policies and calculates important performance metrics such as **hit rate, miss rate, average memory access latency, and memory accesses**.

## Problem Statement

Design and implement a multi-level cache simulator supporting configurable cache sizes, associativity, and replacement policies, and evaluate its performance using cache hit rate, miss rate, latency, bandwidth, and throughput.

## Objectives

* Simulate L1, L2, and L3 cache levels.
* Support different cache replacement policies.
* Analyze cache hit and miss behavior.
* Calculate average memory access latency.
* Compare the performance of LRU, FIFO, and RANDOM policies.
* Study the effect of cache hierarchy on system performance.

## Cache Configuration

| Cache Level |  Size | Associativity | Latency |
| ----------- | ----: | ------------: | ------: |
| L1          |  4 KB |         2-way |    1 ns |
| L2          | 16 KB |         4-way |    8 ns |
| L3          | 64 KB |         4-way |   30 ns |
| Main Memory |     — |             — |  100 ns |

**Block Size:** 64 bytes

## Replacement Policies

The simulator supports:

* **LRU (Least Recently Used)**
* **FIFO (First In First Out)**
* **RANDOM**

## Technologies Used

* Python 3.10
* Matplotlib
* Object-Oriented Programming
* Cache and Memory Hierarchy Concepts

## Project Structure

```text
Multi-Level-Cache-Simulator/
│
├── cache_simulator.py
├── README.md
├── requirements.txt
│
├── results/
│   ├── hit_rate_comparison.png
│   ├── latency_comparison.png
│   └── level_hit_rates.png
│
└── report/
    └── Computer_Architecture_Common_Assignment_Report.docx
```

## Installation

Install the required Python library:

```bash
pip install matplotlib
```

## How to Run

Open Command Prompt in the project folder and run:

```bash
python cache_simulator.py
```

## Expected Output

The program displays performance results for the three replacement policies.

Example:

```text
LRU
L1 Hit Rate      : 71.70%
L2 Hit Rate      : 3.53%
L3 Hit Rate      : 1.47%
Overall Hit Rate : 73.10%
Miss Rate        : 26.90%
Average Latency  : 38.35 ns

FIFO
L1 Hit Rate      : 71.80%
L2 Hit Rate      : 3.55%
L3 Hit Rate      : 7.72%
Overall Hit Rate : 74.90%
Miss Rate        : 25.10%
Average Latency  : 36.52 ns

RANDOM
L1 Hit Rate      : 71.70%
L2 Hit Rate      : 2.83%
L3 Hit Rate      : 2.91%
Overall Hit Rate : 73.30%
Miss Rate        : 26.70%
Average Latency  : 38.21 ns
```

## Results

Among the tested replacement policies, **FIFO achieved the lowest average latency and the highest overall hit rate** for the selected workload.

The simulator demonstrates how cache hierarchy and replacement policies affect memory access performance.

## Applications

The concepts demonstrated by this project are applicable to:

* CPU cache design
* Memory hierarchy analysis
* Processor performance optimization
* Computer architecture education
* Performance evaluation of cache systems

## Team Project

This project was developed as a **group assignment** for the Computer Architecture course.

All team members contributed to the design, implementation, testing, analysis, documentation, and evaluation of the project.

## References

1. J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, Morgan Kaufmann.
2. D. A. Patterson and J. L. Hennessy, *Computer Organization and Design: The Hardware/Software Interface*, Morgan Kaufmann.
3. Python Software Foundation, “Python 3 Documentation.”
4. Matplotlib Development Team, “Matplotlib Documentation.”
5. Course Notes and Laboratory Material for Computer Architecture.
