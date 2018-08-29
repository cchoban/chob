---
title: How to create package | Choban package manager
---


Before you begin you'll need an authentication key from Choban to be able push your packages..
====
You will need authentication key to push your package, register [here](https://choban.herokuapp.com/register). Then go to [Choban packages page](https://choban.herokuapp.com/packages/) and login, then click to your name and click 'Get API Token'

After you got your API Token, type


```markdown
chob --authenticate <Api Token>
```


How to create package with Choban package manager?
====





1. Create an empty directory and type

```markdown
chob --create package-name
```
This will bring wizard to create package with some questions.

2. After the wizard directory will be created on your parent directory with your package name. Example: brave-browser

3. Join the directory created by Choban and type

```markdown
chob --packit
```

4. After you packing it .zip file will be created. Type 
```markdown
chob --test-package package-name.zip
```
And if your installation is correct you'll be fine. Just type 

```markdown
chob --push
```
to push your package to Choban servers. 