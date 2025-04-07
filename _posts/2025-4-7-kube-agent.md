---
layout: post
title: Kubenetes Agent Gitlab
subtitle: Deploy Kubernetes Agent on Gitlab and use Pipeline CI/CD
cover-img: /assets/img/wallpaper2.png
thumbnail-img: /assets/images/kube-agent/kube_agent_gitlab.png
share-img: /assets/img/wallpaper2.png
tags: ['Kubernetes', 'GitLab CI/CD', 'Helm', 'DevOps']
author: Najwan Octavian Gerrard
---

Dalam era DevOps dan automasi modern, integrasi antara sistem kontrol versi seperti GitLab dengan platform orkestrasi container seperti Kubernetes menjadi kebutuhan utama. Banyak perusahaan dan tim pengembang mencari solusi yang dapat mempercepat proses build, testing, dan deployment secara otomatis ke dalam lingkungan Kubernetes. Melalui project ini, saya mengeksplorasi bagaimana GitLab Kubernetes Agent dan GitLab Runner dapat bekerja sama untuk menciptakan pipeline CI/CD yang aman, efisien, dan sepenuhnya terintegrasi dengan cluster Kubernetes.

## Tools yang digunakan
- **Kubernetes Cluster**
- **GitLab Project**
- **Helm**
- **glab**
- **Docker**

### Implementasi

#### 1. Create Cluster Kubernetes

Bisa cek pada postingan saya yang ini [Kubernetes](https://vianaja.github.io/blog-najwan/2024-11-2-kubernetes/) untuk lebih detal terkait Create Cluster Kubernetes.
Setelah selesai Creating Cluster Kubernetesnya

#### 2. Buat Project GitLab dan buat Kube agent di projectnya
