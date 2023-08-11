<template>
  <input class="asset-code" type="text" v-model.lazy = "asset_code" placeholder="Input Asset Code">
  <input class="time-start" type="text" v-model.lazy = "start_time" placeholder="Input Start Time">
  <input class="time-end" type="text" v-model.lazy = "end_time" placeholder="Input End Time">
  <input class="time-frequency" type="text" v-model.lazy = "frequency" placeholder="Input Frequency">
  <select class="factor1-select" v-model="factor1">
    <option disabled selected value>- Choose Factor 1</option>
    <option v-for="item in factorList" v-bind:value="item.name" :key="item.id" v-text="item.name" ></option>
  </select>
  <select class="operator-select" v-model="operator">
    <option disabled selected value>- Operator</option>
    <option v-for="item in operatorList" v-bind:value="item.name" :key="item.id" v-text="item.name" ></option>
  </select>
  <select class="factor2-select" v-model="factor2">
    <option disabled selected value>- Choose Factor 2</option>
    <option v-for="item in factorList" v-bind:value="item.name" :key="item.id" v-text="item.name" ></option>
  </select>
  <div class = "factor-button" @click="getAsset()" type="submit">Calculate</div>
  <el-table id="DataTable"
      v-if="flag==1"
      :data="asset_show"
      @header-click="Draw"
      height="480"
      :header-cell-style="{'text-align':'center'}"
      style="width:50%">
      
      <el-table-column
        fixed
        prop="trade_time"
        label="Trade time"
        width="160"
        align="center">
      </el-table-column>
      <el-table-column 
        v-for="(item,index) in tableHead"  
        :prop="item.column_name" 
        :label="item.column_comment" 
        :key="index"
        width="120"
        align="center">
      </el-table-column>
    
    </el-table>
</template>


<script>
import axios from 'axios'
import * as d3 from 'd3'

