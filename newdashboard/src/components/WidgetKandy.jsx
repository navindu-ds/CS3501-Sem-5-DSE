import React, { useState, useRef, useEffect } from "react";
import * as d3 from "d3";
import axios from "axios";

const WidgetKandy = () => {
  const svgRef = useRef(null);
  let [timeOfDay, setTimeOfDay] = useState(" ");

  function generateTimeIntervals(time) {
    const result = [];
    const format = (date) => {
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      return `${hours}:${minutes}`;
    };

    // Convert input time to a Date object
    const [hours, minutes] = time.split(":");
    const currentDate = new Date();
    currentDate.setHours(Number(hours), Number(minutes), 0, 0);

    // Round to the closest 5-minute interval
    const roundedMinutes = Math.round(currentDate.getMinutes() / 5) * 5;
    currentDate.setMinutes(roundedMinutes);

    // Set the starting time to 20 minutes before the given time
    currentDate.setMinutes(currentDate.getMinutes() - 20);

    // Generate time strings for a total of 70 minutes (20 + 50)
    for (let i = 0; i < 15; i++) {
      result.push(format(currentDate));
      currentDate.setMinutes(currentDate.getMinutes() + 5);
    }

    return result;
  }

  function findDataPoint(dataPoints, startTime, targetTime) {
    const getTimeInMinutes = (timeString) => {
      const [hours, minutes] = timeString.split(":").map(Number);
      return hours * 60 + minutes;
    };

    const startMinutes = getTimeInMinutes(startTime);
    const targetMinutes = getTimeInMinutes(targetTime);

    const indexOffset = targetMinutes - startMinutes;

    return dataPoints[indexOffset];
    // return dataPoints[5];
  }

  function timeSetter() {
    axios
      .get("http://127.0.0.1:8000/avg-buses/")
      .then((res) => {
        let newObject = res.data;
        setTimeOfDay(newObject["time"].split(":").slice(0, 2).join(":"));
      })
      .catch((err) => {
        console.log(err);
      });
  }

  useEffect(() => {
    timeSetter();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const data = [
      { x: 20.0, y: -250 },
      { x: 85.0, y: -250 },
      { x: 150.0, y: -250 },
      { x: 215.0, y: -250 },
      { x: 280.0, y: -250 },
      { x: 345.0, y: -250 },
      { x: 410.0, y: -250 },
      { x: 475.0, y: -250 },
      { x: 540.0, y: -250 },
      { x: 605.0, y: -250 },
      { x: 670.0, y: -250 },
      { x: 735.0, y: -250 },
      { x: 800.0, y: -250 },
      { x: 865.0, y: -250 },
      { x: 930.0, y: -250 },
    ];

    const labels = generateTimeIntervals(timeOfDay);

    const xScale = d3.scaleLinear().domain([0, 800]).range([0, 800]);
    const yScale = d3.scaleLinear().domain([0, 400]).range([400, 0]);

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
      .attr("stroke-width", 5) // Making the line thicker
      .attr("d", line);

    const numOfPoints = 71; // from 1:00 to 3:00 is 2 hours i.e., 120 minutes plus 1:00, so 121 points.
    const xInterval = 910 / 70; // width divided by 120 intervals
    const data2 = Array.from({ length: numOfPoints }, (_, i) => {
      return {
        x: i * xInterval + 20,
        y: -250, // keeping the y constant for this example, adjust as needed
      };
    });

    function getYPos(busStop, data, dottedLineSpacing) {
      if (busStop === "100") {
        return data[0].y + dottedLineSpacing;
      } else if (busStop === "101") {
        return data[0].y + 2 * dottedLineSpacing;
      } else if (busStop === "102") {
        return data[0].y + 3 * dottedLineSpacing;
      } else if (busStop === "103") {
        return data[0].y + 4 * dottedLineSpacing;
      } else if (busStop === "104") {
        return data[0].y + 5 * dottedLineSpacing;
      } else if (busStop === "105") {
        return data[0].y + 6 * dottedLineSpacing;
      } else if (busStop === "106") {
        return data[0].y + 7 * dottedLineSpacing;
      } else if (busStop === "107") {
        return data[0].y + 8 * dottedLineSpacing;
      } else if (busStop === "108") {
        return data[0].y + 9 * dottedLineSpacing;
      } else if (busStop === "109") {
        return data[0].y + 10 * dottedLineSpacing;
      } else if (busStop === "110") {
        return data[0].y + 11 * dottedLineSpacing;
      } else if (busStop === "111") {
        return data[0].y + 12 * dottedLineSpacing;
      } else if (busStop === "112") {
        return data[0].y + 13 * dottedLineSpacing;
      } else if (busStop === "113") {
        return data[0].y + 14 * dottedLineSpacing;
      } else if (busStop === "114") {
        return data[0].y + 15 * dottedLineSpacing;
      } else if (busStop === "115") {
        return data[0].y + 16 * dottedLineSpacing;
      }
    }

    function circlePos(data, labels) {
      return new Promise((resolve, reject) => {
        let circleLocations = [];
        axios
          .get("http://127.0.0.1:8000/arrival-times/")
          .then((res) => {
            let newObject = JSON.parse(res.data);
            for (let i = 0; i < newObject.length; i++) {
              let tempLocations = [];
              for (let j = 0; j < 15; j++) {
                if (Object.values(newObject[i]["fields"])[j] !== "passed") {
                  let temp1 = findDataPoint(
                    data,
                    labels[0],
                    Object.values(newObject[i]["fields"])
                      [j].split(":")
                      .slice(0, 2)
                      .join(":")
                  );
                  let temp2 = getYPos(
                    Object.keys(newObject[i]["fields"])[j],
                    data,
                    40
                  );
                  if (temp1 !== undefined && temp2 !== undefined) {
                    tempLocations.push({
                      x: temp1.x,
                      y: temp2,
                    });
                  }
                }
              }
              circleLocations.push(tempLocations);
            }
            resolve(circleLocations);
          })
          .catch((err) => {
            console.log(err);
            reject(err);
          });
      });
    }

    data.forEach((d, i) => {
      svg
        .append("line")
        .attr("x1", xScale(d.x))
        .attr("y1", yScale(d.y) - (5 + (1 - (i % 2)) * 5))
        .attr("x2", xScale(d.x))
        .attr("y2", yScale(d.y) + (5 + (1 - (i % 2)) * 5)) // Length of the vertical line
        .attr("stroke", "black")
        .attr("stroke-width", 2);

      svg
        .append("text")
        .attr("x", xScale(d.x))
        .attr("y", yScale(d.y) + 30) // position the text 30px below the line
        .attr("text-anchor", "middle") // center the text
        .attr("font-weight", "bold")
        .text(labels[i]); // add the label text

      const numDottedLines = 17;
      const dottedLineSpacing = 40;
      // (yScale(0) - yScale(data[0].y)) / numDottedLines;
      for (let i = 1; i < numDottedLines; i++) {
        // const yPos = yScale(data[0].y) - i * dottedLineSpacing;

        svg
          .append("line")
          .attr("x1", xScale(data[0].x))
          .attr("y1", yScale(data[0].y) - i * dottedLineSpacing)
          .attr("x2", xScale(data[data.length - 1].x))
          .attr("y2", yScale(data[0].y) - i * dottedLineSpacing)
          .attr("stroke", "blue")
          .attr("stroke-width", 1)
          .attr("stroke-dasharray", "3,10"); // makes the line dotted
      }
    });
    if (findDataPoint(data2, labels[0], timeOfDay) !== undefined) {
      const xPosBlinkingLine = findDataPoint(data2, labels[0], timeOfDay).x; // Set the x position of the blinking line

      // Appending a blinking vertical dotted line
      svg
        .append("line")
        .attr("x1", xPosBlinkingLine)
        .attr("y1", yScale(data[0].y))
        .attr("x2", xPosBlinkingLine)
        .attr("y2", yScale(data[0].y + 16 * 40)) // Assume 0 is the top position
        .attr("stroke", "green")
        .attr("stroke-width", 5)
        .attr("stroke-dasharray", "10,5") // makes the line dotted
        .attr("class", "blinking"); // Assigning a class for CSS animation
    }

    async function handleCirclePositions() {
      const result = await circlePos(data2, labels);

      const colors = ["red", "blue", "orange", "purple", "pink"];

      for (let i = 0; i < result.length; i++) {
        console.log(result);
        result[i].forEach((pos) => {
          svg
            .append("circle")
            .attr("cx", xScale(pos.x))
            .attr("cy", yScale(pos.y))
            .attr("r", 8) // radius of the circle
            .attr("fill", colors[i]); // color of the circle
        });
      }
    }

    handleCirclePositions();

    const intervalID = setInterval(() => {
      timeSetter();
    }, 20000);
    return () => {
      clearInterval(intervalID);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeOfDay]);
  return (
    <div style={{ width: "800px", overflowX: "scroll" }}>
      <svg ref={svgRef} width="950" height="700"></svg>
    </div>
  );
};

export default WidgetKandy;
