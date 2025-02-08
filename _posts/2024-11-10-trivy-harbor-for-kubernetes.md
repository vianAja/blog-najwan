---
layout: post
title: Harbor, Trivy Scanner for Kubernetes Cluster
subtitle: Secure Kubernetes Cluster with Harbor and Trivy for Images Scanning Vulnerability.
cover-img: /assets/img/wallpaper1.png
thumbnail-img: https://juststickers.in/wp-content/uploads/2018/11/kubernetes-wordmark.png
share-img: /assets/img/wallpaper1.png
tags: [Project, Kubernetes, Trivy, Harbor, Docker, Python, Slack]
author: Najwan Octavian
---

Pada Blog ini akan memberikan panduan lengkap dalam memanfaatkan Harbor dan Trivy sebagai solusi keamanan images container yang nantinya akan digunakan di dalam Kubernetes. Dengan Harbor, Anda bisa mengelola private registry yang terstruktur dan aman, sedangkan Trivy membantu mendeteksi kerentanan pada image container, menjaga standar keamanan aplikasi yang Anda gunakan.

Tutorial ini juga menjelaskan cara mengintegrasikan Slack sebagai platform notifikasi, sehingga setiap hasil scan Trivy dapat langsung diinformasikan ke tim secara real-time. Notifikasi ini memungkinkan tim untuk merespons dengan cepat, memastikan langkah mitigasi yang efektif terhadap potensi ancaman.

<br>

### Latar Belakang

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Di Era digitalisasi sekarang yang semakin pesat, banyak perusahaan yang memerlukan solusi yang efektif dan handal dalam mengelola aplikasi yang bersifat fleksibel, otomatis serta aman dari kejahatan digital. Serta dengan adanya Cloud Computing menjadikan banyak perusahaan membutuhkan tools yang dapat di jalankan pada environment tersebut. Kubernetes menjadi salah satu tools yang paling banyak diminati oleh beberapa perusahaan, karena kemampuannya dalam mengelola container dalam skala besar.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Karena Hal tersebut juga menyebabkan adanya kebutuhan untuk penyimpanan Image private atau biasa disebut sebagai Private Registry agar menjaga keamanan dari perusahaannya, dan juga karena banyak nya kasus terkait pencurian data, menjadikan kebutuhan akan Scanning Vulnerability atau kerentanan menjadi cukup penting. Apalagi di era Cloud dan Containerisasi, Trivy dan Harbor merupakan salah satu solusi terkait dua hal tersebut. Yang dimana harbor sebagai tempat registry dan Trivy untuk scanning otomatis yang di trigger oleh Harbor saat ada event tertentu seperti Ada images yang baru di Push ke Harbor Registry.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Serta dibutuhkan juga Tools untuk mengirim notifikasi secara cepat dan otomatis, sehingga dapat secara cepat juga untuk mengatasi Vulnerability atau kerentanan terhadap Images yang akan di simpan di Harbor, malasah tersebut juga bisa diatasi dengan menggunakan Slack.

<br>

### Tools

1. Kubernetes – v1.28.15
2. Kubeadm
3. Kubectl
4. Kubelet
5. Harbor – 2.10.0
6. Trivy – 0.47.0
7. Docker – 27.3.1
8. OpenSSL – 3.0.2
9. Slack

<br>

### Topologi

![Branching](../assets/images/trivy-harbor-for-kubernetes/topologi.png)

#### Harbor

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Harbor adalah registry open source yang digunakan untuk menyimpan dan mengelola Images yang akan digunakan untuk membuat Container. Harbor sendiri cukup diminati karena mudahnya integrasi dengan tools scanning Vulnerability seperti Trivy atau Clair, yang memungkinkan untuk melakukan pengecekan kerentanan (Vulnerability) terhadap Images yang disimpan menjadi lebih mudah.

