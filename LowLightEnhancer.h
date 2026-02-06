//
// Created by Berke on 28.01.2026.
//

#ifndef CMAKELISTS_TXT_LOW_LIGHT_ENHANCER_H
#define CMAKELISTS_TXT_LOW_LIGHT_ENHANCER_H

#include <opencv2/opencv.hpp>
#include <vector>
#include <cmath>

#ifdef _WIN32
    #define EXPORT extern "C" __declspec(dllexport)
#else
    #define EXPORT extern "C"
#endif

class LowLightEnhancer {
public:
    // Constructor
    LowLightEnhancer();

    // Destructor
    ~LowLightEnhancer();

    /**
     * @brief Ana işlem fonksiyonu (Pipeline).
     * Tüm alt algoritmaları sırasıyla uygulayarak nihai görüntüyü verir.
     * @param input Kameradan gelen ham görüntü
     * @return İyileştirilmiş görüntü
     */
    cv::Mat processImageFull(const cv::Mat& input);

    /**
     * @brief Gürültü Azaltma (Denoising).
     * Düşük ışıkta oluşan karıncalanmayı temizler.
     */
    static cv::Mat applyDenoising(const cv::Mat& input);

    /**
     * @brief Kontrast Dengeleme (CLAHE).
     * Contrast Limited Adaptive Histogram Equalization algoritması.
     * Görüntüyü patlatmadan karanlık detayları açar.
     */
    static cv::Mat applyCLAHE(const cv::Mat& input);

    /**
     * @brief Parlaklık Düzeltmesi (Gamma Correction).
     * Doğrusal olmayan parlaklık artışı sağlar.
     * @param gamma Değer < 1.0 ise parlaklığı artırır (Örn: 0.5)
     */
    static cv::Mat applyGammaCorrection(const cv::Mat& input, float gamma);

    /**
     * @brief Keskinleştirme (Sharpening).
     * Denoising sonrası yumuşayan kenarları tekrar belirginleştirir.
     */
    static cv::Mat applySharpening(const cv::Mat& input);
};
#endif //CMAKELISTS_TXT_LOW_LIGHT_ENHANCER_H