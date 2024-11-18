const { createApp } = Vue
const { createRouter, createWebHistory } = VueRouter

import { alert } from './stores.js'
import App from './views/_app.js'
import Accounts from './views/accounts.js'
import Agreement from './views/agreement.js'
import Config from './views/config.js'
import Courses from './views/courses.js'
import Home from './views/home.js'
import Logs from './views/logs.js'
import Support from './views/support.js'

const routes = [
  { path: '/', component: Home, meta: { requiresConsent: true } },
  { path: '/accounts', component: Accounts, meta: { requiresConsent: true } },
  { path: '/config', component: Config, meta: { requiresConsent: true } },
  { path: '/courses', component: Courses, meta: { requiresConsent: true } },
  { path: '/logs', component: Logs, meta: { requiresConsent: true } },
  { path: '/support', component: Support },
  { path: '/agreement', component: Agreement },
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresConsent)) {
    const { consent } = await fetch('/api/agreement').then(res => res.json())
    if (!consent) {
      alert.message = 'Por favor, aceite os termos de uso antes de prosseguir.'
      console.log(alert)
      next({ path: '/agreement' })
    } else {
      alert.message = ''
      next()
    }
  } else {
    alert.message = ''
    next()
  }
})

const app = createApp(App)

app.use(router)

app.mount('#app')