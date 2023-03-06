import * as d3 from 'd3'
var margin = {top: 0, right: 20, bottom: 60, left: 60}


let preprocessData = function(rows) {
  var data = [];
  rows.forEach(function(d) {
    var x = d[""];
    delete d[""];
    for (let prop in d) {
      var y = prop,
        value = d[prop];
      data.push({
        x: x,
        y: y,
        value: +value
      });
    }
  })
  return data
}

let autoFix = function() {
  let div = d3.select('#heatmap')
  let bbox = div.node().getBoundingClientRect()
  let width = Math.ceil(bbox.width)
  let height = Math.ceil(bbox.height)
  let svg = div.html('')
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    // .attr('viewBox', `${0} ${0} ${width+ margin.left + margin.right} ${height+ margin.top + margin.bottom}`)
  return {
    svg,
    width: width - margin.left - margin.right,
    height: height - margin.top - margin.bottom
  }

}
let drawMatrix = function(rawdata) {
  let data  = preprocessData(rawdata)
  let { svg, width, height } = autoFix()
  const domain = Array.from(new Set(data.map(function(d) {
    return d.x
}))),

num = Math.sqrt(data.length),

color = d3.scaleLinear()
.domain([-1, 0, 1])
.range(["#B22222", "#fff", "#000080"]);


let xSpace = width / domain.length
let ySpace = height / domain.length


const x = d3.scalePoint()
.range([xSpace/2, width-xSpace/2])
.domain(domain)

const y = d3.scalePoint()
.range([ySpace/2, height-ySpace/2])
.domain(domain)

var ytext = svg.selectAll(".ytext")
.data(domain)
.enter()
.append("g")
.attr("class", "ytext")

ytext.append("text")
.attr("x", -5)
.attr("y", d => y(d))
.attr("text-anchor", "end")
.attr("fill", "#000080")
.text(function(d){
    return d
})
.style("font-size", 10)

var xtext = svg.selectAll(".xtext")
.data(domain)
.enter()
.append("g")
.attr("class", "xtext")
.attr("transform", function(d){ 
    return "translate(" + x(d) + "," + `${height +5}`+ ")"; 
});
xtext.append("text")
.attr("x", 0)
.attr("y", 0)
.attr("text-anchor", "end")
.attr("transform", "rotate(-90)")
.attr("fill", "#000080")
.text(function(d){
    return d
})
.style("font-size", 10)

var cor = svg.selectAll(".cor")
.data(data)
.enter()
.append("g")
.attr("class", "cor")
.attr("transform", function(d) {
    return "translate(" + x(d.x) + "," + y(d.y) + ")";
});

cor.append("rect")
.attr("width", xSpace)
.attr("height", ySpace)
.attr("x", -xSpace / 2)
.attr("y", -ySpace / 2)  
//         function mouseover(p) {
//     console.log(p)
//     console.log(ytext)
//     d3.selectAll(".ytext text").classed("active", function(d) {return d == p.y;});
//     d3.selectAll(".xtext text").classed("active", function(d) {return d == p.x;});
//     // d3.selectAll(".ytext").attr("fill", "red");
// }

// function mouseout() {
//     d3.selectAll("text").classed("active", false);
//     // d3.selectAll("text").attr("fill", "red");
// }

cor.filter(function(d){
    var ypos = domain.indexOf(d.y);
    var xpos = domain.indexOf(d.x);
    for (var i = (ypos + 1); i < num; i++){
        if (i === xpos) return false;
    }
    return true;
})
.append("text")
.attr("y", 5)
.text(function(d) {
    return d.value.toFixed(2);
})
.style("fill", function(d){
    return color(d.value);
})
.attr("opacity", 0.8)
.on("mouseover", function(p){
    console.log(p)
    d3.selectAll(".ytext text").attr("fill", function(d){if(d == p.y){return "#B22222"}else{return "#000080"}});
    d3.selectAll(".xtext text").attr("fill", function(d){if(d == p.x){return "#B22222"}else{return "#000080"}});
})
.on("mouseout", function(){
    d3.selectAll(".ytext text").attr("fill", "#000080");
    d3.selectAll(".xtext text").attr("fill", "#000080");
});

cor.filter(function(d){
    var ypos = domain.indexOf(d.y);
    var xpos = domain.indexOf(d.x);
    for (var i = (ypos + 1); i < num; i++){
        if (i === xpos) return true;
    }
    return false;
})
.append("circle")
.attr("r", function(d){
    return (Math.abs(d.value) * xSpace / 2);
})
.style("fill", function(d){
    return color(d.value);
})
.attr("opacity", 0.8)
.on("mouseover", function(p){
    d3.selectAll(".ytext text").attr("fill", function(d){if(d == p.y){return "#B22222"}else{return "#000080"}});
    d3.selectAll(".xtext text").attr("fill", function(d){if(d == p.x){return "#B22222"}else{return "#000080"}});
})
.on("mouseout", function(){
    d3.selectAll(".ytext text").attr("fill", "#000080");
    d3.selectAll(".xtext text").attr("fill", "#000080");
});

var aS = d3.scaleLinear()
.range([0, height])
.domain([1, -1]);


var aG = svg.append("g")
.attr("class", "y axis")
.attr("transform", "translate(" + (width + margin.right / 2) + " ,0)")

var iR = d3.range(-1, 1.01, 0.01);
var h = height / iR.length + 1;
iR.forEach(function(d){
aG.append('rect')
.style('fill',color(d))
.style('stroke-width', 0)
.style('stoke', 'none')
.attr('height', h)
.attr('width', margin.right * 0.8)
.attr('x', 0)
.attr('y', aS(d))
});
}

export  { drawMatrix }