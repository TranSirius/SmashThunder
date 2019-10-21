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

```json
{
	news: [{
		title: str,
		author: str,
		description: str,
		img: url,
		time: Unix Time Stamp str,
	}],
	friendsActivities: // the same as `news`
}
```