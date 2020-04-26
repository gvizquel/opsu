<template>
  <div>
    <nav id="sidebar" class="active">
      <div class="sidebar-header">
        <h3>Libro de Oportunidades</h3>
      </div>
      <ul class="components">
        <h4 class="text-center">FILTRAR</h4>
        <li>
          <b-button v-b-modal.state variant="primary">
                Por estado
          </b-button>
        </li>
        <li>
          <b-button v-b-modal.municipality 
                    :class="disabled">
                Por municipio
          </b-button>
        </li>
        <li>
          <b-button v-b-modal.parish 
                    :class="disabled">
                Por parroquía
          </b-button>
        </li>
        <li>
          <b-button v-b-modal.modal-scrollable 
                    :class="disabled">
                Por centro poblado
          </b-button>
        </li>   
      </ul>
    </nav>

    <FilterModalState
      :states="states"
      @enable="enable">
    </FilterModalState>

     <FilterModalMunicipality
      :municipalitys="municipalitys">
    </FilterModalMunicipality>

     <FilterModalParish
      :parishs="parishs">
    </FilterModalParish>

  </div>
</template>
<script>

import EventBus from '../../bus'
import FilterModalState from '@/components/templates/FilterModalState.vue'
import FilterModalMunicipality from '@/components/templates/FilterModalMunicipality.vue'
import FilterModalParish from '@/components/templates/FilterModalParish.vue'
import axios from 'axios'
  export default {
    
    data() {
      return {
        states: [],
        municipalitys: [],   
        parishs: [],
        disabled: 'disabled'
      }
    },
    components: {
      FilterModalState,
      FilterModalMunicipality,
      FilterModalParish
    },
    methods: {
      enable(params) {
        
        if (params[0] != undefined) 
        {

          this.disabled = ''
          this.getmunicipality(params);
          this.getParish(params);

        } else {
          
          this.disabled = 'disabled';

        }

      },
      dataProcess(data, filter) {

        let array = [];
        
        for (var j =0; j < filter.length; j++) 
        {
            for (var i = 0; i < data.length; i++) 
            {
              if(data[i].estado == filter[j]) 
              { 
                array.push(data[i])
              }
            }

        }

        return array;
      },
      async getStates(){            
            try {
                const response = await axios.get('http://loe.terna.net/api-v1/estado/listar/')

                if (response.data.results.length == 0) {
                    this.messageNull = 'Disculpe, en estos momentos no hay carreras registradas'
                }else{

                  this.states = await response.data.results; 

                }
            } catch (error) {
                console.log('error', error);    
            }
        },
        async getmunicipality(params){            
            try {
                const response = await axios.get('http://loe.terna.net/api-v1/municipio/listar/')

                if (response.data.results.length == 0) {
                    this.messageNull = 'Disculpe, en estos momentos no hay carreras registradas'
                }else{

                  let me = this;
                  let municipality = await response.data.results;
                  me.municipalitys = me.dataProcess(municipality, params);

                }
            } catch (error) {
                console.log('error', error);    
            }
        },
        async getParish(params){            
            try {
                const response = await axios.get('http://loe.terna.net/api-v1/parroquia/listar/')

                if (response.data.results.length == 0) {
                    this.messageNull = 'Disculpe, en estos momentos no hay carreras registradas'
                }else{
                  
                  let self = this;
                  let parish = await response.data.results;
                  self.parishs = self.dataProcess(parish, params);

                }
            } catch (error) {
                console.log('error', error);    
            }
        }
    },
    mounted () {
      this.getStates();
    }

}
</script>

<style>
/* ---------------------------------------------------
    SIDEBAR STYLE
----------------------------------------------------- */
#states {
  font-size: 15px;
}

#sidebar {
  min-width: 250px;
  max-width: 250px;
  background: #C22974;
  color: #fff;
  transition: all 0.3s;
  height: 100%;
  box-shadow: 3px 3px 3px rgba(0, 0, 0, .3);
}

#sidebar.active { margin-left: -250px; }

#sidebar .sidebar-header {
  padding: 20px;
  box-shadow: 3px 3px 3px rgba(0, 0, 0, .3);
  background: #F3BD19;
}

#sidebar ul.components { padding: 20px 0; }

#sidebar ul li button{ width: 100%; }

#sidebar ul li a, 
#sidebar ul li button{
  padding: 10px;
  font-size: 1.1em;
  display: block;
  text-decoration: none;
  color:#fff;
}

#sidebar ul li a:hover,
#sidebar ul li button:hover {
  color: rgb(192, 75, 132);
  background: #fff;
}

.dropdown-toggle::after {
    display: block;
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
}

.collapse > li > a {
    font-size: .95em !important;
    padding-left: 30px !important;
    background: rgb(187, 54, 118);
}
/* ---------------------------------------------------
    MEDIAQUERIES
----------------------------------------------------- */

@media (max-width: 768px) {
    #sidebar {
        margin-left: -250px;
    }
    #sidebar.active {
        margin-left: 0;
    }
    #sidebarCollapse span {
        display: none;
    }
}

</style>