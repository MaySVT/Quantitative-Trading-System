<template>
  <input class="asset-code" type="text" v-model.lazy = "asset_code" placeholder="Input Asset Code">
  <input class="time-start" type="text" v-model.lazy = "start_time" placeholder="Input Start Time">
  <input class="time-end" type="text" v-model.lazy = "end_time" placeholder="Input End Time">
  <input class="time-frequency" type="text" v-model.lazy = "frequency" placeholder="Input Frequency">
  <div class = "basic-button" @click="getLayers()" type="submit">Basic</div>
  <!--div class = "basic-button" @click="mode='basic'" type="submit">Basic</div-->
  <div class = "ga-button" @click="mode='ga'" type="submit">Genetic Algorithm</div>
  <div class = "IC-title" type="submit">Factor IC</div>
  <div class = "FI-title" type="submit">Xgboost Factor Importance</div>
  <div class = "Layer-title" type="submit">Layer Backtest</div>

  <svg id = "IC" class="ic" style = 'width:450px; height:210px'></svg>
  <svg id = "Layer" class="ly" style = 'width:580px; height:210px'></svg>
  <svg id = "feature-importance" class="fi" style = 'width:450px; height:210px'></svg>

  <div id="basic-cal" v-if="mode=='basic'">
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
        height="450"
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
    </div>
    <div id="ga_factor_mining" v-if="mode=='ga'">
      <div>
        <progress :value="progress" max="100"></progress>
        <p>{{ progressMessage }}</p>
      </div>
      <el-select class="gaFactor-select" v-model="gaFactorList" multiple placeholder="请选择需要进行挖掘的初代因子">
        <el-option
          v-for="(item,index) in options"
          :key="index"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>

      <div class = "factor-button" @click="getGpFactors()" type="submit">挖掘</div>
      <el-table id="DataTable"
          v-if="gaFactors_show.length==200"
          :data="gaFactors_show"
          @header-click="getLayers,DrawLayers"
          height="450"
          :header-cell-style="{'text-align':'center'}"
          style="width:50%">
          
          <el-table-column
            fixed
            prop="open_time"
            label="open time"
            width="160"
            align="center">
          </el-table-column>
          <el-table-column 
            v-for="(item,index) in new_gaFactorList"  
            :prop="item" 
            :label="item" 
            :key="index"
            width="120"
            align="center">
          </el-table-column>
        
      </el-table>
      <input type="checkbox" id='layer1-select' class="layer1-selector" v-model="manifest[0]" @change="layer_manifest(1)"/>
      <input type="checkbox" id='layer2-select' class="layer2-selector" v-model="manifest[1]" @change="layer_manifest(2)"/>
      <input type="checkbox" id='layer3-select' class="layer3-selector" v-model="manifest[2]" @change="layer_manifest(3)"/>
      <input type="checkbox" id='layer4-select' class="layer4-selector" v-model="manifest[3]" @change="layer_manifest(4)"/>
      <input type="checkbox" id='layer5-select' class="layer5-selector" v-model="manifest[4]" @change="layer_manifest(5)"/>
      <p v-text="'Layer 1'" style="position:absolute; top:625px; left:610px;font-size:smaller;"></p>
      <p v-text="'Layer 2'" style="position:absolute; top:655px; left:610px;font-size:smaller;"></p>
      <p v-text="'Layer 3'" style="position:absolute; top:685px; left:610px;font-size:smaller;"></p>
      <p v-text="'Layer 4'" style="position:absolute; top:715px; left:610px;font-size:smaller;"></p>
      <p v-text="'Layer 5'" style="position:absolute; top:745px; left:610px;font-size:smaller;"></p>
    </div>
    
</template>


