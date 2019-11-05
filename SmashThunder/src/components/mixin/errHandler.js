export default {
	methods: {
		toastErr(title = 'Error!', msg = 'Internal Server Error!', variant = 'danger', toaster = 'top-right') {
			this.$bvToast.toast(msg, {
				title,
				variant,
				toaster: 'b-toaster-' + toaster,
				autoHideDelay: 5000
			});
		}
	}
}