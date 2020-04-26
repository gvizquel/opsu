<template>
    <div>
        <b-modal id="municipality" scrollable title="Filtros por municipio"
          @ok="emitMunicipalitys()">
            <b-form-group label="Municipios:">
                <br>
                <b-form-checkbox
                  v-for="municipality in municipalitys"
                  v-model="filter_municipality"
                  :key="municipality.id"
                  :value="municipality.nombre"
                  name="flavour-3a"
                  switch
                >
                  {{ municipality.nombre }}
                </b-form-checkbox>

            </b-form-group>
        </b-modal>
    </div>
</template>
<script>

import EventBus from '../../bus'
import axios from 'axios'
  export default {
    props: ['municipalitys'],   
    data() {
      return {
        filter_municipality: [],
      }
    },
    methods: {
      emitMunicipalitys() {
        let self = this;        

        if (self.filter_municipality){
          EventBus.$emit('municipality_filter',self.filter_municipality);
        }
      }      
    },
}
</script>