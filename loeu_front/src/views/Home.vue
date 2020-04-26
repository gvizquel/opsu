<template>
  <div class="home">
    <careersMap/>
    <button @click="getCarreras">obtener</button>

    <ul v-for="(carrera, index) in carreras" :key="index">
      {{carrera.results}}
    </ul>
  </div>
</template>

<script>
import careersMap from '@/components/CareersMap.vue'
import { mapMutations, mapActions, mapState } from 'vuex'

  export default {
    name: 'Home',
    components: {
      careersMap
    },
    computed:{
      ...mapState(['carreras'])
    },
    methods: {
      ...mapMutations(['hideInputNavInstitutions']),
      ...mapActions(['getCarreras'])
    },
    mounted(){
      this.hideInputNavInstitutions()

    }
  }
</script>
