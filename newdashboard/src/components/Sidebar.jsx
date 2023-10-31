import React from "react";

const Sidebar = () => {
  const sidebarStyle = {
    width: "50px",
    height: "400vh", // Adjust height as per your requirement
    backgroundColor: "#333",
    color: "#fff",
    position: "absolute",
    top: "100%",
    transform: "translateY(-50%)",
    // borderRadius: "0 16px 16px 0",
  };

  return (
    <div>
      <div style={sidebarStyle}></div>
    </div>
  );
};

export default Sidebar;
