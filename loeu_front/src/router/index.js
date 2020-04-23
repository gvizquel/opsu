import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/busqueda',
    name: 'Busqueda',
    component: () => import('../views/Busqueda.vue'),
    children: [
      { path: 'carreras-pnf', component: () => import('../components/busqueda/CarrerasMap.vue') },
      { path: 'instituciones', component: () => import('../components/busqueda/InstitutionsMap.vue')}
    ]
  },
  {
    path: '*',
    name: '404',
    component: () => import('../views/404.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
