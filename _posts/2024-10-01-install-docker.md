---
layout: post
title: Docker Container
subtitle: Explanation and Installation Docker Container 
cover-img: /assets/img/wallpaper2.png
thumbnail-img: https://ant.ncc.asia/wp-content/uploads/2024/05/docker.png
share-img: /assets/img/wallpaper2.png
tags: [Docker]
author: Najwan Octavian Gerrard
---

Docker adalah salah satu platform software yang digunakan untuk membuat, mengelola aplikasi yang nantinya dikemas dalam sebuah wadah yang terisolasi yaitu container. Docker nantinya akan mengemas aplikasi berserta dependensi yang diperlukan dalam satu paket yang ringan. Sehingga dapat dijalankan secara konsisten tanpa mengubah konfigurasi.

### Container

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Container adalah sebuah unit yang mengemas code dan semua dependensinya. Sehingga dapat berjalan atau berpindah environment dengan lebih cepat dan efisien. Container tersebut sangat ringan tidak seperti Virtual Machine (VM) yang memerlukan OS untuk setiap VM nya, karena dalam container hanya berisikan source code dan dependensinya saja, jadi memungkinkan menginstal apa yang di perlukan saja.

### Kelebihan

- Portabilitas, kemampuan untuk menjalankan aplikasi dalam container yang sama di beberapa lingkungan (seperti cloud) tanpa perlu merubah konfigurasi yang banyak.
- Penggunaan resource yang efisien. Dari pada menggunakan Virtual Machine (VM), container docker lebih ringan karena tidak perlu hypervisor.
  
### Kekurangan

- Kompatibilitas terbatas antar OS, walaupun selain di linux masih bisa digunakan, akan tetapi secara performanya tidak sebaik di Linux.
- Kompleksitas orchestration, docker menggunakan tools Docker Swarm yang cukup sulit bagi pemula yang baru belajar.

### Installations

- Update Package, install package untuk curl dan certificate.
  ```bash
  sudo apt-get update
  sudo apt-get install ca-certificates curl -y
  ```

  ---
- Mengatur untuk kunci GPG docker, agar memastikan bahwa source code Docker nya itu legal.
  ```bash
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  ```
  
  ---
- Menambahkan Repositori docker agar dapat di install
  ```bash
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  ```

  ---
- Install Docker.
  ```bash
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
  ```
  
  ---
- Mengatur agar user **_“biasa”_** atau user biasa (Bukan Root) dapat menggunakan perintah docker
  ```bash
  sudo usermod -aG docker $USER
  sudo chmod 666 /var/run/docker.sock
  docker version
  ```
  
  ---
