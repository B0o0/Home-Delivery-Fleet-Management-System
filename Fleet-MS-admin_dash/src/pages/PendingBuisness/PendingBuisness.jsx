import { useEffect } from 'react'
import { Container , Placeholder} from "react-bootstrap";
import MainPageText from "../../component/MainPageText/MainPageText";
import TableView from "../../component/TableView/TableView";
import { useSelector } from "react-redux";
import SkeltonLoader from '../../component/SkeltonLoader/SkeltonLoader'
import ErrorGettingData from "../../component/ErrorGetingData/ErrorGettingData";
import { useDispatch } from 'react-redux';
import { getAllPendingBusiness } from '../../store/pendingBuisness-actions';
const PendingBuisness = () => {
    const dispatch = useDispatch()
    const allPendingBuisness = useSelector((state) => state.pendingBuisness.allPendingBuisness);
    
    const isWaitingForGetPendingBusiness = useSelector(
      (state) => state.pendingBuisness.isWaitingForGetPendingBusiness
    );
   
    const errorInGetPendingBusiness = useSelector(
      (state) => state.pendingBuisness.errorInGetPendingBusiness
    );
    const isRequireRender = useSelector(
        (state) => state.pendingBuisness.isRequireRender
      );
    useEffect(()=>{
        dispatch(getAllPendingBusiness())
    } ,[isRequireRender])
  return (
    <Container fluid>
    <MainPageText text="Pending Buisness" />
    <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
      {isWaitingForGetPendingBusiness ? (
        <SkeltonLoader />
      ) : errorInGetPendingBusiness ? (
        <ErrorGettingData />
      ) : (
        allPendingBuisness.length > 0 &&
        <>
        <MainPageText text="Pending Buisness Table" />
       <TableView  to='pendingB' isRequireApprove={true} columns={Object.keys(allPendingBuisness[0])} data={allPendingBuisness} />
       </>
      )}
    </Container>
  </Container>
  )
}

export default PendingBuisness