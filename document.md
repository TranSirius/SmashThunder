# 结构文档

## 前提



## 注册

### 路由

/auth/register

### Method

POST

### Request 格式

```python
{
    'username':'username',
    'password':'password',
}
```

### Response 格式

```json
{
    'status':'status',		//正常返回ok，或者错误类型
}
```

### 用户名格式

```py
[a-zA-Z0-9_]{7,}
```

### 密码格式

## 登陆

### 路由

/auth/login

### Request 格式

```json
{
    'username':'username',
    'password':'password',
}
```

### Response 格式

## 自动登陆

### 路由

/auth/autoLogin

### Request 格式

### Response 格式
```json
{
    'status':str,           //ok, error
    'username':str,
}
```