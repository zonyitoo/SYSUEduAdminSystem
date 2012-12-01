# 教务系统
这是大三软件工程作业
*依然开发中*

## Members
* [叶晓军](https://github.com/iphkwan) 产品
* [杨曦华](https://github.com/19thhell) 前端
* [钟宇腾](https://github.com/zonyitoo) 架构
* [柯毅豪](https://github.com/sheepke) 后台

## Installation
* Django框架

我们的开发均基于Django框架，因此要运行先要安装Django。

```bash
sudo apt-get install python-pip  # 这是Python的包管理器
sudo pip install django
```

检查是否安装成功，在python的交互终端中输入
```python
>>> import django
>>> django.VERSION
(1, 4, 2, 'final', 0)  # You may be glad to see this.
>>>
```

安装Django AJAX-utils, xlutils
```bash
sudo pip install django-ajaxutils, xlutils
```



## Database

### Postgresql

先安装相关的软件包

```bash
sudo apt-get install postgresql postgresql-client postgresql-server-all # Postgresql的数据库服务器
```

由于必须要使用`postgres`用户才能修改数据库，所以要修改用户`postgres`的默认密码

```bash
sudo passwd postgres
```

建立新的数据库`easdb`，登录用户名为`eas`，密码是`eduadminsystem`

```bash
sudo -u postgres createuser eas -P
sudo -u postgres createdb -O eas easdb
```

安装Postgresql的Python组件，及Django-Database-URL工具，用来根据系统环境变量`DATABASE_URL`来设定数据库的地址

```bash
sudo pip install psycopg2 dj-database-url
```

同步Django数据库并生成测试用数据

```bash
python manage.py syncdb
python createTestData.py
```

删除数据库

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

## 项目提交日期和方法
* Jan 3, 2013 23:00
* Mail to 杨腾飞
* 学号（后两位）名...项目
* xxx.doc/xxx.tex  打印一份
* 3~5min 视频
* /CODE 文件夹装代码
* 其它
