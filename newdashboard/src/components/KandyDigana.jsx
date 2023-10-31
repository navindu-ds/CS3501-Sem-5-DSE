import React, { useRef, useEffect, useState } from "react";
import axios from "axios";
import * as d3 from "d3";
import busIcon from "../data/bus-20.png";
import "../pages/MainPage.css";

const KandyDigana = () => {
  const svgRef = useRef(null);
  let [locations, setLocations] = useState([]);

  // Initialize with 16 time strings
  let [timeObj, setTimeObj] = useState({
    101: " ",
    102: " ",
    103: " ",
    104: " ",
    105: " ",
    106: " ",
    107: " ",
    108: " ",
    109: " ",
    110: " ",
    111: " ",
    112: " ",
    113: " ",
    114: " ",
    115: " ",
  });

  const data = [
    { x: 20.0, y: 300.0 },
    { x: 150.0, y: 300.0 },
    { x: 280.0, y: 300.0 },
    { x: 410.0, y: 300.0 },
    { x: 540.0, y: 300.0 },
    { x: 670.0, y: 300.0 },
    { x: 800.0, y: 300.0 },
    { x: 930.0, y: 300.0 },
    { x: 930.0, y: 100.0 },
    { x: 800.0, y: 100.0 },
    { x: 670.0, y: 100.0 },
    { x: 540.0, y: 100.0 },
    { x: 410.0, y: 100.0 },
    { x: 280.0, y: 100.0 },
    { x: 150.0, y: 100.0 },
    { x: 20.0, y: 100.0 },
  ];

  let subdividedPoints = [];

  for (let i = 0; i < data.length - 1; i++) {
    const A = data[i];
    const B = data[i + 1];

    subdividedPoints.push({ x: A.x, y: A.y });

    const X = (B.x + A.x) / 2;
    const Y = (B.y + A.y) / 2;
    subdividedPoints.push({ x: X, y: Y });

    if (i === data.length - 2) {
      subdividedPoints.push({ x: B.x, y: B.y });
    }
  }

  function compareTimes(time1, time2) {
    time1 += ":00";
    const date1 = new Date(`2023-11-01 ${time1}`);
    const date2 = new Date(`2023-11-01 ${time2}`);

    if (date1 < date2) {
      return true;
    } else {
      return false;
    }
  }

  let upper_labels = [
    `Kandy`,
    `Wales\nPark ${Object.values(timeObj)[0]}`,
    `Mahamaya ${Object.values(timeObj)[1]}`,
    `Lewella Junction ${Object.values(timeObj)[2]}`,
    `Talwatta ${Object.values(timeObj)[3]}`,
    `Tennekumbura Bridge ${Object.values(timeObj)[4]}`,
    `Kalapura Junction ${Object.values(timeObj)[5]}`,
    `Nattarampotha Junction ${Object.values(timeObj)[6]}`,
  ];

  let lower_labels = [
    `Kundasale New\nTown ${Object.values(timeObj)[7]}`,
    `Warapitiya ${Object.values(timeObj)[8]}`,
    `Pallekele ${Object.values(timeObj)[9]}`,
    `Pachchakaatuwa ${Object.values(timeObj)[10]}`,
    `Balagolla ${Object.values(timeObj)[11]}`,
    `BOI ${Object.values(timeObj)[12]}`,
    `Kengalla ${Object.values(timeObj)[13]}`,
    `Digana ${Object.values(timeObj)[14]}`,
  ];

  useEffect(() => {
    let tempArr = {
      101: " ",
      102: " ",
      103: " ",
      104: " ",
      105: " ",
      106: " ",
      107: " ",
      108: " ",
      109: " ",
      110: " ",
      111: " ",
      112: " ",
      113: " ",
      114: " ",
      115: " ",
    };
    function setNewTimes() {
      axios
        .get("http://127.0.0.1:8000/arrival-times/")
        .then((res) => {
          let newObject = JSON.parse(res.data);
          console.log(newObject);
          let newLocations = [];
          for (let i = 0; i < newObject.length; i++) {
            for (let j = 0; j < 15; j++) {
              if (Object.values(newObject[i]["fields"])[j] !== "passed") {
                if (Object.values(newObject[i]["fields"])[j - 1] === "passed") {
                  newLocations.push(subdividedPoints[2 * j + 1]);
                } else if (j === 0) {
                  newLocations.push(subdividedPoints[2 * j + 1]);
                }
                if (Object.values(timeObj)[j] === " ") {
                  tempArr[101 + j] = Object.values(newObject[i]["fields"])
                    [j].split(":")
                    .slice(0, 2)
                    .join(":");
                } else if (
                  compareTimes(
                    Object.values(newObject[i]["fields"])[j],
                    Object.values(timeObj)[j]
                  )
                ) {
                  tempArr[Object.keys(newObject[i]["fields"])[j]] =
                    Object.values(newObject[i]["fields"])
                      [j].split(":")
                      .slice(0, 2)
                      .join(":");
                } else {
                  tempArr[Object.keys(newObject[i]["fields"])[j]] =
                    Object.values(timeObj)[j];
                }
              } else {
                tempArr[101 + j] = " ";
                // continue;
              }
            }
          }
          setLocations(newLocations);
          setTimeObj({ ...timeObj, ...tempArr });
          console.log(tempArr);
        })
        .catch((err) => {
          console.log(err);
        });
    }
    setNewTimes();
    const intervalID = setInterval(() => {
      setNewTimes();
    }, 20000);
    return () => clearInterval(intervalID);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    // Adjusted scales for larger visualization
    const xScale = d3.scaleLinear().domain([0, 800]).range([10, 810]);
    const yScale = d3.scaleLinear().domain([0, 400]).range([400, 0]);

    // Define the curve generator
    const line = d3
      .line()
      .x((d) => xScale(d.x))
      .y((d) => yScale(d.y))
      .curve(d3.curveStep);

    // Draw the thicker curve
    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "gray")
      .attr("stroke-width", 10) // Making the line thicker
      .attr("d", line);

    // Draw larger dots on the curve
    svg
      .selectAll("circle")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", (d) => xScale(d.x))
      .attr("cy", (d) => yScale(d.y))
      .attr("r", (d) => {
        if (d.x === 20.0) {
          return 15; // Larger radius for leftmost circles
        }
        return 12; // Normal radius for all other circles
      })
      .attr("fill", (d) => {
        if (d.x === 20.0) {
          return "firebrick"; // Red color for leftmost circles
        }
        return "#D3D3D3"; // Gray color for all other circles
      });

    // Draw texts above each point
    svg
      .selectAll(".text-above")
      .data(data)
      .enter()
      .append("text")
      .attr("x", (d, i) => {
        if (i === 0) return xScale(d.x); // Shift first label to the right
        return xScale(d.x);
      })
      .attr("y", (d) => yScale(d.y) - 50) // 50 units above the point
      .attr("text-anchor", "middle")
      .each(function (d, i) {
        const label = upper_labels[i];
        if (label) {
          // Check for undefined
          const words = label.split(" ");
          const x = d3.select(this).attr("x");
          const y = d3.select(this).attr("y");
          for (let j = 0; j < words.length; j++) {
            d3.select(this)
              .append("tspan")
              .attr("x", x)
              .attr("y", y)
              .attr("dy", `${j * 1.2}em`)
              .attr("font-size", "14px")
              .attr("font-family", "monospace")
              .attr("font-weight", "bold")
              .text(words[j]); // Use arrival times from state
          }
        }
      });

    // Draw times below each point
    svg
      .selectAll(".text-below")
      .data(data)
      .enter()
      .filter((d, i) => i >= data.length - 8) // Only consider last 8 points
      .append("text")
      .attr("x", (d, i) => {
        if (i === data.length - 9) return xScale(d.x); // Shift first label to the right
        return xScale(d.x);
      })
      .attr("y", (d) => yScale(d.y) + 30) // 20 units below the point
      .attr("text-anchor", "middle")
      .each(function (d, i) {
        const label = lower_labels[i];
        if (label) {
          // Check for undefined
          const words = label.split(" ");
          const x = d3.select(this).attr("x");
          const y = d3.select(this).attr("y");
          for (let j = 0; j < words.length; j++) {
            d3.select(this)
              .append("tspan")
              .attr("x", x)
              .attr("y", y)
              .attr("dy", `${j * 1.2}em`)
              .attr("font-size", "14px")
              .attr("font-family", "monospace")
              .attr("font-weight", "bold")
              .text(words[j]);
          }
        }
      });
    // Add the bus icon
    // Need to implement a for loop when the actual data comes
    function deduplicateByProperties(array, props) {
      return array.filter(
        (obj, index, self) =>
          index ===
          self.findIndex((t) => props.every((prop) => obj[prop] === t[prop]))
      );
    }

    const distinctLocations = deduplicateByProperties(locations, ["x", "y"]);

    distinctLocations.forEach((location) => {
      svg
        .append("image")
        .attr("xlink:href", busIcon)
        .attr("class", "blinking-icon")
        .attr("x", xScale(location.x) - 12) // Offset so the center of the icon is at the point
        .attr("y", yScale(location.y) - 12)
        .attr("width", 25)
        .attr("height", 25);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeObj]);

  return <svg ref={svgRef} width="1050" height="400"></svg>;
};

export default KandyDigana;
