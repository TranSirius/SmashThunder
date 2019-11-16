import axios from 'axios'
import errHandler from './errHandler'

/**
 * Because the function `apiPost` need to use the mixin `errHandler` to this file has to be a mixin.
 */
export default {
	methods: {
		toastErr: errHandler.methods.toastErr,
		/**
		 * `data`, `okFunc`, `errTitle` and `errFunc` can be undefined
		 */
		apiPost({ route, data }, okFunc, errTitle, errFunc) {
			axios.post(route, data).then(res => {
				if (res.data.status == 'ok') { okFunc && okFunc(res.data) }
				else {
					this.toastErr(errTitle, res.data.status);
					errFunc && errFunc()
				}
			}).catch(() => {
				this.toastErr(errTitle)
				errFunc && errFunc()
			})
		}
	}
}