import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component:() =>  import('../components/Home.vue')
  },
  {
    path: '/backtest',
    name:'Backtest',
    component: () => import('../components/Backtest.vue')
  },
  {
    path: '/strategy',
    name:'Strategy',
    component: () => import('../components/Strategy.vue')
  },{
    path: '/data',
    name:'Data',
    component: () => import('../components/DataAPI.vue')
  },{
    path: '/factor',
    name:'Factor',
    component: () => import('../components/Factor.vue')
  },{
    path: '/mannual',
    name:'Mannual',
    component: () => import('../components/Mannual.vue')
  },{
    path: '/login',
    name:'Login',
    component: () => import('../components/Login.vue')
  },{
    path: '/register',
    name:'Register',
    component: () => import('../components/Register.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router