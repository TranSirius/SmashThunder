import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import VueRouter from 'vue-router'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(BootstrapVue)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// register global filter
Vue.filter('timeOffset', s => {
  var now = new Date(Date.now());
  var t = new Date(s);
  var offset = new Date(now - t);
  // different year
  if (offset.getFullYear() - 1970 == 1) return "1 year";
  else if (offset.getFullYear() - 1970 > 0)
    return offset.getFullYear() - 1970 + " years";
  // different month
  else if (offset.getMonth() == 1) return "1 month";
  else if (offset.getMonth() > 0) return offset.getMonth() + " months";
  // different day
  else if (offset.getDate() == 2) return "1 day";
  else if (offset.getDate() > 1) return offset.getDay() - 1 + " days";
  // different hour
  else if (offset.getHours() == 9) return "1 hour";
  else if (offset.getHours() > 8) return offset.getHours() - 8 + "hours";
  // different minutes
  else if (offset.getMinutes() == 1) return "1 minute";
  else if (offset.getMinutes() > 0) return offset.getMinutes() + " minutes";
  // just now
  else return "less than 1 minute";
})
Vue.filter('peekDate', s => {
  var t = new Date(s);
  return t.toDateString();
})

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
