export default {
	filters: {
		/**
		 * `s` has to be a `Number`
		 */
		timeOffset(s) {
			var now = new Date(Date.now());
			var t = new Date(s);
			var offset = new Date(now - t);
			// different year
			if (offset.getFullYear() - 1970 == 1) return "1 year";
			else if (offset.getFullYear() - 1970 > 0)
				return offset.getFullYear() - 1970 + " years";
			// different month
			else if (offset.getMonth() == 1) return "1 month";
			else if (offset.getMonth() > 0) return offset.getMonth() + " months";
			// different day
			else if (offset.getDate() == 2) return "1 day";
			else if (offset.getDate() > 1) return offset.getDay() - 1 + " days";
			// different hour
			else if (offset.getHours() == 9) return "1 hour";
			else if (offset.getHours() > 8) return offset.getHours() - 8 + " hours";
			// different minutes
			else if (offset.getMinutes() == 1) return "1 minute";
			else if (offset.getMinutes() > 0) return offset.getMinutes() + " minutes";
			// just now
			else return "less than 1 minute";
		},
		/**
		 * `s` has to be a `Number`
		 */
		peekDate(s) {
			var t = new Date(s);
			return t.toDateString();
		}
	}
}