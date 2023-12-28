<template>
<div>

  <el-row :gutter="10" style="margin-bottom: 60px">
    <el-col :span="6">
      <el-card style="color: #409EFF">
        <div><i class="el-icon-user-solid" /> 用户总数</div>
        <div style="padding: 10px 0; text-align: center; font-weight: bold">
          100
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card style="color: #F56C6C">
        <div><i class="el-icon-money" /> 销售总量</div>
        <div style="padding: 10px 0; text-align: center; font-weight: bold">
          ￥ 100000
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card style="color: #67C23A">
        <div><i class="el-icon-bank-card" /> 收益总额</div>
        <div style="padding: 10px 0; text-align: center; font-weight: bold">
          ￥ 100
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card style="color: #E6A23C">
        <div><i class="el-icon-s-shop" /> 门店总数</div>
        <div style="padding: 10px 0; text-align: center; font-weight: bold">
          100
        </div>
      </el-card>
    </el-col>
  </el-row>

  <el-row>
    <el-col :span="12">
      <div id="main" style="width: 500px; height: 450px"></div>
    </el-col>

    <el-col :span="12">
      <div id="pie" style="width: 500px; height: 450px"></div>
    </el-col>
  </el-row>
</div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: "Home",
  data() {
    return {

    }
  },
  mounted() { //页面元素渲染之后再触发
    var option = {
      title: {
        text: '会员数量统计',
        subtext: '趋势图',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      xAxis: {
        type: 'category',
        data: ["第一季度", "第二季度","第三季度","第四季度"]
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: 1,
          data: [],
          type: 'line'
        },
        {
          name: 1,
          data: [],
          type: 'bar'
        },
        {
          name: 2,
          data: [],
          type: 'line'
        },
        {
          name: 2,
          data: [],
          type: 'bar'
        }
      ]
    };


//饼图

    var pieOption = {
      title: {
        text: '会员数量统计',
        subtext: '比例图',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br>{b} : {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: 111,
          type: 'pie',
          radius: '50%',
          center: ['25%', '50%'],
          label: {
            normal: {
              show: true,
              position: 'inside',
              formatter: '{d}%',//模板变量有 {a}、{b}、{c}、{d}，分别表示系列名，数据名，数据值，百分比。{d}数据会根据value值计算百分比
              textStyle: {
                fontSize: 14,
                fontWeight: 300,
                color: "#fff"
              },
            },
          },
          data: [
            { value: 1048, name: 'Search Engine' },
            { value: 735, name: 'Direct' },
            { value: 580, name: 'Email' },
            { value: 484, name: 'Union Ads' },
            { value: 300, name: 'Video Ads' }
          ]
        },
        {
          name: 'www',
          type: 'pie',
          radius: '50%',
          center: ['75%', '50%'],
          label: {
            normal: {
              show: true,
              position: 'inside',
              formatter: '{d}%',//模板变量有 {a}、{b}、{c}、{d}，分别表示系列名，数据名，数据值，百分比。{d}数据会根据value值计算百分比
              textStyle: {
                fontSize: 14,
                fontWeight: 300,
                color: "#fff"
              },
            },
          },
          data: [
            { value: 1048, name: 'Search Engine' },
            { value: 735, name: 'Direct' },
            { value: 580, name: 'Email' },
            { value: 484, name: 'Union Ads' },
            { value: 300, name: 'Video Ads' }
          ]
        }
      ]
    };

    var chartDom = document.getElementById('main');
    var myChart = echarts.init(chartDom);

    var piechartDom = document.getElementById('pie');
    var piemyChart = echarts.init(piechartDom);


    this.request.get("/echarts/members").then(res => {
      //option.xAxis.data = res.data.x
      option.series[0].data = [10, 20, 66, 7]
      option.series[1].data = [5, 4, 8, 6]
      option.series[2].data = [1, 2, 5, 4]
      option.series[3].data = [1, 2, 5, 4]


      myChart.setOption(option);

      pieOption.series[0].data = [
        {name: "第一季度", value: 0},
        {name: "第二季度", value: 1},
        {name: "第三季度", value: 9},
        {name: "第四季度", value: 4},

      ]
      pieOption.series[1].data = [
        {name: "第一季度", value: 1},
        {name: "第二季度", value: 2},
        {name: "第三季度", value: 5},
        {name: "第四季度", value: 4},
      ]
      piemyChart.setOption(pieOption);

    })


    //piemyChart.setOption(pieOption);

  }
}
</script>

<style scoped>

</style>