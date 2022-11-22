<template>
  <div>
    <el-row class="row-bg" justify="center" style="top: 30px">
      <el-col :span="8">
        <!-- <el-row>
          <el-col :span="8">
            <label>
              <gmap-autocomplete
                @place_changed="initMarker"
              ></gmap-autocomplete>
            </label>
          </el-col>
          <el-col :span="16">
            <el-button @click="addLocationMarker" type="primary">Add</el-button>
          </el-col>
        </el-row> -->
        <el-row>
          <el-input
            placeholder="Location"
            v-model="query.location"
            ref="key"
            style="width: 200px"
          >
          </el-input>
        </el-row>
        <el-row style="top: 10px">
          <el-select
            v-model="query.type"
            placeholder="Food type"
            style="width: 200px"
          >
            <el-option label="Vegan" value="vegan"></el-option>
            <el-option label="Halal" value="halal"></el-option>
            <el-option label="Pizza" value="pizza"></el-option>
            <el-option label="Burger" value="burger"></el-option>
            <el-option label="Salad" value="salad"></el-option>
            <el-option label="Sandwich" value="sandwich"></el-option>
          </el-select>
        </el-row>
        <el-row style="top: 20px">
          <el-button
            type="primary"
            icon="el-icon-search"
            @click="filterData"
            style="width: 200px"
            >Filter</el-button
          >
        </el-row>
        <el-row style="top: 30px">
          <el-button
            type="danger"
            icon="el-icon-back"
            @click="goBack"
            style="width: 200px"
            >Main Menu</el-button
          >
        </el-row>
        <gmap-map
          :zoom="12"
          :center="center"
          style="width: 400px; height: 400px; top: 40px"
        >
          <gmap-marker
            :key="index"
            v-for="(m, index) in locationMarkers"
            :position="m.position"
            @click="center = m.position"
          ></gmap-marker>
        </gmap-map>
      </el-col>

      <el-col :span="16">
        <el-table
          border
          :data="tableData"
          style="width: 100%; border: 0px"
          height="600"
          :cell-style="tableColor"
          :header-cell-style="headerColor"
        >
          <el-table-column fixed prop="time" label="Time"> </el-table-column>
          <el-table-column prop="location" label="Location"> </el-table-column>
          <el-table-column prop="type" label="Food Type"> </el-table-column>
          <el-table-column prop="campus" label="Campus"> </el-table-column>
          <el-table-column prop="org" label="Organization"> </el-table-column>
          <el-table-column prop="req" label="Requirement"> </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>
 
<script>
import axios from "axios";
const path = "http://localhost:5000/";
export default {
  name: "GoogleMap",
  data() {
    return {
      welcome: true,
      center: {
        lat: 39.7837304,
        lng: -100.4458825,
      },
      locationMarkers: [],
      locPlaces: [],
      existingPlace: null,
      tableData: [],
      query: {
        location: "",
        type: "",
      },
    };
  },

  mounted() {
    this.locateGeoLocation();
  },

  created() {
    this.filterData();
  },

  methods: {
    goBack() {
      this.$root.$refs.H.go_back();
    },
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
    headerColor(row) {
      if (row.rowIndex === 0) {
        return "background-color: #409EFF; color: white;";
      }
    },
    tableColor() {
      return "background-color: lightblue; color: white";
    },
    filterData() {
      //alert("trigger with" + this.query.location + ";" + this.query.type);
      axios
        .post(path + "query", {
          location: this.query.location,
          type: this.query.type,
        })
        .then((response) => {
          this.tableData = response.data;
          console.log(response.data);
          for (let i = 0; i < response.data.length; ++i) {
            const marker = {
              lat: response.data[i].lat,
              lng: response.data[i].lng,
            };
            this.locationMarkers.push({ position: marker });
          }
          if (welcome) {
            this.$notify({
              title: "Success",
              message: "Welcome to the world of Free Food.",
              type: "success",
            });
            welcome = false;
          } else {
            this.$notify({
              title: "Success",
              message: "Filter success.",
              type: "success",
            });
          }
        })
        .catch(() => {
          this.$notify.error({
            title: "Error",
            message: "Network error.",
          });
        });
    },
  },
};
</script>