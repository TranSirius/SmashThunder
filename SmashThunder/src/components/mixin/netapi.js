import axios from 'axios'
import errHandler from './errHandler'

/**
 * Because the function `apiPost` need to use the mixin `errHandler` to this file has to be a mixin.
 */
export default {
	methods: {
		toastErr: errHandler.methods.toastErr,
		/**
		 * `data`, `config`, `okFunc`, `errTitle` and `errFunc` can be undefined
		 */
		apiPost({ route, data, config }, okFunc, errTitle, errFunc) {
			axios.post(route, data, config).then(res => {
				if (res.data.status == 'ok') { okFunc && okFunc(res.data) }
				else {
					this.toastErr(errTitle, res.data.status);
					errFunc && errFunc()
				}
			}).catch((err) => {
				this.toastErr(errTitle)
				// TODO: remove console.log
				this.console.log(err)
				errFunc && errFunc()
			})
		}
	}
}