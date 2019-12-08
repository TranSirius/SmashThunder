// ref: https://segmentfault.com/a/1190000015709430
module.exports = {
	externals: {
		'vue': 'Vue',
		'vue-router': 'VueRouter',
		'axios': 'axios',
		// 'bootstrap-vue': 'BootstrapVue',
		'chart.js': 'Chart',
		'js-sha256': 'sha256',
		'showdown': 'showdown',
		'latex.js':'latexjs',
		'iframe-resizer': 'iFrameResize',
		// TODO: no showdown-math cdn
	}
}