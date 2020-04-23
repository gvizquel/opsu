import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    inputSearch: false,
    searchInstitutions: false,
    iconNavbar: false,
  },
  mutations: {
    showInputNavCarreras(state){ // MOSTRAR INPUT PARA BUSCAR CARRERAS
      state.inputSearch = true    
    },
    hideInputNavCarreras(state){ // OCULTAR INPUT PARA BUSCAR CARRERAS  
      state.inputSearch = false;    
    },
    showInputNavInstitutions(state){ // MOSTRAR INPUT PARA BUSCAR INSTITUCIONES 
      state.inputSearch = true;
      state.searchInstitutions = ! state.searchInstitutions;
    },
    hideInputNavInstitutions(state){ // OCULTAR INPUT PARA BUSCAR INSTITUCIONES
      state.inputSearch = false;    
    },
    showSidebar_iconNav(state){ //CAMBIA EL ESTADO DEL SIDEBAR Y MODIFICA EL ICONO DEL NAVBAR
      state.iconNavbar = ! state.iconNavbar;    
      let sidebar = document.getElementById("sidebar");
      sidebar.classList.toggle("active");
    },

  },
  actions: {
  },
  modules: {
  }
})
