<template>
  <div id = "DataAPI">
    <div class="panel-header">期货数据</div>
    <div class="panel-header-end"></div>
    <!--button id = 'ATR' @click = 'getATR(),Scale(),Draw()'>ATR</button-->
    <!--button id = 'DT' @click = 'trial()'>Dual Thrust</button-->
    <input class="asset-code" type="text" v-model.lazy = "asset_code" placeholder="Input Asset Code">
    <input class="time-start" type="text" v-model.lazy = "start_time" placeholder="Input Start Time">
    <input class="time-end" type="text" v-model.lazy = "end_time" placeholder="Input End Time">
    <input class="time-frequency" type="text" v-model.lazy = "frequency" placeholder="Input Frequency">
    <div class = "time-button" @click="getAsset()" type="submit">Search</div>
    <div class="panel-header pr">{{flag}}</div>
    <div class="panel-header-end pr-end"></div>
    <div class="panel-header vl">Volume</div>
    <div class="panel-header-end vl-end"></div>
    <svg id = "Price"  class="prices" style = 'width:520px; height:200px'></svg>
    <svg id = "Vol"  class="volume" style = 'width:520px; height:200px'></svg>
    <el-table id="DataTable"
      :data="asset_show"
      @header-click="Draw"
      height="480"
      header-align="center"
      style="width: 52%">
      <el-table-column
        fixed
        prop="trade_time"
        label="Trade Time"
        width="140">
      </el-table-column>
      <el-table-column
        prop="open"
        label="open"
        width="100">
      </el-table-column>
      <el-table-column
        prop="close"
        label="close"
        width="100">
      </el-table-column>
      <el-table-column
        prop="high"
        label="high"
        width="100">
      </el-table-column>
      <el-table-column
        prop="low"
        label="low"
        width="100">
      </el-table-column>
      <el-table-column
        prop="vol"
        label="vol"
        width="80">
      </el-table-column>
      <el-table-column
        prop="amount"
        label="amount"
        width="90">
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import axios from 'axios'
import * as d3 from 'd3'

export default {
  name:'DataAPI',
  data(){
    return {
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
      asset_code:"",
      start_time:"",
      end_time:"",
      frequency:"",
      strategy:"",
      flag:"price"
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
    }
  },
  methods:{
     getAsset(){
      const path = "http://127.0.0.1:5000/CU1811.SHF/st=20180101ed=20180301freq=D";
      // const path = "http://127.0.0.1:5000/"+this.asset_code+"/st="+this.start_time+"ed="+this.end_time+"freq="+this.frequency;
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
        console.log(t)
        this.asset[i]['trade_time'] = y+'-'+m+'-'+d+' '+h+':'+minute;
        if(i < 200){
          this.asset_show.push(this.asset[i]);
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

     Vol(){
      d3.select('#Volscale').remove()
      const g = d3.select('#Vol').append('g').attr('id', 'Volscale')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
               
      //防止代码中将this错认为当前数据，用that代替全局的this
      let that = this;

      var vol_show = [];
      for(let j=0;j<that.asset.length;){
        let current_date = that.asset[j]['trade_time'].slice(0,10);
        let v = 0;
        for(let i = 0; ;i++){
          if(j+i>=that.asset.length||that.asset[j+i]['trade_time'].slice(0,10)!=current_date){
            vol_show.push({'trade_date':current_date,'vol':v});
            j = j+i;
            break;
          }
          if(that.asset[j+i]['trade_time'].slice(0,10)==current_date){
            v += that.asset[j+i]['vol']
          }
        }
      }
            
      //设置x轴、y轴的映射函数，将数据映射到x、y轴坐标上
      var [a,b] = d3.extent(vol_show,function(d){return d['vol'];});
      console.log(a,b)
      const xscale = d3.scaleLinear()
                       .domain([0,vol_show.length])
                       .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
                       .domain([b,0])
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
                        return d==0?"":vol_show[d-1]['trade_date'].slice(5,);
                      })
                     g.append('g').call(yaxis)
                      .attr('id' ,'yaxis');
                     g.append('g').call(xaxis)
                      .attr('id', 'xaxis')
                      .attr('transform', `translate(${0},${this.innerHeight})`);
                      
                     d3.select('#xaxis')
                       .selectAll('.tick')
                       .selectAll('text')
                       .attr("font-size","6px")
                       .attr('transform', `translate(${0},${20})`);

      const stack = d3.stack()
                      .keys(['vol'])
                      .order(d3.stackOrderNone)
                      .offset(d3.stackOffsetNone)
      const series = stack(vol_show)
      console.log(series);
      const g2 = d3.select('#Vol').append('g').attr('id', 'VolBar')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      g2.selectAll('rect')
       .data(series[0]).enter()
       .append("rect")
       .attr('class', 'bar')
       .attr("x", function(d,i) { return xscale(i+0.5); })
       .attr("y", function(d) { return yscale(d[1]); })
       .attr("height", function(d) { return yscale(d[0])-yscale(d[1]); })
      .attr("width", this.innerWidth/vol_show.length)
      .attr("fill", 'red')
      .attr("stroke", "#000");

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
  },
  beforeUnmount() {
  },
  watch:{
    asset(){
      this.convertTime();
      this.Vol();
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
.time-button{
display: flex;
position: absolute;
top: 50px;
left:555px;
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
  top:65px;
  left:10px;
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
