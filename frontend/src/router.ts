import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import RequestCreateView from './views/RequestCreateView.vue'
import RequestDetailView from './views/RequestDetailView.vue'
import RequestsListView from './views/RequestsListView.vue'

const routes: RouteRecordRaw[] = [
  { path: '/', redirect: '/requests' },
  { path: '/requests', name: 'requests-list', component: RequestsListView },
  { path: '/requests/new', name: 'requests-new', component: RequestCreateView },
  {
    path: '/requests/:id',
    name: 'requests-detail',
    component: RequestDetailView,
    props: true
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
