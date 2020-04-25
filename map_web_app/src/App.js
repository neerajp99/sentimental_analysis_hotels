import React, { Component, useState, useEffect } from "react";
import "./App.css";
import mapboxgl from "mapbox-gl";
// Bring in react wrapper for mapbox
import ReactMapGL, { Marker, Popup } from "react-map-gl";
// Bring in map data
// import * as hotelsData from "./data/initial/bangkok.json";
// import * as hotelsData from "./check_data.json";
// Bring in marker icon
import marker from "./marker.png";
const hotelsData = require("./data/polarity/bangkok.json"); //with path

function App() {
  // Initialse viewport state
  const [viewport, setViewport] = useState({
    latitude: 13.7245601,
    longitude: 100.4930261,
    width: "100vw",
    height: "100vh",
    zoom: 10
  });

  // Checked hotel state
  const [checkedHotel, setCheckedHotel] = useState(null);

  // Use useEffect hook
  useEffect(() => {
    // Check the updated viewport
    // console.log(viewport);

    const listener = event => {
      if (event.key === "Escape") {
        setCheckedHotel(null);
      }
    };
    window.addEventListener("keydown", listener);
    return () => {
      window.removeEventListener("keydown", listener);
    };
  }, []);

  return (
    <div className="App">
      <ReactMapGL
        {...viewport}
        mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        mapStyle="mapbox://styles/neerajpandey99/ck9ebhrie05qx1iqpdgrzf46g"
        onViewportChange={viewport => {
          setViewport(viewport);
        }}
      >
        {hotelsData.map((hotel, index) => (
          <Marker
            key={index}
            latitude={parseFloat(hotel[2])}
            longitude={parseFloat(hotel[3])}
          >
            <img
              src={marker}
              alt="Hotel Icon"
              className="marker_icon"
              onClick={event => {
                event.preventDefault();
                setCheckedHotel(hotel);
              }}
            />
          </Marker>
        ))}

        {checkedHotel ? (
          <Popup
            latitude={parseFloat(checkedHotel[2])}
            longitude={parseFloat(checkedHotel[3])}
            onClose={() => {
              setCheckedHotel(null);
            }}
          >
            <div className="pop-up">
              <h2>{checkedHotel[0]}</h2>
              <h3>{checkedHotel[1]}</h3>
            </div>
          </Popup>
        ) : null}
      </ReactMapGL>
    </div>
  );
}

export default App;
