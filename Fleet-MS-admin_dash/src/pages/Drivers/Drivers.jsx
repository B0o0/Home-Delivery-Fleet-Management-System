import React from "react";
import { Container } from "react-bootstrap";
import MainPageText from "../../component/MainPageText/MainPageText";
import TableView from "../../component/TableView/TableView";
import { useSelector , useDispatch } from "react-redux";
import SkeltonLoader from '../../component/SkeltonLoader/SkeltonLoader'
import ErrorGettingData from "../../component/ErrorGetingData/ErrorGettingData";

const Orders = () => {
  const dispatch = useDispatch()
  const allDriversForPreview = useSelector((state) => state.driver.driversForPreview);

 

  const isWaitingForGetDrivers = useSelector(
    (state) => state.driver.isWaitingForGetDrivers
  );
  const errorInGetDrivers = useSelector(
    (state) => state.driver.errorInGetDrivers
  );
  
 
  
  return (
    <Container fluid>
      <MainPageText text="Drivers"/>
      <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
        {isWaitingForGetDrivers ? (
          <SkeltonLoader />
        ) : errorInGetDrivers ? (
          <ErrorGettingData />
        ) : (
          allDriversForPreview.length > 0 &&
          <>
          <MainPageText text="Drivers Table" />
         <TableView to='drivers' columns={Object.keys(allDriversForPreview[0])} data={allDriversForPreview} />
         </>
        )}
      </Container>
    </Container>
  );
};

export default Orders;
