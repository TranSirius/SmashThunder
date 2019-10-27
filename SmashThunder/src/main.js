import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import VueRouter from 'vue-router'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(BootstrapVue)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import News from "./components/view/News.vue"
import Album from "./components/view/Album.vue"

const routes = [
  {
    path: '/', component: News,
  },
  {
    path: '/:username/album', component: Album
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})


new Vue({
  render: h => h(App),
  data: {
    user: {
      username: "",
      loggedIn: false
    }
  },
  router
}).$mount('#app')
