export default {
	methods: {
		/**
		 * Check whether every element in this array is unique.
		 */
		checkUniqueness(arr, key = '') {
			var t = arr.slice().sort((a, b) => {
				if (key)
					return a[key] - b[key]
				else return a - b
			})
			for (let i = 0; i < t.length - 1; ++i)
				if (key) {
					if (t[i][key] == t[i + 1][key]) return false
				}
				else {
					if (t[i] == t[i + 1]) return false
				}
			return true
		}
	}
}