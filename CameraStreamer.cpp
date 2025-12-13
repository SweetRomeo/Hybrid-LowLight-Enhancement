#include "CameraStreamer.h"
#include <iostream>

// Ctor: Değişkenleri güvenli başlatma (Initialization List)
CameraStreamer::CameraStreamer() : isRgb(false), width(0), height(0) {
    // Boş başlangıç
}

CameraStreamer::CameraStreamer(const cv::Mat& sourceImage) {
    setImage(sourceImage);
}

void CameraStreamer::setImage(const cv::Mat& sourceImage) {
    // clone() kullanıyoruz çünkü dışarıdaki resim silinse bile
    // bizim sınıfın içindeki kopya yaşasın istiyoruz.
    this->image = sourceImage.clone();
    
    // Metadata güncelleme
    this->width = image.cols;
    this->height = image.rows;
    
    // OpenCV varsayılan olarak 3 kanallıysa RGB(BGR)'dir
    if (image.channels() == 3) isRgb = true;
    else isRgb = false;
}

cv::Mat CameraStreamer::getImage() const {
    return this->image.clone(); // Güvenli kopya döndür
}

void CameraStreamer::display(const std::string& windowName) const {
    if (!image.empty()) {
        cv::imshow(windowName, image);
        // waitKey koymuyoruz, ana döngüde kontrol edilmeli
    } else {
        std::cerr << "Hata: Gosterilecek resim yok!" << std::endl;
    }
}

// --- Robot İçin Performans Fonksiyonları ---

void CameraStreamer::resize(int newWidth, int newHeight) {
    if (image.empty()) return;
    cv::resize(image, image, cv::Size(newWidth, newHeight));
    this->width = newWidth;
    this->height = newHeight;
}

void CameraStreamer::toGray() {
    if (image.empty() || !isRgb) return; // Zaten griyse işlem yapma
    cv::cvtColor(image, image, cv::COLOR_BGR2GRAY);
    isRgb = false;
}

// --- Çizim Fonksiyonları (Zincirleme Kullanım İçin) ---

CameraStreamer& CameraStreamer::drawLine(cv::Point start, cv::Point end, cv::Scalar color, int thickness) {
    if (!image.empty()) {
        cv::line(image, start, end, color, thickness);
    }
    return *this; // Nesnenin kendisini döndür
}

CameraStreamer& CameraStreamer::drawRectangle(cv::Point start, cv::Point end, cv::Scalar color, int thickness) {
    if (!image.empty()) {
        cv::rectangle(image, start, end, color, thickness);
    }
    return *this;
}

CameraStreamer& CameraStreamer::drawCircle(const cv::Point center, const int radius, const cv::Scalar color, const int thickness) {
    if (!image.empty()) {
        cv::circle(image, center, radius, color, thickness);
    }
    return *this;
}