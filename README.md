# Education Administration System
This is our homework of Software Engineering

*Developing* Be careful, it is awesome!

## Members
* [月亮脸](https://github.com/iphkwan) Project Manager
* [虫尾巴](https://github.com/19thhell) Front-end Web Developer
* [尖头叉子](https://github.com/zonyitoo) Server Side Developer
* [大脚板](https://github.com/sheepke) Server Side Developer

## Installation
### Django Web Framework

Our server use Django Web Framework as the sever side framework.

```bash
sudo apt-get install python-pip  # the Python Package Index(PyPI)
sudo pip install django
```

Invoke the Python Interpreter and type commands as below
```python
>>> import django
>>> django.VERSION
(1, 4, 2, 'final', 0)  # You may be glad to see this.
>>>
```

Install Django AJAX-utils, xlutils
```bash
sudo pip install django-ajaxutils xlutils
```

### PostgreSQL Database

PostgreSQL(Post-gress-Q-L), often simply Postgres, is an object-relational database management system (ORDBMS) avaliable for many platforms.

Install related packages

```bash
sudo apt-get install postgresql postgresql-client postgresql-server-dev-all # Postgresql server & client
```

Create a new database named `easdb`，own by `eas`，password is `eduadminsystem`

```bash
sudo -u postgres createuser eas -P
sudo -u postgres createdb -O eas easdb
```

Install the PostgreSQL adapter for Python and a simple Django Utility to configure Django application by `DATABASE_URL` environment variable..

```bash
sudo pip install psycopg2 dj-database-url
```

Create tables and generate testing data.

```bash
python manage.py syncdb && ./createTestData.py
```

Delete database

```
sudo -u postgres dropdb easdb
```

## Runserver with https

Install stunnel

```bash
sudo apt-get install stunnel
```

Create a directory in project to hold the necessary configuration files and SSLish stuff.

```bash 
mkdir stunnel
cd stunnel
```

Next we will need to create a local certificate and key to be used for the SSL communication. For this we turn to openssl.

Create the key:

```bash
openssl genrsa 1024 > stunnel.key
```

Create the certificate that uses this key.

```bash
openssl req -new -x509 -nodes -sha1 -days 365 -key stunnel.key > stunnel.cert
```

Now combine these into a single file that stunnel will use for its SSL communication

```bash
cat stunnel.key stunnel.cert > stunnel.pem
```

Create a config file for stunnel called dev\_https with the following contents
```
pid=

cert = stunnel/stunnel.pem
sslVersion = SSLv3
foreground = yes
output = stunnel.log

[https]
accept=443
connect=8000
TIMEOUTclose=1
```

Now pop back to the Django project directory (the one with manage.py in it) and create a script named runserver

```
sudo stunnel4 stunnel/dev_https &
HTTPS=on python manange.py runserver &
```

Then the stunnel will listen on port 443, wrap any connection it receives in SSL, and pass them along to port 8000.

If you don't want the two program keep running in the background, type the following commands mannually.

```bash
## In one shell window
sudo stunnel4 stunnel/dev_https

## An other shell window
HTTPS=on python manage.py runserver
```

```bash
## Runserver in 8000 port
python manage.py runserver
```

Try to assess the website `https://localhost` or `https://127.0.0.1` or `https://[YOUR IP ADDRESS]`

Don't forget the `https` !!

## Shortcuts
Install all the required python packages by
```
sudo pip install -r requirements.txt
```

`resetdb.sh` is a script for developers to reset database.
```bash
./resetdb.sh ## If you get errors, please tell us
```

## Document
Our document is written in Chinese and composed by LaTeX. You can clone it by 

```bash
git submodule update
```

Click [Here](https://github.com/zonyitoo/EduAdminSystemDoc) for more details.

## Trouble Shooting
### How to deploy it?

Run `python manage.py runserver 0.0.0.0:80` directly. If you get error, please make sure that you have installed all the related packages. And you should gain the root priviledge for assessing the 80 port.

### Why static files I saw in the browser are not the lastest version?

Execute `python manange.py collectstatic` after modifying static files. CAUTIONS! Don't try to modify the files in `/gstatic`.

## Reference
* [Django Project](https://www.djangoproject.com/) Django is a high-level python web framework that encourages rapid development and clean, pragmatic design.
* [Bootstrap](https://github.com/twitter/bootstrap) Bootstrap is a sleek, intuitive, and powerful front-end framework for faster and easier web development, created and maintained by Mark Otto and Jacob Thornton.
* [PostgreSQL](http://www.postgresql.org/) PostgreSQL is a powerful, open source object-relational database system.
* [Python](http://www.python.org/) Python is a programming language that lets you work more quickly and integrate your systems more effectively. You can learn to use Python and see almost immediate gains in productivity and lower maintenance costs.

## Submit
* Jan 3, 2013 23:00
* Mail to 杨腾飞
* 学号（后两位）名...项目
* xxx.doc/xxx.tex  打印一份
* 3~5min 视频
* /CODE 文件夹装代码
* 其它
