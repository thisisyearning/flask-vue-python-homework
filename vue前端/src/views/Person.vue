<template>
   <el-card style="width: 500px;">
    <el-form label-width="80px" size="small">
      <div class="container">
        <img v-if="form.avatarUrl" :src="form.avatarUrl" class="avatar">
      </div>
      <el-form-item label="图片URL">
      <el-input v-model="form.avatarUrl" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="用户名">
        <el-input v-model="form.username" disabled autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="昵称">
        <el-input v-model="form.nickname" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="地址">
        <el-input type="textarea" v-model="form.address" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="save">确 定</el-button>
      </el-form-item>
     </el-form>
    </el-card>
</template>

<script>
export default {
  name: "Person",
  data() {
    return {
      form: {},
      user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {}
    }
  },
  created() {
    this.getUser().then(res => {
      console.log(res)
      this.form = res
    })
  },
  methods: {
    async getUser() {
      // return (await this.request.get("/user/username/" + this.user.username)).data
      return (await this.request.get("/user/username/" + this.user.username))

    },
    save(){
      this.request.post("/user", this.form).then(res => {
        if (res.code === '200'){
          this.$message.success("保存成功")
          //触发父级更新user
          this.$emit("refreshUser")

          //更新浏览器存储的用户信息
          this.getUser().then(res => {
            res.token = JSON.parse(localStorage.getItem("user")).token
            localStorage.setItem("user", JSON.stringify(res))
          })

        }else{
          this.$message.error("保存失败")
        }
      })
    },
    handleAvatarSuccess(res) {
      this.form.avatarUrl = res
    }
  }
}
</script>

<style>
.avatar-uploader {
  text-align: center;
  padding-bottom: 10px;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 128px;
  height: 128px;
  line-height: 128px;
  text-align: center;
}
.avatar {
  width: 128px;
  height: 128px;
  display: block;
}

.container {
  display: flex;
  justify-content: center; /* 在x轴上居中 */
  align-items: center; /* 在y轴上居中 */
  padding-bottom: 10px;
}

</style>