export default {
  name:'DataAPI',
  data(){
    return {
      factorList:[{name:"open",id:1},{name:"close",id:2},{name:"high",id:3},{name:"low",id:3}],
      operatorList:[{name:"+",id:1},{name:"-",id:2},{name:"x",id:3},{name:"÷",id:4}],  
      asset:[],
      asset_show:[],
      feature_show:[],
      width: 490,
      height: 200,
      margin:{
        top:20,
        right:10,
        bottom:10,
        left:50
      },
      r:10,
      c:20,
      factor1:"",
      factor2:"",
      operator:"",
      asset_code:"",
      start_time:"",
      end_time:"",
      frequency:"",
      strategy:"",
      flag1:0,
      flag2:0,
      gaFactorList:[],
      gaFactors:[],
      IC:{}
    }
  },
  mounted(){

  },
  computed:{
    innerWidth(){
      return this.width - this.margin.left - this.margin.right
    },
    innerHeight(){
      return this.height - this.margin.top - this.margin.bottom
    },
    tableHead(){
      return [{column_name: this.factor1,column_comment:this.factor1},{column_name: this.factor2,column_comment:this.factor2},{column_name: "new_factor",column_comment:"new factor"}];
    },
    flag(){
      return this.flag1*this.flag2;
    }
  },
  methods:{
     getAsset(){
      const path = "http://127.0.0.1:5000/CU1811.SHF/st=20180101ed=20180301freq=D";
      //const path = "http://127.0.0.1:5000/"+this.asset_code+"/st="+this.start_time+"ed="+this.end_time+"freq="+this.frequency;
      axios
         .get(path)
         .then(res => {
           this.asset=res.data;
           console.log(this.asset);
         })
         .catch(error => {
           console.error(error);
         });
     },
     getGpFactors(){
      const path = "http://127.0.0.1:5000/CU1811.SHF/st=20180101ed=20180301freq=D/['OBV','EMA','ATR','AD','ROC']/gr=2ps=20ts=10hof=20comp=2method=half%20and%20halfdepth=(2,4)";
      // const path = "http://127.0.0.1:5000/CU1811.SHF/st=20180101ed=20180301freq=D/"+this.gaFactorList+"/gr=2ps=20ts=10hof=20comp=2method=half%20and%20halfdepth=(2,4)";
      axios
         .get(path)
         .then(res => {
           this.gaFactors=eval(res.data)['factors'];
           this.IC = eval(res.data)['IC'];
           console.log(this.gaFactors);
           console.log(this.IC);
         })
         .catch(error => {
           console.error(error);
         });
     },
     convertTime(){
      for(let i = 0; i < this.asset.length;i++){
        let t = new Date(this.asset[i]['trade_time']);
        let y = t.getFullYear();
        let m = t.getMonth();
        m = m<10?'0'+m:m;
        let d = t.getDate();
        d = d<10?'0'+d:d;
        let h = t.getHours();
        h = h<10?'0'+h:h;
        let minute = t.getMinutes();
        minute = minute<10?'0'+minute:minute;
        let tmp = {}
        tmp['ts_code']=this.asset[i]['ts_code']
        tmp['trade_time'] = y+'-'+m+'-'+d+' '+h+':'+minute;
        tmp[this.factor1] = this.asset[i][this.factor1]
        tmp[this.factor2] = this.asset[i][this.factor2]
        if(this.operator=="+"){
          tmp["new_factor"]=tmp[this.factor1]+tmp[this.factor2];
        }
        if(this.operator=="-"){
          tmp["new_factor"]=tmp[this.factor1]-tmp[this.factor2];
        }
        if(this.operator=="x"){
          tmp["new_factor"]=tmp[this.factor1]*tmp[this.factor2];
        }
        if(this.operator=="÷"){
          tmp["new_factor"]=tmp[this.factor1]/tmp[this.factor2];
        }
        if(i < 200){
          this.asset_show.push(tmp);
        }
      }
      console.log(this.asset_show);
     },
 
     //ATR strategy的函数实现
     Draw(column){
      let feature = column.label;        
      console.log(feature)
      if (feature=="Trade Time" || feature=="vol"||feature=="amount"){
        return
      }
      d3.select('#Price').selectAll('g').remove()
      //d3.select('#priceCurve').remove()
      const g = d3.select('#Price').append('g').attr('id', 'Pricesscale')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
               
      //防止代码中将this错认为当前数据，用that代替全局的this
      let that = this;
      var temp = [];
      for (let j = 0; j < that.asset.length;j++){
        temp.push(that.asset[j][feature]);
      }
      //设置x轴、y轴的映射函数，将数据映射到x、y轴坐标上
      var [a,b] = d3.extent(temp);

      console.log(a,b)
      const xscale = d3.scaleLinear()
                       .domain([0,that.asset.length])
                       .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
                       .domain([b,a])
                       .range([0, this.innerHeight]);
      
      const yaxis = d3.axisLeft(yscale)
                      .ticks(10)
                      .tickSize(5)
                      .tickPadding(2)
                      .tickFormat(function(d){
                        return d;
                      })
      const xaxis = d3.axisBottom(xscale)
                      .ticks(20)
                      .tickSize(-5)
                      .tickPadding(-15)
                      .tickFormat(function(d){
                        //return i;
                        //console.log(that.asset[d]['trade_time'])
                        return d<that.asset.length?that.asset[d]['trade_time'].slice(5,10):that.asset[d-1]['trade_time'].slice(5,10);
                      })
                     g.append('g').call(yaxis)
                      .attr('id' ,'yaxis');
                     g.append('g').call(xaxis)
                      .attr('id', 'xaxis')
                      
                     d3.select('#xaxis')
                       .selectAll('.tick')
                       .selectAll('text')
                       .attr("font-size","9px");

      //选择id为'Classics'的svg，增添g并取id为classicCurve，移动画布使其与设置的margin对其
      const g2 = d3.select('#Price').append('g').attr('id', 'priceCurve')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      
      //设置旗帜为ATR，表示按下了ATR按钮
      that.flag=feature;
   
      //设置折线图的映射函数，会将数据映射为每个点的坐标/每条线段的路径值
      const line = d3.line()
                     .x(function(d,i){return xscale(i)})
                     .y(function(d){return yscale(d)})
                     .curve(d3.curveLinear)
    
      //在g上增添路径path，并将目标画线的数据传入line映射函数中
      g2.append('path')
        .attr('d',line(temp))
        .attr('fill','none')
        .attr('stroke',"#3366ff")
     },

  colorbox(sel, size, colors){
    var [x0,x1] = d3.extent( colors.domain());
    var bars = d3.range( x0, x1, (x1-x0)/size[1]);
    var sc = d3.scaleLinear()
        .domain([x0,x1]).range([0, size[1]]);
    sel.selectAll("line").data(bars).enter().append("line")
      .attr("x1", 0).attr("x2",size[0])
      .attr("y1", sc).attr("y2",sc)
      .attr("stroke",colors);
    
    sel.append("rect")
        .attr("width",size[0]).attr("height",size[1])
        .attr("fill","none").attr("stroke","black")
      }
  },
  created(){
    this.getGpFactors();
  },
  beforeUnmount() {
  },
  watch:{
    asset(){
      this.convertTime();
      console.log(this.tableHead);
  },
    factor1(){
      this.flag1=1;
    },
    factor2(){
      this.flag2=1;
    }
}
};
</script>

