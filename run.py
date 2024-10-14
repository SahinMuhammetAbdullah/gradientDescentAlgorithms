import pandas as pd
import pickle

# Pickle dosyasını aç
dosya_ismi = input("Model ismini giriniz: ")  # Kaydedilen model dosyasının ismi
dosya_ismi = dosya_ismi +".pkl"

try:
    with open(dosya_ismi, "rb") as file:
        Q0_optimal, Q1_optimal, Q2_optimal, scaler = pickle.load(file)
except FileNotFoundError:
    print(f"Dosya '{dosya_ismi}' bulunamadı. Lütfen dosya adını ve yolunu kontrol edin.")

# Test fonksiyonu
def test_model(Q0, Q1, Q2):
    print("\nTest için giriş yapın (Çıkmak için 'q' yazın):")
    
    while True:
        # Kullanıcıdan test verilerini al
        yasam_alani = input("Yaşam alanı (sqft) için bir değer girin: ")
        if yasam_alani.lower() == 'q':
            print("Testten çıkılıyor...")
            break
        yatak_odasi_sayisi = input("Yatak odası sayısı için bir değer girin: ")
        if yatak_odasi_sayisi.lower() == 'q':
            print("Testten çıkılıyor...")
            break
        
        # Girilen değerleri float'a çevir
        try:
            yasam_alani = float(yasam_alani)
            yatak_odasi_sayisi = float(yatak_odasi_sayisi)
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue

        # Test verisini normalize etmek için önce bir DataFrame'e dönüştür
        test_verisi_df = pd.DataFrame([[0, yasam_alani, yatak_odasi_sayisi]], columns=['price', 'sqft_living', 'bedrooms'])

        # Test verisini normalize et
        test_verisi = scaler.transform(test_verisi_df)[0][1:]

        # Tahmini hesapla (normalize edilmiş hali)
        tahmin_normalize = Q0 + Q1 * test_verisi[0] + Q2 * test_verisi[1]
        
        # Tahmini normal değere dönüştür
        tahmin = scaler.inverse_transform([[tahmin_normalize, yasam_alani, yatak_odasi_sayisi]])[0][0]
        tahmin = int(tahmin)
        print(f"Model tahmini (normal değer): {tahmin}")
        continue

# Modeli test et
test_model(Q0_optimal, Q1_optimal, Q2_optimal)
