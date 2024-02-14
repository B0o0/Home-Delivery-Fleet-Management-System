import React, { useState } from "react";
import {
  Navbar,
  Nav,
  Form,
  Container,
  InputGroup,
  Image,
  NavDropdown,
} from "react-bootstrap";
import DelImg from "../../assets/images/del.png";
import UserImg from "../../assets/images/pic.png";
import './style.css'
import { useSelector , useDispatch } from "react-redux";
import { authActions } from "../../store/authSlice";
import { Link } from "react-router-dom";
const TopNav = ({ isNotActive, setNotActive }) => {
  const dispatch = useDispatch()
  const userEmail = useSelector((state) => state.auth.userEmail);
  console.log(userEmail)
  var barsIcon = (
    <i className="fas fa-bars fs-2" style={{ color: "rgb(2, 36, 71)" }}></i>
  );
  var crossIcon = <i className="fa-solid fa-xmark fs-2"></i>;

  const logoutHandler = ()=>{
      dispatch(authActions.userLogout())
  }

  return (
    <Navbar
      className="shadow"
      bg="white"
      expand="lg"
      style={{ position: "fixed", top: "0", width: "100%", zIndex: "10" }}
    >
      <Container fluid>
        <button
          type="button"
          onClick={() => setNotActive(!isNotActive)}
          className="btn"
        >
          <span className={isNotActive ? "text-primary" : "hidden"}>
            {barsIcon}
          </span>
          <span className={isNotActive ? "text-primary hidden" : ""}>
            {crossIcon}
          </span>
        </button>
        <Navbar.Brand
          className="d-flex align-items-center justify-content-center mx-2"
          style={{ fontWeight: "800" }}
        >
          <img
            alt="logo"
            src={DelImg}
            width="50"
            height="50"
            className="d-inline-block align-top mx-2"
          />{" "}
          FAST <span className="text-primary">X</span>
        </Navbar.Brand>

        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll" className="justify-content-end">
          <Nav className="d-flex justify-content-center align-items-center">
            <Image
              alt="logo"
              src={UserImg}
              width="50"
              height="50"
              roundedCircle
              className="border border-1 border-primary p-1"
            />
            <NavDropdown title={userEmail} className="mx-4">
              <NavDropdown.Item className='d-flex justify-content-between align-items-center' onClick={logoutHandler}>
                Log Out
                <i class="fa-solid fa-right-from-bracket text-muted"></i>
                </NavDropdown.Item>
              <NavDropdown.Item className='d-flex justify-content-between align-items-center'>
                <Link to='/addadmin'>
                Add Admin
                </Link>
                <i class="fa-solid fa-user-plus text-muted"></i>
                 </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};
export default TopNav;
