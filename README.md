# Self-Hosted Server Lab

A personal, always-on **two-node home lab** running a full self-hosted stack on **Ubuntu Linux** — used for cloud storage, media, photo archiving, local AI, automation, monitoring and backend hosting. Built and maintained end-to-end: hardware, OS, Docker, networking, security and a custom monitoring dashboard.

> This is an active hands-on lab, not a tutorial fork. Everything here runs on real hardware I administer daily.

---

## Overview

The lab runs across two machines with split responsibilities: a modern mini PC handles compute-heavy and AI workloads, while an older repurposed laptop serves storage, media and lightweight always-on services. The goal is production-style infrastructure — containerized services, secure remote access without opening router ports, personal cloud, and self-hosted AI — all monitored from a dashboard I wrote myself.

## Hardware

**Node 1 — GMKtec EVO-X1 (primary compute / AI node)**

| Component | Spec |
|---|---|
| CPU | AMD Ryzen AI 9 HX 370 — Zen 5, 12 cores / 24 threads (4× Zen 5 + 8× Zen 5c), up to 5.1 GHz |
| NPU | XDNA 2, up to 50 TOPS |
| GPU | Radeon 890M (RDNA 3.5, 16 CUs) |
| RAM | 32 GB |
| Storage | 1 TB NVMe SSD |

**Node 2 — Lenovo Z510 (storage / lightweight services node)**

| Component | Spec |
|---|---|
| CPU | Intel Core i5-4200M |
| RAM | 16 GB DDR3 |
| System disk | ~220 GB |
| Storage | ~1 TB (NTFS) |

Roughly: **Node 1** runs local AI, databases and heavier containers; **Node 2** handles the media server, photo archive, backups and always-on utilities.

## Stack

Services are containerized with **Docker** and managed through **Portainer** / **CasaOS**.

**Cloud & files**
- Nextcloud — personal cloud / file sync
- Immich — self-hosted photo & video archive

**Media**
- Jellyfin — media server

**AI (local)**
- Ollama — local LLM runtime
- Open WebUI — chat interface for local models
- AllTalk TTS — local text-to-speech

**Automation & dashboards**
- n8n — workflow automation
- Homarr — service dashboard

**Data**
- PostgreSQL 16 + PostGIS — relational / geospatial data
- Redis — caching / queues

**Networking, access & monitoring**
- Cloudflare Tunnel (`cloudflared`) — expose services over a custom domain **without opening inbound ports**
- Cloudflare Access — email OTP gate in front of private services
- SSH — remote administration
- Nginx — reverse proxy / interfaces
- Uptime Kuma — service uptime & health checks

## Custom Monitoring Dashboard

A lightweight system monitor written from scratch in **Python (Flask + psutil)**, served on port `5050`:

- Live CPU / RAM / disk usage
- Running process list
- Disk temperature (with SMART data)
- Container-to-process mapping
- Roadmap: GPU temperature, optional network-traffic view

## Operations handled

Deploying and updating Docker services · container lifecycle management · mounting and using NTFS storage · SMART disk-health checks · Cloudflare Tunnel setup and domain publishing · SSH hardening and remote admin · Cloudflare Access OTP gating · restart policies · log and error inspection · port management · PostgreSQL / PostGIS / Redis administration · local AI model management · CPU/RAM/disk/process monitoring · uptime and service-health tracking · workload distribution across two nodes · backend hosting for personal projects.

## Skills demonstrated

`Linux (Ubuntu Server)` · `Docker` · `Self-hosting` · `Multi-node setup` · `Networking` · `Cloudflare Tunnel & Access` · `Reverse proxy (Nginx)` · `PostgreSQL / PostGIS` · `Redis` · `Python (Flask)` · `System monitoring` · `Backup & storage` · `Local AI (Ollama)` · `Automation (n8n)`

## Known limitations

Kept here deliberately, for honesty:

- Local LLMs on the Ryzen AI node run mainly on **CPU + system RAM**. Full ROCm acceleration on the Radeon 890M iGPU under Linux is still experimental, and the XDNA 2 NPU currently has limited Linux tooling for general inference — so I don't claim NPU-accelerated inference here.
- The Lenovo Z510 is an older machine used as a secondary node; its legacy NVIDIA GPU is not usable for compute on Linux (`nvidia-smi` fails with the DKMS 470 driver), so that node is scoped to storage and lightweight services rather than AI workloads.

---

*Built and maintained by Safa Enes İşcioğlu as a hands-on IT infrastructure / self-hosting lab.*
