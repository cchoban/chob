---
title: 'Create package'
visible: true
---

The wizard will provide basic of package creation script,  you may need edit the script for your needs.
You can refer to [Creating ZIP package](creating-zip-file) to see some examples

1. Create an empty directory and type

```
chob --create package-name
```
This will bring wizard to create package with some questions.

2. After the wizard directory will be created on your parent directory with your package name. Example: brave-browser

3. Join the directory created by Choban and type

```
chob --packit
```
Test your package before you push to our servers.
```
chob --test--package brave-browser.zip -y
```

If the process was successfull then you can push your package to our server


```
chob --push
```

