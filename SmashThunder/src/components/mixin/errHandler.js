export default {
	methods: {
		/**
		 * `msg` defaults to `'Internal Server Error!'`
		 */
		toastErr(title, msg) {
			this.$bvToast.toast(msg || 'Internal Server Error!', {
				title,
				autoHideDelay: 5000
			});
		}
	}
}