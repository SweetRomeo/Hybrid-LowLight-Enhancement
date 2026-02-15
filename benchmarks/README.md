# 🐍 Pure Python Benchmark Implementation (Control Group)

![Language](https://img.shields.io/badge/Language-Python%203.x-blue)
![Library](https://img.shields.io/badge/Library-OpenCV%20(cv2)-green)
![Performance](https://img.shields.io/badge/Performance-Baseline-yellow)
![Status](https://img.shields.io/badge/Status-Benchmark%20Only-red)

## 🎯 Purpose
This module (`main_pure_python.py`) serves as the **Control Group** for the Master's Thesis research on *Real-Time Hybrid Low-Light Enhancement*.

It implements the **exact same algorithms** (Gamma Correction, CLAHE, Denoise, Sharpening) as the main project, but utilizes **standard Python interpreters and OpenCV wrappers** instead of the proposed Hybrid C++ Architecture.

**The goal is to measure the overhead caused by:**
1.  Python Interpreter (GIL - Global Interpreter Lock).
2.  Memory copying between NumPy arrays and OpenCV native calls.
3.  Lack of direct memory management and pointer arithmetic.

## ⚙️ Technical Comparison

| Feature | Hybrid C++ Engine (Main) | Pure Python (This Module) |
| :--- | :--- | :--- |
| **Execution** | Compiled Machine Code | Interpreted Bytecode |
| **Memory Access** | Direct Pointer Arithmetic | Buffer Copying (NumPy Overhead) |
| **Pipeline** | Single-Pass (Zero-Copy) | Multi-Pass (Object Creation per Step) |
| **Parallelism** | SIMD & OpenMP Optimized | Single Threaded (Mostly) |
| **Latency Target** | **< 33 ms** (Real-Time) | **> 100 ms** (High Latency) |

## 🛠️ Implemented Pipeline (Standard API)

Unlike the optimized C++ engine, this module uses high-level API calls standard in the industry:

1.  **Gamma Correction:** `cv2.LUT` (Look-Up Table) optimization.
2.  **CLAHE:** `cv2.createCLAHE` wrapper.
3.  **Denoising:** `cv2.bilateralFilter` (Intentionally computationally expensive).
4.  **Sharpening:** `cv2.filter2D` with a convolution kernel.

## 💻 Usage

To run the benchmark and observe the latency difference:

```bash
# Run the Python-only version
python main_pure_python.py
