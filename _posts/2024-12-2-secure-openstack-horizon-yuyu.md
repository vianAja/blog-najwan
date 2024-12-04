---
layout: post
title: Secure Service OpenStack and Yuyu Biliing OpenStack with TLS
subtitle: Explanation and Implementation Project Secure Service OpenStack and Yuyu Biliing OpenStack with TLS
cover-img: /assets/img/wallpaper2.png
thumbnail-img: https://banner2.cleanpng.com/20180602/jkl/avoucosdm.webp
share-img: /assets/img/wallpaper2.png
tags: [Project ,OpenStack, Container, Apache, Python]
author: Najwan Octavian Gerrard
---
Perusahaan pada zaman modern saat ini telah mengimplementasikan private cloud menggunakan OpenStack untuk mengelola infrastruktur TI secara lebih fleksibel dan efisien. Namun, dalam operasional sehari-hari, tantangan sering muncul terkait dengan pengelolaan sumber daya dan meminimalkan risiko human error, terutama ketika pengembang melakukan pengujian pada lingkungan yang sama dengan produksi. Risiko ini dapat mengganggu stabilitas sistem dan mengakibatkan pemanfaatan resource cloud tidak efisiensi. Untuk mengatasi tantangan tersebut, manajer tim operasional berencana untuk memisahkan lingkungan antara project developer dan production. 

Selain itu, perusahaan ingin memantau dan menghitung penggunaan resource secara terukur menggunakan Yuyu, sebuah solusi untuk pencatatan dan perhitungan pemakaian resource OpenStack dengan integrasi Yuyu, karena dapat melacak penggunaan sumber daya mulai dari volume, flavor, image, dan lain – lain, bahkan sampai router pada OpenStack yang digunakan. Serta dapat menganalisa biaya penggunaan agar dapat menghemat pengeluaran operasional perusahaan.

### Tools yang digunakan :
- **OpenStack– Antelope – v2023.1**
- **Kolla Ansible – v2023.1**
- **Ansible – v2.14.18**
- **Horizon – v2023.1**
- **Yuyu – v2023.1**
- **Python – 3.10.12**

## Topologi

![Topologi](../assets/images/topologi_secure_openstack.png)

## Langkah Implementasi
### 1. Konfigurasi SSL Certificate untuk service Horizon dan Yuyu.
- Buat file IP SAN untuk Node Controller karena Service Horizon dan Yuyu berada pada Node Controller.
  ```bash
  sudo nano /etc/ssl/IP_SANS.txt
  ```
  ```bash
  subjectAltName=IP:<IP Server / Node>
  ```
  ---
- Buat directory untuk menyimpan Certificate di dalam directory **_“/etc/ssl/”_** agar lebih rapi serta mudah di identifikasi.
  ```bash
  ~$ sudo mkdir -p /etc/ssl/
  ~$ sudo mkdir -p /etc/ssl/
  ```
  ---
- Buat certificate untuk service Horizon dan Yuyu
  - Horizon.
    ```bash
    sudo openssl genrsa -out /etc/ssl/horizon/horizon.key 2048
    
    sudo openssl req -sha512 -new \
      -subj "/C=IN/ST=jateng/L=kendal/0=Horizon Najwan/OU=Horizon Najwan/CN=Horizon Najwan>" \
      -key /etc/ssl/horizon/horizon.key \
      -out /etc/ssl/horizon/horizon.csr
    
    sudo openssl x509 -req -sha512 -days 3650 \
      -key /etc/ssl/horizon/horizon.key \
      -extfile /etc/ssl/IP_SANS.txt \
      -in /etc/ssl/horizon/horizon.csr\
      -out /etc/ssl/horizon/horizon.crt
    ```
    ---
  - Yuyu.
    ```bash
    sudo openssl genrsa -out /etc/ssl/yuyu/yuyu.key 2048
    
    sudo openssl req -sha512 -new \
      -subj "/C=IN/ST=jateng/L=kendal/0=Yuyu Najwan/OU=Yuyu Najwan/CN=Yuyu Najwan>" \
      -key /etc/ssl/yuyu/yuyu.key \
      -out /etc/ssl/yuyu/yuyu.csr
    
    sudo openssl x509 -req -sha512 -days 3650 \
      -key /etc/ssl/yuyu/yuyu.key \
      -extfile /etc/ssl/IP_SANS.txt \
      -in /etc/ssl/yuyu/yuyu.csr\
      -out /etc/ssl/yuyu/yuyu.crt
    ```
    ---
- Kemudian pindahkan file certificate (dengan format .crt ) yang sudah dibuat tadi, agar certificate nya di akui oleh system operasi ubuntu, agar tidak menjadi certificate self-signed. Karena untuk Django di Horizon perlu di buat seperti itu.
  ```bash
  ~$ sudo apt-get install ca-certificates
  ~$ sudo cp /etc/ssl/horizon/horizon.crt /usr/local/share/ca-certificates
  ~$ sudo cp /etc/ssl/yuyu/yuyu.crt /usr/local/share/ca-certificates

  ~$ sudo update-ca-certificates
  ```
