import React from "react";
import AnalysticCard from "../Analystic/AnalysticCard";
import {useSelector} from 'react-redux'
const HomeCard = () => {
  const numOfBuisness = useSelector((state)=>state.buisness.numOfallBuisness)
  const numOfOrders = useSelector((state)=>state.order.numOfallOrders)
  const numOfCustomers = useSelector((state)=>state.customer.numOfallCustomers)
  const numOfDrivers = useSelector((state)=>state.driver.numOfallDrivers)

  return (
    <div className="container-fluid ms-3">
      <div className="row justify-content-between">
        <AnalysticCard
          iconColor="#4154f1"
          bgColor="#f6f6fe"
          number={numOfBuisness}
          text="Total Buisness"
          icon="fa-solid fa-shop"
        />
        <AnalysticCard
          iconColor="#2eca6a"
          bgColor="#e0f8e9"
          number={numOfOrders}
          text="Total Orders"
          icon="fa-solid fa-briefcase"
        />
        <AnalysticCard
          iconColor="#1b0158"
          bgColor="#e1e9ff"
          number={numOfCustomers}
          text="Total Customer"
          icon="fa-solid fa-people-group "
        />
        <AnalysticCard
          iconColor="#ff771d"
          bgColor="#ffecdf"
          number={numOfDrivers}
          text="Total Drivers"
          icon="fa-solid fa-motorcycle"
        />
      </div>
    </div>
  );
};

export default HomeCard;
