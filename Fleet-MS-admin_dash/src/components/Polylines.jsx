
import React, { useState, useEffect } from "react";
import { Polyline } from "react-google-maps";
import DriverIconRed  from "../icons/driverRed.png";
import DriverIconOrange  from "../icons/driverOrange.png";
import DriverIconGreen  from "../icons/driverGreen.png";
import { Icon } from "@mui/material";

  
export default function PolyLines({socket}) {

    const [BluePolyLine, setBluePolyLine] = useState({});
    const [RedPolyLine, setRedPolyLine] = useState({});


    function getPolyLine(obj,color){
      const PolylineArray = [];
      Object.keys(obj).forEach(function(key, index) {
        const polyLine = obj[key];
        PolylineArray.push(
          <Polyline
          key={key}
          path={polyLine}
          options={{
            strokeColor: color,
          }}
          />
        )
      })
      return PolylineArray
    }


    function objectify(array) {
      var objs = array.map(x => ({ 
        lat: x[0], 
        lng: x[1] 
      }));
      return objs
  }
    
    useEffect(() => {

      socket.on('setBluePolyLine', (Polyline) => {
        const driverNumber = Object.keys(Polyline)[0]
        const PolylineArray = Polyline[driverNumber]
        const polyLine = objectify(PolylineArray)        
        Polyline[driverNumber] = polyLine

        setBluePolyLine(PolyLines => ({
          ...PolyLines,
          ...Polyline
        }));
      });

      socket.on('setRedPolyLine', (Polyline) => {
        const driverNumber = Object.keys(Polyline)[0]
        const PolylineArray = Polyline[driverNumber]
        const polyLine = objectify(PolylineArray)        
        Polyline[driverNumber] = polyLine

        setRedPolyLine(PolyLines => ({
          ...PolyLines,
          ...Polyline
        }));
      });


      socket.on('removeRedPolylineStep', (driver_num) => {
        setRedPolyLine(PolyLines => {
          if (PolyLines !== undefined){
          const Polyline = PolyLines[driver_num];
          if (Polyline !== undefined){
          const NewPolyline = Polyline.slice(1, Polyline.length)
          const newPolylineInState = {}
          newPolylineInState[driver_num] = NewPolyline
          return {...PolyLines, ...newPolylineInState}
          };
        }

        });
      });

      socket.on('removeBluePolylineStep', (driver_num) => {
        setBluePolyLine(PolyLines => {
          if (PolyLines !== undefined){
          const Polyline = PolyLines[driver_num];
          console.log("Polyline", Polyline);
          if (Polyline !== undefined){
          const NewPolyline = Polyline.slice(1, Polyline.length)
          const newPolylineInState = {}
          newPolylineInState[driver_num] = NewPolyline
          return {...PolyLines, ...newPolylineInState}
          };
        }
        });

      });


    }, []);
  

    return (
      <div>
        {
        typeof RedPolyLine === 'object' && 
        RedPolyLine !== undefined &&
        Object.keys(BluePolyLine).length > 0 
        ? 
        (getPolyLine(BluePolyLine, '#669Df6'))
        :
        ('')
        }
        {
        typeof RedPolyLine === 'object' && 
        RedPolyLine !== undefined &&
        Object.keys(BluePolyLine).length > 0 
        ? 
        (getPolyLine(RedPolyLine, '#F75D59'))
        :
        ('')
        }

      </div>
    );
  }

  // {ActiveDrivers.map(driver => (
  //   <Marker
  //     key={driver.number}
  //     position={{
  //       lat: driver.lat,
  //       lng: driver.lng
  //     }}
  //     onClick={() => {
  //       setSelectedMarker(driver);
  //     }}
  //     icon={{
  //       url:  "https://img.icons8.com/fluency/48/delivery-scooter.png",
  //       scaledSize: new window.google.maps.Size(30, 30)
  //     }}
  //   />
  // ))}