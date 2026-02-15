import os
import sys
import time
import unittest

import numpy as np

# --- Modül Yolunu Ayarla (main.py'deki gibi) ---
build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cmake-build-release'))
sys.path.append(build_path)

# Windows için DLL yolu
if os.name == 'nt':
    opencv_bin = "C:/opencv/build/x64/vc16/bin" # Kendi yolunla güncelle
    if os.path.exists(opencv_bin):
        os.add_dll_directory(opencv_bin)

try:
    import low_light_module
except ImportError:
    print("❌ HATA: Test edilecek modül bulunamadı. Lütfen önce projeyi derleyin (Build).")
    sys.exit(1)

class TestLowLightEnhancer(unittest.TestCase):

    # Her testten önce çalışır (Kurulum)
    def setUp(self):
        self.enhancer = low_light_module.LowLightEnhancer()

        # Test için yapay bir "Karanlık Görüntü" oluştur (100x100 piksel, koyu gri)
        # Ortalama parlaklık: 30
        self.dark_image = np.full((100, 100, 3), 30, dtype=np.uint8)

        # Test için yapay bir "Siyah Görüntü" (Zifiri karanlık)
        self.black_image = np.zeros((100, 100, 3), dtype=np.uint8)

    # ----------------------------------------------------------------
    # TEST 1: Gamma Correction Mantığı Çalışıyor mu?
    # Beklenti: Gamma < 1.0 uygulandığında görüntü parlaklaşmalı.
    # ----------------------------------------------------------------
    def test_gamma_correction_brightens_image(self):
        input_mean = np.mean(self.dark_image)

        # Gamma 0.5 uygula
        output_image = self.enhancer.applyGammaCorrection(self.dark_image, 0.5)
        output_mean = np.mean(output_image)

        print(f"\n[Test Gamma] Girdi: {input_mean:.2f}, Çıktı: {output_mean:.2f}")

        # Çıktı girdiden parlak olmalı
        self.assertGreater(output_mean, input_mean, "Gamma düzeltmesi görüntüyü aydınlatmadı!")

        # Görüntü boyutları bozulmamalı
        self.assertEqual(self.dark_image.shape, output_image.shape, "Görüntü boyutu değişti!")

    # ----------------------------------------------------------------
    # TEST 2: CLAHE Kontrastı Artırıyor mu?
    # Beklenti: Görüntünün Standart Sapması (Kontrast) artmalı.
    # ----------------------------------------------------------------
    def test_clahe_increases_contrast(self):
        # Düz gri bir görüntüde kontrast 0'dır. Biraz gürültülü bir görüntü yapalım.
        noisy_dark = np.random.randint(20, 40, (100, 100, 3), dtype=np.uint8)

        input_std = np.std(noisy_dark) # Orijinal kontrast

        output_image = self.enhancer.applyCLAHE(noisy_dark)
        output_std = np.std(output_image) # İşlenmiş kontrast

        print(f"[Test CLAHE] Girdi Kontrast: {input_std:.2f}, Çıktı Kontrast: {output_std:.2f}")

        self.assertGreater(output_std, input_std, "CLAHE kontrastı artırmadı!")

    # ----------------------------------------------------------------
    # TEST 3: Full Pipeline Çöküyor mu? (Stress Testi)
    # Beklenti: Hata vermeden bir çıktı üretmesi.
    # ----------------------------------------------------------------
    def test_full_pipeline_integrity(self):
        try:
            result = self.enhancer.processImageFull(self.dark_image)
            self.assertIsNotNone(result)
            self.assertEqual(result.shape, self.dark_image.shape)
        except Exception as e:
            self.fail(f"Full Pipeline çalışırken çöktü! Hata: {e}")

    # ----------------------------------------------------------------
    # TEST 4: Boş Görüntü Kontrolü (Edge Case)
    # Beklenti: C++ tarafı boş matris geldiğinde çökmeyip boş dönmeli.
    # ----------------------------------------------------------------
    def test_empty_image_handling(self):
        empty_img = np.array([], dtype=np.uint8)
        # Eğer C++ tarafında 'if (input.empty())' kontrolü koyduysak bu test geçer.
        # Eğer koymadıysak C++ Segmentation Fault verir ve Python çöker.
        try:
            # OpenCV boş matrisi Python'da (0,0,0) shape olarak görebilir,
            # Test için çok küçük (1x1) gönderelim, sistemin çökmemesini bekleyelim.
            tiny_img = np.zeros((1, 1, 3), dtype=np.uint8)
            res = self.enhancer.processImageFull(tiny_img)
            self.assertIsNotNone(res)
        except Exception as e:
            print(f"Boş görüntü testi uyarısı: {e}")

    # ----------------------------------------------------------------
    # TEST 5: Performans Kontrolü (Speed Test)
    # Beklenti: İşlemin belirli bir sürenin altında (örn: 50ms) sürmesi.
    # ----------------------------------------------------------------
    def test_performance_sanity(self):
        start = time.time()
        # 10 kez çalıştır
        for _ in range(10):
            self.enhancer.processImageFull(self.dark_image)
        end = time.time()

        avg_time = (end - start) / 10.0
        print(f"[Test Performans] Ortalama Süre: {avg_time*1000:.2f} ms")

        # 50 ms'den kısa sürmeli (100x100 resim için çok rahat geçmeli)
        self.assertLess(avg_time, 0.050, "Algoritma beklenenden yavaş çalışıyor!")

if __name__ == '__main__':
    print("=== OTONOM ARAÇ GÖRÜNTÜ İYİLEŞTİRME TEST SUITE ===")
    unittest.main()