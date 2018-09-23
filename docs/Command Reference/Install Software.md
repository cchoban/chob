---
title: 'Install Software'
visible: true
---

### Usage
``` 
chob --install <pkg> <pkg2> <pkg3> [Options]
``` 
you may use like this
``` 
chob -S <pkg> <pkg2> <pkg3> [Options]
``` 
### Examples
``` 
chob -S yarn git firefox
``` 
Option to skip agreements (You can also use [config](/config/skip-agreements) to skip agreements.)
``` 
chob -S yarn git firefox -y
``` 
Option to skip checking hash of a file.  (You can also use [config](/config/skip-hash) to skip checking of hash.)
``` 
chob -S yarn git firefox -skipHash
``` 
Option to force installation of software ( You may want to reinstall )
``` 
chob -S yarn git firefox --force
``` 