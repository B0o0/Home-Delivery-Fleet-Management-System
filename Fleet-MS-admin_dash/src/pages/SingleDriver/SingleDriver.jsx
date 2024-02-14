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
import { deleteDriver, getSingleDriver, updateDriver } from "../../store/driver-actions";
import updateDriverSchema from "../../validationSchema/updateDriverSchema";

const SingleDriver = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const dispatch = useDispatch();

  const selectedDriver = useSelector((state) => state.driver.selectedDriver);

  
  const isWaitingForGetDrivers = useSelector(
    (state) => state.driver.isWaitingForGetDrivers
  );
  const errorInGetDrivers = useSelector(
    (state) => state.driver.errorInGetDrivers
  );

  const isRequireRender = useSelector((state) => state.driver.isRequireRender);
  useEffect(() => {
    dispatch(getSingleDriver(id));
  }, [isRequireRender]);

  const navigateHandler = () => {
    navigate("/drivers", { replace: true });
  };
  const deleteHandler = () => {
      dispatch(deleteDriver(id, navigateHandler));
  };

 



  return (
    <Container fluid>
      <MainPageText text="Drivers" />
      <Container className="container my-5 pb-4 bg-white rounded-2 shadow-sm">
        <MainPageText text="Driver Information" />
        {isWaitingForGetDrivers ? (
          <SkeltonLoader />
        ) : errorInGetDrivers ? (
          <ErrorGettingData />
        ) : (
          selectedDriver &&
          Object.keys(selectedDriver).length > 0 && (
            <>
              <Formik
                initialValues={{
                  email: selectedDriver.email,
                  first_name: selectedDriver.first_name,
                  last_name: selectedDriver.last_name,
                  phone: selectedDriver.phone,
                  licence_id: selectedDriver.licence_id,
                  address: selectedDriver.address,
                }}
                validationSchema={updateDriverSchema}
                onSubmit={(values) => {
                  dispatch(updateDriver(id, values));
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
                        name="licence_id"
                        label="Licence"
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

export default SingleDriver;
