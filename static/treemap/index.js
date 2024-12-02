const width = 600;
const height = 400;

const tetrad = [
  "#5215fc",  // Original Violet
  "#fc154b",  // Original Red
  "#bffc15",  // Original Lime Green
  "#15fca1",  // Teal
  "#15bffc",  // Cyan
  "#fc8915",  // Orange
  "#fc15e0",  // Magenta
  "#15fc42",  // Bright Green
  "#8a15fc",  // Purple
  "#fc1515",  // Bright Red
  "#15fcfc",  // Aqua
  "#fcf315",  // Yellow
  "#a115fc",  // Deep Violet
  "#fc7015",  // Deep Orange
  "#5ffc15",  // Yellow-Green
  "#15fc9a",  // Mint Green
  "#15a1fc",  // Sky Blue
  "#e015fc",  // Bright Pink
  "#fc4567",  // Coral
  "#6a15fc",  // Indigo
]

// Load JSON data and render the chart
fetch("https://wcrp-cmip.github.io/LD-Collection/universe_contents/universe_hierarchy.json")
  .then((response) => response.json())
  .then((data) => {
    const colors = tetrad.map((color) =>
      d3.scaleSequential([5, 0], (t) => d3.interpolateRgb(color, "white")(t))
    );

    const colorMap = {};
    data.children.forEach((d, i) => (colorMap[d.prefix] = colors[i]));

    const treemap = (data) =>
      d3
        .treemap()
        .size([width, height])
        .paddingOuter(3)
        .paddingTop(19)
        .paddingInner(1)
        .round(true)(
          d3
            .hierarchy(data)
            .sum((d) => d.size)
            .sort((a, b) => b.size - a.size)
        );

    const root = treemap(data);

    const svg = d3
      .create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr(
        "style",
        "max-width: 100%; height: auto; overflow: visible; font: 10px sans-serif;"
      );

    svg
      .append("filter")
      .attr("id", shadow.id)
      .append("feDropShadow")
      .attr("flood-opacity", 0.3)
      .attr("dx", 0)
      .attr("stdDeviation", 3);

    const node = svg
      .selectAll("g")
      .data(d3.group(root, (d) => d.height))
      .join("g")
      .attr("filter", shadow)
      .selectAll("g")
      .data((d) => d[1])
      .join("g")
      .attr("transform", (d) => `translate(${d.x0},${d.y0})`);

    const format = d3.format(",d");
    node.append("title").text(
      (d) =>
        `${d
          .ancestors()
          .reverse()
          .map((d) => d.data.name)
          .join("/")}\n${format(d.value)}`
    );

    node
      .append("rect")
      .attr("id", (d) => (d.nodeUid = DOM.uid("node")).id)
      .attr("fill", (d) =>
        d.depth > 0 ? color[d.data.prefix](d.height) : "white"
      )
      .attr("width", (d) => d.x1 - d.x0)
      .attr("height", (d) => d.y1 - d.y0);

    node
      .append("clipPath")
      .attr("id", (d) => (d.clipUid = DOM.uid("clip")).id)
      .append("use")
      .attr("xlink:href", (d) => d.nodeUid.href);

    node
      .append("text")
      .attr("clip-path", (d) => d.clipUid)
      .selectAll("tspan")
      .data((d) => d.data.name.split(/(?=[A-Z][^A-Z])/g).concat(format(d.value)))
      .join("tspan")
      .attr("fill-opacity", (d, i, nodes) =>
        i === nodes.length - 1 ? 0.7 : null
      )
      .text((d) => d);

    node
      .filter((d) => d.children)
      .selectAll("tspan")
      .attr("dx", 3)
      .attr("y", 13);

    node
      .filter((d) => !d.children)
      .selectAll("tspan")
      .attr("x", 3)
      .attr(
        "y",
        (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`
      );

    document.body.appendChild(svg.node());
  })
  .catch((error) => console.error("Error loading JSON data:", error));

