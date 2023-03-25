<template>
  <div class="header">
    <div class="topic">
      <h1>
        <img src="./assets/logo.png" class="img_title">
        <span>教学科研一体化量化交易仿真系统</span>
      </h1>
    </div>
    <div class = "features">
      <nav class="nav_link">
        <router-link class="link_btn one" active-class="active" to="/backtest">回测框架</router-link>
        <router-link class="link_btn two" active-class="active" to="/strategy">策略研究</router-link>
        <router-link class="link_btn three" active-class="active" to="/data">数据API</router-link>
        <router-link class="link_btn four" active-class="active" to="/factor">因 子</router-link>
        <router-link class="link_btn five" active-class="active" to="/mannual">使用说明</router-link>
      </nav>
    </div>
  </div>
  <router-view></router-view>
  <!--div>
    <svg id = "bottomLayer" style = 'width:1400px; height:720px; background-color:lightgrey'></svg>

  </div -->
</template>

<script>
//import Classics from "./components/Classics.vue"
//import Asset from "./components/Asset.vue"

export default {
    name:'App',
    components:{
     // Classics,
     // Asset
    },
 
 
    data(){
      return{
      details_display: 0,
      epoch_index:-1,
      value:0
      }
    },
    mounted(){
  },
    methods:{
      // check(){
      //   this.value ++;
      //   console.log(this.value);
      // },
      Details(data){
        this.details_display = data;
      },
      DayDetail(data){
        this.epoch_index = data;
      }
    }
  }
</script>
<style lang="scss">
.header{
  display:flex;
  align-items:center;
  justify-content: space-between;
  height:40px;
  background-color: #ffffff;
  color:#ffffff;
  border: 1px solid #2c2c2c;
}

.topic{
  display: flex;
  align-items: center;
}

h1{
  display: flex;
  align-items: center;
  font:normal 18px Cookie;
  padding:0px 20px;
  color: #2c2c2c;
  font-family: "Microsoft SimHei";
}

.img_title{
  width:30px;
  height:30px;
}

.nav_link{
  display: flex;
  align-items: center;
  padding:0 10px;
}

.one{
  position:absolute;
  left:400px;
}
.two{
  position:absolute;
  left:520px;
}
.three{
  position:absolute;
  left:640px;
}
.four{
  position:absolute;
  left:770px;
}
.five{
  position:absolute;
  left:880px;
}
.link_btn{
  text-decoration: none;
  color: #7f7f7f;
  font-size:15px;
  font-weight:normal;
  font-family: "Microsoft KaiTi";
}

#bottomLayer{
  position:absolute;
  top:50px;
  z-index: -1;
}

#app {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  
#Classics {
  position: absolute;
  top:50px;
  left:10px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
  z-index:0;
}

#Heatmap {
  position: absolute;
  top:385px;
  left:3px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
  z-index:0;
}

#Asset{
  position: absolute;
  top:385px;
  left:815px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
  z-index:0;
}
</style>
