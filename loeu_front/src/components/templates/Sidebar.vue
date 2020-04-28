<template>
  <div>
    <nav id="sidebar" class="active">
      <ul class="components">
          <h4 class="text-center text-white">Filtrar datos</h4>
        <hr>  
        <li>
          <b-button v-b-modal.state variant="transparent">
                Por estado
          </b-button>
        </li>
        <li>
          <b-button v-b-modal.municipality 
                    :class="disabled"
                    variant="transparent">
                Por municipio
          </b-button>
        </li>
        <li>
          <b-button v-b-modal.parish 
                    :class="disabled"
                    variant="transparent">
                Por parroquia
          </b-button>
        </li>
        <li>
          <b-button v-b-modal.modal-scrollable 
                    :class="disabled"
                    variant="transparent">
                Por centro poblado
          </b-button>
        </li>  
        <div class="sidebar-header">
        <h4 class="text-center text-white">Libro de oportunidades de estudio</h4>
      </div> 
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
        municipalityAll: [],  
        parishs: [],
        parishAll: [],
        disabled: '' /*revisar esta funcionalidad*/
      }
    },
    components: {
      FilterModalState,
      FilterModalMunicipality,
      FilterModalParish
    },
    methods: {
      enable(params) {
        if (params){
          this.municipalitys = this.dataProcess(this.municipalityAll, params);
          this.parishs = this.dataProcess(this.parishAll, params);
          
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
      async getSMP(url, datas, variable) {
          try {
              const response = await axios.get(url)

              if (response.data.results.length == 0) {
                  this.messageNull = 'Disculpe, en estos momentos no hay carreras registradas'
              }else{

                let me = this;
                const retrivedData = datas.concat(response.data.results)
                
                if (response.data.next !== null) {
                  me.getSMP(response.data.next, retrivedData, variable);
                } else {
                  let allData = retrivedData;
                  
                  if (variable == 'states') {
                    this.states = allData;
                  } else if (variable == 'municipality') {
                    this.municipalityAll = allData;
                  } else if (variable == 'parish') {
                    this.parishAll = allData
                  }
                }

              }

          } catch (err) {
            console.log('error:', err);    
          }
      },
    },
    created () {
      this.getSMP('http://loe.terna.net/api-v1/estado/listar/', [], 'states');      
      this.getSMP('http://loe.terna.net/api-v1/municipio/listar/', [], 'municipality');
      this.getSMP('http://loe.terna.net/api-v1/parroquia/listar/', [], 'parish');
    }
}
</script>

<style>

#states { font-size: 15px }

#sidebar {
  min-width: 290px;
  max-width: 290px;
  background: url('../../assets/login.jpg') no-repeat;
  transition: all 0.3s;
  height: 100%;
  box-shadow: 3px 3px 3px rgba(0, 0, 0, .3);
}

#sidebar.active { margin-left: -290px; }

#sidebar .sidebar-header {
  max-width: 300px;
  padding: 20px 20px; 
  bottom: 1px;
  position: fixed;
}

#sidebar ul.components { padding: 5px 0;}

#sidebar ul li button{ width: 100%; }

#sidebar ul li a, 
#sidebar ul li button{
  padding: 10px;
  font-size: 1.29em;
  display: block;
  text-decoration: none;
  color:#000;
  margin-top: 5px;
}

#sidebar ul li a:hover,
#sidebar ul li button:hover {
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