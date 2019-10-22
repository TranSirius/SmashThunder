# SmashThunder

## Front route

- `/` - News
- `/static/` - Static asset files
- `/:username` - User homepage
- `/:username/album` - User's image management page
- `/:username/posts` - User's posts management page
- `/:username/posts/:post` - User's post
- `/edit` - New post or edit existing post
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
		"imgs": [{
			"url": "str",
			"title": "str",
			"subtitle": "str",
			"time": "Unix Time Stamp(int)"
		}]
	}]
}
```

## Backend folder structure

### User data

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

- dist/
  - index.html
  - static/
    - css/
      - :filename
    - js/
      - :filename