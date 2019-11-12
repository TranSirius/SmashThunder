# 网络接口文档

## 概述

网络接口使用RPC设计原则，所有接口均使用POST方法，返回HTTP状态码均为200

## 鉴权

鉴权接口路由前缀：`/auth`

用户名满足正则表达式`[a-zA-Z0-9_]{7,}`，密码客户端sha256加密，原密码可以为空

### 注册

```python
route = '/auth/register'

req = {
  username: str,
  password: str,
}

res = {
  status: str, # 正常返回ok，否则返回错误信息
}
```

### 登陆

```python
route = '/auth/login'

req = {
  username: str,
  password: str,
}

res = {
  status: str, # 正常返回ok，否则返回错误信息
}
```

### 自动登陆

使用请求中的cookie鉴权，请求中不带参数

```python
route = '/auth/autoLogin'

res = {
  username: str,
  status: str, # ok / error msg
}
```

## 数据交互

路由前缀`/get`

### 上传图片

将图片上传到指定用户的指定相册

```

### 新闻和好友动态

返回最新的博客文章。使用cookie判断用户身份

```python
route = '/get/news`

req = {
  target: str, # 'news' or 'friendsActivity'
}

res = {
  status: str, # ok / err msg
  posts: [{
    title: str,
    author: str,
    description: str,
    img: str, # url
    time: int, # Unix Time Stamp, a big integer
  }]
}
```
