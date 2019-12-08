// ref: https://segmentfault.com/a/1190000015709430
module.exports = {
	externals: {
		'vue': 'Vue',
		'vue-router': 'VueRouter',
		'axios': 'axios',
		// 'bootstrap-vue': 'BootstrapVue', // TODO: no china cdn
		'chart.js': 'Chart',
		'js-sha256': 'sha256',
		'showdown': 'showdown',
		// TODO: no latex.js cdn
		'iframe-resizer': 'iFrameResize',
		// TODO: no showdown-math cdn
	}
}