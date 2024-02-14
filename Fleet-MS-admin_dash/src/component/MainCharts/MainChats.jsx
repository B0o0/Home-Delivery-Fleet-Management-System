import React from "react";
import PieChartt from "../Chart/PieChart";
import ComposeChart from "../ComposeChart/ComposeChart";

const MainChats = () => {
  return (
    <div className=" container-fluid  chart mt-5 ">
      <div className="row justify-content-around">
        <PieChartt />
        <ComposeChart />
      </div>
    </div>
  );
};

export default MainChats;
