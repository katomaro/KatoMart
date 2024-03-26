const { createApp } = Vue
const { createRouter, createWebHistory } = VueRouter

import App from './views/_app.js'
import Accounts from './views/accounts.js'
import Config from './views/config.js'
import Courses from './views/courses.js'
import Home from './views/home.js'
import Logs from './views/logs.js'
import Support from './views/support.js'
import Terms from './views/terms.js'

const routes = [
  { path: '/', component: Home },
  { path: '/accounts', component: Accounts },
  { path: '/config', component: Config },
  { path: '/courses', component: Courses },
  { path: '/logs', component: Logs },
  { path: '/support', component: Support },
  { path: '/terms', component: Terms },
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)

app.use(router)

app.mount('#app')