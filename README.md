# 教务系统
这是大三软件工程作业

## Members
* [叶晓军](https://github.com/iphkwan)
* [杨曦华](https://github.com/19thhell)
* [钟宇腾](https://github.com/zonyitoo)
* [柯毅豪](https://github.com/sheepke)

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

## 数据库
* 用户名：eduadminsystem
* 密码：eduadminsystem
* 数据库名：eduadminsystemdb

```sql
grant all privileges on eduadminsystemdb.* to eduadminsystem@localhost identified by
"eduadminsystem";
```

* 创建数据库时要设置字符集为UTF-8
```sql
create database eduadminsystemdb character set utf8;
```

## Trouble Shooting
* 怎么运行？

直接在根目录执行`python manage.py runserver`，若看到出错信息，先保证你已安装好Django，安装方向见上。

* 看起来css或js用的不是最新的代码？

在根目录执行`python manage.py collectstatic`然后再`runserver`就可以了。

* 管理员帐号的创建？

在根目录执行`python manage.py syncdb`然后按提示创建管理员帐号。（e.g. admin@admin）

利用django自带的后台，创建管理员帐号，即可在:`127.0.0.1：8000/admin/`中进行帐号/组管理。

## 项目提交日期和方法
* Jan 3, 2013 23:00
* Mail to 杨腾飞
* 学号（后两位）名...项目
* xxx.doc/xxx.tex  打印一份
* 3~5min 视频
* /CODE 文件夹装代码
* 其它
=
