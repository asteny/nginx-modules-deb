![build](https://github.com/asteny/nginx-modules-deb/actions/workflows/make-packages.yml/badge.svg) <a href="https://packagecloud.io"><img src="https://img.shields.io/badge/deb-packagecloud.io-844fec.svg"/></a>
# Nginx dynamic modules

This repo contains Ubuntu packages for popular Nginx modules as built dynamically and packed as deb packages

Each package contains nginx configuration files like `/etc/nginx/modules-available/50-${MODULE_NAME}.conf`, it does not require knowladge absolut so-library path.
    
In default ubuntu nginx contains includes like `/etc/nginx/modules-enabled/*.conf`, so you should create symlink links to module configs.
    
For mainline nginx just add `include /etc/nginx/modules-available/*.conf`.

Installation for mainlain
------------
```bash
apt-get update
apt-get install gnupg2 apt-transport-https ca-certificates -y
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C87187E0F279DECD
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys A57ED69D49D1012A
printf "deb https://packagecloud.io/the_asten/nginx-modules-mainline/ubuntu/ focal main \ndeb-src https://packagecloud.io/the_asten/nginx-modules-mainline/ubuntu/ focal main" | tee -a /etc/apt/sources.list.d/nginx-modules-mainline.list
apt-get update
```

Installation for Ubuntu
------------
```bash
apt-get update
apt-get install gnupg2 apt-transport-https ca-certificates -y
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 32E8B63A047C452C
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys A57ED69D49D1012A
printf "deb https://packagecloud.io/the_asten/nginx-modules-ubuntu/ubuntu/ jammy main \ndeb-src https://packagecloud.io/the_asten/nginx-modules-ubuntu/ubuntu/ jammy main" | tee -a /etc/apt/sources.list.d/nginx-modules-ubuntu.list
apt-get update
```

Special thanks for the ability to use the package repository for open source projects - :rocket: https://packagecloud.io :rocket:

All package versions in packagecloud.io repos:
[Mainline](https://packagecloud.io/the_asten/nginx-modules-mainline)
[Ubuntu](https://packagecloud.io/the_asten/nginx-modules-ubuntu)
-------------------------------------------------------------------------------
