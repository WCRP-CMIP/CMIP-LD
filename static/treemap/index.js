const width = 928;
const height = 1060;

// Load JSON data and render the chart
fetch("https://wcrp-cmip.github.io/LD-Collection/universe_contents/universe_hierarchy.json")
  .then((response) => response.json())
  .then((data) => {
    const colors = d3.schemeCategory10.map((color) =>
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

    const shadow = svg.append("filter").attr("id", "shadow");
    shadow
      .append("feDropShadow")
      .attr("flood-opacity", 0.3)
      .attr("dx", 0)
      .attr("stdDeviation", 3);

    const node = svg
      .selectAll("g")
      .data(root.descendants())
      .join("g")
      .attr("transform", (d) => `translate(${d.x0},${d.y0})`);

    const format = d3.format(",d");

    node
      .append("title")
      .text(
        (d) =>
          `${d
            .ancestors()
            .reverse()
            .map((d) => d.data.name)
            .join("/")}\n${format(d.value)}`
      );

    node
      .append("rect")
      .attr("fill", (d) =>
        d.depth > 0 ? colorMap[d.data.prefix](d.height) : "white"
      )
      .attr("width", (d) => d.x1 - d.x0)
      .attr("height", (d) => d.y1 - d.y0);

    node
      .append("text")
      .attr("clip-path", (d) => `url(#clip-${d.data.name})`)
      .selectAll("tspan")
      .data((d) => d.data.name.split(/(?=[A-Z][^A-Z])/g).concat(format(d.value)))
      .join("tspan")
      .attr("fill-opacity", (d, i, nodes) =>
        i === nodes.length - 1 ? 0.7 : null
      )
      .text((d) => d);

    document.body.appendChild(svg.node());
  })
  .catch((error) => console.error("Error loading JSON data:", error));