#### Trivy

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Trivy adalah salah satu tools scanning yang berbasis open source yang digunakan untuk mendeteksi kerentanan yang berfokus pada images container. Trivy memindai mulai dari Library atau Apps Dependencies (seperti Composer, npm, yarn) sampai kedalam Operating System (OS) yang digunakan, apakah aman atau tidak.

#### Slack

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Slack adalah tools komunikasi yang digunakan di tempat kerja, yang memungkinkan pengguna untuk mengirim pesan, file dan tools. Slack memiliki 2 metode, yaitu Direct Message (pesan langsung dari satu user ke user lain) dan Channel Group. Dan juga Slack dapat di integrasikan dengan aplikasi atau tools lain juga yang memungkinkan melakukan otomatisasi untuk notifikasi dari suatu aplikasi.

<br>

### Langkah Implementasi

#### 1. Install Docker Untuk Harbor Registry

Panduan Dibahwah ini mencakup langkah-langkah konfigurasi Docker di sistem yang akan dibutuhkan, sehingga Anda dapat dengan mudah memahami dan mengimplementasikannya. Untuk dependensi yang dibutuhkan.

```css
docker-ce                # Package utama Docker
docker-ce-cli            # Package untuk CLI Docker
containerd.io            # Package untuk Container RunTime Docker
docker-buildx-plugin     # Package untuk Membuat Image Docker
docker-compose-plugin    # Package untuk Docker Compose
```

Untuk lebih detail terkait pengertian dan langkah installasi, bisa kunjungi postingan saya yang berjudul [Docker Container](https://vianaja.github.io/blog-najwan/2024-10-01-install-docker/)

<br>

#### 2. Create SSL Certificate untuk Harbor

* Membuat file Config IP SAN, agar SSL Certificate dapat membaca akses jika melalui IP, dan di simpan di directory **_+“/etc/ssl/”_**.
  ```bash
  ~$ echo "subjectAltName=IP:<IP Address Node>" > IP_SANS.txt
  ```

  ---
* Membuat Certificate dan Key untuk koneksi https pada Harbor, yang nantinya disimpan di directory **_“/etc/ssl/harbor/”_**.
  ```bash
  ~$ sudo openssl genrsa -out harbor.key 4096

  ~$ sudo openssl req -sha512 -new \
      -subj "/C=IN/ST=jateng/L=kendal/O=<Company Name>/OU=Personal/CN=<Domain>"\
      -key harbor.key \
      -out harbor.csr
      
  ~$ sudo openssl x509 -req -sha512 -days 3650 \
      -key harbor.key
      -extfile /etc/ssl/IP_SANS.ext \
      -in harbor.csr \
      -out harbor.crt
  ```

  ---

<br>

#### 3. Install Harbor

* Download Source Code untuk harbor, lalu unzip file source code harbor yang sudah di download.
  ```bash
  ~$ wget https://github.com/goharbor/harbor/releases/download/v2.10.0/harbor-offline-installer-v2.10.0.tgz
  ~$ tar -xvzf harbor-offline-installer-v2.10.0.tgz
  ```

  ---
* Lalu edit pada file ”harbor.yaml”. sesuaikan seperti di contoh berikut.
  ```bash
  ~$ cp harbor.yml.tmpl harbor.yml
  ~$ nano harbor.yml
  ```

  ```bash
  hostname: <IP or Domain> 
  http:
      port: 80
  https:
      port: 443
      certificate: /path/to/ca_harbor.crt
      private_key: /path/to/ca_habror.key

  harbor_admin_password: <password admin harbor>
  ```

  ---
* Lalu jalankan script **_“install.sh”_** dengan parameter **_“--with-trivy”_**untuk secara otomatis integrasi Harbor dengan Trivy. Lalu verifikasi container komponen dari harbor nya berjalan dengan baik tanpa error.
  ```bash
  ~$ sudo ~/harbor/install.sh --with-trivy
  ~$ docker ps -a
  ```

  ---

<br>

#### 4. Konfigurasi Harbor untuk Trigger Scan Trivy saat ada Image yang baru di Push dan mengatur agar user dapat Pull Image dengan tingkat kerentanan yang rendah atau aman

* Login ke Harbor dengan user **_“admin”_**, lalu masuk ke project yang ingin di konfigurasi.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.19.png)
  
  ---
