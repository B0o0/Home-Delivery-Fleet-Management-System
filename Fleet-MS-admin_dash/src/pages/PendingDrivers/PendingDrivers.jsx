import { useEffect } from 'react'
import { Container , Placeholder} from "react-bootstrap";
import MainPageText from "../../component/MainPageText/MainPageText";
import TableView from "../../component/TableView/TableView";
import { useSelector } from "react-redux";
import SkeltonLoader from '../../component/SkeltonLoader/SkeltonLoader'
import ErrorGettingData from "../../component/ErrorGetingData/ErrorGettingData";
import { useDispatch } from 'react-redux';
import { getAllPendingDrivers } from '../../store/pendingDrivers-actions'; 
const PendingDrivers = () => {
    const dispatch = useDispatch()
    const allPendingDrivers = useSelector((state) => state.pendingDrivers.allPendingDrivers);
    
    const isWaitingForGetPendingDrivers = useSelector(
      (state) => state.pendingDrivers.isWaitingForGetPendingDrivers
    );
   
    const errorInGetPendingDrivers = useSelector(
      (state) => state.pendingDrivers.errorInGetPendingDrivers
    );
    const isRequireRender = useSelector(
        (state) => state.pendingDrivers.isRequireRender
      );
    useEffect(()=>{
        dispatch(getAllPendingDrivers())
    } ,[isRequireRender])
  return (
    <Container fluid>
    <MainPageText text="Pending Drivers" />
    <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
      {isWaitingForGetPendingDrivers ? (
        <SkeltonLoader />
      ) : errorInGetPendingDrivers ? (
        <ErrorGettingData />
      ) : (
        allPendingDrivers.length > 0 &&
        <>
        <MainPageText text="Pending Buisness Table" />
       <TableView  to='pendingD' isRequireApprove={true} columns={Object.keys(allPendingDrivers[0])} data={allPendingDrivers} />
       </>
      )}
    </Container>
  </Container>
  )
}

export default PendingDrivers