<template>
    <div>
       <b-card no-body>
            <b-tabs card>
                <b-tab title="Lista de instituciones" active>
                    <b-card-text>prueba</b-card-text>
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
import { mapMutations } from 'vuex'


export default {
    components:{
        Map
    },
     methods: {
       ...mapMutations(['showInputNavInstitutions'])
    },
    mounted(){
       this.showInputNavInstitutions()
    }
}
</script>