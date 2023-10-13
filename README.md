# leightweight_django
A leightweight django startproject template. Could be suit for API service with token authorized.

Requirements:
1. Python 3.7+
2. Django 3.2LTS (Should be work with lower or higher version, but I'ver not tested.)

Quick Start:
1. Use this template project as your basement.
```
#django-admin startproject YourDemoName --template=https://github.com/BroHui/leightweight_django/archive/refs/heads/main.zip -e ini
```
2. Build your own docker image.
```
#docker build -t leightweight-django .
```
3. Boost your app with docker power!
```
docker run -it --rm -v $(pwd):/usr/src/app -p 8081:8081 -e TOKEN_LIST=simpletoken lightweight_django
```

Debug:
```
docker run -it --rm -v .:/app -v ./requirements.txt:/app/requirements.txt -p 8000:8000 django:lts /bin/bash
```

Thanks to:  
<Lightweight Django> Copyright © 2015 Julia Elman and Mark Lavin. Published by O’Reilly Media, Inc.  
Thanks to these guys, Their great works inspire me.
