
import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import {
    withScriptjs,
    withGoogleMap,
    GoogleMap,
    InfoWindow,
  } from "react-google-maps";
import Markers from "../../components/Markers";
import SimDialog from "../../components/SimModal";
import { io } from 'socket.io-client';
import { assignOrder } from "../../api/assignOrder";
import PolyLines from "../../components/Polylines";
import AssignOrderSnackbars from "../../components/assignOrdersnackBar";

const SOCKET_URL = import.meta.env.VITE_APP_SOCKET_URL;
const SOCKET_PATH = import.meta.env.VITE_APP_SOCKET_PATH;

const socket = io(SOCKET_URL, {path: SOCKET_PATH});
  
  function Map() {
    const [selectedMarker, setSelectedMarker] = useState(null);
    useEffect(() => {

      function onConnect() {
        console.log("onConnect");
      }
  
      function onDisconnect() {
        console.log("onDisconnect");
      }
  
      socket.on('connect', onConnect);
      socket.on('disconnect', onDisconnect);




      const listener = e => {
        if (e.key === "Escape") {
          setSelectedMarker(null);
        }
      };

      window.addEventListener("keydown", listener);
      return () => {
        window.removeEventListener("keydown", listener);
      };
    }, []);
  

    return (
      <GoogleMap
        defaultZoom={13}
        defaultCenter={{ lat: 30.1491, lng: 31.6290}}
        onClick={ev => {
          console.log("latitide = ",  ev.latLng.lat());
          console.log("longitude = ", ev.latLng.lng());
          setSelectedMarker(null);
        }}
      >
        <Markers 
        setSelectedMarker={setSelectedMarker}
        socket={socket}
        />
        <PolyLines
        socket={socket}
        />

        {selectedMarker && (
          <InfoWindow
            onCloseClick={() => {
              setSelectedMarker(null);
            }}
            position={{
              lat: selectedMarker.lat,
              lng: selectedMarker.lng
            }}
          >
            <div>
            <span><strong>Driver name: </strong>{selectedMarker.name}</span>
              <br/>
              <span><strong>Driver status: </strong> {selectedMarker.status}</span>
              <br/>
              {selectedMarker.order.delivery_address !== undefined ? (
              <>
                <span><strong>Delivery address: </strong>{selectedMarker.order.delivery_address}</span>
                <br/>
                <span><strong>Delivery status: </strong>{selectedMarker.order.status}</span>
                <br/>
                <span><strong>Total cost: </strong> {selectedMarker.order.total_cost}</span>
                </>
              ):('')}
            </div>
          </InfoWindow>
        )}

      </GoogleMap>
      
    );
  }
  
  const MapWrapped = withScriptjs(withGoogleMap(Map));
  
  export default function MainMap() {
    const [open, setOpen] = useState(false);
    const [Message, setMessage] = useState("");
    const [MessageType, setMessageType] = useState("");

    function assignOrderHandler(){
      assignOrder().then((result) => {
        let keys = Object.keys(result);
        let message = result[keys[0]];
        if (result){
          setMessageType(keys[0]);
          setMessage(message);
          setOpen(true);
        }
        
      });
    }

    return (
      <div style={{ marginLeft: "5vh" }}>
      <SimDialog socket={socket}/>
      <Button
      onClick={assignOrderHandler}
      >
        Assign Order
      </Button>
      <div style={{ width: "93vw", height: "100vh" }}>
        <MapWrapped
          googleMapURL={`https://maps.googleapis.com/maps/api/js?key=AIzaSyAv4TshMqyQUcBc_oWM6w9hjlxIKqiUOvA&v=3.exp&libraries=geometry,drawing,places}`}
          loadingElement={<div style={{ height: `80%` }} />}
          containerElement={<div style={{ height: `100%` }} />}
          mapElement={<div style={{ height: `90%` }} />}
        />
      </div>
      <AssignOrderSnackbars
      setOpen={setOpen}
      open={open}
      message={Message}
      type={MessageType}
      />
      </div>
    
      );
}
  