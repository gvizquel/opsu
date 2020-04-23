<template>
  <div class="about">
    <b-container>
      <b-row>
        <b-col cols="1"></b-col>
        <b-col cols="10">
          <h3> 
            <b-icon-info ></b-icon-info>Aquí podrás obtener información referente a:
          </h3>
          <ul>
            <li>Ubicación de las Instituciones de Educación Universitaria por Región y Estados.</li>
            <li>Carreras o Programas Nacionales de Formación (PNF), que se ofrecen por áreas del conocimiento.</li>
            <li>Requisitos de ingreso, contactos y servicios disponibles en las Instituciones de Educación Universitaria del país.</li>
            <li>Índice de referencia.</li>
            <li>Áreas prioritarias para el desarrollo de la nación.</li>
          </ul>
          <hr>
          <h4 class="sub-title">Recomendaciones para la selección de Carreras, Programas Nacionales de Formación e Instituciones de Educación Universitaria.</h4>
            <p>Para la mayoría de los aspirantes que desean ingresar al subsistema de Educación Universitaria, la elección de una profesión es compleja y plantea interrogantes e inquietudes que requieren una respuesta oportuna:</p>
            <ol>
              <li>¿Cómo elegir acertadamente la Carrera o Programa Nacional de Formación que voy a estudiar?</li>
              <li>¿Qué factores debo tomar en cuenta a la hora de seleccionar una institución, Carrera o Programa Nacional de Formación?</li>
              <li>¿Me decido por una Universidad, Instituto o Colegio Universitario?</li>
              <li>¿Dónde puedo consultar para saber si una Carrera, Programa Nacional de Formación o Institución de Educación Universitaria está aprobada y reconocida legalmente por el Consejo Nacional de Universidades?</li>
              <li>¿Qué Carreras o Programas Nacionales de Formación se ofrecen en la región?</li>
            </ol>
            <p>A la hora de seleccionar una carrera o Programa Nacional de Formación, las y los estudiantes deben considerar ciertos aspectos que tienen relación con los intereses, aptitudes, habilidades y preferencias laborales. Por lo tanto, la elección no debe hacerse por tradición o azar, debe ser el resultado de un proceso de reflexión que implique un análisis del concepto que cada uno tiene de si mismo, sobre las oportunidades específicas que existen en las regiones y el país, la motivación, el conocimiento del mundo ocupacional, entre otras. Al seleccionar una carrera o Programa Nacional de Formación estás eligiendo lo que en el futuro será la ocupación habitual con la que te insertarás al mercado laboral y te vincularás con el desarrollo del país. </p>

            <p>A fin de ofrecerte una orientación adecuada y ayudarte a responder algunas de tus interrogantes e inquietudes, te ofrecemos está página web, considerada una publicación oficial del Consejo Nacional de Universidades, donde aparecen las Instituciones, Carreras y Programas Nacionales de Formación aprobadas y reconocidas legalmente hasta la actualidad.</p>
        </b-col>
        <b-col cols="1"></b-col>
      </b-row>
    </b-container>
    
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
  methods: {
      ...mapMutations(['hideInputNavCarreras'])
    },
    mounted(){
      this.hideInputNavCarreras()
    }
}
</script>

<style scoped>

.sub-title{ color: #2da7db; }
ul, ol li, p{ font-size: 17px; }

ol li {
  list-style-type: none;
  counter-increment: list; 
  position: relative;
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
ol li::before {
  content: counter(list) ")"; /* Indica el separador para tu contenido */
  left: -32px;
  position: absolute;
  text-align: right;
  width: 26px;
}

</style>