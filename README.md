# Gradient Descent Algorithms
Bu repo Ondokuz Mayıs Üniversitesi Makine Öğrenimine Giriş dersi 1. ödev için oluşturulmuştur.
Ödev kapsamında Gradient Descent Algoritması kullanılarak en az 2 boyutlu (X1, X2, ..., Xn) bir veri seti üzerinde python programlama dili kullanılarak kullanılarak gerçeklenmesi istenmiştir.

## Bağımlılıklar

### Pandas
Pandas, Python için veri analizi ve manipülasyonu sağlayan güçlü bir kütüphanedir. Verilerin kolay bir şekilde işlenmesine olanak tanır, özellikle tablo formatındaki verilerle (DataFrame) çalışırken oldukça etkilidir.

Bende bunu excel tablolarını okuyabilmek için kodlarım arasında kullandım.
```shell
pip install pandas 
```
Yukarıdaki shell komutu ile indirilip

```python
import pandas as pd
```
komutu ile kodumuzda bağımlılık olarak kullanılmıştır.

### Random

Katsayılarımıza rastgele değerlerden başlaması adına Random kütüphanesinden yararlanılmıştır

```python
import random
```
komutu ile kodumuzda bağımlılık olarak kullanılmıştır.

### Sklearn

Scikit-learn, makine öğrenimi için yaygın olarak kullanılan bir kütüphanedir. Veri ön işleme, model oluşturma, model değerlendirme ve daha birçok makine öğrenimi görevi için araçlar sunar.

Bizde normalizasyon işlemleri için kodlarımız arasında **Sklearn** yer verdik.
```shell
pip install sklearn 
```
Yukarıdaki shell komutu ile indirilip

```python
from sklearn.preprocessing import StandardScaler
```
komutu ile kodumuzda bağımlılık olarak kullanılmıştır.

### Pickle

Pickle, Python nesnelerini serileştirmek (diskte dosya olarak saklamak) ve serileştirilmiş nesneleri geri yüklemek için kullanılan yerleşik bir kütüphanedir. Bu sayede, oluşturulan modellerin ve veri yapıların kolaylıkla kaydedilmesi ve daha sonra yüklenmesi sağlanır.


Bizde değerlendirme sonucu modelimizi kaydetmek adına bu pakete kodlarımız arasında yer verdik
```shell
pip install pickle 
```
Yukarıdaki shell komutu ile indirilip

```python
import pickle
```
komutu ile kodumuzda bağımlılık olarak kullanılmıştır.

## Veri Seti
[Data dosyası 1](/data1.xlsx) ve [Data dosyası 2](/data2.xlsx) içerisindeki veriler [Keggle](https://www.kaggle.com/datasets/shree1992/housedata)'dan alınmış ve düzenlemeler yapılarak kullanılmıştır.

## Kullanım

Ev fiyatlarını araştırdığımız bu projede [house-price-gda.py](house-price-gda.py) dosyamızda bulunan kodu çaılştırdığımızda bizlere iterasyon dönüşlerini ve bu dönüşlerin (Her 100 dönüşte bir) optimum Qn değerlerinin dönüşlerini vermekte.

1000\. itarasyon sonucu oluşan değerler ise ulaşılan en optimum değeri bizlere göstermekte.

Bunun sonucunda derleme sonucu oluşan optimum Qn değerleri ile modelimizi test edmek için giriş bekleyen bir fonksiyonumuz bulunmakta. Bunun amacı biz her derleme sonucunda farklı bir local minimum değere ulaşmış olabiliriz. Bunu test ederek en yakın sonuçları veren değere ulaşınca bizden bu modeli kayderek yeniden kullanıma sunmakdayız. Bunun için modeli kaydettikten sonra [run.py](run.py) çalıştırarak optimum modeli tekrar kullanabilmekteyiz.