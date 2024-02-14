import React from "react";
import { Container } from "react-bootstrap";
import MainPageText from "../../component/MainPageText/MainPageText";
import TableView from "../../component/TableView/TableView";
import { useSelector } from "react-redux";
import SkeltonLoader from '../../component/SkeltonLoader/SkeltonLoader'
import ErrorGettingData from "../../component/ErrorGetingData/ErrorGettingData";

const Orders = () => {

  const allOrders = useSelector((state) => state.order.allOrders);
 
  const isWaitingForGetOrders = useSelector(
    (state) => state.order.isWaitingForGetOrders
  );
  const errorInGetOrders = useSelector(
    (state) => state.order.errorInGetOrders
  );
  
 
  const formattedOrders = allOrders.map(({_id , total_cost , status , cancellation_reason ,rating , date})=>{
      return {_id , total_cost , date ,status , cancellation_reason , rating}
  })
  return (
    <Container fluid>
      <MainPageText text="Orders"/>
      <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
        {isWaitingForGetOrders ? (
          <SkeltonLoader />
        ) : errorInGetOrders ? (
          <ErrorGettingData />
        ) : (
            allOrders.length > 0 &&
          <>
          <MainPageText text="Order List" />
         <TableView to='orders' columns={Object.keys(formattedOrders[0])} data={formattedOrders} />
         </>
        )}
      </Container>
    </Container>
  );
};

export default Orders;
