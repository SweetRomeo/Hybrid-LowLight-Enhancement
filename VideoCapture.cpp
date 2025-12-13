//
// Created by berke on 12/12/2025.
//
#include "VideoCapture.h"
#include <opencv2/opencv.hpp>

VideoCapture::VideoCapture(const int deviceIndex) {
    cap = cv::VideoCapture(deviceIndex);
}

void VideoCapture::catchCameraView() {
    while (true) {
        // 1. Kameradan yeni bir kare (frame) oku
        cap.read(frame);

        if (frame.empty()) {
            std::cout << "Goruntu alinamadi!" << std::endl;
            break;
        }

        // 2. Görüntüyü Gri tona çevir (Color to Gray)
        // BGR (Blue Green Red) formatından GRAY formatına
        cv::cvtColor(frame, grayFrame, cv::COLOR_BGR2GRAY);

        // 3. İki pencereyi de göster (Orijinal ve Gri)
        cv::imshow("Renkli Dunya", frame);
        cv::imshow("Gri Dunya", grayFrame);

        // 4. 'q' tuşuna basılırsa döngüden çık
        // waitKey(1) -> 1 milisaniye bekle. Hem görüntüyü ekranda tutar hem tuş dinler.
        if (cv::waitKey(1) == 'q') {
            break;
        }
    }
}

VideoCapture::~VideoCapture() {
    cap.release();
    cv::destroyAllWindows();
}

