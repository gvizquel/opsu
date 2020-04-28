<template>
  <div class="home">
    <careersMap/>
  </div>
</template>

<script>
import careersMap from '@/components/CareersMap.vue'
import {mapMutations} from 'vuex'
  export default {
    name: 'Home',
    components: {
      careersMap
    },
    methods: {
      ...mapMutations(['showInputNavCarreras']),
      ...mapMutations(['hideInputNavInstitutions']),
    }
  }
</script>
