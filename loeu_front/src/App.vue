<template>
  <div id="app">    
    <Principal/>
  </div>
</template>

<script>
  import Principal from '@/components/principal.vue'

  export default {
    components: {
      Principal
    }
}
</script>

<style>

@import url('https://fonts.googleapis.com/css?family=Varela+Round&display=swap');
*{ font-family: 'Varela Round', sans-serif }

p {
  font-family: 'Poppins', sans-serif;
  font-size: 1em;
  font-weight: 300;
  line-height: 1.7em;
  color: #474747;
}

a, a:hover, a:focus {
  color: inherit;
  text-decoration: none;
  transition: all 0.3s;
}

</style>
