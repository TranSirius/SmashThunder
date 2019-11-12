export default {
	methods: {
		/**
		 * `s` can not contain reserved chars of URL
		 */
		checkFileName(s) {
			return !/[!*'();:@&=+$,/?#[\]]/.test(s)
		}
	}
}