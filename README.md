# Education Adminstration System
This is our homework of Software Engineering

*Developing*

## Members
* [月亮脸](https://github.com/iphkwan) Project Manager
* [虫尾巴](https://github.com/19thhell) Front-end Web Develper
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
sudo pip install django-ajaxutils, xlutils
```

### PostgreSQL Database

PostgreSQL(Post-gress-Q-L), often simply Postgres, is an object-relational database management system (ORDBMS) avaliable for many platforms.

Install related packages

```bash
sudo apt-get install postgresql postgresql-client postgresql-server-dev-all # Postgresql server and client
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
python manage.py syncdb
```

`resetdb.sh` is a script for developers to reset database.
```bash
./resetdb.sh
```

Delete database

```
sudo -u postgres dropdb easdb
```

## Trouble Shooting
* 怎么运行？

直接在根目录执行`python manage.py runserver`，若看到出错信息，先保证你已安装好Django，安装方向见上。

* 看起来css或js用的不是最新的代码？

在根目录执行`python manage.py collectstatic`然后再`runserver`就可以了。

* 管理员帐号的创建？

在根目录执行`python manage.py syncdb`然后按提示创建管理员帐号。（e.g. admin@admin）

利用django自带的后台，创建管理员帐号，即可在:`127.0.0.1：8000/admin/`中进行帐号/组管理。

* 修改了一些js/css后没有反应？

Don't try to modify /static/\*，这个文件夹是由`collectstatic`自动聚集各模块中的static文件，修改应进入特定模块修改，并执行`collectstatic`使其生效。

## Reference
* [Django Project](https://www.djangoproject.com/) Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* [Bootstrap](https://github.com/twitter/bootstrap) Bootstrap is a sleek, intuitive, and powerful front-end framework for faster and easier web development, created and maintained by Mark Otto and Jacob Thornton.
* [PostgreSQL](http://www.postgresql.org/) PostgreSQL is a powerful, open source object-relational database system.
* [Python](http://www.python.org/) Python is a programming language that lets you work more quickly and integrate your systems more effectively. You can learn to use Python and see almost immediate gains in productivity and lower maintenance costs.

## 项目提交日期和方法
* Jan 3, 2013 23:00
* Mail to 杨腾飞
* 学号（后两位）名...项目
* xxx.doc/xxx.tex  打印一份
* 3~5min 视频
* /CODE 文件夹装代码
* 其它
