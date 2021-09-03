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
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EA8AECDE414187DB
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys A57ED69D49D1012A
printf "deb https://packagecloud.io/the_asten/nginx-modules-mainline/ubuntu/ focal main \ndeb-src https://packagecloud.io/the_asten/nginx-modules-mainline/ubuntu/ focal main" | tee -a /etc/apt/sources.list.d/nginx-modules-mainline.list
apt-get update
```

Installation for Ubuntu
------------
```bash
apt-get update
apt-get install gnupg2 apt-transport-https ca-certificates -y
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EA8AECDE414187DB
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys A57ED69D49D1012A
printf "deb https://packagecloud.io/the_asten/nginx-modules-ubuntu/ubuntu/ focal main \ndeb-src https://packagecloud.io/the_asten/nginx-modules-ubuntu/ubuntu/ focal main" | tee -a /etc/apt/sources.list.d/nginx-modules-ubuntu.list
apt-get update
```

Special thanks for the ability to use the package repository for open source projects - :rocket: https://packagecloud.io :rocket:

All package versions in packagecloud.io repos:
[Mainline](https://packagecloud.io/the_asten/nginx-modules-mainline)
[Ubuntu](https://packagecloud.io/the_asten/nginx-modules-ubuntu)
-------------------------------------------------------------------------------
