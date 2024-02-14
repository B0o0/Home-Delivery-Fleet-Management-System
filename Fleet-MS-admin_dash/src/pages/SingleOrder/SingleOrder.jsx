import React from 'react'
import { useParams } from "react-router-dom";
import { useSelector } from 'react-redux';
import SkeltonLoader from '../../component/SkeltonLoader/SkeltonLoader';
import ErrorGettingData from '../../component/ErrorGetingData/ErrorGettingData';
import MainPageText from '../../component/MainPageText/MainPageText';
import { Container } from 'react-bootstrap';
import DataImg from '../../assets/images/data.png'
import DetailItem from '../../component/DetailItem/DetailItem';
const SingleOrder = () => {
    
   
   const {id} = useParams() 
   const allOrders = useSelector((state)=>state.order.allOrders) 
   const isWaitingForGetOrders = useSelector((state)=>state.order.isWaitingForGetOrders) 
   const errorInGetOrders =  useSelector((state)=>state.order.errorInGetOrders) 
   const selectedOrder = allOrders.find((item)=> Object.values(item._id)[0]  === id)
   console.log(selectedOrder)
  return (
    <Container fluid >
    <MainPageText text="Order" />
    <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
      <MainPageText text="Order Information" />
      {isWaitingForGetOrders ? (
        <SkeltonLoader />
      ) : errorInGetOrders ? (
        <ErrorGettingData />
      ) : (
       
        <div className="row justify-content-center bg-white rounded p-3" >
        <div className="col-md-4" >
            <img  src={DataImg} alt="" className="w-100" />
        </div>
        <div className="col-md-7" style={{maxHeight : '400px' , overflow : 'auto'}}>
           <DetailItem title='Total Cost' txt={`${selectedOrder.total_cost} LE `}/>
           <DetailItem title='Status' txt={`${selectedOrder.status}  `}/>
           <DetailItem title='Rating' txt={`${selectedOrder.rating}  `}/>
           <DetailItem title='Date' txt={`${selectedOrder.date}  `}/>
           <DetailItem title='Feedback' txt={`${selectedOrder.feedback}  `}/>
           <DetailItem title='Delivery Address' txt={`${selectedOrder.delivery_address}  `}/>
           <DetailItem title='Pickup Address' txt={`${selectedOrder.pickup_address}  `}/>
           
           


        </div>
        </div>
        
      )}
    </Container>
  </Container>
  )
}

export default SingleOrder