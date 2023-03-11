import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/classics',
    name:'Classics',
    component: () => import('../components/Classics.vue')
  },
  {
    path: '/heatmap',
    name:'Heatmap',
    component: () => import('../components/Heatmap.vue')
  },{
    path: '/asset',
    name:'Asset',
    component: () => import('../components/Asset.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router