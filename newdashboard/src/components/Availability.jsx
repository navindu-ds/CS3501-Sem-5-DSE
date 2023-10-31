import React, { useEffect, useState } from "react";
import axios from "axios";

function Availability() {
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const dayNames = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const [dateString, setDateString] = useState("");
  const [dayString, setDayString] = useState("");

  let [K_D_availability, setKDAvailability] = useState(0);
  const D_K_availability = 2;

  function formatDate(inputDate) {
    const date = new Date(inputDate);

    const day = date.getDate();
    let suffix = "th";
    if (day === 1 || day === 21 || day === 31) {
      suffix = "st";
    } else if (day === 2 || day === 22) {
      suffix = "nd";
    } else if (day === 3 || day === 23) {
      suffix = "rd";
    }

    const formattedMonthAndDay = `${
      monthNames[date.getMonth()]
    } ${day}${suffix}`;
    const formattedDayName = dayNames[date.getDay()];

    return [formattedMonthAndDay, formattedDayName];
  }

  function availability() {
    axios
      .get("http://127.0.0.1:8000/avg-buses/")
      .then((res) => {
        let newObject = res.data;
        const [formattedMonthAndDay, formattedDayName] = formatDate(
          newObject.date
        );
        setDateString(formattedMonthAndDay);
        setDayString(formattedDayName);
        const avgBusValueInt = Math.round(parseFloat(newObject.avg_bus_value));
        setKDAvailability(avgBusValueInt);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  useEffect(() => {
    availability();
    const intervalID = setInterval(() => {
      availability();
    }, 60000);
    return () => clearInterval(intervalID);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="availability-card">
      <p className="card-header">Estimated Bus Availability</p>
      <p className="card-subheader">
        {dateString} <br /> {dayString}
      </p>
      <div className="bus-availability">
        <p className="card-subheader">Kandy to Digana</p>
        <p className="card-subheader2">{K_D_availability}</p>
        <p className="card-text">
          Buses per
          <br /> Hour
        </p>
      </div>
      <div className="bus-availability">
        <p className="card-subheader">Digana to Kandy</p>
        <p className="card-subheader2">{D_K_availability}</p>
        <p className="card-text">
          Buses per
          <br /> Hour
        </p>
      </div>
    </div>
  );
}

export default Availability;
