# Django 1.11 project template

##### Requrements:
 - Python 2.7
 - Django 1.11.* (+ psycopg2)
 - PostgreSQL >= 9
 - Node.js >= 10.10

##### Installation
Create bash file "new_project.sh" in your projects directory with following content:
``` sh
#!/bin/bash
project_name=$1
#pip install Django==1.11.*
django-admin startproject -e py,js,json,gitignore --template=https://github.com/oldroute/django-box-1/archive/master.zip $project_name
cd $project_name
virtualenv --system-site-packages venv
. venv/bin/activate
pip install -r requirements.txt
createdb $project_name
python init_settings.py
rm init_settings.py
rm readme.md
python manage.py migrate
python manage.py init_db
npm i
git init
git remote add origin gitolite3@git.redsolution.ru:sites/$project_name
python manage.py runserver 0:8000
```
Run bash script with project_name parameter, like this:
``` sh
. new_project.sh project_name
```
After installation project will be available at [localhost:8000](http://localhost:8000)