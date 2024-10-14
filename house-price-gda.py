import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
import pickle

# Excel dosyasını oku
df = pd.read_excel("data2.xlsx")

# Sütun isimlerini yazdır
print("Sütun İsimleri:", df.columns)

# StandardScaler oluştur
scaler = StandardScaler()

# Fiyat, Yaşam Alanı ve Oda Sayısı sütunlarını normalize et
veriler_normalize = scaler.fit_transform(df[['price', 'sqft_living', 'bedrooms']])

# Normalizasyon öncesi ilk satırdaki veriyi yazdır
print("Normalizasyon öncesi ilk satır:")
print(df.iloc[0, 1:4].values)  # B, C, D sütunları (Fiyat, Yaşam Alanı, Oda Sayısı)

# Normalize edilmiş ilk satırdaki veriyi yazdır
print("\nNormalize edilmiş ilk satır:")
print(veriler_normalize[0])

# İlk satırı geri normalize et (orijinal haline dönüştür)
ilk_satir_geri_donusum = scaler.inverse_transform([veriler_normalize[0]])

# Geri normalize edilmiş ilk satırdaki veriyi yazdır
print("\nGeri normalize edilmiş ilk satır:")
print(ilk_satir_geri_donusum[0])

# Verileri ayır (X: yaşam alanı ve oda sayısı, Y: fiyat)
X = veriler_normalize[:, 1:3]  # Girişler: yaşam alanı ve oda sayısı (C ve D sütunları)
Y = veriler_normalize[:, 0]  # Çıkış: fiyat (B sütunu)

# Satır sayısını al
satir_sayisi = df.shape[0]

# Başlangıç Q değerlerini rastgele ata
Q0 = random.uniform(0, 1)
Q1 = random.uniform(0, 1)
Q2 = random.uniform(0, 1)

# Maliyet fonksiyonu
def maliyet_fonksiyonu(X, Y, Q0, Q1, Q2):
    toplam_maliyet = 0
    for i in range(satir_sayisi):
        Hq = Q0 + Q1 * X[i][0] + Q2 * X[i][1]
        maliyet = (Hq - Y[i]) ** 2
        toplam_maliyet += maliyet
    return toplam_maliyet / (2 * satir_sayisi)

# Gradyan hesaplama
def gradyan_hesapla(X, Y, Q0, Q1, Q2):
    grad_Q0, grad_Q1, grad_Q2 = 0, 0, 0
    for i in range(satir_sayisi):
        Hq = Q0 + Q1 * X[i][0] + Q2 * X[i][1]  # Tahmin (hipotez fonksiyonu)
        fark = Hq - Y[i]  # Hata hesaplama (Hq - gerçek değer)

        # Gradyanların hesaplanması:
        grad_Q0 += fark  # Q0'a göre türev
        grad_Q1 += fark * X[i][0]  # Q1'e göre türev
        grad_Q2 += fark * X[i][1]  # Q2'ye göre türev

    # Ortalama gradyan değerleri:
    grad_Q0 /= satir_sayisi
    grad_Q1 /= satir_sayisi
    grad_Q2 /= satir_sayisi
    return grad_Q0, grad_Q1, grad_Q2

# Gradyan inişi
def gradient_descent(X, Y, Q0, Q1, Q2, ogrenme_orani, iterasyon_sayisi):
    for iterasyon in range(iterasyon_sayisi):
        grad_Q0, grad_Q1, grad_Q2 = gradyan_hesapla(X, Y, Q0, Q1, Q2)
        Q0 -= ogrenme_orani * grad_Q0
        Q1 -= ogrenme_orani * grad_Q1
        Q2 -= ogrenme_orani * grad_Q2

        maliyet = maliyet_fonksiyonu(X, Y, Q0, Q1, Q2)
        if iterasyon % 100 == 0:
            print(f"Iterasyon {iterasyon}, Maliyet: {maliyet}")
            print(f"Q0: {Q0}, Q1: {Q1}, Q2: {Q2}")
    return Q0, Q1, Q2

# Öğrenme oranı ve iterasyon sayısı
ogrenme_orani = 0.001
iterasyon_sayisi = 1000

# Gradyan inişi çalıştır
Q0_optimal, Q1_optimal, Q2_optimal = gradient_descent(X, Y, Q0, Q1, Q2, ogrenme_orani, iterasyon_sayisi)
print(f"Optimum Q0: {Q0_optimal}, Q1: {Q1_optimal}, Q2: {Q2_optimal}")

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

    # Kullanıcıdan kaydetme isteğini al
    kaydetme_onayi = input("Modeli kaydetmek ister misiniz? (Evet için 'e', Hayır için 'h'): ").lower()
    if kaydetme_onayi == 'e':
        # Modelin kaydedileceği dosya ismini al
        dosya_ismi = input("Modeli kaydetmek için bir dosya ismi girin (örn: model.pkl): ")
        dosya_ismi = dosya_ismi +".pkl"
        with open(dosya_ismi, "wb") as file:
            pickle.dump((Q0_optimal, Q1_optimal, Q2_optimal, scaler), file)
            print(f"Model '{dosya_ismi}' adıyla başarıyla kaydedildi.")
    else:
        print("Model kaydedilmedi.")

# Modeli test et
test_model(Q0_optimal, Q1_optimal, Q2_optimal)
