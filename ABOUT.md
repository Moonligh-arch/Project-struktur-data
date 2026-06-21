# About This Project

**Simulasi Lift dengan Priority Queue**

This project demonstrates a lift (elevator) scheduling simulation using a **Priority Queue** implemented via the **SCAN (Elevator) algorithm**. It serves as a case study for data structures courses, showing how dynamic data structures can improve real‑world scheduling problems.

## What It Does
- Simulates a multi‑floor building where passengers request rides.
- Uses a priority queue (`heapq`) to decide the next floor based on the SCAN algorithm, sweeping in one direction before reversing.
- Provides an interactive CLI for adding passengers, viewing status, and running stress‑test scenarios.

## How It Works
- The core data structure is a nested dictionary mapping floors to queues of passengers for each direction (`up`/`down`).
- The SCAN algorithm ensures the elevator moves monotonically in one direction, reducing travel time compared to naïve FIFO handling.

## Educational Value
- Illustrates the practical use of priority queues beyond classic heap examples.
- Shows algorithmic optimization (SCAN) that is also used in disk scheduling.
- Demonstrates clean, PEP‑8‑compliant Python code with modular design.

## License
This work is released under the **MIT License**.

---

*Created for the Structure Data course assignment.*
