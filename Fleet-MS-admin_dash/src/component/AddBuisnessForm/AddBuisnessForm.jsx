import React from "react";
import { Formik } from "formik";
import { Button, Form } from "react-bootstrap";
import CustomInput from "../CustomInput/CustomInput";
import CustomSelectInput from '../CustomSelectInput/CustomSelectInput'
import {  faEnvelope, faPhone , faMapLocation , faBusinessTime , faList} from "@fortawesome/free-solid-svg-icons";
import MainPageText from "../MainPageText/MainPageText";
import addBuisnessSchema from "../../validationSchema/addBuisnessSchema";
import {useDispatch , useSelector} from 'react-redux'
import {Container} from 'react-bootstrap'
import { addNewBuisness } from "../../store/bus-actions";

import ErrorGettingData from "../ErrorGetingData/ErrorGettingData";
import SkeltonLoader from "../SkeltonLoader/SkeltonLoader";
import OverLoader from "../OverLoader/OverLoader";
const AddBuisnessForm = () => {
  const dispatch = useDispatch()
  
 
  const isWaitingForGetBusiness = useSelector(
    (state) => state.buisness.isWaitingForGetBusiness
  );
  const isErrorGetBuisness = useSelector(
    (state) => state.buisness.errorInGetBusiness
  );
  return (

    <Container fluid>
   
    <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm" style={{position : 'relative'}}>
      {isWaitingForGetBusiness ? <OverLoader /> : null}
      { isErrorGetBuisness ? (
        <ErrorGettingData />
      ) : (
       
        <>
         <MainPageText text='Fill Buisness Information'/> 
      <Formik
        initialValues={{
          name: "",
          phone: "",
          password : "" ,
          email: "",
          business_website : "" , 
          contact_name : "" , 
          postal_code : "" , 
          address: "",
          type: "Choose Buisness Type",
        }}
        onSubmit={(values , {resetForm , setFieldError  }) => {
         
            dispatch(addNewBuisness(values , resetForm , setFieldError))
        }} 
        validationSchema={addBuisnessSchema}
      >
        {({ handleSubmit }) => {
          return (
            <Form onSubmit={handleSubmit} noValidate>
              <CustomInput
                name='name' 
                label="Name"
                placeholder="Enter Buisness Name"
                icon={faBusinessTime}
              />
               <CustomInput
                name='email' 
                label="Email"
                placeholder="Enter Buisness Email"
                icon={faEnvelope}
              />  
               <CustomInput
                name='password' 
                label="Password"
                placeholder="Enter Buisness Password"
                type='password'
                icon={faEnvelope}
              />  
               <CustomInput
                name='phone' 
                label="Phone"
                placeholder="Enter Buisness Phone"
                icon={faPhone}
              />
                <CustomInput
                name='contact_name' 
                label="Contact Name"
                placeholder="Enter Contact Name"
                icon={faPhone}
              />
                <CustomInput
                name='address' 
                label="Address"
                placeholder="Enter Buisness Address"
                icon={faMapLocation}
              />
                <CustomSelectInput
                name='type' 
                label="Type"
                placeholder="Choose Buisness Type"
                icon={faList}
                options={[  {type : 'Restaurant'} ,  {type :  "Market"}]}
              />
               <CustomInput
                name='business_website' 
                label="Website"
                placeholder="Enter Buisness Website"
                icon={faBusinessTime}
              />
               <CustomInput
                name='postal_code' 
                label="Postal code"
                placeholder="Enter Buisness Postal code"
                icon={faBusinessTime}
              />
              <Button type='submit' className='w-100 p-2 mt-4'>Add</Button>
            </Form>
          );
        }}
      </Formik>
       </>
      )}
    </Container>
  </Container>
   
  );
};

export default AddBuisnessForm;
