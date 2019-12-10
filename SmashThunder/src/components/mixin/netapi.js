import axios from 'axios'
import errHandler from './errHandler'

var urlEncodeTable = [
	{ raw: '%', target: '%25' }, // `%` has to be replaced first.
	{ raw: '+', target: '%2B' },
	{ raw: ' ', target: '%20' },
	{ raw: '/', target: '%2F' },
	{ raw: '?', target: '%3F' },
	{ raw: '#', target: '%23' },
	{ raw: '&', target: '%26' },
	{ raw: '=', target: '%3D' },
]

// ref: https://stackoverflow.com/questions/1144783/how-to-replace-all-occurrences-of-a-string
String.prototype.replaceAll = function (search, replacement) {
	var target = this;
	return target.split(search).join(replacement);
};

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
		},
	},
	filters: {
		urlEncode(s) {
			return urlEncodeTable.reduce((result, current) => result.replaceAll(current.raw, current.target), s)
		},
		urlDecode(s) {
			return urlEncodeTable.reduce((result, current) => result.replaceAll(current.target, current.raw), s)
		}
	}
}