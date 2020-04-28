<template>
    <div>
        <b-modal id="university" scrollable 
        :title="'Institución: '+university.localidad.ieu.nombre+' ('+university.localidad.ieu.siglas+')'"
        ok-only
        ok-title="cerrar">
            
            <p class="text-center"><strong>Detalles</strong></p>
            <p v-text="university.nombre"></p>
            <p v-text="university.titulo"></p>
            <p v-text="university.descripcion"></p>
            <p v-text="university.duracion"></p>
            <p v-text="university.area_conocimiento"></p>
            <p v-text="university.sub_area_conocimiento"></p>
            <p v-text="university.localidad.nombre"></p>
            <p v-text="university.localidad.estado"></p>
            <p v-text="university.localidad.parroquia"></p>
            <p v-text="university.localidad.direccion"></p>
            <p v-text="university.localidad.ieu.dep_admin"></p>
            <p v-if="university.localidad.punto === null" class="text-center"></p>
            <span v-else>
                <b-button class="mt-3" variant="outline-danger" block @click="map(university.localidad.punto.coordinates)">Ver en el mapa</b-button>
            </span>

        </b-modal>
    </div>
</template>
<script>

import EventBus from '../bus'
import axios from 'axios'
  export default {
    props: ['university'],   
    data() {
      return {

      }
    },
    filters: {
        fiters(){
            
        }
    },
    methods: {
      map(coordinates) {
          EventBus.$emit('coordinates_map',coordinates.reverse());
          this.$bvModal.hide('university')          
      }      
    },
}
</script>