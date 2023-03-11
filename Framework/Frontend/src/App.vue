<template>
  <div>
    <svg id = "botteomLayer" style = 'width:1400px; height:720px; background-color:lightgrey'></svg>
    <Classics></Classics>
    <Asset></Asset>
  </div>
</template>
<script>
import Classics from "./components/Classics.vue"
import Asset from "./components/Asset.vue"

export default {
    name:'App',
    components:{
      Classics,
      Asset
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
#bottomLayer{
  z-index: -1;
}

#Classics {
  position: absolute;
  top:0px;
  left:3px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
  z-index:0;
}

#Heatmap {
  position: absolute;
  top:345px;
  left:3px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
  z-index:0;
}

#Asset{
  position: absolute;
  top:345px;
  left:815px;
  background: #ffffff;
  border-radius: 2px;
  border-color: blueviolet;
  z-index:0;
}
#app {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
</style>
