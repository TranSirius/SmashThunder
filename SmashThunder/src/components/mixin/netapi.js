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
		 * 
		 * If `errTitle` is `''`, no err toast will be shown.
		 * 
		 * For debug, every request should be sent by this api 
		 * because this api will modify the path to an absolute path
		 * to fit CORS
		 */
		apiPost({ route, data, config }, okFunc, errTitle, errFunc) {
			axios.post((process.env.NODE_ENV === 'development' ? 'http://smashthunder.com' : '') + route, data, config).then(res => {
				if (res.data.status == 'ok') { okFunc && okFunc(res.data) }
				else {
					if (errTitle)
						this.toastErr(errTitle, res.data.status);
					errFunc && errFunc()
				}
			}).catch(() => {
				if (errTitle)
					this.toastErr(errTitle)
				errFunc && errFunc()
			})
		}
	}
}