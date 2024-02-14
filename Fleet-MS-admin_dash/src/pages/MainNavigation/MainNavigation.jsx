import React, { useState, useEffect } from "react";
import TopNav from "../../component/TopNav/TopNav";
import LeftNav from "../../component/LeftNav/LeftNav";
import { Navigate, Outlet } from "react-router-dom";
import "./style.css";
import { useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
const MainNavigation = () => {
  const isUserLoggedIn = useSelector((state) => state.auth.isLoggedIn);

  const currentRoute = useLocation();

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentRoute.pathname]);
  const [isNotActive, setNotActive] = useState("true");
  if (!isUserLoggedIn) return <Navigate to="/login" replace />;

  return (
    <>
      <TopNav isNotActive={isNotActive} setNotActive={setNotActive} />
      <div className="d-flex">
        <LeftNav isNotActive={isNotActive} setNotActive={setNotActive} />
        <div
          className="outlet container-fluid mt-4"
          style={{
            paddingLeft: isNotActive ? "4rem" : "16rem",
          }}
        >
          <Outlet />
        </div>
      </div>
    </>
  );
};

export default MainNavigation;
