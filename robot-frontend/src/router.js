import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Layout from './components/Layout.vue'
import Dashboard from './views/Dashboard.vue'
import Robots from './views/Robots.vue'
import Alerts from './views/Alerts.vue'
import Monitor from './views/Monitor.vue'
import Profile from './views/Profile.vue'



const routes = [
  { path: '/login', component: Login },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: Dashboard },
      { path: 'robots', component: Robots },
      { path: 'monitor', component: Monitor },
      { path: 'alerts', component: Alerts },
      { path: 'profile', component: Profile },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录只能去 login
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router