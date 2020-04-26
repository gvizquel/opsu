<template>
    <div>
       <b-card no-body>
            <b-tabs card>
                <b-tab title="Lista de Carreras" active>
                    <TablaCarreras/>
                </b-tab>
                <b-tab title="Mapa">
                   <Map/>
                </b-tab>
            </b-tabs>
        </b-card>
    </div>
</template>
<script>

import Map from '@/components/busqueda/Map.vue'
import TablaCarreras from '@/components/TableCareers.vue'
import {mapMutations} from 'vuex'

export default {
    components:{
        Map,
        TablaCarreras
    },
    methods: {
       ...mapMutations(['showInputNavCarreras'])
    },
    mounted(){
       this.showInputNavCarreras()
    }
}
</script>