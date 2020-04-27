<template>
    <div class="row">
        {{ message }}
        <div class="col-xs-12 table table-hover table-responsive">
            <datatable :columns="columns" :data="rows" :filter="filter" :per-page="25"></datatable>
            <datatable-pager v-model="page"></datatable-pager>
        </div>
    </div>
</template>
<script>

import EventBus from '../bus'
import axios from 'axios'
export default {
     data() {
        return {
            filter:  '',
            bus: true,
            rows: [],
            rowsData: [],
            columns: [
                {label: 'Nombre', field: 'nombre'},
                {label: 'Titulo', field: 'titulo'},
                {label: 'Universidad', field: 'localidad.ieu.nombre'},
                {label: 'Localidad',  representedAs: row => 
                                        `${ row.localidad.estado },
                                        ${ row.localidad.municipio }, 
                                        ${ row.localidad.parroquia }`,
                                        align: 'left',sortable: false},
            ],
            page: 1,
            apiRequests: [],
            message: ''
        }
    },    
    methods: {
        events (me,rowsData) {

            EventBus.$on('state_filter', function (states) {
                if (states[0] != undefined) {                            
                    var attr = 'data[i].localidad.estado';
                    me.bus = false;
                    me.rows = me.filters(me.rowsData, states,attr);

                } else if (states[0] == undefined) {
                    me.bus = true;
                    me.rows = me.rowsData;
                }
            });

            EventBus.$on('municipality_filter', function (municipality) {
                if (municipality[0] != undefined) {
                    var attr = 'data[i].localidad.municipio';                           
                    me.bus = false;                            
                    me.rows = me.filters(me.rowsData, municipality, attr);
                }
            });

            EventBus.$on('parish_filter', function (parish) {
                if (parish[0] != undefined) {
                    var attr = 'data[i].localidad.parroquia';                            
                    me.bus = false;                            
                    me.rows = me.filters(me.rowsData, parish, attr);
                }
            });

        },
        filters(data, states,atribute) {

            let array = [];
            let attr = atribute;

            for (var j = 0; j < states.length; j++) 
            {
                for (var i = 0; i < data.length; i++) 
                {
                    if (eval(attr) == states[j]) 
                    {                        
                        array.push(data[i]);
                    }                              
                }
            }

            return array;
        },
        async getInstitutions(url, institutions){            
            try {
                const response = await axios.get(url)

                if (response.data.results.length == 0) {

                    this.messageNull = 'Disculpe, en estos momentos no hay carreras registradas'
                
                }else{

                    var me = this;
                    const retrivedInstitutions = institutions.concat(response.data.results)
                    
                    if (response.data.next !== null && institutions.length !== 1000) {
                        me.getInstitutions(response.data.next, retrivedInstitutions);
                        me.message = 'loading register, please wait...';
                    } else {
                        me.rowsData = retrivedInstitutions
                        me.message = '';
                    }

                    me.rowsData = retrivedInstitutions
                    me.events(me,me.rowsData);
                    if (me.bus) me.rows = me.rowsData;

                }

            } catch (error) {
                console.log('error', error);    
            }
        },
    },
    created() {
        this.getInstitutions('http://loe.terna.net/api-v1/programa-academico/pre-grado/listar/', []);
    },  
}
</script>

<style scoped>
    *{
        font-size: 13px;
    }    
</style>