/**
 * Because the function `toastErr` need to use `this` so it has to be a mixin.
 */
export default {
	methods: {
		/**
		 * `toastErr(title = 'Error!', msg = 'Internal Server Error!', variant = 'danger', toaster = 'top-right', autoHideDelay = 5000)`
		 */
		toastErr(title = 'Error!', msg = 'Internal Server Error!', variant = 'danger', toaster = 'top-right', autoHideDelay = 5000) {
			this.$bvToast.toast(msg, {
				title,
				variant,
				toaster: 'b-toaster-' + toaster,
				autoHideDelay
			});
		}
	}
}