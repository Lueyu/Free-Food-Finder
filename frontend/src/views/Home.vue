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
              :rules="rules"
            >
              <el-form-item label="Uniqname:" prop="name">
                <el-input
                  placeholder="Enter your uniqname"
                  v-model="form.name"
                ></el-input>
              </el-form-item>

              <el-form-item label="Campus:" prop="campus">
                <el-select
                  v-model="form.campus"
                  placeholder="Select your location"
                  clearable
                >
                  <el-option label="North Campus" value="North"></el-option>
                  <el-option label="Central Campus" value="Central"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="Location:" prop="location">
                <gmap-autocomplete
                  class="gmap-auto"
                  @place_changed="initMarker"
                >
                </gmap-autocomplete>
              </el-form-item>

              <el-form-item label="Type of Food:" prop="type">
                <el-select
                  v-model="form.type"
                  placeholder="Select food type"
                  width="100%"
                  clearable
                >
                  <el-option label="Vegan" value="Vegan"></el-option>
                  <el-option label="Pizza" value="Pizza"></el-option>
                  <el-option label="Burger" value="Burger"></el-option>
                  <el-option label="Salad" value="Salad"></el-option>
                  <el-option label="Sandwich" value="Sandwich"></el-option>
                  <el-option label="Halal" value="Halal"></el-option>
                  <el-option label="Kosher" value="Kosher"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="Time:" required>
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
                <el-input type="textarea" v-model="form.req"></el-input>
              </el-form-item>

              <el-form-item label="Event/Organization:">
                <el-input v-model="form.event"></el-input>
              </el-form-item>
              <el-form-item style="margin-left: 0px">
                <el-button type="primary" @click="create_event('form')"
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
import axios from "axios";
const path = "http://localhost:5000/";
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
        req: "",
        event: "",
        type: "",
      },
      rules: {
        name: [
          { required: true, message: "Uniqname is required", trigger: "blur" },
        ],
        campus: [
          { required: true, message: "Campus is required", trigger: "blur" },
        ],
        location: [
          { required: true, message: "Location is required", trigger: "blur" },
        ],
        time: [
          {
            type: "date",
            required: true,
            message: "Date is required",
            trigger: "change",
          },
        ],
        type: [
          {
            required: true,
            message: "Food type is required",
            trigger: "blur",
          },
        ],
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
    create_event(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post(path, this.form);
          this.form = {
            name: "",
            location: "",
            campus: "",
            date1: "",
            date2: "",
            req: "",
            event: "",
            type: "",
          };
          this.$notify({
            title: "Success",
            message: "You have created a free food event!!!",
            type: "success",
          });
        } else {
          this.$notify.error({
            title: "Error",
            message:
              "Please make sure you have entered all required information.",
          });
        }
      });
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
  border: 1px solid??#DCDFE6;
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
  padding: 0??15px;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 15px;
  transition: border-color 0.2s??cubic-bezier (0.645, 0.045, 0.355, 1);
  width: 100%;
}
</style>
