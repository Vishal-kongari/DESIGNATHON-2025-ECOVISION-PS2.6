import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const MapComponent = () => {
  return (
    <div className="map-container">
      <h5 className="fw-bold mb-3">🌍 Biodiversity Map (India)</h5>
      <MapContainer center={[20, 78]} zoom={4} className="w-100" style={{ height: "250px" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={[23.2599, 77.4126]}>
          <Popup>Biodiversity Hotspot</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default MapComponent;
