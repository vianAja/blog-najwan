---
layout: post
title: Alert Manager
subtitle: Explanation and Installation Alert Manager Prometheus
cover-img: /assets/img/wallpaper1.png
thumbnail-img: https://user-images.githubusercontent.com/92439/89548426-51fb0f00-d807-11ea-890f-afb3f9d8110a.png
share-img: /assets/img/wallpaper1.png
tags: [Prometheus, Alert Manager]
author: Najwan Octavian Gerrard
---

Exporter Prometheus adalah suatu tools yang digunakan untuk mengubah data metrics dari suatu layanan aplikasi atau sistem yang tadinya tidak bisa di baca oleh Prometheus menjadi bisa di baca, bertindak sebagai perantara untuk layanan yang di pantau dengan Prometheus.

#### Fitur yang ada di Grafana

- Visualisasi, Grafana menediakan beberapa pilihan visualisasi, yang dapat membantu untuk memahami data dengan lebih mudah, dan cepat
- Alerting, Grafana juga menyediakan fitur alerting, yang dimana nanti dapat di integrasikan ke beberapa saluran notifikasi seperti Email, Slack, Telegram dll.

<br>

## Installations

- Download Package Grafana, lalu pindahkan ke **_/etc_**.
  ```bash
  sudo su
  wget https://dl.grafana.com/oss/release/grafana-11.2.2.linux-amd64.tar.gz
  tar -zxvf grafana-v11.2.2.linux-amd64.tar.gz
  cp grafana-v11.2.2.linux-amd64/etc/grafana
  ```
  
  ---
- Atur di Prometheus untuk menggunakan Alert Manager di file **_"/etc/prometheusconfig.yml"_**.
  ```yaml
  alerting:
    alertmanagers:
      - static_configs:
          - targets:
            - IP_ALERT_MANAGER:PORT
  ```
  
  ---
- Atur untuk File Rules / aturan yang akan digunakan untuk alerting di file **_"etc/prometheus/config.yml"_**.

  ```yaml
  rule_files:
  - "FILE_RULES.yml"
  ```

  ---

- Konfigurasi untuk Alert Managernya untuk mengirim notifikasi ke mana. sebagai contoh saya menggunakan Alerting ke Email, untuk lebih detailnya terkait bisa di hubungkan dengan apa saja, bisa kunjungi website resmi dari [Prometheus](https://prometheus.io/docs/alerting/latest/configuration/#receiver) nya. 
  ```yaml
  global:
    resolve_timeout: 15s
  
  route:
    receiver: email
  
  receivers:
  - name: email
    email_configs:
    - to: "email@test.id"
      from: "email@test.id"
      smarthost: smtp.gmail.com:587
      auth_username: "email@test.id"
      auth_identity: "email@test.id"
      auth_password: "TOKEN_EMAIL"
      send_resolved: True
  ```
  
  ---
- Konfigurasi untuk rules yang mentrigger alert manager mengirim notifikasi.
  Rules untuk Web Server Apache atau Nginx yang Down.

  ```yaml
  groups:
  - name: NAME_RULES
    rules:
    - alert: NAME_ALERT
      expr: METRICS_UNTUK_ALERT
      for: 1m
      annotations:
        summary: "SUMMARY FOR ALERT"
        description: "DESCRIPTIONS FOR ALERT."
  ```
  
  ---
- Lalu buat service, agar dapat berjalan di background.
  ```bash
  sudo nano /etc/systemd/system/alert_manager.service
  ```
  ```bash
  [Unit]
  Description=Alert Manager
  
  [Service]
  User=root
  ExecStart=/etc/alertmanager/alertmanager \
          --config.file=/etc/alertmanager/config.yml \
          --web.external-url=http://IP_SERVER:9093/ \
          --log.level=debug
  
  [Install]
  WantedBy=default.target
  ```
  
  ---
- Restart Daemon dan jalankan Service Alert Manager nya.
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl start alert_manager.service
  sudo systemctl enable alert_manager.service
  sudo systemctl status alert_manager.service
  ```

  ---
