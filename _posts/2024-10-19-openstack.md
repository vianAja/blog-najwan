---
layout: post
title: OpenStack and Kolla-Ansible
subtitle: Explanation and Installation OpenStack with Kolla-Ansible
cover-img: /assets/img/wallpaper2.png
thumbnail-img: https://banner2.cleanpng.com/20180602/jkl/avoucosdm.webp
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
- **Keystone**, aadalah indentity service, semua komponen pada openstack akan melewati keystone untuk melakukan verifikasi akses,
- **Neutron**,  service untuk networking pada openstack. Yang mengatur jaringan internal dan external dari Cluster Openstack.
- **Nova**, sebagai compute service, yang nantinya bertugas untuk membuat instance (atau VM) di dalam Cluster Openstack
- **Glance**, berfungsi sebagai tempat menyimpan images OS yang nantinya akan digunakan saat membuat suatu Instance.
- **Cinder**, service yang memiliki tugas sebagai menyedia volume, yang nantinya akan digunakan oleh Instance di Cluster Openstack
- **Horizon**, Dashboard untuk management Cluster Openstack.
- **RabbitMQ**, salah satu Message Broker yang bertugas untuk mengirimkan pesan yang nantinya akan di diterima oleh client dari RabbitMQ.

Keuntungan Menggunakan Openstack:
- **Fleksibilitas dan Kustomisasi**: OpenStack memungkinkan pengguna untuk menyesuaikan lingkungan cloud mereka sesuai dengan kebutuhan spesifik mereka.
- **Efisiensi Biaya**: Ini dapat membantu mengurangi total biaya kepemilikan karena gratis.
- **Skalabilitas**: OpenStack mendukung penskalaan horizontal, yang berarti Anda dapat menambahkan lebih banyak mesin ke lingkungan cloud Anda untuk menangani peningkatan beban.
- **Keamanan**: Ini memiliki fitur keamanan yang kuat yang dapat ditingkatkan oleh pengguna atau melalui layanan pihak ketiga.

### Kolla-Ansible
Kolla-Ansilbe adalah salah satu Tools Deployment Openstack Cluster untuk skala Production, yang scalable, cepat, dan mudah di upgrade yang menjadikannya banyak di pakai oleh perusahaan. Kolla-Ansible akan mendeploy Openstack pada sebuah Container, dan karena Kolla-Ansible menggunakan Ansible, jadi saat proses deployment akan lebih mudah, simple, serta cepat, dan juga lebih fleksible dalam konfigurasi sesuai yang dibutuhkan.
Manfaat menggunakan Kolla-Ansible:
- Praktis, karena menggunakan Ansible, jadi semua deployment dilakukan otomatis, tinggal menyesuaikan kebutuhan sesuai keinginan saja, misalkan service apa saja yang ingin di buat, sampai opsi TLS.
- Mengurangi kelalaian manusia apabila melakukan deployment Openstack manual.


### Langkah Implementasi
- Install dependencies yang dibutuhkan OpenStack dan Kolla-Ansible
  ```bash
  sudo apt-get install python3-dev python3-selinux python3-setuptools python3-venv gcc libffi-dev libssl-dev -y
  ```<br>
  
- Membuat Virtual Environment Python, agar saat membutuhkan versi tertentu dari library python, tidak akan berpengaruh ke system host langsung. lalu aktifkan Virtual Env Pythonnya.
  ```bash
  ~$ python3 -m venv kolla-venv
  ~$ source kolla-venv/bin/activate
  ```

- Install ansible dan kolla-ansible untuk deployment Openstack.
  ```bash
  (kolla-venv) student@controller:~$ pip install -U pip
  (kolla-venv) student@controller:~$ pip install 'ansible>=6,<8'
  (kolla-venv) student@controller:~$ pip install git+https://opendev.org/openstack/kolla-ansible@stable/2023.1
  (kolla-venv) student@controller:~$ kolla-ansible install-deps
  ```

- Buat directory untuk kolla, dan copy file “globals.yml”  dan “passwords.yml” untuk nanti memilih opsi untuk deployment OpenStack. Lalu konfigurasi file “globals.yml” , seperti dibawah ini.
  ```bash
  (kolla-venv) student@controller:~$ sudo mkdir -p /etc/kolla
  (kolla-venv) student@controller:~$ sudo chown $USER:$USER /etc/kolla
  (kolla-venv) student@controller:~$ cp -r kolla-venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
  ```
  ```yaml
  kolla_base_distro: "ubuntu"
  openstack_release: "2023.1"
  network_interface: "ens3"
  neutron_external_interface: "ens4"
  kolla_internal_vip_address: "{IP HOST}"
  neutron_plugin_agent: "openvswitch"
  enable_keystone: "yes"
  enable_horizon: "no"
  enable_neutron_provider_networks: "yes"
  enable_cinder: "yes"
  enable_cinder_backend_lvm: "yes"
  ```
  
