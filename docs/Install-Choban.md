---
title: 'Installing Choban'
---

### Requirements
1. Windows 7+ / Windows Server 2003+
2. PowerShell v2+

### Installing Choban
Installation of Choban package manager is quite easy! 
Just copy and paste code below to your PowerShell (as admin) and watch the magic!

1. Open PowerShell with administrative rights
2. Copy and paste the text below
3. Wait until command finishes
4. Re-start all your PowerShell sessions



** PowerShell.exe command: **
```
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/cchoban/installer/master/install.ps1'))
```

### Didn't worked?
Please refer to [Troubleshooting](/troubleshooting)

Want to see what installation script does? You can always visit our [GitHub](https://github.com/cchoban/installer/)
 page because it's Open Source!

