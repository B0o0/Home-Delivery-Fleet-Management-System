import React, { useEffect } from "react";
import Home from "./pages/Home/Home";
import Map from "./pages/Map/Map";
import { Navigate, RouterProvider, createBrowserRouter } from "react-router-dom";
import MainNavigation from "./pages/MainNavigation/MainNavigation";
import LoginPage from "./pages/LoginPage/LoginPage";
import AddBuisness from "./pages/AddBuisness/AddBuisness";
import ContactUs from "./pages/ContactUs/ContactUs";
import { useDispatch, useSelector } from "react-redux";
import { getAllBusiness, getAllMarketOrders, getAllResOrders } from "./store/bus-actions";
import Buisness from "./pages/Buisness/Buisness";
import SingleBuisness from "./pages/SingleBuisness/SingleBuisness";
import BuisnessMenu from "./pages/BuisnessMenu/BuisnessMenu";
import { getAllCustomers } from "./store/customer-actions";
import { getAllOrders } from "./store/order-actions";
import Customers from "./pages/Customers/Customers";
import SingleCustomer from "./pages/SingleCustomer/SingleCustomer";
import SingleDriver from "./pages/SingleDriver/SingleDriver";
import Orders from "./pages/Orders/Orders";
import {
  getAllDrivers,
  getAllAvailableDrivers,
  getAllUnAvailableDrivers,
  getAllBusyDrivers,
} from "./store/driver-actions";
import Drivers from "./pages/Drivers/Drivers";
import PendingBuisness from "./pages/PendingBuisness/PendingBuisness";
import PendingDrivers from "./pages/PendingDrivers/PendingDrivers";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import SingleOrder from "./pages/SingleOrder/SingleOrder";
import AddAdmin from "./pages/AddAdmin/AddAdmin";

function App() {
  const dispatch = useDispatch();
  
  const toastToDisplay = useSelector((state) => state.toast.toast);
  const notify = (message, type, close) =>
    toast(message, {
      position: "top-right",
      autoClose: close,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
      type: type,
    });
  useEffect(() => {
    if (toastToDisplay.message === "") return;
    notify(toastToDisplay.message, toastToDisplay.type, toastToDisplay.close);
    return () => toast.dismiss();
  }, [toastToDisplay]);
  const isCustomerRequireRender = useSelector(
    (state) => state.customer.isRequireRender
  );
  const isRequireRender = useSelector(
    (state) => state.buisness.isRequireRender
  );

  const isPendingDriversRequireRender = useSelector(
    (state) => state.pendingDrivers.isRequireRender
  );
  const isDriversRequireRender = useSelector((state) => state.driver.isRequireRender);

  useEffect(() => {
    dispatch(getAllBusiness());
    dispatch(getAllResOrders());
    dispatch(getAllMarketOrders());
    
  }, [isRequireRender]);

  useEffect(() => {
    dispatch(getAllCustomers());
   
  }, [isCustomerRequireRender]);

  useEffect(() => {
    dispatch(getAllOrders());
  }, []);

  useEffect(() => {
    dispatch(getAllDrivers());
    dispatch(getAllAvailableDrivers());
    dispatch(getAllUnAvailableDrivers());
    dispatch(getAllBusyDrivers());
  }, [isDriversRequireRender , isPendingDriversRequireRender]);
  const routers = createBrowserRouter([
    {
      path: "",
      element: <MainNavigation />,
      children: [
        { path: "", element: <Home /> },
        { path: "/map", element: <Map /> },
        { path: "/addBuisness", element: <AddBuisness /> },
        { path: "/buisness", element: <Buisness /> },
        { path: "/buisness/:id", element: <SingleBuisness /> },
        { path: "/pendingBuisness", element: <PendingBuisness /> },
        { path: "/pendingDrivers", element: <PendingDrivers /> },
        { path: "/customers", element: <Customers /> },
        { path: "/customers/:id", element: <SingleCustomer /> },
        { path: "/drivers", element: <Drivers /> },
        { path: "/drivers/:id", element: <SingleDriver /> },
        { path: "/orders", element: <Orders /> },
        { path: "/orders/:id", element: <SingleOrder /> } , 
        { path: "/contactus", element: <ContactUs /> },
        { path: "/addadmin", element: <AddAdmin /> },
        
      ],
    },
    {
      path: "/login",
      element: <LoginPage />,
    },
  ]);
  
  return (
    <>
      <RouterProvider router={routers} />;
      <ToastContainer />
    </>
  );
}
export default App;
