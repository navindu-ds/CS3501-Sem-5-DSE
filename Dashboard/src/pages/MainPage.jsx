import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import Kandy_Digana from "../components/Kandy_Digana";
import Digana_Kandy from "../components/Digana_Kandy";
import "./MainPage.css";
import { RxDashboard } from "react-icons/rx"; // Importing the icon

const MainPage = () => {
  const [showKandyDigana, setShowKandyDigana] = useState(true);

  const today = new Date();
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
  const dateString = `${monthNames[today.getMonth()]} ${
    today.getDate() + "th"
  }`;
  const dayString = `${dayNames[today.getDay()]}`;

  const K_D_availability = 3;
  const D_K_availability = 2;

  return (
    <div className="background">
      <Sidebar />
      <div className="dashboard-title">
        <h3>
          <RxDashboard className="dashboard-icon" /> DASHBOARD
        </h3>
      </div>
      <div className="adjust">
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

        <div className="card-container">
          {/* Toggle buttons */}
          <div className="toggle-buttons">
            <button
              className={`toggle-btn ${showKandyDigana ? "active" : ""}`}
              onClick={() => setShowKandyDigana(true)}
            >
              Kandy-Digana
            </button>
            <button
              className={`toggle-btn ${!showKandyDigana ? "active" : ""}`}
              onClick={() => setShowKandyDigana(false)}
            >
              Digana-Kandy
            </button>
          </div>

          {/* Components */}
          <div className="map-container">
            {showKandyDigana ? <Kandy_Digana /> : <Digana_Kandy />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
