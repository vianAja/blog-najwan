---
layout: post
title: Simple Machine Learning
subtitle: Simple Machine Learning for Weather Classifiers
cover-img: /assets/img/wallpaper2.png
thumbnail-img: https://ant.ncc.asia/wp-content/uploads/2024/05/docker.png
share-img: /assets/img/wallpaper2.png
tags: 2025-02-14
author: Najwan Octavian Gerrard
---

Di zaman yang serba canggih seperti sekarang ini, sudah sangat marak sekali yang namanya kecerdasan buatan atau Artificial Intelligence (AI), yang mana AI sendiri itu memiliki beberapa jenis juga, sebagaimana berikut ini :

- Machine learning
- Deep learning
- Natural Language Processing (NLP)
- Computer Vision
- Reinforcement Learning
- Robotics
- Speech Recognition

Pada blog ini, saya akan sedikit menerangkan terkait salah satu jenis kecerdasan buatan atau Artificial Intelligence (AI) yaitu Machine Learning (ML).

## Machine Learning (ML)?
Machine Learning (ML) sendiri merupakan cabang dari kecerdasan buatan atau Artificial Intelligence (AI) yang memungkinkan komputer untuk belajar dari data tanpa harus diprogram secara eksplisit atau secara mudahnya kita tidak perlu memberikan perintah misalkan suatu function akan menghasilkan penambahan, jadi saat saya mengisikan data 1 dan 4, akan menghasilkan nilai 5 (karena function penambahan). Dengan ML, komputer dapat mengenali pola, membuat prediksi, dan mengambil keputusan berdasarkan data yang diberikan.

**Proses kerja Machine Learning melibatkan beberapa langkah:**

1. Pengumpulan Data – Data dikumpulkan dari berbagai sumber, seperti sensor, database, atau teks.
2. Preprocessing Data – Data dibersihkan, diubah, dan disiapkan agar bisa digunakan oleh model ML.
3. Pemilihan Model – Memilih algoritma yang sesuai, seperti regresi, decision tree, atau neural networks.
4. Pelatihan Model – Model dilatih dengan menggunakan dataset, di mana ia belajar untuk mengenali pola dan membuat prediksi.
5. Evaluasi Model – Model diuji untuk mengukur kinerjanya dengan data yang belum pernah dilihat sebelumnya.
6. Deployment & Penggunaan – Model yang sudah terlatih digunakan dalam sistem nyata untuk melakukan tugas tertentu.

## Jenis Machine Learning
### 1. Supervised Learning
Supervised Learning adalah salah satu terknik Machine Learning (ML) yang menggunakan data berlabel untuk malatih Algoritma atau Model ML nya. Model ini nantinya akan dapat melakukan prediksi sesuai pola yang ada pada data tersebut.

Type Supervised Learning :
- Classification
  Classification merupakan tipe Supervised Learning yang mana nantinya algoritma ini akan mengelompokan atau grouping data sesuai kategori label atau sesuai variable output yang di hasilkan dari data inputnya.
  Contoh:
  **Classification Email spam**
  Dimana nantinya akan mengelompokan mana kategori email yang spam dan email yang penting

  ---

- Regresion
  Regresion merupakan tipe Supervised Learning yang akan memprediksi nilai numerik continuation berdasarkan hubungan antara variabel input dan output.
  Contoh:
  **Prediksi harga rumah berdasarkan luas tanah dan lokasi rumah**
  Apabila luas tanah semakin luas, otomatis harganya akan mahal juga, begitu juga dengan lokasinya, apabila di dataran tinggi akan semakin mahal misalkan. Data itu semua akan di kalkulasi oleh Regression ini.


### 2. Unsupervised Learning
Model belajar dari data yang tidak memiliki label dan mencoba menemukan pola tersembunyi.
Contoh algoritma: K-Means Clustering, Principal Component Analysis (PCA).
Contoh kasus: Segmentasi pelanggan berdasarkan perilaku belanja.

### 3. Reinforcement Learning
Model belajar dengan mencoba berbagai aksi dan mendapatkan reward atau punishment.
Contoh algoritma: Q-Learning, Deep Q-Network (DQN).
Contoh kasus: Game AI, robot otonom, trading saham otomatis.