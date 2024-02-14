import React from "react";
import { Container , Placeholder} from "react-bootstrap";
import MainPageText from "../../component/MainPageText/MainPageText";
import TableView from "../../component/TableView/TableView";
import { useSelector } from "react-redux";
import SkeltonLoader from '../../component/SkeltonLoader/SkeltonLoader'
import ErrorGettingData from "../../component/ErrorGetingData/ErrorGettingData";
const Customers = () => {

  const allCustomers = useSelector((state) => state.customer.allCustomers);
  
  const isWaitingForGetCustomers = useSelector(
    (state) => state.customer.isWaitingForGetCustomers
  );
  
  const errorInGetCustomers = useSelector(
    (state) => state.customer.errorInGetCustomers
  );
  
 
  
  return (
    <Container fluid>
      <MainPageText text="Customers" />
      <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
        {isWaitingForGetCustomers ? (
          <SkeltonLoader />
        ) : errorInGetCustomers ? (
          <ErrorGettingData />
        ) : (
          allCustomers.length > 0 &&
          <>
          <MainPageText text="customer Table" />
         <TableView to='customers' columns={Object.keys(allCustomers[0])} data={allCustomers} />
         </>
        )}
      </Container>
    </Container>
  );
};

export default Customers;
