//
// Created by berke on 12/13/2025.
//

#ifndef OPENCVTEST1_IMAGEPROCESS_H
#define OPENCVTEST1_IMAGEPROCESS_H
#include <opencv2/core/mat.hpp>

#include <opencv2/opencv.hpp>

class CameraStreamer {
public:
    // 1. Constructor: Boş başlatıcı
    CameraStreamer();

    // 2. Constructor: Resim ile başlatıcı (Overloading)
    CameraStreamer(const cv::Mat& sourceImage);

    // Destructor: Varsayılan yeterlidir
    ~CameraStreamer() = default;

    // --- Temel İşlemler ---
    void setImage(const cv::Mat& sourceImage);
    cv::Mat getImage() const; // İşlenmiş resmi geri almak için
    void display(const std::string& windowName = "Debug Window") const;

    // --- Robot/Tez İçin Kritik İşlemler ---
    void resize(int width, int height); // İşlemciyi yormamak için küçültme
    void toGray(); // İşlem hızını artırmak için griye çevirme
    CameraStreamer& drawLine(cv::Point start, cv::Point end, cv::Scalar color, int thickness = 2);
    CameraStreamer& drawRectangle(cv::Point start, cv::Point end, cv::Scalar color, int thickness = 2);
    CameraStreamer& drawCircle(cv::Point center, int radius, cv::Scalar color, int thickness = 2);

private:
    cv::Mat image;
    bool isRgb;
    int width;
    int height;
};
#endif //OPENCVTEST1_IMAGEPROCESS_H