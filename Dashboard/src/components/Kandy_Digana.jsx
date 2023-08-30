import React, { useRef, useEffect, useState } from "react";
import * as d3 from "d3";
import busIcon from "../data/bus-20.png";
import "../pages/MainPage.css";

const Kandy_Digana = () => {
  const svgRef = useRef(null);

  const [arrivalTimes, setArrivalTimes] = useState([]);

  const fetchNewTimes = () => {
    // Mockup: Replace with actual data fetching logic
    const newTimes = upper_labels.map(() => new Date().toLocaleTimeString());
    setArrivalTimes(newTimes);
  };

  // Initialize with 16 time strings
  const [timeArray, setTimeArray] = useState([
    "12:00",
    "12:05",
    "12:10",
    "12:15",
    "12:20",
    "12:25",
    "12:30",
    "12:35",
    "12:40",
    "12:45",
    "12:50",
    "12:55",
    "13:00",
    "13:05",
    "13:10",
    "13:15",
  ]);

  const upper_labels = [
    `Kandy ${timeArray[0]}`,
    `Wales\nPark ${timeArray[1]}`,
    `Mahamaya ${timeArray[2]}`,
    `Lewella Junction ${timeArray[3]}`,
    `Talwatta ${timeArray[4]}`,
    `Tennekumbura Bridge ${timeArray[5]}`,
    `Kalapura Junction ${timeArray[6]}`,
    `Nattarampotha Junction ${timeArray[7]}`,
  ];

  const lower_labels = [
    `Kundasale New\nTown ${timeArray[8]}`,
    `Warapitiya ${timeArray[9]}`,
    `Pallekele ${timeArray[10]}`,
    `Pachchakaatuwa ${timeArray[11]}`,
    `Balagolla ${timeArray[12]}`,
    `BOI ${timeArray[13]}`,
    `Kengalla ${timeArray[14]}`,
    `Digana ${timeArray[15]}`,
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      // Update the times here. This is just an example.
      const newTimes = timeArray.map((time) => {
        const [hour, minute] = time.split(":");
        const newMinute = (parseInt(minute) + 1) % 60;
        const newHour =
          (parseInt(hour) + Math.floor((parseInt(minute) + 1) / 60)) % 24;
        return `${newHour.toString().padStart(2, "0")}:${newMinute
          .toString()
          .padStart(2, "0")}`;
      });
      setTimeArray(newTimes);
    }, 60000); // Update every minute

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    // Generated data points
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

    const subdividedPoints = [];

    for (let i = 0; i < data.length - 1; i++) {
      const A = data[i];
      const B = data[i + 1];

      subdividedPoints.push({ x: A.x, y: A.y });

      // // Calculate 3 points that divide AB into 4 equal parts
      // for (let j = 1; j <= 3; j++) {
      //     const m = j,
      //       n = 4 - j;
      //     const X = (m * B.x + n * A.x) / (m + n);
      //     const Y = (m * B.y + n * A.y) / (m + n);
      //     subdividedPoints.push({ x: X, y: Y });
      //   }

      //   if (i === data.length - 2) {
      //     subdividedPoints.push({ x: B.x, y: B.y });
      //   }
      // }

      const X = (B.x + A.x) / 2;
      const Y = (B.y + A.y) / 2;
      subdividedPoints.push({ x: X, y: Y });

      if (i === data.length - 2) {
        subdividedPoints.push({ x: B.x, y: B.y });
      }
    }

    // Need to implement a for loop when the actual data comes
    const busPoint1 = subdividedPoints[7];
    const busPoint2 = subdividedPoints[21];
    const busPoint3 = subdividedPoints[30];
    const busPoint4 = subdividedPoints[14];

    // Adjusted scales for larger visualization
    const xScale = d3.scaleLinear().domain([0, 800]).range([0, 800]);
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
          return "red"; // Red color for leftmost circles
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
        if (i === 0) return xScale(d.x) + 5; // Shift first label to the right
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
        if (i === data.length - 9) return xScale(d.x) + 5; // Shift first label to the right
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
              .attr("font-weight", "bold")
              .text(words[j]);
          }
        }
      });
    // Add the bus icon
    // Need to implement a for loop when the actual data comes
    svg
      .append("image")
      .attr("xlink:href", busIcon)
      .attr("class", "blinking-icon")
      .attr("x", xScale(busPoint1.x) - 12) // Offset so the center of the icon is at the point
      .attr("y", yScale(busPoint1.y) - 12)
      .attr("width", 25)
      .attr("height", 25);
    svg
      .append("image")
      .attr("xlink:href", busIcon)
      .attr("class", "blinking-icon")
      .attr("x", xScale(busPoint2.x) - 12) // Offset so the center of the icon is at the point
      .attr("y", yScale(busPoint2.y) - 12)
      .attr("width", 25)
      .attr("height", 25);
    svg
      .append("image")
      .attr("xlink:href", busIcon)
      .attr("class", "blinking-icon")
      .attr("x", xScale(busPoint3.x) - 12) // Offset so the center of the icon is at the point
      .attr("y", yScale(busPoint3.y) - 12)
      .attr("width", 25)
      .attr("height", 25);
    svg
      .append("image")
      .attr("xlink:href", busIcon)
      .attr("class", "blinking-icon")
      .attr("x", xScale(busPoint4.x) - 12) // Offset so the center of the icon is at the point
      .attr("y", yScale(busPoint4.y) - 12)
      .attr("width", 25)
      .attr("height", 25);
    return () => clearInterval(interval);
  }, [timeArray]);

  return <svg ref={svgRef} width="1050" height="400"></svg>;
};

export default Kandy_Digana;
