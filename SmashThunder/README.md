# SmashThunder

## Set up

- Run `npm install` to install.
- Run `npm run serve` to start server.
- Run `npm run build` to build.

## Front route

- `/` - News
- `/static/` - Static asset files
- `/:username` - User homepage
- `/:username/album` - User's image management page
- `/:username/posts` - User's posts management page
- `/:username/posts/:folder/:post` - User's post
- `/:username/edit` - New post or edit existing post
- `/:username/star` - User's star management page
- `/:username/follow` - User's follow management page'
- `/admin` - Admin homepage

## Data format

### News page

```jsonc
{
	"news": [{
		"title": "str",
		"author": "str",
		"description": "str",
		"img": "url",
		"time": "Unix Time Stamp(int)",
	}],
	"friendsActivities": [{}] // the same as `news`
}
```

### Album page

```jsonc
{
	"albums": [{
		"title": "str",
		"createTime": "Unix Time Stamp(int)",
		"imgs": [{
			"url": "str",
			"title": "str",
			"time": "Unix Time Stamp(int)"
		}]
	}]
}
```

## Backend folder structure

### User data

This folder is under `/share`.

- data/
  - :username/
    - img/
      - :foldername/
        - :filename
    - html/
      - :filename
    - md/
      - :filename

### Static

This folder is under `/share`.

- SmashThunder/
  - index.html
  - static/
    - css/
      - :filename
    - js/
      - :filename