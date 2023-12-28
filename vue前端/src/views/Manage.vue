<template>
  <div style="height: 100%">
 <el-container style="height: 100%">

   <el-aside :width="sideWidth + 'px'" style="background-color: rgb(255,255,255); height: 100vh">
     <Aside :isCollapse="isCollapse" :logoTextShow="logoTextShow" />
   </el-aside>

   <el-container>
     <el-header  style=" border-bottom: 1px solid #ccc;">
       <Header @asideCollapse="collapse" :collapseBtnClass="collapseBtnClass" :collapse="isCollapse" :user="user"/>
     </el-header>

     <el-main>
<!--当前页面子路由在 router-view 展示-->
       <router-view @refreshUser="getUser" />
     </el-main>
   </el-container>
 </el-container>

  </div>
</template>

<script>

import Aside from "@/components/Aside";
import Header from "@/components/Header";
import User from "@/views/User";


export default {
  name: 'HomeView',
  data(){
    return {

      collapseBtnClass: 'el-icon-s-fold',
      isCollapse: false,
      sideWidth: 200,
      logoTextShow: true,
      headerBg: 'headerBg',
      user: {}

    }
  },

  components: {
    User,
    Aside,
    Header
  },
  created() {
    this.getUser()
  },
  methods: {
    collapse(){
      this.isCollapse = !this.isCollapse
      if(this.isCollapse){
        this.sideWidth = 64
        this.collapseBtnClass = 'el-icon-s-unfold'
        this.logoTextShow = false
      } else {
        this.sideWidth = 200
        this.collapseBtnClass = 'el-icon-s-fold'
        this.logoTextShow = true
      }
    },
    getUser() {
      let username = localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")).username : ""
      //从后台获取数据
      this.request.get("/user/username/" + username).then(res => {
        this.user = res
        // console.log("Manage user!!!")
        // console.log(res)
      })
    }
  }
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse){
  width: 200px;
  height: 100%;
}
.el-menu-vertical-demo{
  transition: width 1s;
}

</style>
