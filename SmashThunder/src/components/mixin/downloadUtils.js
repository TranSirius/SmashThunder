export default {
	methods: {
		download(url, title) {
			var t = document.createElement("a");
			t.setAttribute("href", url);
			t.setAttribute("download", title);
			t.click();
		}
	}
}