<style scoped>
.tooltip{
    position: absolute;
    padding-left:5px;
    padding-right:5px;
    width:auto;
    height:auto;
    border:1px solid #2ea44f;
    border-radius:5px;
    background-color: white;
    font-size: 8px;
    text-align: center;
    opacity:0;
    z-index:999;
        }

.tooltip2{
  position:absolute;
  left:0px;
  top:0px;
  width:auto;
  height:auto;
  border:2px solid lightcoral;
  border-radius:5px;
  padding-left:1px;
  padding-right:1px;
  padding-top:1px;
  padding:1px;
  background-color: white;
  font-size: 1px;
  text-align: center;
  opacity:0;
  z-index:99;
}
.panel-header {
  position: absolute;
  top: 90px;
  left:10px;
  padding: 2px 2px-2px 20px;
  width: 60px;
  height: 22px;
  line-height: 18px;
  font-size: 6px;
  text-align: right;
  background: #415c68;
  color: #fcfcfc;
  display: flex;
  justify-content:space-evenly;
  align-items: center;
  align-content:stretch;
  font-weight: bold;
  border-radius: 1px;
  box-shadow: 0 1px 2px rgba(26 26 26 0.2);
  z-index:99;
}

.panel-header-end {
  position: absolute;
  top: 90px;
  left:70px;
  border-top: 22px solid #455a64;
  border-right: 22px solid #ffffff;
  border-bottom: 0px solid #ffffff;
  z-index:98;
}
.pr{
  position:absolute;
  top:90px;
  left:640px;
}
.pr-end{
  position:absolute;
  top:90px;
  left:700px;
}
.vl{
  position:absolute;
  top:350px;
  left:640px;
}
.vl-end{
  position:absolute;
  top:350px;
  left:700px;
}
.asset-code{
position: absolute;
top: 50px;
left:20px;
width: 125px;
height: 18px;
border-top: 5px solid #455a64;
border-bottom: 2px solid #455a64;
z-index:98;
}
.time-start{
position: absolute;
top: 50px;
left:160px;
width: 125px;
height: 18px;
border-top: 5px solid #455a64;
border-bottom: 2px solid #455a64;
z-index:98;
}

.time-end{
position: absolute;
top: 50px;
left:300px;
width: 125px;
height: 18px;
border-top: 5px solid #455a64;
border-bottom: 2px solid #455a64;
z-index:98;
}
.time-frequency{
position: absolute;
top: 50px;
left:440px;
width: 100px;
height: 18px;
border-top: 5px solid #455a64;
border-bottom: 2px solid #455a64;
z-index:98;
}
.factor1-select{
  position:absolute;
  top:90px;
  left:10px;
  width:150px;
  height:25px;
  margin-top:5px;
  margin-bottom:5px;
  margin-left:10px;
}

.operator-select{
  position:absolute;
  top:90px;
  left:170px;
  width:90px;
  height:25px;
  margin-top:5px;
  margin-bottom:5px;
  margin-left:10px;
}

.factor2-select{
  position:absolute;
  top:90px;
  left:270px;
  width:150px;
  height:25px;
  margin-top:5px;
  margin-bottom:5px;
  margin-left:10px;
}

.factor-button{
display: flex;
position: absolute;
top: 95px;
left:455px;
width: 90px;
height: 25px;
appearance: none;
background-color: #455a64;
border: 1px solid rgba(27, 31, 35, .15);
border-radius: 5px;
box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
box-sizing: border-box;
color: #fff;
cursor: pointer;
display: inline-block;
font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
font-size: 15px;
font-weight: 520;
line-height: 10px;
padding: 5px 5px;
text-align: center;
text-decoration: none;
justify-content:space-evenly;
align-items: center;
align-content:stretch;
user-select: none;
-webkit-user-select: none;
touch-action: manipulation;
vertical-align: middle;
white-space: nowrap;
}

.price-button{
display: flex;
position: absolute;
top: 50px;
left:675px;
width: 90px;
height: 25px;
appearance: none;
background-color: #455a64;
border: 1px solid rgba(27, 31, 35, .15);
border-radius: 5px;
box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
box-sizing: border-box;
color: #fff;
cursor: pointer;
display: inline-block;
font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
font-size: 15px;
font-weight: 520;
line-height: 10px;
padding: 5px 5px;
text-align: center;
text-decoration: none;
justify-content:space-evenly;
align-items: center;
align-content:stretch;
user-select: none;
-webkit-user-select: none;
touch-action: manipulation;
vertical-align: middle;
white-space: nowrap;
}

#DataTable{
  top:100px;
  left:20px;
}
#Price{
  position:absolute;
  top:115px;
  left:670px;
}
#Vol{
  position:absolute;
  top:380px;
  left:670px;
}
</style>
