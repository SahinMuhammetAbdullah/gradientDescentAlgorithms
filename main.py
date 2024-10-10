# import pandas as pd
# import random


# # Excel dosyasını oku.
# df = pd.read_excel("data.xlsx")

# # İlk satırı atla (index 0'daki satırı atlayacağız) ve A sütununu (ID sütunu) hariç tut.
# veriler = df.iloc[0:, 1:].values

# # Xn değişkenine ata.
# X = veriler.tolist()

# # Satır sayısını al.
# satir_sayisi = df.shape[0]

# # Verileri kontrol etmek için yazdır.
# print(X[0])
# print(X[0][0])
# print(df.shape[1] - 1)
# print(df.shape[0])
# '''
# Maliyet formülü tanımı.
# i = 0
# Qn = [Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12]
# while i < df.shape[1] - 1
#     Qn[i] = random.uniform(1, max_deger)
#     i += 1

# while i < df.shape[0]:
#     Y[i] = X[i][0]

# while i < df.shape[0]:
#     Hq[i] = Q0 + Q1*X[i][1] + Q2*X[i][2] + Q3*X[i][3]+ Q4*X[i][4]+ Q5*X[i][5]+ Q6*X[i][6]+ Q7*X[i][7]+ Q8*X[i][8]+ Q9*X[i][9]+ Q10*X[i][10]+ Q11*X[i][11]+ Q12*X[i][12]
#     Y = X[i][0]
#     Maliyet = (Hq[i] - Y[i])**2
#     Maliyet = Maliyet * (1/(2*df.shape))
    
# a = 0.03 # çalışma zamanının uzunluğuna bağlı 3 ile çarpılarak artırılabilir.

# while i < Qn.len:
#     Qn[i] = Qn[i] - a* ((Qn[i] ile türevlenmesi)(Maliyet))

# Tempn = [Temp0,Temp1,Temp2,Temp3,Temp4,Temp5,Temp6,Temp7,Temp8,Temp9,Temp10,Temp11,Temp12]

# while i < Qn.len:
#     Tempn[i] = Qn[i] - a* ((Qn[i] ile türevlenmesi)(Maliyet))

# while i < Qn.len:
#     Qn[i] = Tempn[i]
# '''
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler

# Excel dosyasını oku ve verileri normalize et
df = pd.read_excel("data.xlsx")
scaler = MinMaxScaler()
veriler_normalize = scaler.fit_transform(df.iloc[:, 1:].values)
X = veriler_normalize.tolist()

# Satır ve sütun sayısını al
satir_sayisi = df.shape[0]
sutun_sayisi = df.shape[1] - 1

# Daha küçük başlangıç Qn değerleri
Qn = [random.uniform(0, 1) for _ in range(sutun_sayisi)]

# Maliyet fonksiyonu
def maliyet_fonksiyonu(X, Qn):
    toplam_maliyet = 0
    for i in range(satir_sayisi):
        Hq = sum(Qn[j] * X[i][j] for j in range(1, sutun_sayisi)) + Qn[0]
        Y = X[i][0]
        maliyet = (Hq - Y) ** 2
        toplam_maliyet += maliyet
    return toplam_maliyet / (2 * satir_sayisi)

# Gradyan hesaplama
def gradyan_hesapla(X, Qn):
    grad = [0] * len(Qn)
    for i in range(satir_sayisi):
        Hq = sum(Qn[j] * X[i][j] for j in range(1, sutun_sayisi)) + Qn[0]
        Y = X[i][0]
        fark = Hq - Y
        grad[0] += fark
        for j in range(1, sutun_sayisi):
            grad[j] += fark * X[i][j]
    grad = [g / satir_sayisi for g in grad]
    return grad

# Gradyan inişi
def gradient_descent(X, Qn, ogrenme_orani, iterasyon_sayisi):
    en_dusuk_maliyet = float('inf')  # Sonsuz maliyet değeri ile başla
    en_iyi_iterasyon = 0  # En iyi iterasyon numarasını izlemek için
    en_iyi_Qn = Qn  # En düşük maliyete ulaşıldığında Qn değerlerini saklamak için

    for iterasyon in range(iterasyon_sayisi):
        grad = gradyan_hesapla(X, Qn)
        Qn = [Qn[i] - ogrenme_orani * grad[i] for i in range(len(Qn))]
        
        maliyet = maliyet_fonksiyonu(X, Qn)
        
        # Her 100 iterasyonda bir maliyeti yazdır
        if iterasyon % 100 == 0:
            print(f"Iterasyon {iterasyon}, Maliyet: {maliyet}")
        
        # En düşük maliyeti kontrol et ve güncelle
        if maliyet < en_dusuk_maliyet:
            en_dusuk_maliyet = maliyet
            en_iyi_iterasyon = iterasyon
            en_iyi_Qn = Qn.copy()  # En iyi Qn değerlerini sakla
    
    print(f"En düşük maliyet {en_dusuk_maliyet} değerine {en_iyi_iterasyon}. iterasyonda ulaşıldı.")
    return en_iyi_Qn

# Öğrenme oranı ve iterasyon sayısı
ogrenme_orani = 0.001
iterasyon_sayisi = 1000

# Gradyan inişi çalıştır
Qn_optimal = gradient_descent(X, Qn, ogrenme_orani, iterasyon_sayisi)
print("Optimum Qn:", Qn_optimal)
