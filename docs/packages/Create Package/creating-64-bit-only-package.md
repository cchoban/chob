---
title: 'Creating 64 bit only package'
visible: true
---

Choban using 'JSON' as it's installation scripts serializer, which makes easier for end users to create their own packages without any coding experience.

Example 64 bit only package script: 
```
{
    "version": "3.0.2",
    "checksum": "65bf42b15a05b13197e4dd6cdf181e39f30d47feb2cb6cc929db21cd634cd36f",
    "fileType": "exe",
    "64bitonly": true,
    "checksum64": "a40f651bb2f5a9088637b7b43bb73c16b96192b7ceac2d21cef556ed94bfc84d",
    "silentArgs": "/S",
    "description": "VLC is a free and open source cross-platform multimedia player and framework that plays most multimedia files as well as DVDs, Audio CDs, VCDs, and various streaming protocols. ",
    "downloadUrl": "https://mirror.zetup.net/videolan/vlc/3.0.3/win32/vlc-3.0.3-win32.exe",
    "packageName": "vlc",
    "checksumType": "sha256",
    "softwareName": "VLC for Windows",
    "downloadUrl64": "https://mirror.zetup.net/videolan/vlc/3.0.2/win64/vlc-3.0.2-win64.exe",
    "checksumType64": "sha256",
    "validExitCodes": [
        0,
        1223
    ]
}
```

Better understand of variables? Here is the more useful documentation for what variables does.

Telling Choban that this software should only be installed on 64 bit devices.
```
64bitonly: true
```