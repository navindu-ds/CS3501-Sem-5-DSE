import React, { useEffect, useState } from "react";
import KandyDigana from "../components/KandyDigana";
import Sidebar from "../components/Sidebar";
import DiganaKandy from "../components/DiganaKandy";
import "./MainPage.css";
import { RxDashboard } from "react-icons/rx"; // Importing the icon
import Availability from "../components/Availability";
import MapView from "../components/MapView";
import WidgetDigana from "../components/WidgetDigana";
import WidgetKandy from "../components/WidgetKandy";
import Footer from "../components/Footer";

const MainPage = () => {
  const [disable, setDisable] = useState(false);
  const [showKandyDigana, setShowKandyDigana] = useState(true);
  const [showMarkers, setShowMarkers] = useState(true);
  const [showKandyMap, setShowKandyMap] = useState(true);
  const [showKandyWidget, setShowKandyWidget] = useState(true);
  const [showRoute, setShowRoute] = useState(true);

  const kandy_digana_bus_stops = [
    "Digana",
    "Kengalla",
    "BOI",
    "Balagolla",
    "Pachchakaatuwa",
    "Pallekele",
    "Warapitiya",
    "Kundasale New Town",
    "Nattarampotha Junction",
    "Kalapura Junction",
    "Tennekumbura Bridge",
    "Talwatta",
    "Lewella Junction",
    "Mahamaya",
    "Wales Park",
    "Kandy",
  ];

  const digana_kandy_bus_stops = [
    "",
    "Kandy",
    "Hilwood",
    "Chidren's Park",
    "Dharmaraja",
    "Buwelikada",
    "Tennekumbura",
    "Nattarampotha",
    "Kundasale Police College",
    "Warapitiya",
    "Pallekele",
    "Pachchakaatuwa",
    "Balagolla",
    "BOI",
    "Kengalla",
    "Digana",
  ];

  const kandy_digana = [
    { lat: 7.292462226, lng: 80.6349778, name: "Kandy" },
    { lat: 7.291186017, lng: 80.63766185, name: "Wales Park" },
    { lat: 7.28784, lng: 80.64584, name: "Mahamaya" },
    { lat: 7.29443, lng: 80.65003, name: "Lewella Junction" },
    { lat: 7.286701, lng: 80.6603357, name: "Talwatta" },
    { lat: 7.281866, lng: 80.66603, name: "Tennekumbura Bridge" },
    { lat: 7.27983, lng: 80.67621, name: "Kalapura Junction" },
    { lat: 7.279117, lng: 80.67945, name: "Nattarampotha Junction" },
    { lat: 7.2809, lng: 80.68416, name: "Kundasale New Town" },
    { lat: 7.28149, lng: 80.68635, name: "Warapitiya" },
    { lat: 7.281322369, lng: 80.69676, name: "Pallekele" },
    { lat: 7.28473, lng: 80.70539, name: "Pachchakaatuwa" },
    { lat: 7.287349019, lng: 80.71400511, name: "Balagolla" },
    { lat: 7.28411, lng: 80.7221, name: "BOI" },
    { lat: 7.29152, lng: 80.72133, name: "Kengalla" },
    { lat: 7.29896, lng: 80.73472, name: "Digana" },
  ];

  const digana_kandy = [
    { lat: 7.29896, lng: 80.73472, name: "Digana" },
    { lat: 7.291726007, lng: 80.72143025, name: "Kengalla" },
    { lat: 7.28411, lng: 80.7221, name: "BOI" },
    { lat: 7.287349, lng: 80.71401, name: "Balagolla" },
    { lat: 7.28473, lng: 80.70539, name: "Pachchakaatuwa" },
    { lat: 7.28036, lng: 80.69567, name: "Pallekele" },
    { lat: 7.28148, lng: 80.68672, name: "Warapitiya" },
    { lat: 7.28039, lng: 80.68356, name: "Kundasale Police College" },
    { lat: 7.279799826, lng: 80.67659381, name: "Nattarampotha" },
    { lat: 7.28193, lng: 80.66594, name: "Tennekumbura" },
    { lat: 7.29312, lng: 80.64922, name: "Buwelikada" },
    { lat: 7.29067, lng: 80.64651, name: "Dharmaraja" },
    { lat: 7.28681, lng: 80.64761, name: "Children's Park" },
    { lat: 7.29021, lng: 80.6398, name: "Hilwood" },
    { lat: 7.292462226, lng: 80.6349778, name: "Kandy" },
  ];

  useEffect(() => {
    setDisable(true);
    setTimeout(() => {
      setDisable(false);
    }, 2000);
  }, [showKandyDigana, showKandyMap, showMarkers, showKandyWidget, showRoute]);

  return (
    <div>
      <Sidebar />
      <div className="background">
        <div className="dashboard-title">
          <h3>
            <RxDashboard className="dashboard-icon" /> DASHBOARD
          </h3>
        </div>

        <div className="parent-container">
          <div className="adjust">
            <div className="availadjust">
              <Availability />
            </div>
            <div className="card-container">
              <div className="toggle-buttons">
                <button
                  className={`toggle-btn ${showKandyDigana ? "active" : ""}`}
                  onClick={() => {
                    setDisable(true);
                    setShowKandyDigana(true);
                  }}
                  disabled={disable}
                >
                  Kandy - Digana
                </button>
                <button
                  className={`toggle-btn ${!showKandyDigana ? "active" : ""}`}
                  onClick={() => {
                    setDisable(true);
                    setShowKandyDigana(false);
                  }}
                  disabled={disable}
                >
                  Digana - Kandy
                </button>
              </div>
              <div className="map-container">
                {showKandyDigana ? <KandyDigana /> : <DiganaKandy />}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="mapview-parent">
        <div className="map-card">
          <div className="mapview-container">
            <button
              className="bus-route-btn"
              onClick={() => {
                setDisable(true);
                setShowRoute(!showRoute);
              }}
              disabled={disable}
            >
              Show/Hide Route
            </button>
            <button
              className="bus-stop-btn"
              onClick={() => {
                setDisable(true);
                setShowMarkers(!showMarkers);
              }}
              disabled={disable}
            >
              Show/Hide Bus Stops
            </button>
            <button
              className="map-kandy-btn"
              onClick={() => {
                setDisable(true);
                setShowKandyMap(true);
              }}
              disabled={disable}
            >
              Kandy - Digana
            </button>
            <button
              className="map-digana-btn"
              onClick={() => {
                setDisable(true);
                setShowKandyMap(false);
              }}
              disabled={disable}
            >
              Digana - Kandy
            </button>
            <MapView
              showMarkers={showMarkers}
              waypoints={showKandyMap ? kandy_digana : digana_kandy}
              direction={showKandyMap}
              showRoute={showRoute}
            />
          </div>
        </div>
      </div>
      <div className="widget-parent">
        <div className="widget-card">
          <div className="new-graph">
            <div className="stop-names">
              {(showKandyWidget
                ? kandy_digana_bus_stops
                : digana_kandy_bus_stops
              ).map((stop, index) => (
                <React.Fragment key={index}>
                  {stop}
                  <br />
                  <br />
                </React.Fragment>
              ))}
              <button
                className="change-direction-btn"
                onClick={() => {
                  setDisable(true);
                  setShowKandyWidget((prevState) => !prevState);
                }}
                disabled={disable}
              >
                Change Direction
              </button>
            </div>
            <div>{showKandyWidget ? <WidgetKandy /> : <WidgetDigana />}</div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default MainPage;
