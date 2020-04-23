<template>
  <div class="home">
   <CardsHome/>  
  </div>
</template>

<script>
import CardsHome from '@/components/CardsHome.vue'
import { mapMutations } from 'vuex'

  export default {
    name: 'Home',
    components: {
      CardsHome
    },
    methods: {
      ...mapMutations(['hideInputNavCarreras', 'hideInputNavCarrerasInstitutions'])
    },
    mounted(){
      this.hideInputNavCarreras()
      this.hideInputNavInstitutions()
    }
  }
</script>
