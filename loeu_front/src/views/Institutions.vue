<template>
    <div>      
        <institutionsMap/>
    </div>
</template>
<script>

import { mapMutations } from 'vuex'
import institutionsMap from '@/components/InstitutionsMap.vue'


export default {
    components:{
        institutionsMap
    },
     methods: {
       ...mapMutations(['showInputNavInstitutions'])
    },
    mounted(){
       this.showInputNavInstitutions()
    }
}
</script>