* Lalu pilih **_“Configuration”_**, kemudian centang pada bagian
  * **_“Prevent vulnerable images from running.”_** Untuk mengatur agar user tidak dapat Pull Images dengan kerentanan yang tinggi. Contohnya di level **“Critical”** (yang berbahaya sekali) atau yang Levelnya diatasnya lagi.
  * **_“Vulnerability Scanning”_**. Untuk mengatur agar saat ada Push images akan secara otomatis di scanning.
![Branching](../assets/images/trivy-harbor-for-kubernetes/harbor_config.png)

  ---

<br>

#### 5. Install Kubernetes Cluster

Pada langkah Installasi Kubernetes Cluster, bisa mengikuti dari Postingan saya [K8S Kubernetes](https://vianaja.github.io/blog-najwan/2024-11-02-kubernetes/). Sudah ada juga penjelasan terkait Kubernetes Cluster. Pastikan Anda membaca panduan tersebut agar mendapatkan pemahaman yang menyeluruh sebelum melanjutkan untuk langkah berikutnya.

<br>

#### 6. Configuration SSL Certificate ke Cluster Kubernetes

> **_Note: jalankan pada Node Master dan Worker_**

* Mengatur letak SSL Certificate untuk containerd pada semua Node yang ada di Cluster Kubenetes.
  ```bash
  ~$ sudo mkdir -p /etc/containerd/certs.d/
  ~$ sudo mkdir -p /etc/containerd/certs.d/<IP or Domain_registry>/

  # Example
  ~$ sudo mkdir -p /etc/containerd/certs.d/10.18.18.40:8443/    
  ```

  ---
* Menambahkan / Copy SSL Certificate yang ada di Node Harbor atau yang digunakan oleh Harbor ke semua Node yang ada di Cluster Kubernetes.
  ```bash
  ~$ sudo nano /etc/containerd/certs.d/10.18.18.40:8443/са.crt
    -----BEGIN CERTIFICATE-----
    MIID6jCCAtKgAwIBAgIUJ@ipQt1@mbC+oFh7HqornSJ2UxAwDQYJKoZIhvcNAQEL
    ...
    eE6/aLPRXcF/72YD3eoER35h/@tnlPuuZTK7iCfYPOFTEsfa@cXGzRtXb2vV4A=
    -----END CERTIFICATE-----

  ~$ sudo nano /etc/containerd/certs.d/10.18.18.40:8443/ca.key
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDHj+SCxIwcgBlM
    ...
    Vkauk44NJ+0iyBPIzizD6qmY
    -----END PRIVATE KEY-----
  ```

  ---

#### 7. Konfigurasi kubernetes untuk Pull images ke Harbor

> **_Note: jalankan pada Node Master_**

* Atur untuk Credentials Harbor registry dengan secret. Yang nantinya akan digunakan saat membuat Pod atau saat Pull Images ke Registry tertentu.
  ```bash
  ~$ kubectl create secret docker-registry <name Secret> \
      --docker-server=<IP or Domain Registry> \
      --docker-username=<User> \
      --docker-password=<Password user> \
      --docker-email=<email for user>
  ```

  ---

#### 8. Konfigurasi Notifikasi Otomatis dari Hasil Scan Harbor ke Slack

* Login ke Website [Slack](https://slack.com/), Buat akun baru jika belum ada.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.1.png)
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.2.png)
  
  ---
* Lalu isi nama untuk Company atau Team yang sesuai, contoh **_“Harbor Vuln Scan”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.3.png)
  
  ---
