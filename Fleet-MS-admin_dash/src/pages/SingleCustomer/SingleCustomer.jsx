import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { Form, Container, Button } from "react-bootstrap";
import CustomInput from "../../component/CustomInput/CustomInput";
import { Formik } from "formik";
import { faEnvelope, faPhone } from "@fortawesome/free-solid-svg-icons";
import MainPageText from "../../component/MainPageText/MainPageText";
import { useDispatch } from "react-redux";
import SkeltonLoader from "../../component/SkeltonLoader/SkeltonLoader";
import ErrorGettingData from "../../component/ErrorGetingData/ErrorGettingData";
import { useNavigate } from "react-router-dom";
import { deleteCustomer, getSingleCustomer, updateCustomer } from "../../store/customer-actions";

const SingleCustomer = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const dispatch = useDispatch();
  const selectedCustomers = useSelector(
    (state) => state.customer.selectedCustomers
  );

  
  const isWaitingForGetCustomers = useSelector(
    (state) => state.customer.isWaitingForGetCustomers
  );
  const errorInGetCustomers = useSelector(
    (state) => state.customer.errorInGetCustomers
  );

  const isRequireRender = useSelector(
    (state) => state.customer.isRequireRender
  );
  useEffect(() => {
    dispatch(getSingleCustomer(id));
  }, [isRequireRender]);

  const navigateHandler = () => {
    navigate("/customers", { replace: true });
  };
  const deleteHandler = () => {
     dispatch(deleteCustomer(id, navigateHandler));
  };
  return (
    <Container fluid>
      <MainPageText text="Customers" />
      <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
        <MainPageText text="Customer Information" />
        {isWaitingForGetCustomers ? (
          <SkeltonLoader />
        ) : errorInGetCustomers ? (
          <ErrorGettingData />
        ) : (
          selectedCustomers &&
          Object.keys(selectedCustomers).length > 0 && (
            <>
              <Formik
                initialValues={{
                  first_name: selectedCustomers.first_name,
                  last_name: selectedCustomers.last_name,
                  email: selectedCustomers.email,
                  
                  phone: selectedCustomers.phone,

                  address: selectedCustomers.address,
                }}
                onSubmit={(values) => {
                  dispatch(updateCustomer(id , values))
                }}
              >
                {({ initialValues, values, handleSubmit }) => {
                  return (
                    <Form className="w-100" onSubmit={handleSubmit}>
                      <CustomInput
                        name="first_name"
                        label="First Name"
                        isUpdate={true}
                        icon={faEnvelope}
                      />
                      <CustomInput
                        name="last_name"
                        label="Last Name"
                        isUpdate={true}
                        icon={faEnvelope}
                      />
                      <CustomInput
                        name="email"
                        label="Email"
                        isUpdate={true}
                        icon={faEnvelope}
                      />
                      <CustomInput
                        name="phone"
                        label="Phone"
                        isUpdate={true}
                        icon={faEnvelope}
                      />

                      <CustomInput
                        name="address"
                        label="Adress"
                        isUpdate={true}
                        icon={faEnvelope}
                      />
                      {JSON.stringify(values) !==
                      JSON.stringify(initialValues) ? (
                        <Button className="w-100" type="submit">
                          UPDATE
                        </Button>
                      ) : null}
                      <Button
                        className="w-100 mt-2 btn-danger"
                        onClick={deleteHandler}
                      >
                        DELETE
                      </Button>
                    </Form>
                  );
                }}
              </Formik>
            </>
          )
        )}
      </Container>
    </Container>
  );
};

export default SingleCustomer;
