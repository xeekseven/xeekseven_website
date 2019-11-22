## 一、 部署
### 部署flask程序
> 有时候需要开发简单的web,可能涉及一点简单的动态操作,flask开发起来效率还不错


> uwsgi这是一个web服务器，负责监听端口，一般有:http(s)和socket模式
1. http(s)这种直接监听http请求。
2. socket模式只是监听了套接字端口,一般配合nginx转发http请求来使用


#### 一、直接http(s)来部署

1. flask程序
```
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return "<span style='color:red'>I am app 1</span>"
```
2. uwsgi.ini 配置,放一个我常用的一种。
```
[uwsgi]
http=0.0.0.0:5005
wsgi-file=/usr/websites/xmrpy/website/index.py
callable=app
processes=4
threads=2
```


3. 运行:当然有很多种管理方式，我们可以使用最傻瓜的轻量后台运行方式
```
nohup uwsgi uwsgi.ini &
```
4. 输入shell命令正常退出,不然异常退出还是很终止
```
exit
```


## 二、vscode测试

#### 1. 直接调试单个python文件，F5 main.py 文件即可
#### 2. 调试的时候选择flask，此时文件选择 xeekswebsite_server/__init__.py




### 附录
[uwsgi官网](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html)


