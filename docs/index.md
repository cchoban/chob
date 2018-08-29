---
title: Choban package manager
---


## Choban Package Manager
Choban is package manager for Windows, built with Python with 💖
![Image](https://i.hizliresim.com/r1a8n7.png)

Install Choban
=====
Open PowerShell(as admin) and paste the code below. You are good to go!
```
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/cchoban/installer/master/install.ps1'))
```


How to use Choban ?
=====

### How to install package with Choban?
```
chob -S package-name

or

chob --install package-name
```

### How to remove package with Choban?
```
chob -R package-name

or

chob --remove package-name
```

### How to upgrade package with Choban?
```
chob --upgrade package-name
```