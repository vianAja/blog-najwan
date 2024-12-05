---
layout: post
title: K8S Kubernetes
subtitle: Explanation and Installation Kubernetes.
cover-img: /assets/img/wallpaper1.png
thumbnail-img: https://juststickers.in/wp-content/uploads/2018/11/kubernetes-wordmark.png
share-img: /assets/img/wallpaper1.png
tags: [Kubernetes, Docker]
author: Najwan Octavian
---

Kubernetes merupakan platform Container Orchestration yang berbasis open source, yang digunakan sering untuk management workload suatu aplikasi yang dikontainerisasi. Kubernetes juga menyediakan konfigurasi dan automation untuk mengelola aplikasi berbasis container, serta dapat mengelola Workload / beban kerja dari sebuah container apps secara Efisien dengan menggunakan fitur Horizontal Pod auto Scaling (HPA).

### Instalation

* Update dan Upgrade packages.

  ```bash
  ~$ sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
  ```

  ---
* Install dependensi dan menambah repository untuk install containerd.

  ```bash
  ~$ sudo apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates

  ~$ sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg
  ~$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  ```

  ---
* Install Containerd lalu Config Containerd.

  ```bash
  ~$ sudo apt update
  ~$ sudo apt install -y containerd.io
  ~$ containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
  ~$ sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml

  ~$ sudo systemctl restart containerd
  ~$ sudo systemctl enable containerd
  ```

  ---
* Add kernel setting overlay.

  ```bash
  ~$ cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    overlay
    br_netfilter
    EOF

  ~$ sudo modprobe overlay
  ~$ sudo modprobe br_netfilter
  ```

  ---
* Konfigurasi iptables.

  ```bash
  ~$ cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-iptables  = 1
    net.bridge.bridge-nf-call-ip6tables = 1
    net.ipv4.ip_forward = 1
    EOF

  ~$ sudo sysctl --system
  ```

  ---
* Menambahkan repository untuk kubectl, kubelet, dan kubeadm dan Install tools tersebut.

  ```bash
  ~$ sudo apt-get install -y apt-transport-https ca-certificates
  ~$ curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

  ~$ echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

  ~$ sudo apt-get update && sudo apt-get install -y kubelet kubeadm kubectl
  ~$ sudo apt-mark hold kubelet kubeadm kubectl
  ```

  ---

> **_Note: jalankan pada Node Master_**

* Initialze untuk membuat Cluster Kubernetes di Master Node.

  ```bash
  ~$ sudo kubeadm init --pod-network-cidr=10.244.XX.0/16
  ~$ mkdir -p $HOME/.kube
  ~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  ~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
  ```

  ---
* Add Flannel.

  ```bash
  ~$ wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
  ~$ kubectl apply -f kube-flannel.yml
  ~$ kubectl get pods --all-namespaces
  ```
  
  ---
* Menampilkan Token dan CA Certificate.

  ```bash
  ~$ sudo kubeadm token list
  ~$ sudo openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
  ```

  ---

> **_Note: jalankan pada Node Worker_**

* Initialze Node Worker

  ```bash
  ~$ sudo kubeadm join --token [TOKEN] [NODE-MASTER]:6443 --discovery-token-ca-cert-hash sha256:[TOKEN-CA-CERT-HASH]
  ```
