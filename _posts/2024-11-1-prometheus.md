---
layout: post
title: Prometheus
subtitle: Explanation and Installation Prometheus
cover-img: /assets/img/wallpaper1.png
thumbnail-img: https://user-images.githubusercontent.com/92439/89548426-51fb0f00-d807-11ea-890f-afb3f9d8110a.png
share-img: /assets/img/wallpaper2.png
tags: [Prometheus]
author: Najwan Octavian Gerrard
---

Prometheus adalah salah satu tools monitoring system yang berbasis Cloud yang open source, yang lebih berfokus pada pengelolaan metrics dari suatu aplikasi atau system. Metrics sendiri merupakan data angka yang menunjukan performa atau nilai kinerja suatu aplikasi atau system.

### Keuntungan Menggunakan Prometheus

- **Fleksibilitas**, karena prometheus bisa untuk memantau berbagai sistem dan layanan, dari yang kecil sampai yang skala besar. Dan mudah di konfigurasikan dengan tools visualisasi atau alerting dengan cukup mudah.
- **Skalabilitas**, Prometheus dapat menangani metrics dalam jumlah besar, dan serta dapat juga diskalakan secara horizontal, yang berarti menambah mesin prometheus nya di suatu cluster Prometheus.

<br>

### Install dan Konfigurasi Prometheus

- Download Package Prometheus.
  ```bash
  ~$ sudo su
  ~# wget https://github.com/prometheus/prometheus/releases/download/v2.48.1prometheus-2.48.1.linux-amd64.tar.gz
  ~# tar -xvfz prometheus-2.48.1.linux-amd64.tar.gz
  ~# cp prometheus-2.48.1.linux-amd64/ /etc/prometheus
  ```
  
  ---
- Lalu Edit di file **_"/etc/prometheus/config.yml"_** untuk mengatur Targetsyang akan di Pantau.
  ```yaml
  global:
    scrape_interval: 15s
    evaluation_interval: 15s
  
  scrape_configs:
    - job_name: "NAME_JOB"
      static_configs:
      - targets: ["IP_TARGET:PORT"]
  ```

  ---
  
- Buat Service agar dapat berjalan di Background.
  ```bash
  ~$ sudo nano /etc/systemd/system/prometheus_server.service
  ```
  ```bash
  [Unit]
  Description=Prometheus Server
  [Service]
  User=root
  ExecStart=/etc/prometheus/prometheus \
      --config.file=/etc/prometheus/config.yml \
      --web.external-url=http://IP_SERVER:9090/ 
  [Install]
  WantedBy=default.target
  ```
  
  ---
- Restart Daemon dan jalankan Service Prometheus nya.
  ```bash
  ~$ sudo systemctl daemon-reload
  ~$ sudo systemctl start prometheus_server.service
  ~$ sudo systemctl enable prometheus_server.service
  ~$ sudo systemctl status prometheus_server.service
  ```
  
  ---

> Untuk Konfigurasi TLS/SSL pada Prometheus, bisa kunjungi Postingan saya berikut ini, **_[Secure Prometheus](https://vianaja.github.io/blog-najwan/2024-11-19-secure-prometheus/)_**.

Lalu setelah deployment Prometheus selesai, kalian bisa lanjut untuk mengkonfigurasi Alert Manager, apabila dibutuhkan. Sudah ada di Postingan saya yang [Alert Manager](https://vianaja.github.io/blog-najwan/2024-11-02-alert-manager/), di dalamnya disertakan penjelasn dan langkah konfigurasi.

Kemudian bila ingin di integrasikan dengan Grafana untuk data Visualisasinya, saya sudah membuatkan Postingan sendiri terkait itu, bisa cek di Postingan saya yang ini [Grafana](https://vianaja.github.io/blog-najwan/2024-10-30-grafana/).
