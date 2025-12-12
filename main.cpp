#include <iostream>
#include <opencv2/opencv.hpp>

int main() {
    // 0 -> Varsayılan web kamerası (Laptop kamerası)
    // Harici USB kamera varsa 1 veya 2 yapabilirsin.
    cv::VideoCapture cap(0);

    if (!cap.isOpened()) {
        std::cout << "Kamera acilamadi!" << std::endl;
        return -1;
    }

    cv::Mat frame, grayFrame;

    std::cout << "Cikmak icin 'q' tusuna basin." << std::endl;

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

    // Temizlik
    cap.release();
    cv::destroyAllWindows();

    return 0;
}