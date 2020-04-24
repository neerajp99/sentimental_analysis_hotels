import React, { Component, useState, useEffect } from "react";
import "./App.css";
import mapboxgl from "mapbox-gl";
// Bring in react wrapper for mapbox
import ReactMapGL, { Marker, Popup } from "react-map-gl";
// Bring in map data
import * as hotelsData from "./check_data.json";
// Bring in marker icon
import marker from "./marker.png";

function App() {
  // Initialse viewport state
  const [viewport, setViewport] = useState({
    latitude: 45.4211,
    longitude: -75.6903,
    width: "100vw",
    height: "100vh",
    zoom: 10
  });

  // Checked hotel state
  const [checkedHotel, setCheckedHotel] = useState(null);

  // Use useEffect hook
  useEffect(() => {
    // Check the updated viewport
    console.log(viewport);

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
        {hotelsData.features.map(hotel => (
          <Marker
            key={hotel.properties.PARK_ID}
            latitude={hotel.geometry.coordinates[1]}
            longitude={hotel.geometry.coordinates[0]}
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
            latitude={checkedHotel.geometry.coordinates[1]}
            longitude={checkedHotel.geometry.coordinates[0]}
            onClose={() => {
              setCheckedHotel(null);
            }}
          >
            <div>Hello world</div>
          </Popup>
        ) : null}
      </ReactMapGL>
    </div>
  );
}

export default App;
