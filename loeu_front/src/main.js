import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'

//IMPORTS BOOTSTRAP-VUE
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.min.css'

//IMPORTS LEAFLETS-MAPS
import 'leaflet/dist/leaflet.css';

// IMPORT DataTable VueJs
import VueGoodTable from 'vue-good-table';

Vue.use(VueGoodTable);
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')