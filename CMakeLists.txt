cmake_minimum_required(VERSION 3.24)
project(OpenCVTest1)

set(CMAKE_CXX_STANDARD 20)

# --- KRİTİK DEĞİŞİKLİK BURADA ---
# Yolu "build" klasöründe bırakma.
# "vc15" veya "vc16" klasörünün içindeki "lib" klasörüne kadar in.
# Bilgisayarında hangisi varsa onu yaz (vc16 yoksa vc15 dene).
set(OpenCV_DIR "C:/opencv/build/x64/vc16/lib")

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(OpenCVTest1 main.cpp)

target_link_libraries(OpenCVTest1 ${OpenCV_LIBS})