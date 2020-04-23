<template>
    <div class="row">
        <div class="col-xs-12 form-inline">
            <form class="form-group">
                <input type="text" class="form-control" v-model="filter" placeholder="Buscar carreras" @keydown="$event.stopImmediatePropagation()">
            </form>
        </div>

        <div class="col-xs-12 table table-hover table-responsive">
            <datatable :columns="columns" :data="rows" :filter="filter" :per-page="15"></datatable>
            <datatable-pager v-model="page" type="long"></datatable-pager>

        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
     data() {
        return {
            filter:  '',
            rows: [],
            columns: [
                {label: 'Nombre', field: 'nombre'},
                {label: 'Titulo', field: 'titulo', headerClass: 'class-in-header second-class'},
                {label: 'Universidad', field: 'localidad.ieu.institucion_ministerial.nombre'},
                {label: 'Localidad', field: 'localidad.municipio'},
            ],
            page: 1,
        }
    },
    
    methods: {
        async getInstitutions(){            
            try {
                let dates = await axios.get('http://loe.terna.net/api-v1/programa-academico/pre-grado/listar/')

                if (dates.data.results.length == 0) {
                    this.messageNull = 'Disculpe, en estos momentos no hay carreras registradas'
                }else{
                    this.rows = await dates.data.results;
                }
            } catch (error) {
                console.log('error', error);    
            }
        }
    },
    mounted(){        
        this.getInstitutions();
    }
    
}
</script>
<style scoped>
    *{
        font-size: 13px;
    }
    
</style>