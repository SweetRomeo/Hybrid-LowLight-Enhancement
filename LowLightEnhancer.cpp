#include "LowLightEnhancer.h"

// Constructor
LowLightEnhancer::LowLightEnhancer() {}

// Destructor
LowLightEnhancer::~LowLightEnhancer() {}

// --- 1. Ana Pipeline Fonksiyonu ---
cv::Mat LowLightEnhancer::processImageFull(const cv::Mat& input) {
    if (input.empty()) return input;

    cv::Mat processedFrame = input.clone();

    // ADIM 1: Gürültü Temizleme (Önce temizle ki, CLAHE gürültüyü parlatmasın)
    processedFrame = applyDenoising(processedFrame);

    // ADIM 2: Kontrast ve Işık Dengeleme (CLAHE)
    processedFrame = applyCLAHE(processedFrame);

    // ADIM 3: Ekstra Parlaklık (Gamma Correction - Gerekirse)
    // 0.6 değeri karanlık bölgeleri aydınlatır
    processedFrame = applyGammaCorrection(processedFrame, 0.6f);

    // ADIM 4: Keskinleştirme (Denoise işlemi görüntüyü yumuşatır, geri keskinleştiriyoruz)
    processedFrame = applySharpening(processedFrame);

    return processedFrame;
}

// --- 2. Gürültü Azaltma (Bilateral Filter) ---
// Bilateral Filter: Kenarları koruyarak (blur yapmadan) gürültüyü siler.
cv::Mat LowLightEnhancer::applyDenoising(const cv::Mat& input) {
    cv::Mat output;
    // d=9: Filtre çapı (daha yüksek = daha yavaş)
    // sigmaColor=75: Renk karışım miktarı
    // sigmaSpace=75: Uzamsal karışım
    cv::bilateralFilter(input, output, 9, 75, 75);
    return output;
}

// --- 3. CLAHE (Akıllı Histogram Eşitleme) ---
cv::Mat LowLightEnhancer::applyCLAHE(const cv::Mat& input) {
    cv::Mat lab_image;

    // 1. RGB'den LAB renk uzayına geç (Parlaklığı (L) renkten ayırmak için)
    cv::cvtColor(input, lab_image, cv::COLOR_BGR2Lab);

    // 2. Kanalları ayır (L, a, b)
    std::vector<cv::Mat> lab_planes(3);
    cv::split(lab_image, lab_planes);

    // 3. Sadece L (Lightness/Aydınlık) kanalına CLAHE uygula
    // clipLimit: Kontrast eşiği (yüksek değer = daha çok kontrast ama daha çok gürültü)
    cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE();
    clahe->setClipLimit(4.0);
    clahe->setTilesGridSize(cv::Size(8, 8));

    cv::Mat dst;
    clahe->apply(lab_planes[0], dst);

    // 4. İşlenmiş L kanalını geri koy
    dst.copyTo(lab_planes[0]);

    // 5. Kanalları birleştir ve tekrar BGR'ye dön
    cv::merge(lab_planes, lab_image);
    cv::Mat output;
    cv::cvtColor(lab_image, output, cv::COLOR_Lab2BGR);

    return output;
}

// --- 4. Gamma Correction (LUT Optimizasyonu ile) ---
cv::Mat LowLightEnhancer::applyGammaCorrection(const cv::Mat& input, float gamma) {
    cv::Mat lookUpTable(1, 256, CV_8U);
    uchar* p = lookUpTable.ptr();

    // Her piksel için tek tek 'pow' hesaplamak yavaştır.
    // O yüzden bir tablo (Look-Up Table) oluşturuyoruz.
    for (int i = 0; i < 256; ++i) {
        p[i] = cv::saturate_cast<uchar>(pow(i / 255.0, gamma) * 255.0);
    }

    cv::Mat output;
    cv::LUT(input, lookUpTable, output);
    return output;
}

// --- 5. Keskinleştirme (Unsharp Masking Tekniği) ---
cv::Mat LowLightEnhancer::applySharpening(const cv::Mat& input) {
    cv::Mat blurred, output;

    // Görüntünün bulanık halini al
    cv::GaussianBlur(input, blurred, cv::Size(0, 0), 3);

    // Orijinal + (Orijinal - Bulanık) * ağırlık formülü
    cv::addWeighted(input, 1.5, blurred, -0.5, 0, output);

    return output;
}