* Nama untuk user sendiri, contoh **_“Najwan”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.4.png)
  
  ---
* Dibagian ini pilih yang **_“skip this step”_** jika tidak ingin invite user lain ke Slack.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.5.png)
  
  ---
* Lalu isi nama untuk Channel nya, contoh **_“Harbor Vuln”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.6.png)
  
  ---
* Lalu pilih yang **_“Start with the limit free version”_** kalau ingin menggunakan yang gratis.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.7.png)
  
  ---
* Lalu klik pada titik tiga di kanan atas, lalu klik yang **_“Edit Settings”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.8.png)
  
  ---
* Lalu pilih yang **_“Integrations”_**, lalu klik **_“Add an App”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.9.png)
  
  ---
* Lalu klik **_“Manage Apps…”_** di bagian kiri atas.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.10.png)
  
  ---
* Lalu pilih **_“Build”_** di kanan atas.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.11.png)
  
  ---
* Lalu klik **_“Create an App”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.12.png)
  
  ---
* Lalu pilih yang **_“From scratch”_** untuk lebih mudah, karena tidak perlu membuat template. Kalau **_“From a manifest”_** kita perlu membuat template dengan format **_“json”_** atau **_“YAML”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.13.png)
  
  ---
  * Lalu isi untuk nama App nya dan pilih Workspace yang sesuai. Lalu klik **_“Create App”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.14.png)
  
  ---
* Lalu setalah selesai membuat app, kita perlu membuat untuk endpoint webhook agar Harbor dapat mengirim ke Slack, dengan pilih **_“Incoming WebHooks”_**, lalu aktifkan **_“Activate Incoming WebHooks”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.15.png)
  
  ---
* Lalu scroll kebawah, lalu klik **_“Add New WebHook to Workspace”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.16.png)
  
  ---
* Lalu pilih tempat untuk mengirim pesan dari WebHook nya, bisa ke Channel dari Slack, atau Direct Message ke user tertentu. Contoh misalkan ke channel **_“harbor-vuln”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.17.png)
  
  ---
* Lalu copy link yang sudah di berikan.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.18.png)
  
  ---
* Lalu login ke Harbor dengan user **_“admin”_** dengan password yang sesuai. Pilih project yang ingin di konfigurasi. Contoh **_“testing”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.19.png)
  
  ---
* Lalu pilih **_“Webhooks”_**, lalu klik **_“+ New WebHook”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.20.png)
  
  ---
* Lalu isikan data berikut :
  * Nama WebHook.
  * Deskripsi apabila ada.
  * Pada bagian **_“Notify Type”_** pilih yang **_“Slack”_**.
  * Pada bagian **_“Event Type”_** untuk memilih saat apa Harbor mengirim notif ke Slack (Trigger), centang pada bagian:
    *	**_Scanning failed_**.
    *	**_Scanning stopped_**.
    * **_Scanning finished_**.

  * Isikan Endpoint URL sesuai dari slack pada step sebelumnya.
![Branching](../assets/images/trivy-harbor-for-kubernetes/9.21.png)
  
<br>

#### 9. Konfigurasi SSH ke semua Node

* Login ke Slack, lalu pergi ke pengaturan App, atau lewat link [ini](https://api.slack.com/apps/). Lalu pilih App yang sesuai, contohnya **_“python-harbor”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/10.1.png)
  
  ---
* lalu pilih yang **_“OAuth & Permissions”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/10.2.png)
  
  ---
* Lalu Scroll kebawah sampai ke bagian **_“Scopes”_**, lalu pilih **_“Add an QAuth Scope”_**, lalu pilih yang **_“chat:write”_** untuk mengatur role agar dapat menulis pesan atau chat.
![Branching](../assets/images/trivy-harbor-for-kubernetes/10.3.png)
  
  ---
