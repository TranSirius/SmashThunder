export default {
	methods: {
		toastErr(title = 'Error!', msg = 'Internal Server Error!', variant = 'danger', toaster = 'top-right') {
			this.$bvToast.toast(msg, {
				title,
				variant: variant,
				toaster: 'b-toastr-' + toaster,
				autoHideDelay: 5000
			});
		}
	}
}