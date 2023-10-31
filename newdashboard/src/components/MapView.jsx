import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, useMap, Marker, Popup } from "react-leaflet";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import L from "leaflet";
import "leaflet-routing-machine";
import { Icon } from "leaflet";
import "leaflet.locatecontrol"; // Import plugin
import "leaflet/dist/leaflet.css";
import "leaflet.locatecontrol/dist/L.Control.Locate.css";
import "../pages/MainPage.css";
import axios from "axios";

function MapView({ showMarkers, waypoints, direction, showRoute }) {
  function RoutingControl() {
    const map = useMap();
    // const terminalMarker = new L.Icon({
    //   iconUrl: require("../data/marker.png"),
    //   iconSize: [41, 41],
    //   iconAnchor: [20.5, 41],
    // });

    useEffect(() => {
      // const locateControl = L.control.locate();
      // locateControl.addTo(map);

      let count = 0;
      let waypointsArr = [];

      if (direction) {
        waypointsArr = [
          L.latLng(7.292462226, 80.6349778),
          L.latLng(7.299102491, 80.7347169),
        ];
      } else {
        waypointsArr = [
          L.latLng(7.299102491, 80.7347169),
          L.latLng(7.292462226, 80.6349778),
        ];
      }

      let routingControl;

      try {
        routingControl = L.Routing.control({
          waypoints: waypointsArr,
          show: false,
          geocoder: true,
          addWaypoints: false,
          draggableWaypoints: false,
          createMarker: function (i, wp, nWps) {
            return null;
            // return L.marker(wp.latLng, { icon: terminalMarker });
          },
        }).addTo(map);
        count++;
      } catch (error) {
        console.error("Error adding routing control: ", error);
      }

      // Cleanup function
      return () => {
        setTimeout(() => {
          console.log("Count: ", count);
          // map.removeControl(locateControl);
          if (count > 0) {
            if (map) {
              try {
                if (routingControl) {
                  map.removeControl(routingControl);
                }
              } catch (error) {
                console.error("Error removing routing control: ", error);
              }
            }
          }
        }, 1000);
      };
    }, [direction, showRoute]); // dependencies

    return null;
  }

  const [busPos, setBusPos] = useState([]);

  useEffect(() => {
    function busLocations() {
      axios
        .get("http://127.0.0.1:8000/arrival-times/")
        .then((res) => {
          let newObject = JSON.parse(res.data);
          const newBusPos = [];
          console.log(newObject);
          for (let i = 0; i < newObject.length; i++) {
            newBusPos.push({
              lat: Object.values(newObject[i]["fields"])[16],
              lng: Object.values(newObject[i]["fields"])[17],
            });
            for (let j = 0; j < 15; j++) {
              console.log(Object.values(newObject[0]["fields"])[j]);
              if (Object.values(newObject[i]["fields"])[j] !== "passed") {
                waypoints[j]["arrivalTime"] = Object.values(
                  newObject[i]["fields"]
                )
                  [j].split(":")
                  .slice(0, 2)
                  .join(":");
              } else {
                waypoints[j]["arrivalTime"] = "Bus has passed";
              }
            }
          }
          console.log("Here");
          setBusPos(newBusPos);
        })
        .catch((err) => {
          console.log(err);
        });
    }
    const intervalID = setInterval(() => {
      busLocations();
    }, 5000);
    return () => clearInterval(intervalID);
  }, []);

  return (
    <div style={{ height: "500px", width: "100%" }}>
      <MapContainer
        center={[7.2880049, 80.6897531]} // Centered at Kandy
        zoom={13} // Adjusted zoom level for better visibility
        style={{ height: "100%", width: "100%" }}
      >
        {showMarkers &&
          waypoints.map((coord, index) =>
            index === waypoints.length - 1 || index === 0 ? (
              <Marker
                key={`coord1-${index}`}
                position={[coord.lat, coord.lng]}
                icon={
                  new Icon({
                    iconUrl: require("../data/marker.png"),
                    iconSize: [41, 41],
                    iconAnchor: [20.5, 41],
                    popupAnchor: [0, -25],
                  })
                }
              >
                <Popup>
                  {coord.name} <br /> {coord.arrivalTime}
                </Popup>
              </Marker>
            ) : (
              <Marker
                key={`coord1-${index}`}
                position={[coord.lat, coord.lng]}
                icon={
                  new Icon({
                    iconUrl: require("../data/busstop.png"),
                    iconSize: [22, 22],
                    iconAnchor: [11, 22],
                    popupAnchor: [0, -10],
                  })
                }
              >
                <Popup>
                  {coord.name} <br /> {coord.arrivalTime}
                </Popup>
              </Marker>
            )
          )}
        {busPos.map((coord, index) => (
          <Marker
            key={`coord-${index}`}
            position={[coord.lat, coord.lng]}
            icon={
              new Icon({
                iconUrl: require("../data/travelling_bus.png"),
                iconSize: [42, 42],
                iconAnchor: [21, 42],
              })
            }
          />
        ))}
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {showRoute && <RoutingControl />}
      </MapContainer>
    </div>
  );
}

export default MapView;
