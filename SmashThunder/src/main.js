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
import Edit from "./components/view/Edit.vue"
import Posts from "./components/view/Posts.vue"
import Manage from "./components/view/Manage.vue"
import Post from "./components/view/Post.vue"
import Admin from "./components/view/Admin.vue"

const routes = [
  {
    path: '/', component: News,
  },
  {
    path: '/admin', component: Admin
  },
  {
    path: '/:username', component: Post,
    name: 'toMainPage'
  },
  {
    path: '/:username/album', component: Album
  },
  {
    path: '/:username/edit', component: Edit
  },
  {
    path: '/:username/posts', component: Posts
  },
  {
    path: '/:username/manage', component: Manage
  },
  {
    path: '/:username/posts/:folder/:title', component: Post,
    name: 'toPost'
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
