import axios from 'axios'
import errHandler from './errHandler'

/**
 * Because the function `apiPost` need to use the mixin `errHandler` to this file has to be a mixin.
 */
export default {
	methods: {
		toastErr: errHandler.methods.toastErr,
		apiPost(route, data, okFunc, errTitle, errFunc = null) {
			axios.post(route, data).then(res => {
				if (res.data.status == 'ok') { okFunc(res.data) }
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