<script>
import axios from 'axios'
//import io from 'socket.io-client'
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
      width: 450,
      height: 200,
      margin:{
        top:30,
        right:15,
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
      options:[{
          value: "OBV",
          label: "OBV"
        }, {
          value: "EMA",
          label: "EMA"
        }, {
          value: "ATR",
          label: "ATR"
        }, {
          value: "AD",
          label: "AD"
        }, {
          value: "ROC",
          label: "ROC"
        }],
      gaFactorList:[],
      gaFactors:[],
      IC:{},
      mode:"",
      new_gaFactorList:[],
      gaFactors_show:[],
      progress: 0,
      progressMessage: '',
      layer:[],
      manifest:[true,true,true,true,true],
      xg_feature_importance:[]
    }
  },
  mounted(){
      // // 建立与后端的 WebSocket 连接
      // const socket = io('http://localhost:5000');

      // // 监听后端发送的 'genetic_algorithm_progress' 事件
      // socket.on('genetic_algorithm_progress', (data) => {
      //   this.progress = data.progress;
      //   this.progressMessage = data.message;
      // });
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
    },
    factorlist(){
      return this.new_gaFactorList;
    },
    layers(){
      return this.layer;
    }
  },
  methods:{
     getAsset(){
      console.log(Object.keys(this.IC))
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
      // const path = "http://127.0.0.1:5000/CU1811.SHF/st=20180101ed=20180301freq=D/['OBV','EMA','ATR','AD','ROC']/gr=2ps=20ts=10hof=20comp=2method=half%20and%20halfdepth=(2,4)";
      const path = "http://127.0.0.1:5000/CU1811.SHF/st=20180101ed=20180301freq=D/[\""+this.gaFactorList.join("\",\"")+"\"]/gr=2ps=20ts=10hof=20comp=2method=half%20and%20halfdepth=(2,4)";
      axios
         .get(path)
         .then(res => {
           this.gaFactors=eval(res.data)['factors'];
           this.IC = eval(res.data)['IC'];
           this.xg_feature_importance = eval(res.data)['feature_importance'];
           this.new_gaFactorList = Object.keys(this.IC);
           console.log(this.gaFactors);
           console.log(this.IC);
           console.log(this.xg_feature_importance);
         })
         .catch(error => {
           console.error(error);
         });
     },
     genetic_algorithm_progress() {
      // try {
      //   // 发起后端请求开始遗传算法
      //   const response = await axios.post('/start_genetic_algorithm');
        
      //   // 通过WebSocket监听进度信息的更新
      //   const socket = new WebSocket('ws://your-backend-websocket-url');
        
      //   socket.addEventListener('message', (event) => {
      //     const data = JSON.parse(event.data);
      //     this.progress = data.progress;
      //     this.progressMessage = data.message;
      //   });
      // } catch (error) {
      //   console.error('Error starting genetic algorithm:', error);
      // }

    },

    getLayers(){
      const path = "http://127.0.0.1:5000/layers/metal/ATR"; 
      axios
         .get(path)
         .then(res => {
           this.layer=res.data;
           console.log(this.layer);
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
 
     show_gaFactors(){
      for(let i = 0; i < 200;i++){
        let t = new Date(this.gaFactors[i]['open_time']);
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
        // tmp['ts_code']=this.asset[i]['ts_code']
        tmp['open_time'] = y+'-'+m+'-'+d+' '+h+':'+minute;
        for(let s=0;s<this.gaFactorList.length;s++ ){
          tmp[this.gaFactorList[s]] = this.gaFactors[i][this.new_gaFactorList[s]];
        }
        for(let s=0;s<this.new_gaFactorList.length;s++ ){
          tmp[this.new_gaFactorList[s]] = this.gaFactors[i][this.new_gaFactorList[s]];
        }
        
        this.gaFactors_show.push(tmp);
      }
      console.log(this.gaFactors_show);
     },
 
     Scale(){
        //const gap = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        const g = d3.select('#IC').append('g').attr('id', 'ICscale')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
        // const b = 30000;
        // const a = -30000;
        // var [a,b] = d3.extent(this.IC)
        
        let that = this;
        const xscale = d3.scaleLinear()
                         .domain([0,that.new_gaFactorList.length])
                         .range([0, this.innerWidth]);
        const yscale = d3.scaleLinear()
                         .domain([1,-1])
                         .range([0,this.innerHeight]);
        // console.log([a,b])
        const yaxis = d3.axisLeft(yscale)
                        .ticks(10)
                        .tickSize(5)
                        .tickPadding(5);
        const xaxis = d3.axisBottom(xscale)
                        .ticks(that.new_gaFactorList.length)
                        .tickSize(-5)
                        .tickPadding(5)
                        .tickFormat(function(d,i){
                          return (i>0)?(that.new_gaFactorList[i-1]):""
                        })
                        //.transform(`translate(${0},${this.innerHeight/2})`);

                       g.append('g').call(yaxis)
                        .attr('id' ,'yaxis');
             const x = g.append('g').call(xaxis)
                        .attr('id', 'xaxis')
                        .attr('transform',`translate(${0},${this.innerHeight/2})`);
                       x.selectAll('text') // 选择所有x轴刻度文字
                        .style('text-anchor', 'end') // 设置文字锚点为末尾
                        .attr('transform', 'rotate(-30) translate(0, 0)');
    },
  
    drawIC(){
      let that = this;
      //const b = d3.max(this.orders_aggregated, function(m){return d3.max(m['value'],d=>d['filled_value']);});
      //const a = d3.min(this.orders, function(m){return d3.min(m['value'],d=>d['filled_value']);});
      // const b = 30000;
      // const a = -30000;

      // var [a,b] = d3.extent(this.IC)
      console.log()
      const xscale = d3.scaleLinear()
                         .domain([0,that.new_gaFactorList.length])
                         .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
                         .domain([1,-1])
                         .range([0, this.innerHeight]);
      // console.log([a,b])

      const g = d3.select('#IC').append('g').attr('id', 'ICview')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

      g.selectAll('.bar')
       .data(that.new_gaFactorList).enter()
       .append("rect")
       .attr('class', 'bar')
       .attr("x", function(d,i) {console.log(d); return xscale(i+0.5); })
       .attr("y", function(d) { return yscale(that.IC[d]>0?that.IC[d]:0); })
       .attr("height", function(d) { return  Math.abs(yscale(0) - yscale(that.IC[d])); })
       .attr("width", that.innerWidth/this.new_gaFactorList.length/2)
       .attr("fill", "#009966")
       .attr("stroke", "#000")
       .on("mouseover",function(){
        let d =d3.select(this).data();
        var str = 'IC:' + that.IC[d[0]];
        var t = 60+ yscale(that.IC[d[0]]);
        
        d3.selectAll('.tooltip')
          .html(str)
               .style("left", (xscale(d[0]['id'])+595)+"px")
               .style("top", (t)+"px")
               .style("opacity",1.0);
    })
      .on("mouseleave",function(){
            d3.select('#Tip')
              .selectAll('.tooltip')
              .style("opacity",0.0);
          })
; 

    },

    DrawLayers(){
      const g = d3.select('#Layer').append('g').attr('id', 'Layerscale')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
        // const b = 30000;
        // const a = -30000;
        // var [a,b] = d3.extent(this.IC)
        
        let that = this;
        const xscale = d3.scaleLinear()
                         .domain([1579651200000,1671148800000])
                         .range([0, this.innerWidth+130]);
        const yscale = d3.scaleLinear()
                         .domain([2.8,0.3])
                         .range([0,this.innerHeight]);
        // console.log([a,b])
        const yaxis = d3.axisLeft(yscale)
                        .ticks(10)
                        .tickSize(5)
                        .tickPadding(5);
        const xaxis = d3.axisBottom(xscale)
                        .ticks(10)
                        .tickSize(-5)
                        .tickPadding(5)
                        .tickFormat(function(d,i){
                          let t = new Date(d);
                          let y = t.getFullYear();
                          let m = t.getMonth()+1;
                          m = m<10?'0'+m:m;
                          let date = t.getDate();
                          date = date<10?'0'+date:date;                  
                          return (i>0)?(y+'-'+m+'-'+date):""
                        })
                        

                       g.append('g').call(yaxis)
                        .attr('id' ,'yaxis');
             const x = g.append('g').call(xaxis)
                        .attr('id', 'xaxis')
                        .attr('transform',`translate(${0},${yscale(1)})`);
                       x.selectAll('text') // 选择所有x轴刻度文字
                        .style('text-anchor', 'end') // 设置文字锚点为末尾
                        .attr('transform', 'rotate(-30) translate(0, 5)');

            const line = d3.line()
                         .x(function(d){return xscale(d['date'])}) // x轴坐标
                         .y(function(d){return yscale(d['1D'])}) // y
                         .curve(d3.curveLinear);

  
            const g2 = d3.select('#Layer').append('g').attr('id', 'LayerCurve')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
            
            const colors = ['red','orange','blue','green','yellow']

                      // // 绑定数据并绘制折线
                      // svg.selectAll(".line")
                      //   .data(that.layer)
                      //   .enter()
                      //   .append("path")
                      //   .attr("class", "line")
                      //   .attr("d", d => line(d))
                      //   .attr("stroke", (d, i) => colors[i]); // 可以设置不同折线的颜色


            for(let k = 1;k<=5;k++){
              g2.append('path').attr('id','layer_curve'+k)
                .attr('d',function(){return line(that.layer[k-1])})
                .attr('fill','none')
                .attr('stroke',function(){return colors[k-1];})
                // .attr('visibility',function(){return })
            }

    },

  layer_manifest(k){
    let that = this;
        d3.select('#Layer')
          .select('#layer_curve'+k)
          .attr('visibility',function(){
            if(that.manifest[k-1]){
              return 'visible';
            }else{
              return 'hidden';
            }
          })

        const colors = ['red','orange','blue','green','yellow']

        d3.select('#layer'+k+'-select')
          .style('border-color',function(){
            if(that.manifest[k-1]){
              return colors[k-1];
            }else{
              return 'lightgray';
            }
          })
  },

  drawFI(){
      let that = this;
      const g = d3.select('#feature-importance').append('g').attr('id', 'FIcale')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

        const xscale = d3.scaleLinear()
                         .domain([0,that.xg_feature_importance.length])
                         .range([0, this.innerWidth]);
        const yscale = d3.scaleLinear()
                         .domain([1,-1])
                         .range([0, this.innerHeight]);

        // console.log([a,b])
        const yaxis = d3.axisLeft(yscale)
                        .ticks(10)
                        .tickSize(5)
                        .tickPadding(5);
        const xaxis = d3.axisBottom(xscale)
                        .ticks(that.xg_feature_importance.length)
                        .tickSize(-5)
                        .tickPadding(5)
                        .tickFormat(function(d,i){
                          return (i>0)?(that.xg_feature_importance[i-1]['factor']):""
                        })
                        //.transform(`translate(${0},${this.innerHeight/2})`);

                       g.append('g').call(yaxis)
                        .attr('id' ,'yaxis');
             const x = g.append('g').call(xaxis)
                        .attr('id', 'xaxis')
                        .attr('transform',`translate(${0},${this.innerHeight/2})`);
                       x.selectAll('text') // 选择所有x轴刻度文字
                        .style('text-anchor', 'end') // 设置文字锚点为末尾
                        .attr('transform', 'rotate(-30) translate(0, 0)');
     
      
      const g2 = d3.select('#feature-importance').append('g').attr('id', 'FIview')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

      g2.selectAll('.bar')
       .data(that.xg_feature_importance).enter()
       .append("rect")
       .attr('class', 'bar')
       .attr("x", function(d,i) {return xscale(i+0.5); })
       .attr("y", function(d) { return yscale(d['importance']>0?d['importance']:0); })
       .attr("height", function(d) { return  Math.abs(yscale(0) - yscale(d['importance'])); })
       .attr("width", that.innerWidth/that.xg_feature_importance.length/2)
       .attr("fill", "#009966")
       .attr("stroke", "#000")
       .on("mouseover",function(){
        let d =d3.select(this).data();
        var str = 'IC:' + that.IC[d[0]];
        var t = 60+ yscale(that.IC[d[0]]);
        
        d3.selectAll('.tooltip')
          .html(str)
               .style("left", (xscale(d[0]['id'])+595)+"px")
               .style("top", (t)+"px")
               .style("opacity",1.0);
    })
      .on("mouseleave",function(){
            d3.select('#Tip')
              .selectAll('.tooltip')
              .style("opacity",0.0);
          }); 
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
    // this.getGpFactors();
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
    },
    factorlist(){
      // this.new_gaFactorList = Object.keys(eval(res.data)['IC']);
      console.log(this.new_gaFactorList);
      this.show_gaFactors();
      this.Scale();
      this.drawIC();
      this.drawFI();
    },
    layers(){
      console.log('Draw');
      this.DrawLayers();
    },
    manifest(){
      console.log(this.manifest);
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

.gaFactor-select{
  position:absolute;
  top:90px;
  left:10px;
  width:420px;
  height:40px;
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

.basic-button{
display: flex;
position: absolute;
top: 50px;
left:560px;
width: 50px;
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
font-size: 14px;
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

.IC-title{
display: flex;
position: absolute;
top: 150px;
left:880px;
width: 80px;
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
font-size: 14px;
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

.FI-title{
display: flex;
position: absolute;
top: 380px;
left:840px;
width: 200px;
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
font-size: 14px;
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

.Layer-title{
display: flex;
position: absolute;
top: 600px;
left:280px;
width: 110px;
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
font-size: 14px;
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

.ga-button{
display: flex;
position: absolute;
top: 50px;
left:620px;
width: 140px;
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
font-size: 14px;
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
  position:absolute;
  top:135px;
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

.ic{
  position:absolute;
  top:150px;
  left:700px;
}

.fi{
  position:absolute;
  top:380px;
  left:700px;
}


.ly{
  position:absolute;
  top:600px;
  left:0px;
}


.layer1-selector {
  position: absolute;
  outline: none;
  width: 13px;
  height: 13px;
  left:590px;
  top:640px;

  background-color: #ffffff;
  border: solid 2px red;
  -webkit-border-radius: 80%;
  border-radius: 80%;
  font-size: 0.8rem;
  margin: 0;
  padding: 0;
  cursor:pointer;
  appearance:none;
  -webkit-appearance: none;
  -webkit-user-select: none;
  user-select: none;
}

.layer2-selector {
  position: absolute;
  outline: none;
  width: 13px;
  height: 13px;
  left:590px;
  top:670px;
 
  background-color: #ffffff;
  border: solid 2px orange;
  -webkit-border-radius: 80%;
  border-radius: 80%;
  font-size: 0.8rem;
  margin: 0;
  padding: 0;
  cursor:pointer;
  appearance:none;
  -webkit-appearance: none;
  -webkit-user-select: none;
  user-select: none;
}

.layer3-selector {
  position: absolute;
  outline: none;
  width: 13px;
  height: 13px;
  left:590px;
  top:700px;

  background-color: #ffffff;
  border: solid 2px blue;
  -webkit-border-radius: 80%;
  border-radius: 80%;
  font-size: 0.8rem;
  margin: 0;
  padding: 0;
  cursor:pointer;
  appearance:none;
  -webkit-appearance: none;
  -webkit-user-select: none;
  user-select: none;
}

.layer4-selector {
  position: absolute;
  outline: none;
  width: 13px;
  height: 13px;
  left:590px;
  top:730px;

  background-color: #ffffff;
  border: solid 2px green;
  -webkit-border-radius: 80%;
  border-radius: 80%;
  font-size: 0.8rem;
  margin: 0;
  padding: 0;
  cursor:pointer;
  appearance:none;
  -webkit-appearance: none;
  -webkit-user-select: none;
  user-select: none;
}

.layer5-selector {
  position: absolute;
  outline: none;
  width: 13px;
  height: 13px;
  left:590px;
  top:760px;

  background-color: #ffffff;
  border: solid 2px yellow;
  -webkit-border-radius: 80%;
  border-radius: 80%;
  font-size: 0.8rem;
  margin: 0;
  padding: 0;
  cursor:pointer;
  appearance:none;
  -webkit-appearance: none;
  -webkit-user-select: none;
  user-select: none;
}
</style>
