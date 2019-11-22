# FPT Edu Hackathon 2019

## Prerequisites

- [Python 3.7+](https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh)
- [Ubuntu 18.04 LTS](https://ubuntu.com/download/desktop)
- [Docker Engine - Ubuntu (Community)](https://hub.docker.com/editions/community/docker-ce-server-ubuntu)

### Docker Installation Guide

```bash
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update
sudo apt install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
```

## Dataset structure

```
$ tree --dirsfirst --filelimit 10 Cyclone_Wildfire_Flood_Earthquake_Database
Cyclone_Wildfire_Flood_Earthquake_Database
├── Cyclone [928 entries]
├── Earthquake [1350 entries]
├── Flood [1073 entries]
└── Wildfire [1077 entries]
 
4 directories
```

## Project structure

```

```

Our project contains:
- The natural disaster dataset.
- An `checkpoint/`  directory where our model and plots will be stored. The results from my experiment are included.
- A selection of `videos/`  for testing the video classification prediction script.
- Our training script, `training.py` . This script will perform fine-tuning on a ResNet18 model pre-trained on the ImageNet dataset.
- Our video classification prediction script, `predict_camera.py` ,
which performs a rolling average prediction to classify the video in real-time.