---

### 2. Install OpenStack dengan Kolla-Ansible
OpenStack terdiri dari beberapa service, yang nantinya berinteraksi satu sama dengan API dari setiap service yang ada, untuk service nya sendiri itu adalah sebagai berikut :
- **Keystone**, untuk identity service (verifikasi akses).
- **Neutron**, untuk Networking OpenStack.
- **Nova**, untuk Compute Service (yang Membuat Instance).
- **Glance**, untuk menyimpan Image yang digunakan untuk membuat Instance.
- **Cinder**, untuk membuat Volume yang digunakan Instance
- **RabbitMQ**, untuk Message Broker yang mengirim event dari komponen OpenStack.

Untuk lebih detail terkait Penjelasan dan Installasi nya bisa ke Postingan saya, akan tetapi harus menjalankan perintah di bawah ini terlebih dahulu. Karena nanti akan ada tambahan penyesuaian dan harus redeploy ulang cluster OpenStacknya, jadi lumayan ribet. Baru bisa mengikuti dari Postingan ini [OpenStack and Kolla-Ansible](https://vianaja.github.io/blog-najwan/2024-10-19-openstack/).

- Edit pada file global.yaml untuk opsi berikut ini untuk enable TLS pada service internal OpenStack, untuk copy CA ke Container Service nya, 
  ```yaml
  kolla_enable_tls_internal: "yes"
  kolla_certificates_dir: "\{\{ node_config \}\}/certificates"
  kolla_admin_openrc_cacert: "/etc/kolla/certificates/ca/root.crt"
  kolla_copy_ca_into_containers: "yes"
  kolla_enable_tls_backend: "yes"
  kolla_verify_tls_backend: "no"
  kolla_tls_backend_cert: "{{ kolla_certificates_dir }}/backend-cert.pem"
  kolla_tls_backend_key: "{{ kolla_certificates_dir }}/backend-key.pem"
  ```
  ---
- lalu pada step sebelum deploy, jalankan perintah ini untuk membuat Certificate.
  ```bash
  (kolla-venv) student@controller:~$ kolla-ansible -i ./multinode certificates
  ```
  ---

### 3. Installasi Horizon dan Yuyu dengan TLS
Service Horizon dan Yuyu atau lebih tepatnya Yuyu Api, keduanya menggunakan Django dalam Implementasinya, jadi untuk menambahkan opsi TLS, kita hanya perlu mengatur pada konfigurasi dari Django nya, untuk menambahkan file Certificate dan key Certificate. Untuk Installasi Horizon dan Yuyu, bisa kunjungi postingan saya yang ini [Yuyu Billing in OpenStack Horizon](https://vianaja.github.io/blog-najwan/2024-10-20-Yuyu-horizon/), untuk penjelasan serta hasil akhirnya juga. 

Ada beberapa penyesuaian apabila ingin di tambahkan opsi TLS pada kedua service ini, yaitu sebagai berikut langkah - langkahnya

#### A. Untuk di bagian Horizon
- Update konfigurasi dari **"local_setting.py"** pada directory Horizon, seperti contoh saya letakan pada directory **/var/www/html/horizon/openstack_dashboard/local/** menjadi seperti dibawah ini.
  ```python
  WEBROOT = '/'
  YUYU_URL = 'https://{IP HOST}:8182'
  
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  CSRF_COOKIE_SECURE = True
  SESSION_COOKIE_SECURE = True
  
  OPENSTACK_KEYSTONE_URL = 'https://{IP HOST}:5000/v3'
  OPENSTACK_KEYSTONE_DEFAULT_ROLE = 'member'
  OPENSTACK_SSL_NO_VERIFY = False
  OPENSTACK_SSL_CACERT = '/etc/ssl/certs/ca-certificates.crt'
  
  OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_group': True,
    'can_edit_user': True,
    'can_edit_role': True,
    'can_edit_project': True,
    'can_edit_domain': True,
  }
  ```
  ---
  
- pada saat generate file konfigurasi apache, tambahkan opsi seperti ini untuk auto generate apache conf dengan SSL/TLS.
  ```bash
  ~# ./manage.py make_web_conf --apache \
    --sslkey  /etc/ssl/horizon/horizon.key \
    --sslcert /etc/ssl/horizon/horizon.crt \
    --cacert /etc/ssl/certs/ca-certificates.crt \
    --ssl > /etc/apache2/sites-available/horizon.conf
  ```
  ---
  
- restart service Apache dan Memcached
  ```bash
  ~# systemctl restart apache2.service memcached
  ```
  ---
  
#### B. Untuk di bagian Yuyu Api
- Update konfigurasi dari **"local_setting.py"** pada directory Yuyu API, seperti contoh, saya letakan pada directory **/var/yuyu/yuyu/** menjadi seperti dibawah ini.
  ```python
  ALLOWED_HOSTS = ['*']

  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  SECURE_SSL_HOST = True
  SECURE_SSL_REDIRECT = False
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```
  ---
  
- Lalu edit pada service Yuyu API, menjadi seperti berikut untuk menambahkan opsi TLS.
  ```bash
  ~# nano /etc/systemd/system/yuyu_api.service
  ---
  ExecStart=/var/yuyu/env/bin/gunicorn yuyu.wsgi \
	--workers 2 \
  	--keyfile  /etc/ssl/yuyu/yuyu.key \
	--certfile /etc/ssl/yuyu/yuyu.crt \
	--bind 10.18.18.10:8182 \
	--log-file=logs/gunicorn.log
  ```
  ---
  
- lalu restart service Yuyu API, Apache dan Memcache.
  ```bash
  ~# systemctl restart yuyu_api.service spache2.service memcached
  ```
  ---
<br>

### Kendala yang mungkin dapat di terjadi saat pembuatan.
- Error saat Login ke Project Admin
  Solusi:
  - Ubah pada file Openrc pada bagian **_export OS_CACERT=_**, kalau tidak ada bisa ditambahkan di line baru, isikan certificate ini **“/etc/kolla/certificates/ca/root.crt”**.
  - Bisa gunakan **”/etc/ssl/certs/ca-certificate.crt”** pada saat berubah file openrc di bagian **_export OS_CACERT=_**, apabila file **“/etc/kolla/certificates/ca/root.crt”** sudah di masukan ke ca-certificate ubuntu, dengan cara copy file **“/etc/kolla/certificates/ca/root.crt”** ke **"/usr/local/share/ca-certificates"**, lalu update ca-certificates dengan perintah ini **_sudo update-ca-certificates_**.
    
---
- Error **“SSLError at /admin/billing_overview/”** saat membuka page Billing di Horizon,  karena Django yang digunakan oleh Horizon tidak diperbolehkan **“Self-Signed Certificate”**.
  Solusi:
  - Tambahkan certificate Horizon dan Yuyu ke **"/usr/local/share/ca-certificates"** lalu update ca-certificate, [referensi](https://ubuntu.com/server/docs/install-a-root-ca-certificate-in-the-trust-store)
   
--- 
- Error **“AttributeError at /auth/logout/”**  saat logout atau sign out project di Horizon.
  Solusi:
  - Versi dari library **“python-memcached”** harus menggunakan versi 1.59. kalau pake yang terbaru tidak bisa.
   
--- 
- Error saat mencoba curl dan ada log error seperti ini, **“Invalid HTTP_HOST header: ’10.18.18.10:8183’, you may need to add ’10.18.18.10’ to ALLOWED_HOSTS”**.
  Solusi:
  - Bisa setting untuk **“ALLOWED_HOSTS“** pada file konfigurasi **“local_setting.py”** dari Yuyu, bisa langsung ke IP **10.18.18.10** (menyesuaikan IP Host masing - masing) atau tanda bintang **“ * ”** jika ingin semua IP boleh masuk.
    
---
- Error **“Did Not Connect: Potential Security Issue”** pada Console Instance di Horizon, bisa disebabkan karena Certificate tidak public (Tidak Berbayar), atau karena Image yang di pakai Instance error.
  Solusi:
  - Bisa coba klik di bawah kata **“Instance Console”** yang ada kotak biru, lalu klik **“Click here to show only console”.** Error itu bisa disebabkan karena Image yang dipakai rusak.
<br>

#### Untuk hasil akhir nya, kurang lebih sama seperti pada Postingan saya yang [**Yuyu Billing in OpenStack Horizon**](https://vianaja.github.io/blog-najwan/2024-10-20-Yuyu-horizon/)

Di blog ini, saya berbagi pengalaman tentang bagaimana mengamankan layanan OpenStack, dashboard Horizon, dan Yuyu Billing OpenStack dengan menggunakan TLS (Transport Layer Security). Langkah-langkah yang saya jelaskan mencakup pembuatan sertifikat SSL, konfigurasi, hingga tips mengatasi masalah yang sering muncul.

Selain teknis, saya juga menambahkan gambaran topologi agar lebih mudah dipahami, terutama bagi yang baru terjun ke dunia cloud. Dengan langkah-langkah ini, layanan OpenStack jadi lebih aman, data yang dikirim juga terlindungi, dan pastinya bikin pengguna lebih percaya sama sistem yang kita bangun.

Kalau kalian lagi cari cara untuk bikin OpenStack lebih aman atau ingin tahu tentang TLS, semoga tulisan ini bisa membantu ya!




