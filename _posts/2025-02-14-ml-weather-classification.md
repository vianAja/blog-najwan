---
layout: post
title: Simple ML for Weather Classifications
subtitle: Simple Machine Learning for Weather Classifications using XGBoost
cover-img: /assets/img/wallpaper2.png
thumbnail-img: /assets/images/ml-weather-classification/weather-icon.jpg
share-img: /assets/img/wallpaper2.png
tags: ['Artificial Intelligence (AI)', 'XGBoost', 'Classification']
author: Najwan Octavian Gerrard
---

Pada Project ini saya membuat sebuah Machine Learning untuk memprediksi terkait cuaca pada sebuah negara, beserta diperlukan juga data seperti Temperature, kecepatan angin, tekanan atmosfer, UV Index UV, dll.Dan untuk tools yang saya gunakan untuk membuat model ML ini, memakai XGBoost

### What is XGBoost?

XGBoost (Extreme Gradient Boosting) adalah salah satu library algoritma Machine Learning yang menggunakan Decision Tree untuk melakukan Classification, Regression dan Ranking. XGBoost sendiri itu open source, jadi kita dapat melakukan training dan test model dengan data yang besar sekalipun secara gratis

**Benefit XGBoost :**
- **Execution Speed**, dari segi kecepatan sendiri itu cukup krusial, apa lagi jika memiliki dataset yang ssangat besar, kecepatan menjadi cukup penting, dengan menggunakan XGBoost, kita tidak perlu terlalu khawatir terkait kecepatannya, karena XGBoost sendiri tergolong cukup cepat walaupun menggunakan dataset yang besar.
- **Model Performance**, untuk segi performa model, XGBoost cukup unggul di bandingkan dengan beberapa algoritma lain seperti random forest (RF), gradient boosting machines (GBM), and gradient boosting decision trees (GBDT). Dan pastinya juga dalam membuat model yang kita cari itu terkait kinerja juga, kan tidak mungkin kita membuat model yang kinerjanya jelek.

jika ingin lebih lanjut mengetahui terkait XGBoost ini, anda dapat mengunjungi website resmi dari [XGBoost](https://xgboost.readthedocs.io/en/stable/).

Lalu lanjut untuk Project yang saya buat kurang lebih seperti ini langkah - langkahnya :

- Import Library pendukungnya.
  ```python
  from sklearn.model_selection import train_test_split
  from sklearn.metrics import accuracy_score
  from sklearn.preprocessing import LabelEncoder
  import numpy as np
  import pandas as pd
  import xgboost as xgb
  import os
  ```
  ---

- Import dataset yang akan digunakan untuk memubuat Machine Learningnya, untuk dataset nya bisa menggunakan yang dari repo github saya yang [ini](https://github.com/vianAja/Weather-Type-Classification)
  ```python
  df = pd.read_csv('weather_classification_data.csv')
  ```
  ---

- Inisialisasi untuk menggunakan data yang berbentuk string / kata menjadi angka numerik
  ```python
  encoder = LabelEncoder()
  ```
  ---

- Melakukan Transformasi data yang sebelumnya string / kata menjadi angka. Karena pada data yang saya gunakan yang bebentuk string hanya pada **Cloud Cover**, **Location**, **Season**, maka data itu akan saya ubah
  ```python
  df['Cloud Cover'] = encoder.fit_transform(df['Cloud Cover'])
  df['Location'] = encoder.fit_transform(df['Location'])
  df['Season'] = encoder.fit_transform(df['Season'])
  ```
  ---

- Melakukan Transformasi juga untuk data yang nantinya akan dibuat sebagai Target Data, karena untuk targetnya ini bertipe String, jadi harus di ubah dulu ke numerik
  ```python
  y_target = encoder.fit_transform(df["Weather Type"])
  ```
  ---

- Melakukan Pemisahan antara Data untuk Feature, dan Data untuk Target.
  ```python
  dataset = df[[i for i in df.columns[:-1]]]
  ```
  ---

- Kemudian di lanjutkan untuk pembagian dataset, yang nantinya akan digunakan untuk Training dan untuk Testing. Pada case kali ini saya ingin membaginya untuk Test size nya itu 20 % (sesuai parameter **test_size=0.2**).
  ```python
  x_train, x_test, y_train, y_test = train_test_split(
    dataset, 
    y_target,
    test_size=0.2,
    random_state=50
  )
  ```
  ---

- Kemudian selanjutnya yaitu menentukan parameter untuk model Machine Learning ini. Seperti ini kurang lebih keterangannya :
  - **objective: 'multi:softmax'** Untuk menentukan jenis klasifikasi. **'multi:softmax'** berarti model menggunakan softmax untuk klasifikasi multikelas.
  - **num_class: len(df.columns[:-1])** Untuk menentukan jumlah kelas dalam masalah klasifikasi. **df.columns[:-1]** mengambil semua kolom kecuali kolom terakhir (biasanya label/target).
  - **eta: 0.01** Untuk Learning rate, juga dikenal sebagai step size shrinkage. Nilai kecil (misalnya 0.01) membantu model belajar lebih lambat tetapi lebih stabil.
  - **max_depth: 6** Untuk menentukan kedalaman maksimum pohon keputusan dalam model. Kedalaman yang lebih besar dapat meningkatkan kapasitas model tetapi juga meningkatkan risiko overfitting.

  ```python
  parameters = {
      'objective':'multi:softmax',
      'num_class': len(df.columns[:-1]),
      'eta': 0.01,
      'max_depth': 6,
  }
  ```
  ---

- Melakukan Pembuatan Model dengan XGBClassifier, lalu save model ke file **XGBClassifier.json**.
  ```python
  model = xgb.XGBClassifier(
      parameters
  )
  model.fit(x_train, y_train)
  model.save_model("XGBClassifier.json")
  ```
  ---

- Melakukan Pengujian terkait Model nya, apakah bagus atau tidak. Untuk pengukurannya sendiri, semakin dekat angka accuracy dari model mendekati angka 1, maka model tersebut sangat baik. Jika angka nya di bawah 0.5, bisa di kategorikan model tersebut kurang layak digunakan, karena prediksi nya hampir banyak salah nya dari pada benarnya
  ```python
  pred = model.predict(x_test)
  accuracy = accuracy_score(y_test, pred)
  print("Accuracy:", accuracy)
  ```