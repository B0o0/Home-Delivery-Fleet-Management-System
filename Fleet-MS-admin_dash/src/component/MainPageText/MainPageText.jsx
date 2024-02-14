import React from "react";

const MainPageText = ({ text }) => {
  return (
    <p
      className="p-3 display-6 text-primary  
    border-bottom border-4 border-muted
    ms-4
    "
      style={{ width: "max-content" }}
    >
      {text}
    </p>
  );
};

export default MainPageText;
