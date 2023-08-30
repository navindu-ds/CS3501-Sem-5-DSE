import React, { useState } from "react";

const Sidebar = ({ setView }) => {
  const sidebarStyle = {
    width: "50px",
    height: "600px", // Adjust height as per your requirement
    backgroundColor: "#333",
    color: "#fff",
    position: "absolute",
    top: "54%",
    transform: "translateY(-50%)",
    borderRadius: "0 16px 16px 0",
  };
  const [activeButton, setActiveButton] = useState("map");

  const handleViewChange = (view) => {
    setActiveButton(view);
    setView(view);
  };

  return (
    <div>
      <div style={sidebarStyle}>{/* Sidebar content */}</div>
      <div className="sidebar">
        {/* ...existing code... */}
        {/* <button
          className={`toggle-button map-button ${
            activeButton === "map" ? "active" : ""
          }`}
          onClick={() => handleViewChange("map")}
        >
          Show Map
        </button>
        <button
          className={`toggle-button kandy-button ${
            activeButton === "kandy" ? "active" : ""
          }`}
          onClick={() => handleViewChange("kandy")}
        >
          Show Kandy_Digana
        </button> */}
      </div>
    </div>
  );
};

export default Sidebar;
