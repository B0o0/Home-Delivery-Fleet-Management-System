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
import addAdminSchema from "../../validationSchema/addAdminSchema";
import { addNewAdmin } from "../../store/auth-actions";
const AddAdminForm = () => {
  const dispatch = useDispatch()
  
 
  const isWaitingForAddAdmin = useSelector(
    (state) => state.auth.isWaitingForLogin
  );
  const errorInAddAdmin = useSelector(
    (state) => state.buisness.errorInLogin
  );
  return (

    <Container fluid>
   
    <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm" style={{position : 'relative'}}>
      {isWaitingForAddAdmin ? <OverLoader /> : null}
      { errorInAddAdmin ? (
        <ErrorGettingData />
      ) : (
       
        <>
         <MainPageText text='Fill Buisness Information'/> 
      <Formik
        initialValues={{
          username: "",
          email: "",
          phone: "",
          password : "" ,
          confirm_password : "" ,
         
        }}
        onSubmit={(values , {resetForm , setFieldError  }) => {
         
             dispatch(addNewAdmin(values , resetForm , setFieldError))
        }} 
        validationSchema={addAdminSchema}
      >
        {({ handleSubmit }) => {
          return (
            <Form onSubmit={handleSubmit} noValidate>
              <CustomInput
                name='username' 
                label="Name"
                placeholder="Enter Admin Name"
                icon={faBusinessTime}
              />
               <CustomInput
                name='email' 
                label="Email"
                placeholder="Enter Admin Email"
                icon={faEnvelope}
              />  
               <CustomInput
                name='phone' 
                label="Phone"
                placeholder="Enter Admin Phone"
                icon={faPhone}
              />
               <CustomInput
                name='password' 
                label="Password"
                placeholder="Enter Admin Password"
                type='password'
                icon={faEnvelope}
              />  
              <CustomInput
                name='confirm_password' 
                label="Password"
                placeholder="Rewrite Admin Password"
                type='password'
                icon={faEnvelope}
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

export default AddAdminForm;
