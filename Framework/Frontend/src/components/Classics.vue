<template>
    <div id = "Tip">
      <div class="panel-header">Asset</div>
      <div class="panel-header-end"></div>
      <svg id = "Classics"  class="classic" style = 'width:810px; height:370px'>
      </svg>
      <div class="tooltip"></div>
      <div class="tooltip2"></div>
      <button id = 'ATR' @click = 'ATR()'>ATR</button>
      <button id = 'DT' @click = 'DT()'>Dual Thrust</button>
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
        width: 780,
        height: 330,
        margin:{
          top:40,
          right:20,
          bottom:10,
          left:45
        },
        r:10,
        c:20,
        startday:"",
        flag:"",
        orders:[],
        timegap:100,
        pricegap:1,
        timelist:[],
        pricelist:[],
        orders_aggregated:[]
      };
    },
    mounted(){
      this.Scale();
    },
    computed:{
      assets(){
        console.log(this.asset[0])
        return this.asset;
      },
      innerWidth(){
        return this.width - this.margin.left - this.margin.right
      },
      innerHeight(){
        return this.height - this.margin.top - this.margin.bottom
      }
    },
    methods:{
       getAsset(){
        const path = 'http://127.0.0.1:5000/Sample/A';
        axios
           .get(path)
           .then(res => {
             console.log(res.data);
             this.asset=res.data;
           })
           .catch(error => {
             console.error(error);
           });
       },
       Scale(){
        //const gap = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        const g = d3.select('#Classics').append('g').attr('id', 'classicscale')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
        var [a,b] = d3.extent(this.investvalue)
        let that = this;
        const xscale = d3.scaleLinear()
                         .domain([0,that.asset.length])
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
                        .tickFormat(function(d){
                           return that.asset[d]["hour"].slice(11,16);
                        })
                       g.append('g').call(yaxis)
                        .attr('id' ,'yaxis');
                       g.append('g').call(xaxis)
                        .attr('id', 'xaxis');
  
    },
       //ATR strategy的函数实现
       ATR(){
        console.log("ATR")
       },

       //Dual Thrust strategy的函数实现
       DT(){
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
      this.getAsset();
    },
    beforeUnmount() {
    },
    watch:{
      assets(){
        this.ATR();
        this.Scale();
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
    top: 5px;
    left:10px;
    padding: -10px 20px;
    width: 60px;
    height: 18px;
    line-height: 18px;
    font-size: 8px;
    text-align: center;
    background: #415c68;
    color: #fcfcfc;
    display: flex;
    font-weight: bold;
    border-radius: 1px;
    box-shadow: 0 1px 2px rgba(26 26 26 0.2);
    z-index:99;
  
  }
  
  .panel-header-end {
    position: absolute;
    top: 5px;
    left:70px;
    border-top: 18px solid #455a64;
    border-right: 18px solid #ffffff;
    border-bottom: 0px solid #ffffff;
    z-index:98;
  }
  </style>
  