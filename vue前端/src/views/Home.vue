<template>
  <div id="bd">
    <el-container>
      <div class="centered-text">商品管理系统</div>
    </el-container>
  </div>
</template>

<style>
.centered-text {
  text-align: center; /* 让文字居中 */
  color: black; /* 设置文字颜色为白色 */
  font-size: 28px; /* 设置文字的大小 */
  font-weight: bold; /* 设置文字为粗体 */
  letter-spacing: 15px; /* 增加文字间的间距 */
  position: absolute; /* 设置为绝对定位，相对于父元素居中 */
  top: 15%; /* 距离顶部50% */
  left: 50%; /* 距离左侧50% */
  transform: translate(-50%, -50%); /* 使用transform来使文字居中 */
}

.image {
  width: 100%;
  display: block;
}

#bd {
  background: url("../assets/sean-pollock-PhYq704ffdA-unsplash.jpg");
  width: 100%;
  height: 100%;
  position: relative;
  background-size: 100% 100%;
}
</style>
