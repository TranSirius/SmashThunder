import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'

Vue.config.productionTip = false

import News from "./components/view/News.vue"
import Album from "./components/view/Album.vue"
import Edit from "./components/view/Edit.vue"
import Posts from "./components/view/Posts.vue"
import Manage from "./components/view/Manage.vue"
import Post from "./components/view/Post.vue"
import Admin from "./components/view/Admin.vue"
import Star from "./components/view/Star.vue"
import Follow from "./components/view/Follow.vue"
import UserSearched from "./components/view/UserSearched.vue"
import PostSearched from "./components/view/PostSearched.vue"
import PhotoSearched from "./components/view/PhotoSearched.vue"

const routes = [
  {
    path: '/', component: News,
  },
  {
    path: '/admin', component: Admin
  },
  {
    path: '/searchusers', component: UserSearched
  },
  {
    path: '/searchposts', component: PostSearched
  },
  {
    path: '/searchphotos', component: PhotoSearched
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
    path: '/:username/star', component: Star
  },
  {
    path: '/:username/follow', component: Follow
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
