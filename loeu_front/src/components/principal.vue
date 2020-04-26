<template>
    <div class="wrapper">
        <Sidebar/>

        <div id="content">
            <Navbar/>
            <transition name="slide-fade" mode="out-in">
                <router-view/>
            </transition>
        </div>    
    </div>
</template>
<script>
    import {mapMutations} from 'vuex'
    import Sidebar from '@/components/templates/Sidebar.vue'
    import Navbar from '@/components/templates/Navbar.vue'

export default {
    components:{
        Sidebar,
        Navbar, 
    },
    methods:{
        ...mapMutations(['showSidebar_iconNav'])
    },
    mounted(){
        this.showSidebar_iconNav()
    }
    
}
</script>

<style>
.wrapper {
    display: flex;
    width: 100%;
    align-items: stretch;
    position: absolute;
}

#content {
    width: 100%;
    padding: 20px;
    min-height: 100vh;
    transition: all 0.3s;
  }
</style>
