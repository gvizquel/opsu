<template>
    <div class="row">
        <div class="col-12 text-center">
            <b-badge variant="warning" v-if="message"><h1>{{ message }}</h1></b-badge>
        </div>
        <vue-good-table
            title="Universidades"
            id="table"
            :columns="columns"
            :rows="rows"
            @on-cell-click="onCellClick"
            styleClass="table condensed table-bordered table-hover"
            :search-options="{
                enabled: true,
                trigger: 'enter',
                skipDiacritics: true,
                placeholder: 'Buscar carreras',
                externalQuery: filter,
                searchFn: myFunc
            }"
            :pagination-options="{
                enabled: true,
                mode: 'records',
                perPageDropdown: [5, 10, 25],
                perPage: 25,
                dropdownAllowAll: false,
                nextLabel: 'Siguiente',
                prevLabel: 'Anterior',
                rowsPerPageLabel: 'Filas por página',
                ofLabel: 'de',
            }">
        </vue-good-table>

        <ModalUniversity
            v-if="university != ''"
            :university="university">
        </ModalUniversity>

    </div>
</template>
<script>

import ModalUniversity from '@/components/ModalUniversity.vue'
import EventBus from '../bus'
import axios from 'axios'
export default {
     data() {
        return {
            filter: '',
            bus: true,
            message: '',
            university: [],
            rows: [],
            rowsData: [],
            columns: [
                {label: 'Nombre', field: 'nombre', filterable: true},
                {label: 'Título', field: 'titulo', filterable: true, html: false},
                {label: 'Universidad', field: 'localidad.ieu.nombre', filterable: true, html: true},
                {label: 'Localidad', field: 'localidad.estado', filterable: true, html: false}
            ],
        }
    },
    components: {
        ModalUniversity
    },    
    methods: {
        myFunc(row, col, cellValue, searchTerm){
            return cellValue === 'my value';
        },
         onCellClick(params) {
            this.university = params.row;
            this.$bvModal.show('university')
        },
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
        filters(data, obj,atribute) {

            let array = [];
            let attr = atribute;

            for (var j = 0; j < obj.length; j++) 
            {
                for (var i = 0; i < data.length; i++) 
                {
                    if (eval(attr) == obj[j]) 
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
                    
                    if (response.data.next !== null) {
                        me.getInstitutions(response.data.next, retrivedInstitutions);
                        me.message = 'Cargando instituciones...';
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
    mounted(){        
    }    
}
</script>

<style scoped>
    *{
        font-size: 13px;
    }
    .h1 {
        font-size: 20px !important;
        background: beige;
        font-weight: bold;
        padding: 10px;
    }
    #table {
        cursor: pointer
    }
</style>