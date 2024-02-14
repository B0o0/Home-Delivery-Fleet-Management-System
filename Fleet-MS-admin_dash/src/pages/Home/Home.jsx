import React from "react";
import "./home.css";
import HomeCard from "../../component/HomeCard/HomeCard";
import MainChats from "../../component/MainCharts/MainChats";
import MainPageText from "../../component/MainPageText/MainPageText";

const Home = () => {
  return (
    <div className="container-fluid">
      <MainPageText text='HOME'/>
      <HomeCard />
      <MainChats />
    </div>
  );
};

export default Home;