- Copy file multimode, dan konfigurasi juga untuk komponen dari OpenStacknya mau di letakkan pada node mana. Sebagai contoh saya menggunakan 3 Node, 1 Controller dan 2 Compute.
  ```bash
  (kolla-venv) student@controller:~$ cp kolla-venv/share/kolla-ansible/ansible/inventory/* .
  (kolla-venv) student@controller:~$ nano ~/multinode
  ```
  ```yaml
  [control]
  pod-controller
  
  [network]
  pod-controller
  
  [compute]
  pod-compute1
  pod-compute2
  
  [monitoring]
  pod-controller
  
  [storage]
  pod-controller
  pod-compute1
  pod-compute2
  
  [deployment]
  localhost ansible_connection=local
  ```

- Konfigurasi untuk Ansible.cfg.
  ```bash
  (kolla-venv) student@controller:~$ sudo mkdir -p /etc/ansible
  (kolla-venv) student@controller:~$ sudo nano /etc/ansible/ansible.cfg
  ```
  ```yaml
  [defaults]
  host_key_checking=False
  pipelining=True
  forks=100
  ```

- Generate password untuk service OpenStack.
  ```bash
  (kolla-venv) student@controller:~$ kolla-genpwd
  ```

- Buat Physical Volume (PV) dan Volume Group (VG) yang nanti akan digunakan oleh service Cinder, untuk membuat Volume yang akan digunakan oleh OpenStack.
  ```bash
  (kolla-venv) student@controller:~$ sudo pvcreate /dev/vdb
  (kolla-venv) student@controller:~$ sudo vgcreate cinder-volumes /dev/vdb
  ```

- Lakukan bootstrap, yang nantinya pada setiap Node yang digunakan oleh cluster OpenStack, nantinya akan melakukan pengaturan awal seperti menginstall dependensi yang dibutuhkan untuk deployment OpenStack via Kolla-Ansible.
  ```bash
  (kolla-venv) student@controller:~$ kolla-ansible -i ./multinode bootstrap-servers
  ```

- Lakukan pengecekan dari dependensi yang diperlukan saat ingin deploy Cluster OpenStack.
  ```bash
  (kolla-venv) student@controller:~$ kolla-ansible -i ./multinode prechecks
  ```

- Lakukan deployment Cluster OpenStack.
  ```bash
  (kolla-venv) student@controller:~$ kolla-ansible -i ./multinode deploy
  ```

- Lalu buat file openrc yang nantinya digunakan untuk login OpenStack via CLI.
  ```bash
  (kolla-venv) student@controller:~$ kolla-ansible -i ./multinode post-deploy
  ```

- Lalu install library python OpenStack client, dan login dengan file openrc, kemudian verifikasi juga untuk service yang sudah di deploy.
  ```bash
  (kolla-venv) student@controller:~$ pip install openstackclient
  (kolla-venv) student@controller:~$ source /etc/kolla/admin-openrc.sh
  
  (kolla-venv) student@controller:~$ openstack service list 
  +----------------------------------+-------------+----------------+
  | ID                               | Name        | Type           |
  +----------------------------------+-------------+----------------+
  | 2016e0d3e67b47f9ab8941f18912b4ed | heat        | orchestration  |
  | 3cc9267de0774fc295f9ff99ad7098ad | glance      | image          |
  | 72f7b5292bbd4cf3aa2594ffe99cf409 | nova_legacy | compute_legacy |
  | 7bbcedc7b0504d79b7b15e4c3619374b | keystone    | identity       |
  | 9bea6c9b9a954d82a0531ba70b0331a6 | heat-cfn    | cloudformation |
  | 9e8e74f5a48b493097014aafe5d82268 | neutron     | network        |
  | b4ed42fee5c64ba18b96a6603dbb5b36 | placement   | placement      |
  | c1f1b5c9fbc24b2ea564e7d8ce121ef9 | nova        | compute        |
  | f03eb26e51694df79fd86174e810f10c | cinderv3    | volumev3       |
  +----------------------------------+-------------+----------------+
  ```




