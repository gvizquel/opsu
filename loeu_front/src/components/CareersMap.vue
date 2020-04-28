<template>
    <div>
       <b-card no-body>
            <b-tabs card v-model="tabIndex">
                <b-tab title="Lista de Carreras" active>
                    <TablaCarreras/>
                </b-tab>
                <b-tab title="Mapa">
                   <Map :coordinates="coordinates"/>
                </b-tab>
            </b-tabs>
        </b-card>
    </div>
</template>
<script>

import EventBus from '../bus'
import Map from '@/components/busqueda/Map.vue'
import TablaCarreras from '@/components/TableCareers.vue'
import {mapMutations} from 'vuex'

export default {
    data() {
        return{
            tabIndex: 0,
            coordinates: []
        }
    },
    components:{
        Map,
        TablaCarreras
    },
    methods: {
       ...mapMutations(['showInputNavCarreras']),
       coordMap() {
            let me = this
            EventBus.$on('coordinates_map', function (coordinates) {
                
                if(coordinates != '') {
                    me.coordinates = coordinates
                    me.tabIndex++
                }

            });
       }
    },
    mounted(){
       this.showInputNavCarreras()
       this.coordMap()
    }
}
</script>