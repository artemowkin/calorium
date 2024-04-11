import { createRouter, createWebHistory } from 'vue-router'
import CalculatorView from '../views/CalculatorView.vue'
import AuthenticationView from '@/views/AuthenticationView.vue'
import StatisticView from '@/views/StatisticView.vue'
import UserView from '@/views/UserView.vue'
import { refresh } from '@/api/users'
import ProductsView from '@/views/ProductsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: CalculatorView,
    },
    {
      path: '/login',
      name: 'login',
      component: AuthenticationView,
    },
    {
      path: '/statistic',
      name: 'statistic',
      component: StatisticView,
    },
    {
      path: '/user',
      name: 'user',
      component: UserView,
    },
    {
      path: '/products',
      name: 'products',
      component: ProductsView,
    }
  ]
})

router.beforeEach(async (to) => {
  if (['login'].includes(to.name as string)) return true

  const token = localStorage.getItem('refreshToken')
  
  if (token) {
    try {
      const tokens = await refresh(token)
      localStorage.setItem('accessToken', tokens.access_token)
      localStorage.setItem('refreshToken', tokens.refresh_token)
    } catch {
      localStorage.clear()
      return
    }
  } else {
    console.log(to.name)
    if (to.name === 'home') return true

    return { name: 'login' }
  }
})

export default router
