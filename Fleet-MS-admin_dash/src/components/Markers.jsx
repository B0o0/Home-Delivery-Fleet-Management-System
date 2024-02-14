
import React, { useState, useEffect } from "react";
import { Marker } from "react-google-maps";
import { get_restaurants } from "../api/getResturent";
import { get_orders } from "../api/getOrdres";
import { get_drivers } from "../api/getDrivers";
import DriverIconRed  from "../icons/driverRed.png";
import DriverIconOrange  from "../icons/driverOrange.png";
import DriverIconGreen  from "../icons/driverGreen.png";
import customerOrder from "../icons/customerOrder.png";
import buffaloBurger from "../icons/Rest/buffaloBurger.jpg";
  
export default function Markers({setSelectedMarker, socket}) {
    const [Orders, setOrders] = useState([]);
    const [Restaurants, setRestaurants] = useState([]);
    const [ActiveDrivers, setActiveDrivers] = useState({});
    const [BusyDrivers, setBusyDrivers] = useState({});
    const [NotAvailableDrivers, setNotAvailableDrivers] = useState({});



    function getDriversMarkers(obj, DriverIcon){
      const DriversMarkersArray = [];
      Object.keys(obj).forEach(function(key, index) {
        const driver = obj[key];
        DriversMarkersArray.push(
          <Marker
            key={key}
            position={{
              lat: driver.lat,
              lng: driver.lng
            }}
            onClick={() => {
              setSelectedMarker(driver);
              console.log("driver", driver);
            }}
            icon={{
              url: DriverIcon,
              scaledSize: new window.google.maps.Size(30, 30)
            }}
          />
        )
      })
      return DriversMarkersArray
    }


    useEffect(() => {

      get_orders().then(res =>{
        setOrders(res.orders);
      })

      get_restaurants().then(res =>{
        console.log(res.restaurants);
        setRestaurants(res.restaurants);
      })

      get_drivers().then(res =>{
        const allDrivers = res.drivers
        allDrivers.map ((driver) =>{
          const driverInState = {};
          driverInState[driver.number] = driver
          if (driver.status === 'busy'){
            setBusyDrivers(Driver => ({
              ...Driver,
              ...driverInState
            }));
          } else 
          if (driver.status === 'available') {
            setActiveDrivers(Driver => ({
              ...Driver,
              ...driverInState
            }));
          }else {
            setNotAvailableDrivers(Driver => ({
              ...Driver,
              ...driverInState
            }));
          }


        })
      })



      

      socket.on('setActiveDriver', (ActiveDriver) => {
        setActiveDrivers(Drivers => ({
          ...Drivers,
          ...ActiveDriver
        }));
      });

      socket.on('setBusyDriver', (BusyDriver) => {
        setBusyDrivers(Drivers => ({
          ...Drivers,
          ...BusyDriver
        }));
      });

      socket.on('setNotAvailableDriver', (NotAvailableDriver) => {
        setNotAvailableDrivers(Drivers => ({
          ...Drivers,
          ...NotAvailableDriver
        }));
      });


      socket.on('removeAvailbleMarker', (driverNumber) => {
        setActiveDrivers(Drivers => {
          delete Drivers[driverNumber];
          return Drivers
        });
      });


    }, []);
  

    return (
      <>
        {Restaurants.map(restaurant => (
          <Marker
            key={restaurant._id.$oid}
            position={{
              lat: restaurant.lat,
              lng: restaurant.lng
            }}
            onClick={() => {

              // setSelectedMarker(restaurant);
            }}
            icon={{
              url:  new URL(`../icons/Rest/${restaurant.icon}`, import.meta.url).href,
              scaledSize: new window.google.maps.Size(25, 25)
            }}
          />
        ))
        }
        {Orders.map(order => (
          <Marker
            key={order._id.$oid}
            position={{
              lat: order.lat,
              lng: order.lng
            }}
            onClick={() => {
              // setSelectedMarker(order);
            }}
            icon={{
              url:  customerOrder,
              scaledSize: new window.google.maps.Size(25, 25)
            }}
          />
        ))}
        {
        Object.keys(BusyDrivers).length > 0 ? 
        (getDriversMarkers(BusyDrivers, DriverIconOrange))
        :
        ('')
        }
        {
        Object.keys(ActiveDrivers).length > 0 ? 
        (getDriversMarkers(ActiveDrivers, DriverIconGreen))
        :
        ('')
        }
        {
        Object.keys(NotAvailableDrivers).length > 0 ? 
        (getDriversMarkers(NotAvailableDrivers, DriverIconRed))
        :
        ('')
        }
      </>
    );
  }
