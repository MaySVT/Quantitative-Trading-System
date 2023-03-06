/**
@author https://observablehq.com/@bmschmidt
*/

import * as d3 from "d3"

let drawScatter = function (svg, data) {
  let width = Math.ceil(parseFloat(svg.attr('width')))
  let height = Math.ceil(parseFloat(svg.attr('height')))
  let quadtree = d3
    .quadtree()
    .extent([[-1, -1], [width + 1, height + 1]])
    .addAll(data)
  svg
    .selectAll(".node")
    .data(nodes(quadtree))
    .enter()
    .append("rect")
    .attr("class", "node")
    .attr("x", d => d.x0)
    .attr("y", d => d.y0)
    .attr("width", d => d.y1 - d.y0)
    .attr("height", d => d.x1 - d.x0)

  let point = svg
    .selectAll(".point")
    .data(data)
    .enter()
    .append("circle")
    .attr("class", "point")
    .attr("cx", d => d[0])
    .attr("cy", d => d[1])
    .attr("r", 2)

    return { point, quadtree }
}

// Find the nodes within the specified rectangle.
let search = function (quadtree, x0, y0, x3, y3) {
    quadtree.visit(function(node, x1, y1, x2, y2) {
      // If a node is entirely within the bounding box, we can safely
      // set all of its children as found and give up on this path.
      if (x1 > x0 && x2 < x3 && y1 > y0 && y2 < y3) {
        flush_node(node, d => d.data.grandfathered = true)
        return true 
      }
      
      if (!node.length) {
        do {
          const { data: d } = node,
            x = +quadtree._x.call(null, d),
            y = +quadtree._y.call(null, d);
          d.scanned = true;
          d.selected = x >= x0 && x < x3 && y >= y0 && y < y3;
        } while ((node = node.next));
      }
      return (x1 >= x3 || y1 >= y3 || x2 < x0 || y2 < y0);
    });
  }

  // Collapse the quadtree into an array of rectangles.
let nodes = function (quadtree) {
    const nodes = [];
    quadtree.visit((node, x0, y0, x1, y1) => {
      nodes.push({ x0, y0, x1, y1 });
    });
    return nodes;
}

function flush_node(node, callback) {
    if (!node.length) {
      do {
        callback(node) 
      // eslint-disable-next-line no-cond-assign
      } while (node = node.next)
    } else {
      node.map(n => flush_node(n, callback))
    }
  }

export {
      drawScatter,
      search
}