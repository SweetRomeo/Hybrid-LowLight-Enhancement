import sys
import os
import cv2
import time
import numpy as np

# C++ Module Upload
build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cmake-build-release'))
sys.path.append(build_path)

if os.name == 'nt':
    # OpenCV DLL yolunu kendi bilgisayarına göre güncelle!
    opencv_bin_path = "C:/opencv/build/x64/vc16/bin"
    if os.path.exists(opencv_bin_path):
        os.add_dll_directory(opencv_bin_path)

try:
    import low_light_module
    print("✅ Hibrit C++ Modülü Başarıyla Yüklendi!")
except ImportError as e:
    print(f"❌ HATA: Modül yüklenemedi. {e}")
    sys.exit(1)

def calculate_brightness(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv[..., 2].mean()

def main():
    enhancer = low_light_module.LowLightEnhancer()
    cap = cv2.VideoCapture(0)

    # Eşik Değerleri
    THRESH_LEVEL_1 = 140.0
    THRESH_LEVEL_2 = 90.0
    THRESH_LEVEL_3 = 40.0

    # Tam ekran modu için pencere ayarı (Opsiyonel)
    window_name = "Master Thesis Project: Original (Left) vs Hybrid Enhancement (Right)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret: break

        # 1. ADIM: Orijinal görüntünün temiz bir kopyasını al (Sol taraf için)
        original_frame_display = frame.copy()

        brightness = calculate_brightness(frame)
        proc_start = time.time()

        # --- ADAPTİF ALGORİTMA SEÇİCİ ---
        if brightness > THRESH_LEVEL_1:
            status = "DURUM: IYI ISIK"
            algorithm = "Passthrough (None)"
            color = (0, 255, 0) # Yeşil
            # DİKKAT: Burada .copy() kullanıyoruz ki orijinal görüntüye yazı yazılmasın
            processed_frame = frame.copy()

        elif brightness > THRESH_LEVEL_2:
            status = "DURUM: HAFIF LOS"
            algorithm = "Gamma Correction"
            processed_frame = enhancer.applyGammaCorrection(frame, 0.5)
            color = (0, 255, 255) # Sarı

        elif brightness > THRESH_LEVEL_3:
            status = "DURUM: KARANLIK"
            algorithm = "CLAHE (Contrast)"
            processed_frame = enhancer.applyCLAHE(frame)
            color = (0, 165, 255) # Turuncu

        else:
            status = "DURUM: KRITIK DUSUK ISIK"
            algorithm = "FULL PIPELINE (Heavy)"
            processed_frame = enhancer.processImageFull(frame)
            color = (0, 0, 255) # Kırmızı

        proc_end = time.time()
        latency_ms = (proc_end - proc_start) * 1000

        # --- GÖRSELLEŞTİRME (HUD) KISMI ---

        # SOL TARAF (Orijinal) İçin Yazılar
        cv2.putText(original_frame_display, "ORIJINAL GORUNTU (RAW)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(original_frame_display, f"Light Level: {brightness:.1f}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        # SAĞ TARAF (İyileştirilmiş) İçin Yazılar
        # Başlık
        cv2.rectangle(processed_frame, (0, 0), (processed_frame.shape[1], 40), (0,0,0), -1) # Başlık arka planı
        cv2.putText(processed_frame, "IYILESTIRILMIS (HIBRIT C++)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Durum Bilgileri (Alt alta)
        cv2.putText(processed_frame, status, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(processed_frame, f"Algo: {algorithm}", (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        # Gecikme bilgisini daha belirgin yapalım
        cv2.rectangle(processed_frame, (15, 130), (250, 165), (50, 50, 50), -1)
        cv2.putText(processed_frame, f"Latency: {latency_ms:.1f} ms", (20, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # --- BİRLEŞTİRME KISMI ---
        # İki görüntüyü yatay olarak (horizontal stack) birleştir
        combined_view = np.hstack((original_frame_display, processed_frame))

        # Sonucu göster
        cv2.imshow(window_name, combined_view)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # 's' tuşuna basarsan o anki ekran görüntüsünü tez için kaydeder
        elif key == ord('s'):
            filename = f"tez_ekran_goruntusu_{int(time.time())}.jpg"
            cv2.imwrite(filename, combined_view)
            print(f"Ekran görüntüsü kaydedildi: {filename}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()