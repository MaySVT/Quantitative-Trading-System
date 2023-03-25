import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component:() =>  import('../components/Home.vue')
  },
  {
    path: '/backtest',
    name:'Classics',
    component: () => import('../components/Classics.vue')
  },
  {
    path: '/strategy',
    name:'Strategy',
    component: () => import('../components/Strategy.vue')
  },{
    path: '/data',
    name:'Heatmap',
    component: () => import('../components/Heatmap.vue')
  },{
    path: '/factor',
    name:'Asset',
    component: () => import('../components/Asset.vue')
  },{
    path: '/mannual',
    name:'Hello',
    component: () => import('../components/HelloWorld.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router