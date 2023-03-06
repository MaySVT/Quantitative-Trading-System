import * as d3 from 'd3'
const xMargin = 0.1
const yMargin = 0.1

let drawHist = function (svg, data, identifier='') {
    let width = svg.attr('width')
    let height = svg.attr('height')
    svg.selectAll('g').remove()

    let bins = d3.bin().thresholds(50)(data)
    let x = d3.scaleLinear()
    .domain([bins[0].x0, bins[bins.length - 1].x1])
    .range([width * xMargin, width])

    let y =  d3.scaleLinear()
    .domain([0, d3.max(bins, d => d.length)]).nice()
    .range([height - height*yMargin, height * yMargin])

    let yAxis = g => g
    .attr('transform', `translate(${width * xMargin},0)`)
    .call(d3.axisLeft(y).ticks(height / 40))
    .call(g => g.select('.domain').remove())
    .call(g => g.select('.tick:last-of-type text').clone()
        .attr('x', 4)
        .attr('text-anchor', 'start')
        .attr('font-weight', 'bold')
        .text(data.y))
    .call(g => g.selectAll('.tick line')
        .attr('x2', width - width * xMargin)
        .style('stroke-width', 0.5)
        .style('opacity', 0.5)
        )

    let xAxis = g => g
    .attr('transform', `translate(0,${height - height * yMargin})`)
    .call(d3.axisBottom(x).ticks(width / 80 ).tickSizeOuter(0))
    .call(g => g.append('text')
        .attr('x', width - width * xMargin)
        .attr('y', -4)
        .attr('fill', 'currentColor')
        .attr('font-weight', 'bold')
        .attr('text-anchor', 'end')
        .text(data.x))

    svg.append('g')
    .call(xAxis);

    svg.append('g')
    .call(yAxis);

    
    svg.append('g')
    .selectAll('rect')
    .data(bins)
    .join('rect')
    .attr('x', d => x(d.x0) + 1)
    .attr('width', d => Math.max(0, x(d.x1) - x(d.x0) - 1))
    .attr('y', d => y(d.length))
    .attr('height', d => y(0) - y(d.length))
    .style('fill', 'steelblue')

    svg.append('g')
      .attr('transform', `translate(${width/2}, 16)`)
      .append('text')
      .text(`Distribution of ${identifier}`)
      .style('text-anchor', 'middle')
      .style('font-size', 10)

    return svg.node();
}



export  { drawHist }