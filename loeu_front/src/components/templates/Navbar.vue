<template>
    <div>
        <nav class="navbar navbar-expand-lg ">
            <b-container fluid>
                <b-button variant="light" @click="showSidebar_iconNav">
                    <span v-if="iconNavbar == true">
                         <b-icon-chevron-right></b-icon-chevron-right>                                
                    </span>
                    <span v-else>
                       <b-icon-chevron-left></b-icon-chevron-left> 
                    </span>
                </b-button>

                <b-navbar-nav v-if="inputSearch == true" class="mr-auto">
                       <FormSearch class="SearchMap"/>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto"> 
                    <b-nav-item>
                        <b-link class="text-dark" to="/">Carreras</b-link>
                    </b-nav-item>
                    <b-nav-item>
                        <b-link class="text-dark" to="/instituciones">Instituciones</b-link>
                    </b-nav-item>
                    <b-nav-item>
                        <b-link class="text-dark" to="/">Sistema Nacional de Ingreso</b-link>
                    </b-nav-item> 
                </b-navbar-nav>
            </b-container>
        </nav>
    </div>
</template>
<script>
    import FormSearch from '@/components/busqueda/FormSearch.vue'
    import { mapState, mapMutations } from 'vuex'
    export default {
        components:{
            FormSearch,
        },
        methods:{
            ...mapMutations(['showSidebar_iconNav'])
        },
        computed: {
            ...mapState(['inputSearch', 'iconNavbar'])
        }
    }
</script>

<style>
.navbar {
    padding: 15px 15px;
    height: 65px;
    background: none;
    border: none;
    border-bottom: 1px solid rgba(175, 175, 175,.2);
    border-radius: 0;
    margin-bottom: 40px;
}

.navbar-nav a{ 
    color: #fff;
    font-size: 1.19em;
    font-weight: 400;
    line-height: 1.7em;
}

.navbar-nav a:hover{ color: #fff } 
@media (max-width: 425px){
    .navbar{ height: 130px }
}

</style>