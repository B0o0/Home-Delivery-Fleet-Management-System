import React from "react";
import { Container, Form } from "react-bootstrap";
import MainPageText from "../../component/MainPageText/MainPageText";
import CustomInput from "../../component/CustomInput/CustomInput";
import { faEnvelope } from "@fortawesome/free-solid-svg-icons";
import ContactUsForm from "../../component/ContactUsForm/ContactUsForm";
const ContactUs = () => {
  return (
    <Container fluid>
      <MainPageText text="Contact Us" />
      <Container className="my-5 pb-4 bg-white rounded-2 shadow-sm">
        <MainPageText text="How To Find Us" />
        <ContactUsForm />
      </Container>
    </Container>
  );
};

export default ContactUs;
