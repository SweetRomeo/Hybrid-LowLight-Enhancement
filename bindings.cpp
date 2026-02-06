#include <pybind11/pybind11.h>
#include <pybind11/numpy.h> // Numpy desteği için şart
#include "LowLightEnhancer.h"

namespace py = pybind11;

// --- YARDIMCI FONKSİYONLAR (Köprüler) ---

// 1. Python'dan gelen Numpy Array'i -> OpenCV Mat'e çevirir
cv::Mat numpy_to_mat(py::array_t<unsigned char>& input) {
    py::buffer_info buf = input.request();

    // OpenCV Matrisini oluştur (Veriyi kopyalamadan, doğrudan belleği işaret eder)
    // Varsayım: Görüntü 3 kanallı (Renkli) ve uint8 formatında
    cv::Mat mat(buf.shape[0], buf.shape[1], CV_8UC3, (unsigned char*)buf.ptr);
    return mat;
}

// 2. OpenCV Mat'i -> Python Numpy Array'e çevirir
py::array_t<unsigned char> mat_to_numpy(const cv::Mat& mat) {
    // Python tarafına dönecek boş bir array oluştur
    py::array_t<unsigned char> result({mat.rows, mat.cols, 3});

    // Matris verisini Python array'ine kopyala
    py::buffer_info buf = result.request();
    std::memcpy(buf.ptr, mat.data, mat.total() * mat.elemSize());

    return result;
}

// bindings.cpp İÇERİĞİ KONTROL ET

PYBIND11_MODULE(low_light_module, m) {
    m.doc() = "Tez projesi modulu";

    py::class_<LowLightEnhancer>(m, "LowLightEnhancer")
        .def(py::init<>())

        // 1. Full Process
        .def("processImageFull", [](LowLightEnhancer &self, py::array_t<unsigned char> input) {
            cv::Mat img = numpy_to_mat(input);
            return mat_to_numpy(self.processImageFull(img));
        })

        // 2. CLAHE
        .def("applyCLAHE", [](LowLightEnhancer &self, py::array_t<unsigned char> input) {
            cv::Mat img = numpy_to_mat(input);
            return mat_to_numpy(self.applyCLAHE(img));
        })

        // 3. GAMMA (BU SATIR EKSİK OLABİLİR Mİ?)
        .def("applyGammaCorrection", [](LowLightEnhancer &self, py::array_t<unsigned char> input, float gamma) {
            cv::Mat img = numpy_to_mat(input);
            return mat_to_numpy(self.applyGammaCorrection(img, gamma));
        });
}