<template>
    <div style="width: 100%;height:100%">
        <div id="guide" class="news-guide">
            <div class='slogan'
                style="no-repeat center;background-size: auto 380px;"
            >
                <div class="data-content">
                    <h2 class="data-banner-sdktitle">
                        本地量化数据开放使用
                    </h2>
                    <p class="data-banner-sdksubtitle">
                        <span class="sdksubtitle-text">支持本地调用，提供以期货为主的全品种量化数据</span>
                    </p>
                </div>
            </div>
        </div>
    <!-- banner结束 -->
    
     <!-- 数据字典开始 -->
        <div class="guide-box">
            <div class="data-dictionary">
                <div class="data-dictionary-title">
                    <div class="line left"></div>
                    <h3>数据字典</h3>
                    <div class="line right"></div>
                </div>
                <div class="data-dictionary-content mb_36">
                    <div class="data-dic">
                        <a href="http://127.0.0.1:5000">
                            <h4>期货数据</h4>
                            <p>涵盖中金所、上期所、郑商所和大商所的所有期货合约数据</p>
                        </a>
                    </div>
                    <div class="data-dic">
                        <a href="/help/api/help#name:Option">
                            <h4>期权数据</h4>
                            <p>提供股票期权和商品期权的合约资料和行情数据</p>
                        </a>
                    </div>
                    <div class="data-dic">
                        <a href="/help/api/help#name:plateData">
                            <h4>行业概念数据</h4>
                            <p>包含行业板块、概念板块数据</p>
                        </a>
                    </div>
                    <div class="data-dic">
                        <a href="/help/api/help#name:index">
                            <h4>指数数据</h4>
                            <p>包含沪深市场多只指数数据</p>
                        </a>
                    </div>
                    <div class="data-dic">
                        <a href="/help/api/help#name:macroData">
                            <h4>宏观经济数据</h4>
                            <p>包含国内的重要宏观经济数据</p>
                        </a>
                    </div>
                    <div class="data-dic">
                        <a href="/help/api/help#name:fund">
                            <h4>场内基金数据</h4>
                            <p>包含ETF、LOF、分级基金、货币基金完整的行情、净值数据</p>
                        </a>
                    </div>
                    <div class="data-dic">
                        <a href="/help/api/help#name:OTCfund">
                            <h4>场外基金数据</h4>
                            <p>提供场外基金单位净值、复权净值、投资组合等数据</p>
                        </a>
                    </div>                
                    <div class="data-dic">
                        <a href="/help/api/help#name:Public">
                            <h4>舆情数据</h4>
                            <p>包含CCTV等舆情数据</p>
                        </a>
                    </div>
                </div>
              </div>
          </div>
        </div>
    </template>
    
    <script>
    import axios from 'axios'
    //import moment from 'moment'
    import * as d3 from 'd3'
    
    export default {
      name:'DataAPI',
      data(){
        return {
          heatmap:[],
          trade:[],
          width: 800,
          height: 360,
          margin:{
            top:40,
            right:30,
            bottom:10,
            left:40
          },
          r:10,
          c:40,
          timegap:100,
          // pricegap:1,
          timelist:[],
          pricelist:[],
          heat_aggregated:[],
          start:"1645361597595"
        };
      },
      mounted(){
        this.Scale();
      },
      computed:{
        pricegap(){
          var [a,b] = d3.extent(this.heatmap, function(d){return d['price'];});
          return (b-a)/10;
        },
        showTip(){
          return this.flag;
        },
        heat(){
          console.log(this.heatmap)
          return this.heatmap;
        },
        innerWidth(){
          return this.width - this.margin.left - this.margin.right
        },
        innerHeight(){
          return this.height - this.margin.top - this.margin.bottom
        },
        trd(){
          return this.trade;
        },
        stt(){
          console.log(new Date(this.start).getTime());
          return new Date(this.start).getTime();
        },
        gap(){
          return this.timegap;
        }
      },
      methods:{
         getHeatmap(){
          //const path = 'http://127.0.0.1:5000/Heatmap1/'+ eval('1645361597595');
          const path = 'http://127.0.0.1:5000/Heatmap/?start='+ this.stt+'&year='+ eval('2022')+'&month='+eval('2')+'&day='+eval('20')+'&timegap='+this.timegap;
          axios
             .get(path)
             .then(res => {
               console.log(res.data);
               this.heatmap=res.data;
             })
             .catch(error => {
               console.error(error);
             });
         },
         
         getTimeList(){
          var [a,b] = d3.extent(this.heatmap, function(d){return d['time'];});
          var t = a;
          for(; t <= b; t += this.timegap){
            this.timelist.push(t);
          }
          this.timelist.push(t);
          //const d = new Date(this.timelist[0])
          console.log(this.timelist);
          console.log(this.timelist[2])
          console.log(new Date(this.timelist[6]));
         },
    
         getPriceList(){
          var [a,b] = d3.extent(this.heatmap, function(d){return d['price'];});
          var p = a;
          for(; p <= b; p += this.pricegap){
            this.pricelist.push(p);
          }
          this.pricelist.push(p);
         },
    
         getTrade(){
          const path = 'http://127.0.0.1:5000/Trade/?beg='+ eval(this.timelist[0])+'&end='+eval(this.timelist[this.timelist.length-1])+'&year='+ eval('2022')+'&month='+eval('2')+'&day='+eval('20');
          axios
             .get(path)
             .then(res => {
               console.log(res.data);
               this.trade=res.data;
             })
             .catch(error => {
               console.error(error);
             });
         },
    
        //  getHeatAggregated(){
        //   for(let i = 0; i < this.timelist.length; i++){
        //     for(let j = 0; j < this.pricelist.length; j++){
        //       var a = {};
        //       a['time'] = this.timelist[i];
        //       a['price'] = this.pricelist[j];
        //       a['vol'] = 0;
        //       this.heat_aggregated.push(a);
        //     }
        //   }
        //   for(let i = 0; i < this.heatmap.length; i++){
        //     this.heat_aggregated[Math.floor((this.heatmap[i]['time']-this.timelist[0])/this.timegap)*this.pricelist.length + Math.floor((this.heatmap[i]['price']-this.pricelist[0])/this.pricegap)]['vol'] += this.heatmap[i]['vol']
        //   }
        //  },
    
         Scale(){
          //const gap = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
          const g = d3.select('#Heatmap').append('g').attr('id', 'heatmapview')
                      .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
          //var [a,b] = d3.extent(this.heatmap, function(d){return d3.extent(d['bid5_price'],d['ask5_price']);})
          let that = this;
          const xscale = d3.scaleLinear()
                           .domain([0,this.timelist.length])
                           .range([0, this.innerWidth]);
          const yscale = d3.scaleLinear()
                           .domain([this.pricelist[this.pricelist.length-1],this.pricelist[0]])
                           .range([0, this.innerHeight]);
    
          const yaxis = d3.axisLeft(yscale)
                          .ticks(this.pricelist.length)
                          .tickSize(5)
                          .tickPadding(5);
          const xaxis = d3.axisBottom(xscale)
                          .ticks(this.timelist.length)
                          .tickSize(-5)
                          .tickPadding(-15)
                          .tickFormat(function(d,i){
                            let temp = i==0? new Date():new Date(that.timelist[i-1])
                          return i==0?'':(temp.getHours()>=10?temp.getHours():'0'+temp.getHours())+':'+(temp.getMinutes()>=10?temp.getMinutes():'0'+temp.getMinutes())+':'+(temp.getSeconds()>=10?temp.getSeconds():'0'+temp.getSeconds())+':'+Math.floor(temp.getMilliseconds()/100);});
                         g.append('g').call(yaxis)
                          .attr('id' ,'yaxis');
                         g.append('g').call(xaxis)
                          .attr('id', 'xaxis');
    
      },
    
      GHOST(){
        let that = this;
        that.flag="GHOST";
        d3.select('#heatmapview').selectAll('rect').remove()
        d3.select('#Heatmap').selectAll('#legend').remove()
        that.r = that.pricelist.length;
        that.c = that.timelist.length;
        console.log(that.c);
        var [bm,bM] = d3.extent(d3.filter(that.heatmap,x=>x['position'].indexOf('bid')>=0), function(d){return d['vol'];})
        var [am,aM] = d3.extent(d3.filter(that.heatmap,x=>x['position'].indexOf('ask')>=0), function(d){return d['vol'];})
          
        const xscale = d3.scaleLinear()
                         .domain([0,this.timelist.length])
                         .range([0, this.innerWidth]);
        const yscale = d3.scaleLinear()
                         .domain([this.pricelist[this.pricelist.length-1],this.pricelist[0]])
                         .range([0, this.innerHeight]);
    
    
        d3.select('#heatmapview')
          .selectAll('circle').data(this.heatmap).enter()
          .append('circle')
          .attr('fill', function(d){return d['position'].indexOf('ask')>=0? d3.interpolateReds((d['vol']-am)/(aM-am)) : d3.interpolateGreens((d['vol']-bm)/(bM-bm));})
          .attr('r', this.innerWidth/this.c/3-3)
          .attr('cx', function(d){return (xscale(d['id']+1))+"px";})
          .attr('cy', function(d){return (yscale(d['price'])+"px");})
          //.attr('height', this.innerHeight/this.r-10)
          //.attr('stroke','black')
          //.attr("transform", function(d) {
          //  return `translate(${xscale(d['id'])+1.5},${yscale(d['price'])-5})`;
          //})
          .on("mouseover",function(){
            let d =d3.select(this).data();
            var str = 'vol:' + d[0]['vol'] + '<br>price:'+ d[0]['price'] + '<br>position:' + d[0]['position'];
            var t = 60+ yscale(d[0]['price'])
            
            d3.selectAll('.tooltip')
              .html(str)
                   .style("left", (xscale(d[0]['id'])+35)+"px")
                   .style("top", (t+270)+"px")
                   .style("opacity",1.0);
        })
          .on("mouseleave",function(){
                d3.selectAll('.tooltip')
                  .style("opacity",0.0);
              })
    
        d3.select("#Heatmap")
          .append("g").attr("id","legend1")
          .call(that.colorbox,[10,120],d3.scaleDiverging([aM, am], function (t){return d3.interpolateReds(t);}))
          .attr("transform",`translate(${10+that.width - that.margin.right},${25})`)
        
        d3.select("#legend1")
           .append("g")
           .call(d3.axisRight(d3.scaleLinear().domain([am,aM]).range([120,0])).ticks(5))
           .attr("transform","translate(10,0)")
    
        d3.select("#legend1") 
          .append("text")
          .text("ask volume")
          .attr("transform","translate(-25,-8)")
          .attr("font-size","10px")
    
        d3.select("#Heatmap")
          .append("g").attr("id","legend2")
          .call(that.colorbox,[10,120],d3.scaleDiverging([bM, bm], function (t){return d3.interpolateGreens(t);}))
          .attr("transform",`translate(${10+that.width - that.margin.right},${165})`)
    
        d3.select("#legend2")
           .append("g")
           .call(d3.axisRight(d3.scaleLinear().domain([bm,bM]).range([120,0])).ticks(5))
           .attr("transform","translate(10,0)")
    
        d3.select("#legend1") 
          .append("text")
          .text("bid volume")
          .attr("transform","translate(-25,272)")
          .attr("font-size","10px")
    
        
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
          },
    
        Price(){
        let that = this;
        const xscale = d3.scaleLinear()
                         .domain([0,this.timelist.length])
                         .range([0, this.innerWidth]);
        const yscale = d3.scaleLinear()
                         .domain([this.pricelist[this.pricelist.length-1],this.pricelist[0]])
                         .range([0, this.innerHeight]);
    
        const a = that.timelist[0];
        const b = that.timelist[that.timelist.length-1];
    
        var pos = that.trade.map(d=>[(d['time']-a)/(b-a),d['price']])
        console.log(pos)
        var lnMkr = d3.line().curve(d3.curveLinear)
                      .x(d=>xscale((d['time']-a)/(b-a)*that.timelist.length))
                      .y(d=>yscale(d['price']));
        console.log(that.trade);
        console.log(lnMkr(that.trade));
          d3.select("#heatmapview")
            .append("g").attr('id','trade')
            .append("path")
            .attr("d", lnMkr(that.trade))
            .attr("fill","none")
            .attr("stroke","lightblue")
            .attr("stroke-width", 2.5)
    
          d3.select("#trade")
            .selectAll('rect')
            .data(that.trade).enter()
            .append('rect')
            .attr('fill', 'orange')
            .attr('width', 10)
            .attr('height', 10)
            .attr('transform',function(d){
              return `translate(${xscale((d['time']-a)/(b-a)*that.timelist.length)-5},${yscale(d['price'])-5})`;
            })
        }
      },
      created(){
        this.getHeatmap();
      },
      beforeUnmount() {
      },
      watch:{
        heat(){
          this.getTimeList();
          this.getPriceList();
          this.getTrade();
          this.Scale();
          this.GHOST();
        },
        trd(){
          this.Price();
        },
        stt(){
          d3.select('#heatmapview').remove()
          this.getHeatmap();
          console.log( Number(new Date(this.start)));
        },
        gap(){
          this.getHeatmap();
          console.log(this.timegap);
        }
      }
    };
    </script>
    
    <style scoped>
    .tooltip{
        position: absolute;
        padding-left:5px;
        padding-right:5px;
        left:0px;
        top:345px;
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
      top:345px;
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
      left:0px;
      top:345px;
      padding: -10px 20px;
      width: 65px;
      height: 18px;
      line-height: 18px;
      font-size: 8px;
      text-align: left;
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
      left:65px;
      border-top: 18px solid #455a64;
      border-right: 18px solid #ffffff;
      border-bottom: 0px solid #ffffff;
      z-index:98;
    }
    
    .time-input1{
      position: absolute;
      top: 720px;
      left:5px;
      width: 115px;
      height: 18px;
      border-top: 5px solid #455a64;
      border-bottom: 2px solid #455a64;
      z-index:98;
    }
    
    .time-input2{
      position: absolute;
      top: 720px;
      left:135px;
      width: 115px;
      height: 18px;
      border-top: 5px solid #455a64;
      border-bottom: 2px solid #455a64;
      z-index:98;
    }
    
    .time-button{
      position: absolute;
      top: 720px;
      left:305px;
      width: 115px;
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
      font-size: 20px;
      font-weight: 1200;
      line-height: 10px;
      padding: 5px 5px;
      text-align: center;
      text-decoration: none;
      user-select: none;
      -webkit-user-select: none;
      touch-action: manipulation;
      vertical-align: middle;
      white-space: nowrap;
    }
    
    /* input[type=text]{
      width:100%;
      padding: 12px 20px;
      margin:8px 0;
      box-sizing:border-box;
    } */
    </style>
    