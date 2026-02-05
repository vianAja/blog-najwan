---
layout: post
title: Permanent Mounting S3 in Ubuntu Ec2 via fstab
subtitle: Explanation and Configure Mounting 
cover-img: /assets/img/wallpaper6.webp
thumbnail-img: https://miro.medium.com/v2/resize:fit:1200/1*Qz8qHl2TEWNK_1rmPZ-t-A.png
share-img: /assets/img/wallpaper6.webp
tags: [Aws, Ec2, Ubuntu, S3]
author: Najwan Octavian Gerrard
---

### Konfigurasi untuk Ubuntu 24.04
- Install dependencies yang dibutuhkan
  ```bash
  sudo snap install aws-cli --classic
  sudo apt install s3fs fuse -y
  ```
  ---
  
- Konfigurasi untuk credential yang akan diperlukan untuk menghubungkan ke S3 nya, [**referensi**](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md) yang bisa digunakan, ada 3 tipe, yaitu:
  - Menggunakan **aws configure**, atau di file **.aws/credentials**. Untuk tipe ini biasanya sering digunakan apa bila akun yang di miliki itu memiliki **_token_session_**, atau akun aws academy yang sifatnya temporary, karena untuk tipe lain tidak bisa jika dengan akun yang ada **_token_session_**, atau akun aws academy yang sifatnya temporary.
  - Menggunakan file **$HOME.passwd-s3fs** yang di isikan **ACCESS_KEY_ID:SECRET_ACCESS_KEY** dengan permission / hak akses 600.
  - Menggunakan file **/etc/passwd-s3fs** yang di isikan **ACCESS_KEY_ID:SECRET_ACCESS_KEY** dengan permission / hak akses 640.
  - Menggunakan environment variables **AWS_ACCESS_KEY_ID** dan **AWS_SECRET_ACCESS_KEY** yang nanti akan secara otomatis di baca oleh s3fs.
  Sebagai contoh saya menggunakan yang pertama atau yang  **aws configure**, atau di **.aws/credentials**. Karena pada Kesempatan kali ini saya menggunakan akun aws academy yang sifatnya temporary.
  ---
  
- untuk lebih mempermudah, hubungkan Ec2 ke IAM yang sesuai, bisa buat IAM baru akan tetapi harus yang ada permission untuk akses ke S3, atau pakai yang sudah ada, untuk kali ini saya menggunakan bawaan yang sudah ada, karena pakai akun academy
  
  ---
  
- Kemudian coba untuk connect ke S3 secara manual dulu. Untuk **iam_role=auto** akan menyesuaikan IAM yang terhubung di Ec2 nya.
  ```bash
  s3fs bucket-name directory-mount -o iam_role=auto
  ```
  example:
  ```bash
  s3fs test-bucket /etc/test-s3 -o iam_role=auto
  ```
  ---
  
- Kemudian cek dulu apakah berhasil atau gagal. Bisa pilih salah satu.
  ```bash
  df -h
  ```
  Kalau untuk lebih detail bisa pakai perintah ini, untuk fungsinya sama, untuk mengecek apakah mounting nya berhasil atau tidak.
  ```bash
  mount
  ```
  ---
  
- Kemudian setelah di pastikan bisa, berarti credentials yang di atur sudah sesuai. Kemudian lanjut untuk konfigurasi di fstab agar permanent saat reboot ec2 tidak lepas. Konfigurasi seperti berikut ini.
  ```bash
  sudo nano /etc/fstab
  ```
  ```bash
  s3fs#bucket-name:/ /dir-mount fuse _netdev,allow_other,nonempty,iam_role=auto 0 0
  ```
  _Atau bisa juga pakai format seperti ini, sama saja_
  ```bash
  bucket-name:/ /dir-mount fuse.s3fs _netdev,allow_other,nonempty,iam_role=auto 0 0
  ```
  ---
  - Opsi **_netdev** digunakan untuk menandakan bahwa block device terhubung lewat networking.
  - Opsi **allow_other** digunakan untuk agar user lain dapat menggunakan block device itu, tidak terbatas user tertentu.
  - Opsi **nonempty** digunakan untuk mengizinkan mounting saat directory yang di pakai mounting ada isi nya, atau ada file di dalam directory itu.
  - Opsi **iam_role=auto** akan melakukan verifikasi menggunakan iam role yang di pasang ke Ec2 nya, jadi otomatis menyesuaikan. **_Wajib ada, jika tidak akan error credential_**.
  
  Pastikan untuk tidak melupakan bagian titik dua setelah nama bucket nya, karena nanti akan ada error [**_s3fs -- bucket name contains illegal character_**](https://stackoverflow.com/questions/64584917/s3fs-bucket-name-contains-illegal-character). Dan di belakangnya menyesuaikan prefix yang di S3 nya, jadi jika ada folder di S3 misalkan folder **"test"**, bisa dibuat spesifik ke folder tersebut dengan **"bucket-name:/test"**.

  Example:
  ```bash
  s3fs#test-bucket:/ /etc/test-s3 fuse _netdev,allow_other,nonempty,iam_role=auto 0 0
  ```
  ---
  
- Lalu Konfigurasi untuk fuse nya, karena pada konfigurasi saya pakai **allow_other** untuk agar dapat di akses siapa saja, saya perlu setting di bagian **/etc/fuse.conf** hapus tanda pager **"#"** di **user_allow_other**.
  ```yaml
  user_allow_other
  ```
  ---

- Lalu restart systemd
  ```bash
  sudo systemctl daemon-reload
  ```
  ---
  
- Kemudian cek konfigurasi nya apakah berhasil atau ada yang salah. Kalau berhasil akan mengeluarkan Output seperti di bawah ini, dan kalau ada error juga nanti akan ada keterangan nya juga, jadi lebih mudah untuk solving error nya, tanpa harus reboot Ec2 nya dan jika salah bisa ada kemungkinan rusak juga.
  ```bash
  mount -fav
  
  /etc/test-s3   : successfully mounted
  ```
  ---

- Jika menemukan error tidak dapat mount padahal sudah di cek dengan **"mount -fav"** sudah **"successfully mounted"**, coba cek dengan perintah ini.
  ```bash
  sudo journalctl -b | grep mount
  ```
  Dan coba cek apakah ada error, seperti contoh jika tidak menggunakan opsi **iam_role**, akan ada error seperti ini.
  ```bash
  ... systemd[1]: Mounting home-ubuntu-testaja.mount - /home/ubuntu/testaja...
  ... mount[537]: s3fs: could not determine how to establish security credentials.
  ... systemd[1]: Mounted home-ubuntu-backup\x2ds3.mount - /home/ubuntu/backup-s3.
  ... systemd[1]: home-ubuntu-testaja.mount: Mount process exited, code=exited, status=1/FAILURE
  ... systemd[1]: home-ubuntu-testaja.mount: Failed with result 'exit-code'.
  ... systemd[1]: Failed to mount home-ubuntu-testaja.mount - /home/ubuntu/testaja.
  ```
  ---


### Konfigurasi jika menggunakan Ubuntu 20.04
- update IMDSv2 (Instance MetaData Service) dari yang tadinya IMDSv2, menjadi IMDSv1 dan v2
