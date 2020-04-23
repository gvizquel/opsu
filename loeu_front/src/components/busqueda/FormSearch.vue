<template>
    <div>
        <form action="" v-if="searchInstitutions == true">
            <input type="search" id="" placeholder="Buscar Institución">
        </form>
        <form v-else>
            <input type="search" id="" placeholder="Buscar Carrera">
        </form>
    </div>
</template>
<script>
import {mapState} from 'vuex'
export default {
    computed: {
        ...mapState(['searchInstitutions'])
    }
}
</script>

<style scoped>
    input[type=search]{
        outline: none;
        margin-left: 50px;
        -webkit-box-sizing: content-box;
        font-family: inherit;
        font-size: 100%;
    }

    input::-webkit-search-decoration,
    input::-webkit-search-cancel-button{
        display: none;
    }

    input[type=search]{
        background: #fff
            url(https://static.tumblr.com/ftv85bp/MIXmud4tx/search-icon.png) no-repeat 9px center;
        border: solid 1px #fff;
        padding: 4.5px 5px 4.5px 32px;
        width: 220px;

        -webkit-border-radius: 10em;
        -moz-border-radius: 10em;
        border-radius: 10em;

        -webkit-box-shadow:  3px 3px 3px rgba(0, 0, 0, 0.2);
        -moz-box-shadow:  3px 3px 3px rgba(0, 0, 0, 0.2);
        box-shadow:  3px 3px 3px rgba(0, 0, 0, 0.2);

        -webkit-transition: all .5s;
        -moz-transition: all .5s;
        transition: all .5s;
    }

    input[type=search]:focus{
        width: 390px;
        background: #fff url(https://static.tumblr.com/ftv85bp/MIXmud4tx/search-icon.png) no-repeat 390px center;
    }

    input:-moz-placeholder{ color: #999 }
    input:-webkit-input-placeholder{ color: #999 }

     @media(max-width: 1024px){
        input[type=search]{
            width: 120px;
            margin-left: 10px;
        }
        input[type=search]:focus{
            width: 250px;
            background: #fff url(https://static.tumblr.com/ftv85bp/MIXmud4tx/search-icon.png) no-repeat 250px center;
        }
    }

    @media(max-width: 375px){
        input[type=search]{
            width: 100px;
        }
        input[type=search]:focus{
            width: 200px;
            background: #fff url(https://static.tumblr.com/ftv85bp/MIXmud4tx/search-icon.png) no-repeat 200px center;
        }
    }

    @media(max-width: 320px){
        input[type=search]{ width: 150px }
        input[type=search]:focus{
            width: 150px;
            background: #fff url(https://static.tumblr.com/ftv85bp/MIXmud4tx/search-icon.png) no-repeat 150px center;
        }
    }
</style>
    
