<template>
    <div>
        <b-row class="mb-5">
            <b-col>
                <b-card class="mb-2"
                    border-variant="primary"
                    header="Buscador de instituciones"
                    header-bg-variant="primary"
                    header-text-variant="white"
                    align="center">
               
                    <b-card-text>
                        <p>Ubica la Institución de Educación Universitaria de tu interés</p>
                    </b-card-text>

                     <b-card-img :src="require('../assets/mapaHome.png')" fluid style="width: 200px"></b-card-img>
                    
                    <b-row>
                        <b-col> <b-button href="#" variant="primary">Por regiones</b-button> </b-col>
                        <b-col> <b-button href="#" variant="primary">Por estados</b-button> </b-col>
                    </b-row>
                </b-card>
            </b-col>

             <b-col>
                <b-card class="mb-2"
                    border-variant="danger"
                    header="Carreras y PNF por área de Conocimiento"
                    header-bg-variant="danger"
                    header-text-variant="white"
                    align="center">
               
                    <b-card-text>
                        <p>Aquí podrás obtener mas información sobre las Carreras y Programas Nacionales de Formación clasificadas por Áreas de Conocimiento:</p>
                    </b-card-text>
                </b-card>
            </b-col>
            <b-col>
                <b-card class="mb-2"
                    border-variant="primary"
                    header="Preguntas frecuentes"
                    header-bg-variant="primary"
                    header-text-variant="white"
                    align="center">
               
                    <b-card-text>
                        <p>Aquí encontrarás todo lo que quieras saber sobre el SNI</p>
                    </b-card-text>                    
                    
                    <b-button v-b-toggle.quest1 variant="white">¿Qué es el Sistema Nacional de Ingreso?</b-button>
                    <b-collapse id="quest1">
                        <b-card>
                            <b-card-text>El Gobierno Bolivariano y Revolucionario fundamentado en la Constitución de la República impulsa el Sistema Nacional de Ingreso a la Educación Universitaria como un conjunto de acciones, procesos y servicios totalmente gratuitos para lograr la inclusión efectiva de venezolanas y venezolanos a la Educación Universitaria, haciendo especial énfasis en la igualdad de condiciones y equiparación de oportunidades sin discriminaciones sociales, étnicas o físicas.</b-card-text>
                        </b-card>
                    </b-collapse>

                    <b-button v-b-toggle.quest2 variant="white">¿Quiénes pueden participar?</b-button>
                    <b-collapse id="quest2">
                        <b-card>
                            <b-card-text>Pueden participar tanto los estudiantes del último año de Educación Media General y Media Técnica (antes Media Diversificada y Profesional), como los bachilleres.</b-card-text>
                        </b-card>
                    </b-collapse>
                    <b-button v-b-toggle.quest3 variant="white">¿Qué debes hacer para participar?</b-button>
                    <b-collapse id="quest3">
                        <b-card>
                            <b-card-text>REGÍSTRATE: Si no estás registrado, debes crear tu cuenta de usuario para ingresar al sistema y completar tu registro.INGRESA AL SISTEMA: Si ya estás registrado, deberás ingresar al sistema con tu correo electrónico y contraseña para realizar el trámite respectivo. En caso de que no recuerdes tu correo electrónico o tu contraseña, selecciona la opción RECUPERAR CONTRASEÑA en el menú principal.</b-card-text>
                        </b-card>
                    </b-collapse>
                    <b-button v-b-toggle.quest4 variant="white">¿Cómo hago para inscribirme en el Sistema Nacional de Ingreso?</b-button>
                    <b-collapse id="quest4">
                        <b-card>

                        </b-card>
                    </b-collapse>

                </b-card>
            </b-col>
        </b-row>
    </div>
</template>
<script>
export default {
    data(){
        return{
            //imgMapHome: './assets/mapaHome.png'
        }
    }
}
</script>