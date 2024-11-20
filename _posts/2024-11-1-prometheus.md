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

### Keuntungan Menggunakan Prometheus:
- **Fleksibilitas**, karena prometheus bisa untuk memantau berbagai sistem dan layanan, dari yang kecil sampai yang skala besar. Dan mudah di konfigurasikan dengan tools visualisasi atau alerting dengan cukup mudah.
- **Skalabilitas**, Prometheus dapat menangani metrics dalam jumlah besar, dan serta dapat juga diskalakan secara horizontal, yang berarti menambah mesin prometheus nya di suatu cluster Prometheus.


### Install dan Konfigurasi Prometheus dengan SSL
  - Download Package Prometheus.
    ```bash
    sudo su
    wget https://github.com/prometheus/prometheus/releases/download/v2.48.1/prometheus-2.48.1.linux-amd64.tar.gz
    tar -xvfz prometheus-2.48.1.linux-amd64.tar.gz
    cp prometheus-2.48.1.linux-amd64/ /etc/prometheus
    ```
    
  - Lalu Edit di file **_"/etc/prometheus/config.yml"_** untuk mengatur Targets yang akan di Pantau.
    ```yaml
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    scrape_configs:
      - job_name: "NAME_JOB"
        static_configs:
        - targets: ["IP_TARGET:PORT"]
    ```
    
  - Atur untuk Alerting, menggunakan Alert Manager di file **_"/etc/prometheus/config.yml"_**.
    ```yaml
    alerting:
      alertmanagers:
        - static_configs:
            - targets:
              - IP_ALERT_MANAGER:PORT
    ```
    
  - Atur untuk File Rules / aturan yang akan digunakan untuk alerting di file **_"/etc/prometheus/config.yml"_**.
    
    ```yaml
    rule_files:
      - "FILE_RULES.yml"
    ```

  - Buat Service agar dapat berjalan di Background.
    ```bash
    sudo nano /etc/systemd/system/prometheus_server.service
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
    
  - Restart Daemon dan jalankan Service Prometheus nya.
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start prometheus_server.service
    sudo systemctl enable prometheus_server.service
    sudo systemctl status prometheus_server.service
    ```
    
Untuk Konfigurasi TLS/SSL pada Prometheus, bisa ke Postingan Blog saya berikut ini, **_[Secure Prometheus](https://vianaja.github.io/blog-najwan/2024-11-19-secure-prometheus/)_** pada Langkah Implementasi nomor 9. 
