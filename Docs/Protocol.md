
## Authentication

### route = `/auth/register`

```python

req = {
  username: str,
  password: str,
}

res = {
status: str, # 正常返回ok，否则返回错误信息
}
```

### route = `/auth/login`

```python

req = {
  username: str,
  password: str,
}

res = {
  status: str, # 正常返回ok，否则返回错误信息
}
```

### route = `/auth/autoLogin`

```python
res = {
  username: str,
  status: str, # ok / error msg
}
```

### route = `/autu/logout`

```python
res = {
  status: str
}
```

## Image and Album

### route = `/submit/img`

```python
req = {
  albumTitle: str,
  files: list
}   # HTML Form

res = {
  status: str
}
```

### route = `/get/album`

```python
req = {
  username: str,
  target: str
}

res = {
  albums: [{
    title: str,
    createTime: int,
    imgs: [{
      url: str,
      title: str,
      time: int   # create time
    }]
  }]
  status: str
}
```

### route = `/edit/album/rename`

```python
req = {
  albumTitle: str,
  newTitle: str
}

res = {
  status: str
}

```

### route = `/edit/album/delete`

```python
req = {
  albumTitle: str
}

res = {
  status: str
}
```

### route = `/edit/img/rename`

```python
req = {
  albumTitle: str
  imgTitle: str
  newTitle: str
}

res = { 
  status: str
}
```

### route = `/edit/img/delete`

```python
req = {
  albumTitle: str
  imgTitle: str
}

res = {
  status: str
}
```

## Post and Folder

### route = `/submit/post`

```python
req = {
  title: str,
  content: str,
  folder: str,
  format: str,
  published: bool
}

res = {
  status = str
}
```

### route = `/get/post`

```python
req = {
  username: str,
  folder: str,
  postTitle: str
}

res = {
  title: str,
  content: str,
  createTime: int,
  format: str,
  postID: str,
  stars: int,
  comments: [{
    username: str,
    comment: str,
    time: int     # create time
  }]
  status: str
}
```

### route = `/get/post/foldersDetail`

```python
req = {

}

res = {
  folders: [{
    title: str,
    createdTime: int,
    posts: [{
      title: str,
      createTime: int,
      format: str,
      id: str,
      published: bool,
      stars: int,
      comments: int,
    }]
  }]
  status: str
}
```

### route = `/get/post/folders`

```python
req = {

}

res = {
  folders: [{
    title: str,
    posts: [{
      title: str
    }]
  }]
  status: str
}
```

### route = `/edit/post/rename`

```python
req = {
  folder: str,
  title: str,
  newTitle: ste
}

res = {
  status: str
}
```

### route = `/edit/post/delete`

```python
req = {
  folder: str,
  title: str
}

res = {
  status: str
}
```

### route = `/edit/post/publish`

```python
req = {
  folder: str,
  title: str,
  publish: bool
}

res = {
  status: str
}
```

### route = `/edit/folder/rename`

```python
req = {
  old: str,
  new: str
}

res = {
  status: str
}
```

### route = `/edit/folder/delete`

```python
req = {
  title: str
}

res = {
  status: str
}
```

## MainPage

### route = `/submit/mainpage`

```python
req = {
  folder: str,
  title: str
}

res = {
  status: str
}
```

### route = `/get/mainpage`

```python
req = {
  username: str
}

res = {
  post: {
    title: str,
    createTime: int,
    content: str,
    format: str,
    postID: str,
    stars: int,
    published: bool
    comments: [{
      username: str,
      comment: str,
      time: int
    }]
  }
}
```

## Social

### route = `/submit/comment`

```python
req = {
  folder: str,
  post: str,
  comment: str
}

res = {
  status: str
}
```

### route = `/submit/star`

```python
req = {
  username: str
  folder: str
  title: str
}

res = {
  status: str
}
```