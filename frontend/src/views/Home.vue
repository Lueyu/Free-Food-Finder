<template>
  <div>
    <!-- Home screen -->
    <div v-if="show_home">
      <el-row type="flex" class="row-bg" justify="center" style="top: 130px">
        <el-col :span="2"><div class="grid-content bg-purple"></div></el-col>
        <el-col :span="5">
          <el-card style="border: 0px" :body-style="{ padding: '0px' }">
            <img :src="require('../assets/add_info.png')" class="image" />
            <div style="padding: 14px; background: aliceblue">
              <div class="bottom clearfix">
                <el-button
                  @click="change_display_add"
                  type="primary"
                  class="button"
                  >Add Food Info</el-button
                >
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4"><div class="grid-content bg-purple"></div></el-col>
        <el-col :span="5">
          <el-card style="border: 0px" :body-style="{ padding: '0px' }">
            <img :src="require('../assets/find_food.png')" class="image" />
            <div style="padding: 14px; background: aliceblue">
              <div class="bottom clearfix">
                <el-button
                  @click="change_display_find"
                  type="primary"
                  class="button"
                  >Find Free Food</el-button
                >
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="2"><div class="grid-content bg-purple"></div></el-col>
      </el-row>
    </div>

    <!-- Add food -->
    <div v-if="show_add">
      <el-row type="flex" class="row-bg" justify="center" style="top: 30px">
        <el-col :span="14">
          <el-card class="box-card" style="border: 0px; background: aliceblue">
            <el-form
              ref="form"
              :model="form"
              label-width="140px"
              justify="left"
            >
              <el-form-item label="Uniqname:">
                <el-input
                  placeholder="Enter your uniqname"
                  v-model="form.name"
                ></el-input>
              </el-form-item>

              <el-form-item label="Campus:">
                <el-select
                  v-model="form.campus"
                  placeholder="Select your location"
                >
                  <el-option label="North Campus" value="north"></el-option>
                  <el-option label="Central Campus" value="central"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="Location:">
                <gmap-autocomplete
                  class="gmap-auto"
                  @place_changed="initMarker"
                >
                </gmap-autocomplete>
              </el-form-item>

              <el-form-item label="Type of Food:">
                <el-select
                  v-model="form.type"
                  placeholder="Select food type"
                  width="100%"
                >
                  <el-option label="Vegan" value="vegan"></el-option>
                  <el-option label="Halal" value="halal"></el-option>
                  <el-option label="Pizza" value="pizza"></el-option>
                  <el-option label="Burger" value="burger"></el-option>
                  <el-option label="Salad" value="salad"></el-option>
                  <el-option label="Sandwich" value="sandwich"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="Time:">
                <el-col :span="11">
                  <el-date-picker
                    type="date"
                    placeholder="Pick a date"
                    v-model="form.date1"
                    style="width: 80%"
                  ></el-date-picker>
                </el-col>
                <el-col class="line" :span="2">-</el-col>
                <el-col :span="11">
                  <el-time-picker
                    placeholder="Pick a time"
                    v-model="form.date2"
                    style="width: 80%"
                  ></el-time-picker>
                </el-col>
              </el-form-item>
              <el-form-item label="Requirements:">
                <el-input type="textarea" v-model="form.desc"></el-input>
              </el-form-item>

              <el-form-item label="Event/Organization:">
                <el-input v-model="form.event"></el-input>
              </el-form-item>
              <el-form-item style="margin-left: 0px">
                <el-button type="primary" @click="create_event"
                  >Create</el-button
                >
                <el-button @click="go_back">Cancel</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          <div class="grid-content bg-purple"></div
        ></el-col>
      </el-row>
    </div>

    <!-- Show info -->
    <div v-if="show_find">
      <GoogleMap />
    </div>
  </div>
</template>

<script>
import GoogleMap from "./GoogleMap.vue";
/* eslint-disable */
export default {
  name: "Home",
  components: {
    GoogleMap,
  },
  created() {
    this.$root.$refs.H = this;
  },
  data() {
    return {
      show_home: true,
      show_add: false,
      show_find: false,
      form: {
        name: "",
        location: "",
        campus: "",
        date1: "",
        date2: "",
        desc: "",
        event: "",
        type: "",
      },
    };
  },
  methods: {
    initMarker(loc) {
      this.form.location = loc;
    },
    change_display_add() {
      this.show_home = false;
      this.show_add = true;
    },
    change_display_find() {
      this.show_home = false;
      this.show_find = true;
    },
    create_event() {
      this.form = {
        name: "",
        location: "",
        campus: "",
        date1: "",
        date2: "",
        desc: "",
        event: "",
        type: "",
      };
      alert("Event created!!!");
    },
    go_back() {
      this.show_home = true;
      this.show_add = false;
      this.show_find = false;
    },
  },
};
</script>

<style>
html {
  background-image: url("../assets/home_background.png");
  background-size: 100%;
}

.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin: 5px;
  line-height: 12px;
}

.button {
  padding: 0;
}

.image {
  width: 100%;
  height: 236px;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
.gmap-auto {
  border-color: #c0c4cc;
  -webkit-appearance: none;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #DCDFE6;
  border-color: #dcdfe6;
  border-style: solid;
  border-width: 1px;
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  height: 40px;
  line-height: 40px;
  outline: 0;
  padding: 0 15px;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 15px;
  transition: border-color 0.2s cubic-bezier (0.645, 0.045, 0.355, 1);
  width: 100%;
}
</style>
