---
layout: post
title: OpenStack
subtitle: Explanation and Installation Grafana
cover-img: /assets/img/wallpaper2.png
thumbnail-img: https://user-images.githubusercontent.com/92439/89548426-51fb0f00-d807-11ea-890f-afb3f9d8110a.png
share-img: /assets/img/wallpaper2.png
tags: [OpenStack, Container]
author: Najwan Octavian Gerrard
---

OpenStack adalah salah satu platform open-source yang digunakan untuk membuat atau mengelola infrastruktur cloud computing, dan Openstack dapat dikelola melalui dashboard berbasis web. 
Cloud computing, atau komputasi awan, itu merupakan teknologi yang memungkinkan pengguna untuk mengakses sumber daya komputasi melalui internet. Sumber daya komputasi tersebut mencakup server, penyimpanan, jaringan, dan perangkat lunak
Beberapa manfaat cloud computing, antara lain:
- Fleksibilitas, karena dapat di akses dari mana saja, tanpa harus pergi ke server fisiknya langsung, dengan ketentuan harus terhubung ke internet
- Skalabilitas, karena dapat di scale up dengan lebih mudah, tidak seperti server fisik yang harus mengganti komponennya untuk scale up
- Efisiensi modal biaya, karena tidak perlu beli komponen fisik secara utuh.
- Kemudahan mengakses informasi dan data karena dapat di akses lewat internet.
- Kemudahan menjalankan program tanpa harus memasang terlebih dahulu.

OpenStack sendiri terdiri dari beberapa Componen, sebagai berikut :
a)	**Keystone**, aadalah indentity service, semua komponen pada openstack akan melewati keystone untuk melakukan verifikasi akses,
b)	**Neutron**,  service untuk networking pada openstack. Yang mengatur jaringan internal dan external dari Cluster Openstack.
c)	**Nova**, sebagai compute service, yang nantinya bertugas untuk membuat instance (atau VM) di dalam Cluster Openstack
d)	**Glance**, berfungsi sebagai tempat menyimpan images OS yang nantinya akan digunakan saat membuat suatu Instance.
e)	**Cinder**, service yang memiliki tugas sebagai menyedia volume, yang nantinya akan digunakan oleh Instance di Cluster Openstack
f)	**Horizon**, Dashboard untuk management Cluster Openstack.
g)	**RabbitMQ**, salah satu Message Broker yang bertugas untuk mengirimkan pesan yang nantinya akan di diterima oleh client dari RabbitMQ.

Keuntungan Menggunakan Openstack:
- **Fleksibilitas dan Kustomisasi**: OpenStack memungkinkan pengguna untuk menyesuaikan lingkungan cloud mereka sesuai dengan kebutuhan spesifik mereka.
- **Efisiensi Biaya**: Ini dapat membantu mengurangi total biaya kepemilikan karena gratis.
- **Skalabilitas**: OpenStack mendukung penskalaan horizontal, yang berarti Anda dapat menambahkan lebih banyak mesin ke lingkungan cloud Anda untuk menangani peningkatan beban.
- **Keamanan**: Ini memiliki fitur keamanan yang kuat yang dapat ditingkatkan oleh pengguna atau melalui layanan pihak ketiga.

