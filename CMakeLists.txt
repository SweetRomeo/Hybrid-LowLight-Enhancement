cmake_minimum_required(VERSION 3.24)
project(OpenCVTest1)

set(CMAKE_CXX_STANDARD 20)

# --- 1. Politika Ayarı ---
if(POLICY CMP0148)
    cmake_policy(SET CMP0148 OLD)
endif()

# --- 2. OpenCV Ayarı (DÜZELTİLEN KISIM) ---
# Sadece 'build' değil, 'x64/vc16/lib' klasörünü gösteriyoruz.
# Config dosyaları ve .lib dosyaları buradadır.
set(OpenCV_DIR "C:/opencv/build/x64/vc16/lib")

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# Emin olmak için bulduğu kütüphaneleri ekrana yazdıralım
message(STATUS "Bulunan OpenCV Kutuphaneleri: ${OpenCV_LIBS}")

# --- 3. Pybind11 Kurulumu ---
include(FetchContent)
FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11
        GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)

# --- 4. Python Kütüphanelerini Bul ---
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# ==========================================
# HEDEF 1: PYTHON MODÜLÜ (.pyd)
# ==========================================
pybind11_add_module(low_light_module
        LowLightEnhancer.cpp
        bindings.cpp
)

# Modüle OpenCV'yi bağlıyoruz
target_link_libraries(low_light_module PRIVATE ${OpenCV_LIBS})

# ==========================================
# HEDEF 2: C++ TEST UYGULAMASI (.exe)
# ==========================================
add_executable(OpenCVTest1
        main.cpp
        LowLightEnhancer.cpp
)

target_link_libraries(OpenCVTest1 ${OpenCV_LIBS})