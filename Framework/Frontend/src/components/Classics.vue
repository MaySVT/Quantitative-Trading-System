<template>
    <div id = "Tip">
      <div class="panel-header">回测结果</div>
      <div class="panel-header-end"></div>
      <svg id = "Classics"  class="classic" style = 'width:810px; height:370px'>
      </svg>
      <div class="tooltip"></div>
      <div class="tooltip2"></div>
      <button id = 'ATR' @click = 'getATR(),Scale(),Draw()'>ATR</button>
      <button id = 'DT' @click = 'trial()'>Dual Thrust</button>
    <form action="strategy=custom" method=post enctype=multipart/form-data>
         <input class="custom-strategy file" type=file name=file>
         <input  class="custom-strategy upload" type=submit value=Upload>
    </form>
    </div>
    <div class="content-left">
      <div class="seg"></div>
      <div class="nav">
        <div class="nav-menu">
          <div class="nav-title">经典策略</div>
          <div class="nav-content">
            <a id="R-breaker" @click='getStrategy("R_breaker"),getInvestvalue()'>R-breaker</a>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import * as d3 from 'd3'
  
  export default {
    name:'Classics',
    data(){
      return {
        asset:[],
        investvalue:[],
        TR:[],
        ATR_param:{
          k:10,
          N:20
        },
        DT_param:{
          k:5
        },
        ATR_bounds:[],
        Unit:[],
        width: 780,
        height: 330,
        margin:{
          top:40,
          right:20,
          bottom:10,
          left:55
        },
        r:10,
        c:20,
        startday:"",
        flag:0,
        timegap:100,
        pricegap:1
      }
    },
    mounted(){
      //this.Scale();
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
       trial(){
        this.flag+=1;
        console.log(this.flag);
       },
       getStrategy(strategy){
        const path = "http://127.0.0.1:5000/P0806.DCE/st=20230101ed=20230410freq=D/strategy="+strategy;
        axios
           .get(path)
           .then(res => {
             this.asset=res.data;
             console.log(this.asset);
             this.flag += 1;
           })
           .catch(error => {
             console.error(error);
           });
           console.log(this.asset);
       },
       getAsset(){
        const path = 'http://127.0.0.1:5000/Sample/A';
        axios
           .get(path)
           .then(res => {
             this.asset=res.data;
             console.log(this.asset);
             this.flag += 1;
             console.log(this.flag);
           })
           .catch(error => {
             console.error(error);
           });

       },
       getATR(){
        let i = 0;
        while(i < this.asset.length){
          this.TR.push(Math.max(this.asset[i]['high']-this.asset[i]['low'],Math.abs(this.asset[i]['high']-this.asset[i]['PDC']),Math.abs(this.asset[i]['PDC']-this.asset[i]['low'])));
          i = i + 1;
        }
        console.log(this.TR)
        i = 0;
        while(i < this.asset.length){
          if(i>=this.ATR_param.k){
            if(i >= this.ATR_param.N - 1){
              let s = {};
              s['Up'] = d3.max(this.asset.slice(i-this.ATR_param.k,i),function(d){return d['high']});
              s['Down'] = d3.min(this.asset.slice(i-this.ATR_param.k,i),function(d){return d['low']});
              s['ATR'] = d3.mean(this.TR.slice(i-this.ATR_param.N+1,i+1));
              this.ATR_bounds.push(s);
            }
            else{
              let s = {};
              s['Up'] = d3.max(this.asset.slice(i-this.ATR_param.k,i),function(d){return d['high']});
              s['Down'] = d3.min(this.asset.slice(i-this.ATR_param.k,i),function(d){return d['low']});
              s['ATR'] = 0;
              this.ATR_bounds.push(s);
            }
          }else{
            if(i >= this.ATR_param.N - 1){
              let s = {};
              s['Up'] = 0;
              s['Down'] = 0;
              s['ATR'] = d3.mean(this.asset.slice(i-this.ATR_param.N+1,i+1));
              this.ATR_bounds.push(s);
            }
            else{
              let s = {};
              s['Up'] = 0;
              s['Down'] = 0;
              s['ATR'] = 0;
              this.ATR_bounds.push(s);
            }
          }
          i = i + 1;
        }
        console.log(this.ATR_bounds);
        i = 0;
        while(i<this.ATR_bounds.length){
          this.Unit.push(0);
          i = i + 1;
        }
        i = 0;
        let prev_price = this.asset[0]['current'];
        while(i<this.ATR_bounds.length){
          if (i==0) {
            if (this.asset[i]['current']>this.ATR_bounds[i]['Up']) {
              prev_price = this.asset[i]['current'];
              this.Unit[i] += 1;
            }else{
              if (this.asset[i]['current']<this.ATR_bounds[i]['Down']){
                prev_price = this.asset[i]['current'];
                this.Unit[i] -= 1;
              }
            }
          }else{
            if(this.Unit[i-1]==0){
              if (this.asset[i]['current']>this.ATR_bounds[i]['Up']) {
                prev_price = this.asset[i]['current'];
                this.Unit[i]=this.Unit[i-1]+1;
              }else{
                if (this.asset[i]['current']<this.ATR_bounds[i]['Down']) {
                  prev_price = this.asset[i]['current'];
                  this.Unit[i] =  this.Unit[i-1]-1;
                }
              }
            }
            if (this.Unit[i-1]>0) {
              if (this.asset[i]['current']>prev_price+0.5*this.ATR_bounds[i]['ATR']){
                this.Unit[i] = this.Unit[i-1]+1;
                prev_price = this.asset[i]['current'];
              }else{
                if(this.asset[i]['current']<prev_price-2*this.ATR_bounds[i]['ATR']){
                  this.Unit[i] = 0;
                }else{
                  if(this.asset[i]['current']<this.ATR_bounds[i]['Down']){
                  this.Unit[i] = 0;
                }
              }
            }
          }
          if (this.Unit[i-1]<0) {
              if (this.asset[i]['current'] < prev_price - 0.5*this.ATR_bounds[i]['ATR']){
                this.Unit[i] = this.Unit[i-1]-1;
                prev_price = this.asset[i]['current'];
              }else{
                if(this.asset[i]['current'] > prev_price + 2*this.ATR_bounds[i]['ATR']){
                  this.Unit[i] = 0;
                }else{
                  if(this.asset[i]['current']>this.ATR_bounds[i]['Up']){
                  this.Unit[i] = 0;
                }
              }
            }
          }
        }
        i = i+1;
      }
      console.log(this.Unit);

      i = 0;
      while(i<this.asset.length){
        if(i==0)
          this.investvalue.push(this.asset[i]['current']*this.Unit[i]);
        else
          this.investvalue.push(this.investvalue[i-1]+this.asset[i]['current']*this.Unit[i]);
        i = i + 1;
      }
      console.log(this.investvalue);
      },

      getInvestvalue(){
        console.log("getinvest");
        let i=0;
        while(i<this.asset.length){
        if(i==0)
          this.investvalue.push(this.asset[i]['total_lot']*100);
        else
          this.investvalue.push(this.investvalue[i-1]+this.asset[i]['total_lot']*100);
        i = i + 1;
        }
        console.log(this.investvalue);
      },

      //Scale函数用来画出坐标轴
       Scale(){
        d3.select('#classicscale').remove()
        const g = d3.select('#Classics').append('g').attr('id', 'classicscale')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
        var [a,b] = d3.extent(this.investvalue);
        let that = this;
        const xscale = d3.scaleLinear()
                         .domain([0,that.investvalue.length])
                         .range([0, this.innerWidth]);
        const yscale = d3.scaleLinear()
                         .domain([b,a])
                         .range([0, this.innerHeight]);
        console.log([a,b])
        const yaxis = d3.axisLeft(yscale)
                        .ticks(10)
                        .tickSize(5)
                        .tickPadding(5);
        const xaxis = d3.axisBottom(xscale)
                        .ticks(20)
                        .tickSize(-5)
                        .tickPadding(-15)
                        //.tickFormat(function(d,i){
                        //   return that.asset[i]["date"];//.slice(11,16);
                        //})
                       g.append('g').call(yaxis)
                        .attr('id' ,'yaxis');
                       g.append('g').call(xaxis)
                        .attr('id', 'xaxis');
  
    },
       //ATR strategy的函数实现
       Draw(){        
        d3.select('#classicCurve').remove()

        //选择id为'Classics'的svg，增添g并取id为classicCurve，移动画布使其与设置的margin对其
        const g2 = d3.select('#Classics').append('g').attr('id', 'classicCurve')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
        
        //防止代码中将this错认为当前数据，用that代替全局的this
        let that = this;

        //设置旗帜为ATR，表示按下了ATR按钮
        that.flag="ATR";
        
        //设置x轴、y轴的映射函数，将数据映射到x、y轴坐标上
        var [a,b] = d3.extent(this.investvalue);
        const xscale = d3.scaleLinear()
                         .domain([0,that.investvalue.length])
                         .range([0, this.innerWidth]);
        const yscale = d3.scaleLinear()
                         .domain([b,a])
                         .range([0, this.innerHeight]);

        //设置折线图的映射函数，会将数据映射为每个点的坐标/每条线段的路径值
        const line = d3.line()
                       .x(function(d,i){return xscale(i)})
                       .y(function(d){return yscale(d)})
                       .curve(d3.curveNatural)
      
        //在g上增添路径path，并将目标画线的数据传入line映射函数中
        g2.append('path')
          .attr('d',line(that.investvalue))
          .attr('fill','none')
          .attr('stroke',"#3366ff")
          //.attr("transform", function(d) {
          //  return `translate(${xscale(d['id'])+1.5},${yscale(d['price'])-5})`;
          //})
          //.on("mouseover",function(){
          //   let d =d3.select(this).data();
          //   console.log(d);
          //   var str = 'value:' + d[0];
          //   var t = 60 + yscale(d[0])
            
          //   d3.selectAll('.tooltip')
          //     .html(str)
          //     .style("left", (xscale(d[0]['id'])+35)+"px")
          //     .style("top", (t+270)+"px")
          //     .style("opacity",1.0);
          //})
          //.on("mouseleave",function(){
          //   d3.selectAll('.tooltip')
          //     .style("opacity",0.0);
          //})
       },

       //Dual Thrust strategy的函数实现
       DT(){
        d3.select('#classicCurve').remove()
        console.log("Dual Thrust")
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
      //this.getAsset();
    },
    beforeUnmount() {
    },
    watch:{
      asset(){
        console.log("getasset");
        this.getInvestvalue();
        this.Scale();
        this.Draw();
    }
  }
  };
  </script>
  
  <style scoped>
  #ATR {
    appearance: none;
    background-color: #39c561;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 5px;
    box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 10px;
    font-weight: 1200;
    line-height: 10px;
    padding: 5px 5px;
    position: absolute;
    top:340px;
    left:680px;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap;
}
#DT{
    appearance: none;
    background-color: #39c561;
    border: 1px solid rgba(27, 31, 35, .15);
    border-radius: 5px;
    box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 10px;
    font-weight: 1200;
    line-height: 10px;
    padding: 5px 5px;
    position: absolute;
    top:340px;
    left:720px;
    text-align: center;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: middle;
    white-space: nowrap;
}
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
    top: 55px;
    left:170px;
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
    top: 55px;
    left:230px;
    border-top: 22px solid #455a64;
    border-right: 22px solid #ffffff;
    border-bottom: 0px solid #ffffff;
    z-index:98;
  }
  .content-left{
    width:12%;
    height:600px;
    background-color: #1c232f;
    float:left;
  }
  .left-title{
    height:50px;
    width:10px;
  }
  .left-title>a{
    display: block;
    width:100%;
    height:50px;
    line-height: 50px;
    text-align:center;
    color:white;
    text-decoration: none;
  }
  .seg{
    height:1px;
    width:100%;
    background-color: black;
  }
  .nav{
    margin-top:5px;
  }
  .nav-title{
    height:40px;
    width:100%;
    color:white;
    text-align:center;
    line-height:40px;
    cursor:pointer;
  }
  .nav-content{
    width:100%;
    height:100%;
    background-color: #0c1119;
  }
  .nav-content>a{
    display:block;
    height:30px;
    width:100%;
    color:#CCCCCC;
    text-decoration: none;
    text-align:center;
    line-height:30px;
  }
  .nav-content>a:hover{
    display:block;
    height:30px;
    width:100%;
    color:#ffffff;
    text-decoration: none;
    text-align:center;
    line-height:30px;
    background-color: #12040c;
  }
  .custom-strategy{
    position:absolute;
    top:500px;
  }
  .file{
    left:200px;
  }
  .upload{
    left:400px;
  }
  </style>
  