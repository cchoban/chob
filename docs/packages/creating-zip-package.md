---
title: 'Creating ZIP file'
visible: true
---

Choban using 'JSON' as it's installation scripts serializer, which makes easier for end users to create their own packages without any coding experience.

Example ZIP file: 
```
{
  "unzip": true,
  "version": "7.2.7",
  "checksum": "2fe0b1a818232f3ed4e20bff5ec1fdeea14ef56f424581b8cd8687c69f25755d",
  "fileType": "zip",
  "silentArgs": "",
  "description": "PHP is an HTML-embedded scripting language. Much of its syntax is borrowed from C, Java and Perl with a couple of unique PHP-specific features thrown in. The goal of the language is to allow web developers to write dynamically generated pages quickly.",
  "downloadUrl": "https://windows.php.net/downloads/releases/php-7.2.9-Win32-VC15-x64.zip",
  "packageName": "php",
  "checksumType": "sha256",
  "softwareName": "PHP",
  "createShortcut": "php.exe",
  "validExitCodes": [
    "0"
  ]
}
```

Better understand of variables? Here is the more useful documentation for what variables does.

Telling Choban that this is not a software, instead it is zip file.
```
unzip: true
```

This creates a shortcut file for you to use from your command line. (If you do not provide this, user need to add the php tools folder to path environment variable directly from command prompt.)
```
createShortcut: "php.exe"
```