* Lalu Scroll ke atas sampai di bagian **_"OAuth Tokens”_**, lalu **_“Install to Harbor Vuln Scan”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/10.4.png)
  
  ---
* Lalu pada bagian ini klik **_“Allow”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/10.5.png)
  
  ---
* Lalu Copy **_“Bot User OAuth Token”_**.
![Branching](../assets/images/trivy-harbor-for-kubernetes/10.6.png)
  
  ---
* Ambil Sample aplikasi sederhana untuk filter data hasil Scanning Trivy dari Harbor dan nanti akan dikirim ke Slack di [github ini](https://github.com/vianAja/python-slack-harbor.git). Lalu sesuaikan untuk data berikut ini.

  ```css
  token_slack = "TOKEN_OAUTH"
  channel_id = "CHANNEL_ID_SLACK"
  name_bot = "NAME_BOT"
  ```
  
  ---
* Install Library yang dibutuhkan Python. 
  ```bash
  ~$ sudo pip3 install -r requirement.txt
  ~$ sudo cp main.py /usr/local/bin/
  ```

  ---
* Copy file service ke **_“/etc/system/system/”_**.
  ```bash
  ~$ sudo cp python-slack.service /etc/systemd/system/
  ```

  ---
* Copy file **_“main.py”_** ke **_“/usr/local/bin/”_**, menyesuaikan dari konfigurasi yang ada di file service nya.
  ```bash
  ~$ sudo cp main.py /usr/local/bin/
  ```

  ---

* Reload system daemon untuk update service. Lalu start dan lihat status service yang sudah di Copy tadi.
  ```bash
  ~$ sudo systemctl daemon-reload
  
  ~$ sudo systemctl start python-slack.service
  ~$ sudo systemctl status python-slack.service
  ```

  ---

<br>

### Hasil Akhir Project

#### Notifikasi Tanpa menggunakan Program Pyhon

![Branching](../assets/images/trivy-harbor-for-kubernetes/hasil_slack.1.png)

---

#### Notifikasi Menggunakan Program Python

![Branching](../assets/images/trivy-harbor-for-kubernetes/hasil_slack.2.png)

---

#### Tidak Bisa Pull Images jika level Vulnerability Critical atau yang lebih tingggi

![Branching](../assets/images/trivy-harbor-for-kubernetes/failed_pull.png)

---

### Referensi

- [KubeAdm Tools](https://kubernetes.io/id/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- [Install Harbor](https://medium.com/@tanmaybhandge/how-to-deploy-the-harbor-on-vm-using-self-signed-certificate-ebfe29c4803a).
- [Trivy Scanner](https://www.jit.io/resources/appsec-tools/when-and-how-to-use-trivy-to-scan-containers-for-vulnerabilities).
- [Trivy Scanner](https://medium.com/@maheshwar.ramkrushna/scanning-docker-images-for-vulnerabilities-using-trivy-for-effective-security-analysis-fa3e2844db22).
- [WebHooks Slack](https://api.slack.com/messaging/webhooks).
- [Kubernetes Pull Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).
- [Container](https://www.docker.com/resources/what-container/).
- [Docker](https://www.hostinger.co.id/tutorial/apa-itu-docker).
- [harbor dokumentasi](https://goharbor.io/).
- [Slack](https://www.nusa.id/apa-itu-slack-yuk-cari-tahu-lebih-jauh-di-sini#:~:text=Apa%20Itu%20Slack%3F,in%20untuk%20tools%20kerja%20lainnya.).
- [SSL (Secure Sockets Layer)](https://www.jagoanhosting.com/blog/pengertian-ssl).
- [Apps Manifest Slack](https://api.slack.com/reference/manifests).
- [Integrasi Python ke Slack](https://www.datacamp.com/tutorial/how-to-send-slack-messages-with-python).
- [Send Messages Python ke Slack](https://medium.com/@sid2631/automating-slack-notifications-sending-messages-as-a-bot-with-python-2beb6c16cd8).
