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
(1, 4, 2, 'final', 0)  # You may glad to see this.
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

## Trouble Shooting
* 看起来css或js用的不是最新的代码？

在根目录执行`python manage.py collectstatic`然后再`runserver`就可以了。
