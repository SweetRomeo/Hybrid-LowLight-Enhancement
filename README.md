# Real-Time Hybrid Low-Light Enhancement for Autonomous Vehicles 🚗🌙

![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue)
![Language](https://img.shields.io/badge/Language-C%2B%2B20%20%7C%20Python%203.x-green)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20(Pybind11)-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 Abstract
This project implements a **high-performance, real-time image enhancement engine** tailored for autonomous vehicle perception systems operating in low-light environments (e.g., tunnels, night streets, pitch-black roads).

To achieve the strict **latency requirements (<33ms for 30 FPS)** of autonomous driving, a **Hybrid Architecture** is utilized:
* **Core Engine (C++):** Executes heavy mathematical operations (Multi-Scale Retinex, CLAHE, Gamma Correction) using optimized memory management and SIMD instructions.
* **Control Layer (Python):** Manages adaptive logic, ambient light sensing, and visualization via `Pybind11` bindings.

The system dynamically switches algorithms based on real-time brightness analysis, optimizing the trade-off between computational cost and image clarity.

## 🚀 Key Features
* **Adaptive Algorithm Switching:** Automatically selects the optimal enhancement method based on ambient light sensors (simulated via pixel intensity).
* **Hybrid C++/Python Core:** Combines the ease of Python with the raw speed of C++.
* **Real-Time HUD:** Heads-Up Display showing active algorithms, latency (ms), and system status.
* **Manual Override Mode:** Allows forcing specific algorithms for demonstration and testing purposes.
* **Unit Tested:** Includes a comprehensive test suite for mathematical integrity and stability.

## 🛠️ Algorithms Pipeline

The system categorizes the environment into 4 distinct zones:

| Zone | Light Condition | Selected Algorithm | Description | Latency Target |
| :--- | :--- | :--- | :--- | :--- |
| **Zone 0** | Daylight (>140) | **Passthrough** | No processing. CPU idle. | ~0.0 ms |
| **Zone 1** | Tunnel / Dim (90-140) | **Gamma Correction** | LUT-optimized non-linear brightening. | ~2.5 ms |
| **Zone 2** | Night Street (40-90) | **CLAHE** | Contrast Limited Adaptive Histogram Equalization. | ~12.0 ms |
| **Zone 3** | Pitch Black (<40) | **Hybrid-MSR** | Multi-Scale Retinex / Restoration Pipeline. | ~35.0 ms |

## ⚙️ Installation & Build

### Prerequisites
* **CMake** (>= 3.10)
* **C++ Compiler** (MSVC for Windows / GCC or Clang for Linux)
* **Python** (3.8+)
* **OpenCV** (Required for both C++ and Python)

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/RealTime-LLE-Cpp.git](https://github.com/YOUR_USERNAME/Hybrid-LowLight-Enhancement.git
cd Hybrid-LowLight-Enhancement
```

### 2. Build the C++ Engine (backend)
```bash
mkdir cmake-build-release
cd cmake-build-release
cmake ..
cmake --build . --config Release
```
Make sure the generated .pyd (Windows) or .so (Linux) file is in the build directory.
