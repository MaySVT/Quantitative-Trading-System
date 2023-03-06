<template>
    <div id = "Tip">
      <div class="panel-header">Asset</div>
      <div class="panel-header-end"></div>
      <svg id = "Asset"  class="asset" style = 'width:810px; height:370px'>
      </svg>
      <div class="tooltip"></div>
      <div class="tooltip2"></div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  //import moment from 'moment'
  import * as d3 from 'd3'
  
  export default {
    name:'Asset',
    data(){
      return {
        invest:[],
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
      invests(){
        console.log(this.invest)
        return this.invest;
      },
      innerWidth(){
        return this.width - this.margin.left - this.margin.right
      },
      innerHeight(){
        return this.height - this.margin.top - this.margin.bottom
      }
    },
    methods:{
       getInvestment(){
        const path = 'http://127.0.0.1:5000/Investment/';
        axios
           .get(path)
           .then(res => {
             console.log(res.data);
             this.invest=res.data;

           })
           .catch(error => {
             console.error(error);
           });
       },
       getValue(){
        let that = this;
        this.orders = Array.from(d3.group(that.invest, d=>d.time, d=>d.asset),([key, value])=>({key,value}));
        for (let i=0; i <this.orders.length;i++){
            this.orders[i]['value'] = Array.from(this.orders[i]['value'],([key,value])=>({key,value}));
            for(let j = 0; j < this.orders[i]['value'].length; j++){
                this.orders[i]['value'][j]['filled_value']= d3.sum(this.orders[i]['value'][j]['value'],d=>d['filled_value']);
            }
        }
        
        console.log(this.orders)
       },
       Scale(){
        //const gap = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        const g = d3.select('#Asset').append('g').attr('id', 'assetscale')
                    .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
        const b = 30000;
        const a = -30000;
        //var b = d3.max(this.orders, function(m){return d3.max(m['value'],d=>d['filled_value']);});
        //var a = d3.min(this.orders, function(m){return d3.min(m['value'],d=>d['filled_value']);});
        // var [a,b] = d3.extent(this.market, function(d){return d3.extent(d['bid5_price'],d['ask5_price']);})
        let that = this;
        const xscale = d3.scaleLinear()
                         .domain([0,that.orders.length])
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
                        // .tickFormat(function(d,i){
                        //   return (i>0)?(that.market[i-1]['date']):""
                        // })
                       g.append('g').call(yaxis)
                        .attr('id' ,'yaxis');
                       g.append('g').call(xaxis)
                        .attr('id', 'xaxis');
  
    },
  
    Value(){
      let that = this;
      //const b = d3.max(this.orders_aggregated, function(m){return d3.max(m['value'],d=>d['filled_value']);});
      //const a = d3.min(this.orders, function(m){return d3.min(m['value'],d=>d['filled_value']);});
      const b = 30000;
      const a = -30000;
      const xscale = d3.scaleLinear()
                         .domain([0,that.orders.length])
                         .range([0, this.innerWidth]);
      const yscale = d3.scaleLinear()
                         .domain([b,a])
                         .range([0, this.innerHeight]);
      const g = d3.select('#Asset').append('g').attr('id', 'assetview1')
                  .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      const stackGen = d3.stack()
                      .keys(['BINANCE_SWAP_BNB-BUSD','BINANCE_SWAP_BNB-USDT','BINANCE_SWAP_FTT-BUSD','BINANCE_SWAP_FTT-USDT','BINANCE_SWAP_BTC-BUSD','BINANCE_SWAP_BTC-USDT'])
                      .order(d3.stackOrderNone)
                      .offset(d3.stackOffsetNone);

     
      for(let i= 0 ; i < this.orders.length; i++){
        var tmp = {}
        if(i>0){
          tmp['BINANCE_SWAP_BNB-BUSD'] = this.orders_aggregated[i-1]['BINANCE_SWAP_BNB-BUSD'];
          tmp['BINANCE_SWAP_BNB-USDT'] = this.orders_aggregated[i-1]['BINANCE_SWAP_BNB-USDT'];
          tmp['BINANCE_SWAP_FTT-BUSD'] = this.orders_aggregated[i-1]['BINANCE_SWAP_FTT-BUSD'];
          tmp['BINANCE_SWAP_FTT-USDT'] = this.orders_aggregated[i-1]['BINANCE_SWAP_FTT-USDT'];
          tmp['BINANCE_SWAP_BTC-BUSD'] = this.orders_aggregated[i-1]['BINANCE_SWAP_BTC-BUSD'];
          tmp['BINANCE_SWAP_BTC-USDT'] = this.orders_aggregated[i-1]['BINANCE_SWAP_BTC-USDT'];
        }else{
          tmp['BINANCE_SWAP_BNB-BUSD'] = 0;
          tmp['BINANCE_SWAP_BNB-USDT'] = 0;
          tmp['BINANCE_SWAP_FTT-BUSD'] = 0;
          tmp['BINANCE_SWAP_FTT-USDT'] = 0;
          tmp['BINANCE_SWAP_BTC-BUSD'] = 0;
          tmp['BINANCE_SWAP_BTC-USDT'] = 0;
        }
        
        tmp['date'] = this.orders[i]['key'];
        for(let j = 0; j < this.orders[i]['value'].length;j++){
          var str = this.orders[i]['value'][j]['key'];
          if(i>0){
            tmp[str] = this.orders_aggregated[i-1][str]+this.orders[i]['value'][j]['filled_value'];
          }else{
            tmp[str] = this.orders[i]['value'][j]['filled_value'];
          }
        }
        this.orders_aggregated.push(tmp);
    //   var chart = d3.stack()
    //               .keys(that.orders[i]['value'].keys)
    //               .order(d3.stackOrderAscending)
    //               .offset(d3.stackOffsetNone)
        //console.log(that.orders[i]['value'].keys)
      }
      console.log(that.orders_aggregated);
      var stackedseries = stackGen(that.orders_aggregated);
    
      console.log(stackedseries);

      var colorScale = d3.scaleOrdinal()
        .domain(['BINANCE_SWAP_BNB-BUSD','BINANCE_SWAP_BNB-USDT','BINANCE_SWAP_FTT-BUSD','BINANCE_SWAP_FTT-USDT','BINANCE_SWAP_BTC-BUSD','BINANCE_SWAP_BTC-USDT'])
        .range(["red", "yellow", "orange","blue","purple","green"]);

      // var areaGen = d3.area()
      //   .x((d,i) => xscale(i))
      //   .y0((d) => yscale(d[0]))
      //   .y1((d) => yscale(d[1]))
      
  //       g.selectAll(".areas")
  // .data(stackedseries)
  // .join("path")
  // .attr("d", areaGen)
  // .attr("fill", (d) => colorScale(d.key));


  // var groups = g.selectAll("g.bars")
  //     .data(stackedseries)
  //     .enter().append("g")
  //     .attr("class", "bars")
  //     .style("fill", function(d) { return colorScale(d.key);})
  //     .style("stroke", "#000");
    console.log(stackedseries[0][0][0])

    for(let k=0;k<stackedseries.length;k++){
      g.selectAll('.bar'+ k)
       .data(stackedseries[k]).enter()
       .append("rect")
       .attr('class', 'bar'+k)
       .attr("x", function(d,i) { return xscale(i+0.5); })
       .attr("y", function(d) { return yscale(d[0]>d[1]?d[0]:d[1]); })
       .attr("height", function(d) { return Math.abs(yscale(d[0])-yscale(d[1])); })
      .attr("width", this.innerWidth/this.orders.length/2)
      .attr("fill", function() { return colorScale(stackedseries[k].key);})
      .attr("stroke", "#000");
    }
    // attr("y", function(d) { return yScale(d.y0 + d.y); })
    //   .attr("height", function(d) { return yScale(d.y0) - yScale(d.y0 + d.y); })
    // g.selectAll("rect")
    //   .data(stackedseries)
    //   .enter()
    //   .append("rect")
    //   .attr("x", function(d,i) { return xscale(i); })
    //   .attr("y", function(d) { return yscale(d[0] + d[1]); })
    //   .attr("height", function(d) { return (yscale(d[0]) - yscale(d[0] + d[1])); })
    //   .attr("width", this.innerWidth/this.orders.length)
    //   .attr("fill", function(d) { return colorScale(d.key);})
    //   .attr("stroke", "#000");

      // g.selectAll("rect")
      //  .data(that.market).enter()
      //  .append("rect")
      //  .attr('width',that.innerWidth/that.c-20)
      //  .attr('height',function(d){
      //   return Math.abs(yscale(d['open'])-yscale(d['close']));
      //  })
      //  .attr("x",function(d,i){return xscale(i+1)-that.innerWidth/2/that.c+10;})
      //  .attr("y",function(d){return yscale(d['open']>d['close']?d['open']:d['close']);})
      //  .attr("fill",function(d){return d['open']<d['close']?"green":"red";})
  
      //  d3.select('#Candlestick').append('g').attr('id','marketview2')
      //    .attr('transform', `translate(${this.margin.left},${this.margin.top})`)  
      //    .selectAll("rect")
      //    .data(that.market).enter()
      //    .append("rect")
      //    .attr('width',5)
      //    .attr('height',function(d){
      //     return yscale(d['low'])-yscale(d['close']);
      //    })
      //    .attr("x",function(d,i){return xscale(i+1)-2.5;})
      //    .attr("y",function(d){return yscale(d['close']);})
      //    .attr("fill",function(d){return d['open']<d['close']?"green":"red";})
  
         
      //  d3.select('#Candlestick').append('g').attr('id','marketview3')
      //    .attr('transform', `translate(${this.margin.left},${this.margin.top})`)
      //    .selectAll("rect")
      //    .data(that.market).enter()
      //    .append("rect")
      //    .attr('width',5)
      //    .attr('height',function(d){
      //     return yscale(d['open'])-yscale(d['high']);
      //    })
      //    .attr("x",function(d,i){return xscale(i+1)-2.5;})
      //    .attr("y",function(d){return yscale(d['high']);})
      //    .attr("fill",function(d){return d['open']<d['close']?"green":"red";})
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
      this.getInvestment();
    },
    beforeUnmount() {
    },
    watch:{
      invests(){
        this.getValue();
        this.Scale();
        this.Value();
        // d3.selectAll('#marketview').remove();
        // this.Scale();
        // this.Candle();
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
    top: 345px;
    left:810px;
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
    top: 345px;
    left:870px;
    border-top: 18px solid #455a64;
    border-right: 18px solid #ffffff;
    border-bottom: 0px solid #ffffff;
    z-index:98;
  }
  </style>
  