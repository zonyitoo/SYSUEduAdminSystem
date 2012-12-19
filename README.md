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

### Apache HTTP Server

Install Apache HTTP Server and dependences

```bash
sudo apt-get install apache2 libapache2-mod-wsgi libapache2-mod-python
```

Then create a new file in `/etc/apache2/sites-enabled/` with contents as below (delete the default configure file if exists), replace `[PATH_TO_PROJECT]` with the abslute path of the project directory. For example: `/home/zonyitoo/workspace/EduAdminSystem`

```apache
<VirtualHost *:80>
    ServerName EduAdminSystem
    LoadModule rewrite_module /usr/lib/apache2/modules/mod_rewrite.so

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
</VirtualHost>

<VirtualHost *:443>
    ServerName EduAdminSystem
    DocumentRoot [PATH_TO_PROJECT] 
    WSGIScriptAlias / [PATH_TO_PROJECT]/apache/wsgi.py

    Alias /static [PATH_TO_PROJECT]/gstatic
    
    #LoadModule ssl_module /usr/lib/apache2/modules/mod_ssl.so

    SSLEngine On

    SSLCertificateFile [PATH_TO_PROJECT]/apache/eas.cert
    SSLCertificateKeyFile [PATH_TO_PROJECT]/apache/eas.key

    <Directory "[PATH_TO_PROJECT]/apache">
        <Files wsgi.py>
            Order deny,allow
            Allow from all
        </Files>
    </Directory>

    <Directory "[PATH_TO_PROJECT]/gstatic/">
        Order deny,allow
        Allow from all
    </Directory>

    <Location "/">
        SetHandler python-program
        PythonHandler django.core.handlers.modpython
        SetEnv DJANGO_SETTINGS_MODULE EduAdminSystem.settings
        PythonPath "['[PATH_TO_PROJECT]'] + sys.path"
        PythonDebug On
    </Location>

    <Location "/static/">
        SetHandler None
    </Location>
</VirtualHost>
```

Then activate the SSL module of Apache and restart Apache Daemon

```
sudo a2enmod ssl
sudo service apache2 restart
```

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
