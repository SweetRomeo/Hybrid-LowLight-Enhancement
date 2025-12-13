//
// Created by berke on 12/12/2025.
//

#ifndef CAMERASTREAMER_H
#define CAMERASTREAMER_H

#include <opencv2/opencv.hpp>
#include <iostream>

class CameraStreamer {
public:
    // 1. Constructor: Cihaz ID'si ile başlat (Örn: 0 veya 1)
    CameraStreamer(int deviceIndex);

    // Destructor: Kamerayı serbest bırakır
    ~CameraStreamer();

    // 2. Kamerayı Başlat/Kontrol Et
    bool isOpened() const;

    // 3. Robot için Kritik Ayarlar
    // Pi işlemcisini yormamak için 640x480 gibi değerlere çekmek isteyebilirsin.
    void setResolution(int width, int height);
    void setFPS(int fps);

    // 4. Kare Yakalama (En Önemli Kısım)
    // Void yerine bool döndürüyoruz. Kare yakalayamazsa false döner.
    // Yakalanan kareyi parametre olarak referansla alır (Performans için).
    bool readFrame(cv::Mat& outFrame);

private:
    cv::VideoCapture cap; // OpenCV'nin kendi sınıfı
    int deviceId;
};

#endif // CAMERASTREAMER_H