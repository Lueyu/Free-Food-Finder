<template>
  <div>
    <el-row type="flex" class="row-bg" justify="center" style="top: 130px">
      <el-col :span="4">
        <div>
          <label>
            <gmap-autocomplete @place_changed="initMarker"></gmap-autocomplete>
            <button @click="addLocationMarker">Add</button>
          </label>
          <gmap-map
            :zoom="14"
            :center="center"
            style="width: 400px; height: 400px"
          >
            <gmap-marker
              :key="index"
              v-for="(m, index) in locationMarkers"
              :position="m.position"
              @click="center = m.position"
            ></gmap-marker>
          </gmap-map>
        </div>
      </el-col>

      <el-col :span="12"><div class="grid-content bg-purple"></div></el-col>
    </el-row>
  </div>
</template>
 
<script>
export default {
  name: "GoogleMap",
  data() {
    return {
      center: {
        lat: 39.7837304,
        lng: -100.4458825,
      },
      locationMarkers: [],
      locPlaces: [],
      existingPlace: null,
    };
  },

  mounted() {
    this.locateGeoLocation();
  },

  methods: {
    initMarker(loc) {
      this.existingPlace = loc;
    },
    addLocationMarker() {
      if (this.existingPlace) {
        const marker = {
          lat: this.existingPlace.geometry.location.lat(),
          lng: this.existingPlace.geometry.location.lng(),
        };
        this.locationMarkers.push({ position: marker });
        this.locPlaces.push(this.existingPlace);
        this.center = marker;
        this.existingPlace = null;
      }
    },
    locateGeoLocation: function () {
      navigator.geolocation.getCurrentPosition((res) => {
        this.center = {
          lat: res.coords.latitude,
          lng: res.coords.longitude,
        };
      });
    },
  },
};
</script>