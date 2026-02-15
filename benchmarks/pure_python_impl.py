import cv2
import time
import numpy as np

# =============================================================================
# 1. SAF PYTHON İYİLEŞTİRME SINIFI (Class Definition)
# =============================================================================
class PurePythonEnhancer:
    def __init__(self):
        # Başlangıç ayarları (gerekirse buraya eklenir)
        pass

    def apply_gamma(self, image, gamma=1.0):
        # Python tarafında LUT (Look-Up Table) ile hızlı Gamma
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    def apply_clahe(self, image):
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # Renkli görüntüde sadece L (Lightness) kanalına uygulanır
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)

        merged = cv2.merge((cl, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    def process_full_pipeline(self, image):
        """
        Zifiri karanlık için ağır işlem zinciri (Saf Python/OpenCV Wrapper):
        1. Bilateral Filter (Denoise)
        2. CLAHE (Kontrast)
        3. Gamma (Parlaklık)
        4. Sharpening (Keskinleştirme)
        """
        # Adım 1: Gürültü Azaltma (Bilateral Filter işlemciyi çok yorar)
        denoised = cv2.bilateralFilter(image, 9, 75, 75)

        # Adım 2: CLAHE
        contrasted = self.apply_clahe(denoised)

        # Adım 3: Gamma
        brightened = self.apply_gamma(contrasted, 0.5) # Gamma 0.5

        # Adım 4: Keskinleştirme (Kernel ile konvolüsyon)
        kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(brightened, -1, kernel)

        return sharpened

# =============================================================================
# 2. YARDIMCI FONKSİYONLAR
# =============================================================================

def calculate_brightness(image):
    if image is None: return 0
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv[..., 2].mean()

def draw_hud(frame, algo_name, latency, fps, brightness, color_bgr):
    h, w, _ = frame.shape

    # Alt Bar Arkaplanı
    cv2.rectangle(frame, (0, h-80), (w, h), (20, 20, 20), -1)

    # Sol Kutu (Algoritma Adı ve Rengi)
    cv2.rectangle(frame, (0, h-80), (300, h), color_bgr, -1)
    cv2.putText(frame, "PURE PYTHON MODE", (10, h-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.putText(frame, algo_name, (10, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

    # Işık Seviyesi (Orta)
    cv2.putText(frame, f"LIGHT: {brightness:.1f}", (320, h-45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    # Performans Göstergeleri (Sağ)
    # Latency Rengi (33ms üstü kırmızı)
    lat_color = (0, 255, 0) if latency < 33 else (0, 0, 255)

    cv2.putText(frame, f"LATENCY: {latency:.1f} ms", (w-250, h-45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, lat_color, 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (w-250, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)

    return frame

# =============================================================================
# 3. ANA DÖNGÜ (MAIN FUNCTION)
# =============================================================================

def main():
    # Sınıf örneğini oluştur (HATANIN ÇIKTIĞI YER BURASIYDI, ARTIK ÇÖZÜLDÜ)
    py_enhancer = PurePythonEnhancer()

    # Kamerayı Başlat
    cap = cv2.VideoCapture(0)

    # Eşik Değerleri
    THRESH_DAYLIGHT = 140.0
    THRESH_TUNNEL   = 90.0
    THRESH_STREET   = 40.0

    print("--- SAF PYTHON (PURE PYTHON) MODU BAŞLATILDI ---")
    print("Bu modda C++ hızlandırması KULLANILMAMAKTADIR.")
    print("Çıkış için 'q' tuşuna basın.")

    prev_frame_time = 0
    new_frame_time = 0

    manual_mode = False
    manual_selection = 0

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Orijinal kopyayı al
        original_frame = frame.copy()
        brightness = calculate_brightness(frame)

        # Algoritma Seçimi
        if manual_mode:
            selected_algo = manual_selection
        else:
            if brightness > THRESH_DAYLIGHT: selected_algo = 0
            elif brightness > THRESH_TUNNEL: selected_algo = 1
            elif brightness > THRESH_STREET: selected_algo = 2
            else: selected_algo = 3

        # --- İŞLEME BAŞLANGICI ---
        start_time = time.time()

        if selected_algo == 0:
            algo_name = "PASSTHROUGH"
            color = (100, 255, 100) # Açık Yeşil
            processed_frame = frame

        elif selected_algo == 1:
            algo_name = "GAMMA (Python)"
            color = (0, 255, 255) # Sarı
            processed_frame = py_enhancer.apply_gamma(frame, 0.5)

        elif selected_algo == 2:
            algo_name = "CLAHE (Python)"
            color = (0, 165, 255) # Turuncu
            processed_frame = py_enhancer.apply_clahe(frame)

        elif selected_algo == 3:
            algo_name = "FULL CHAIN (Py)"
            color = (50, 50, 255) # Kırmızı
            # Burası C++'a göre çok daha yavaş çalışmalı!
            processed_frame = py_enhancer.process_full_pipeline(frame)

        end_time = time.time()
        # --- İŞLEME BİTİŞİ ---

        latency_ms = (end_time - start_time) * 1000

        # FPS Hesabı
        new_frame_time = time.time()
        # Sıfıra bölünme hatasını önlemek için küçük kontrol
        diff = new_frame_time - prev_frame_time
        if diff == 0: diff = 0.001
        fps = 1 / diff
        prev_frame_time = new_frame_time

        # HUD Çizimi
        display_frame = draw_hud(processed_frame.copy(), algo_name, latency_ms, fps, brightness, color)

        # Sadece işlenmiş görüntüyü göster (Performans testi için)
        # İstersen yan yana yapmak için: combined = np.hstack((original_frame, display_frame))
        cv2.imshow("Pure Python Benchmark Mode", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('m'):
            manual_mode = not manual_mode
            print(f"Manuel Mod: {manual_mode}")
        elif key == ord('1'): manual_selection = 0
        elif key == ord('2'): manual_selection = 1
        elif key == ord('3'): manual_selection = 2
        elif key == ord('4'): manual_selection = 3

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()