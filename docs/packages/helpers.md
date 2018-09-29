Installation variables
====
```
(string) author - Software author
(string) lisence - Software lisence
(string) version - Software version. This will help Choban to determine if there is an update available.
(string) checksum - Checksum for file
(string) fileType - File type for file
(string) description - Short description for Software. This description will be used on Choban's software website.
(string) downloadUrl - Download url for file
(string) downloadUrl64 - Download url for file (64-bit)
(string) checksumType - Checksum type for software. (sha256, md5)
(string) checksumType64  - Checksum type for software. (64-bit) (sha256, md5)
(string) silentArgs - Silent args for software. It helps software to be installed silently.
(list) validExitCodes - Exit codes determines if application quit successfully.
(list) dependencies - Dependencies for software, this will help to install dependencies while installing software.
(boolean) unzip - This will also trigger the same thing.
(boolean) 64bitonly - Packages with this key can only be installed on 64-bit computers
(list) path_env - Paths to be added to PATH environment
(dict) environments - Environments to be added
(dict) createShortcut - Shortcuts for software, this will help to run software from command line.

```
