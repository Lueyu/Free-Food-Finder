<template>
  <div class="home">
    <el-row type="flex" class="row-bg" justify="center" style="top: 50px">
      <el-col :span="2"><div class="grid-content bg-purple"></div></el-col>
      <el-col :span="5">
        <div class="grid-content bg-purple-light">
          <el-button type="primary"
            ><router-link style="text-decoration: none; color: black" to="/add"
              >Add Food Info</router-link
            ></el-button
          >
          <el-row style="height: 30px" />
          <el-image
            style="width: 150px; height: 150px"
            :src="require('../assets/add_info.png')"
            fit="fill"
          ></el-image></div
      ></el-col>
      <el-col :span="4"><div class="grid-content bg-purple"></div></el-col>
      <el-col :span="5"
        ><div class="grid-content bg-purple">
          <el-button type="success"
            ><router-link style="text-decoration: none; color: black" to="/find"
              >Find Free Food</router-link
            ></el-button
          >
          <el-row style="height: 30px" />
          <el-image
            style="width: 150px; height: 150px"
            :src="require('../assets/find_food.png')"
            fit="fill"
          ></el-image></div
      ></el-col>
      <el-col :span="2"><div class="grid-content bg-purple"></div></el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Home",
};
</script>
