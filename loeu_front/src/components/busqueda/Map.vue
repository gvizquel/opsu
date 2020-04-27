<template>
  <l-map style="height: 490px" :zoom="zoom" :center="center">
    <l-tile-layer :url="url"></l-tile-layer>
    <l-control-attribution position="topright" prefix="Libro de oportunidades de estudio"></l-control-attribution>  
    <l-circle-marker
      :lat-lng="circle.center"
      :radius="circle.radius"
      :color="circle.color">
        <l-popup>Universidad central de venezuela</l-popup>
      </l-circle-marker>
    </l-map>
</template>

<script>
import {LMap, LTileLayer, LCircleMarker, LControlAttribution, LPopup} from 'vue2-leaflet';

export default {
  components: {
    LMap,
    LTileLayer,
    LCircleMarker,
    LControlAttribution,
    LPopup
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 5.5,
      center: [8.655767, -66.354306],
      circle: {
        center: [10.4883555,-66.8913583],
        radius: 6,
        color: '#C22974'
      },
    };
  }
}

</script>
