
import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "bootstrap/dist/css/bootstrap.min.css";
import DataUploadChart from "./DataUploadChart.js";
import "./BiodiversityDashboard.css";

const data = [
  { year: 2015, species: 50 },
  { year: 2016, species: 65 },
  { year: 2017, species: 80 },
  { year: 2018, species: 75 },
  { year: 2019, species: 90 },
  { year: 2020, species: 100 },
];

// ✅ 12 Biodiversity Hotspots in India
const biodiversityCenters = [
  { name: "Sundarbans National Park", lat: 21.9497, lng: 88.8636 },
  { name: "Kaziranga National Park", lat: 26.6666, lng: 93.33 },
  { name: "Western Ghats", lat: 10.3529, lng: 76.5123 },
  { name: "Great Himalayan National Park", lat: 31.8500, lng: 77.3667 },
  { name: "Nanda Devi Biosphere Reserve", lat: 30.4000, lng: 79.7000 },
  { name: "Manas National Park", lat: 26.6592, lng: 91.0011 },
  { name: "Periyar Wildlife Sanctuary", lat: 9.4669, lng: 77.2399 },
  { name: "Gir Forest National Park", lat: 21.1240, lng: 70.8240 },
  { name: "Silent Valley National Park", lat: 11.1234, lng: 76.1234 },
  { name: "Namdapha National Park", lat: 27.5000, lng: 96.5000 },
  { name: "Simlipal National Park", lat: 21.7562, lng: 86.3495 },
  { name: "Ranthambore National Park", lat: 26.0173, lng: 76.5026 },
];

// ✅ Custom Red Marker Icon
const redIcon = new L.Icon({
  iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const BiodiversityDashboard = () => {
  const [theme, setTheme] = useState("light");

  return (
    <section className="hiii">

   
    <div className={`container-fluid p-5 ${theme}`}>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="fw-bold"><span role="img" aria-label="leaf">🌱</span> Biodiversity Dashboard</h1>
        <select className="form-select w-auto" onChange={(e) => setTheme(e.target.value)}>
          <option value="light">Light Mode</option>
          <option value="dark">Dark Mode</option>
          <option value="midnight-blue">Midnight Blue</option>
          <option value="forest">Forest</option>
        </select>
      </div>

      <div className="row g-4 mb-4">
        {["Total Species: 5,320", "Endangered Species: 1,230", "New Discoveries: 47", "Conservation Projects: 120"].map((item, index) => (
          <div key={index} className="col-md-3">
            <div className="card shadow-lg p-3 text-center">
              <h5 className="fw-semibold">{item.split(":")[0]}</h5>
              <p className="fs-4 fw-bold">{item.split(":")[1]}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="row g-4">
        <div className="col-md-6">
          <div className="card p-4 shadow-lg rounded-3">
            <h5 className="fw-bold mb-3">📈 Biodiversity Over Time</h5>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={data}>
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="species" stroke="#28a745" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card p-4 shadow-lg rounded-3">
            <h5 className="fw-bold mb-3">🌍 Biodiversity Map (India)</h5>
            <MapContainer center={[22, 79]} zoom={5.5} className="w-100" style={{ height: "300px" }}>
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              
              {biodiversityCenters.map((center, index) => (
                <Marker key={index} position={[center.lat, center.lng]} icon={redIcon}>
                  <Popup><b>{center.name}</b></Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>
        </div>
      </div>

      <div className="row g-4 mt-4">
        <div className="col-md-6">
          <div className="card p-4 shadow-lg rounded-3">
            <h5 className="fw-bold mb-3">Recent Updates</h5>
            <ul className="list-unstyled">
              <li>🌱 New species discovered in Amazon rainforest.</li>
              <li>🌎 Conservation project launched in Africa.</li>
              <li>🦜 Study reveals migration patterns of rare birds.</li>
            </ul>
          </div>
        </div>
        
        <div className="col-md-6">
          <div className="card p-4 shadow-lg rounded-3">
            <h5 className="fw-bold mb-3">Contribute to Biodiversity</h5>
            <p>Submit observations and help conservation efforts.</p>
            <button className="btn btn-success w-100">Upload Report</button>
          </div>
        </div>
      </div>

      {/* ✅ Data Upload Chart Ensured */}
      <div className="row g-4 mt-4">
        <div className="col-md-12">
          <div className="card p-4 shadow-lg rounded-3">
            <h5 className="fw-bold mb-3">📊 Upload Biodiversity Data</h5>
            <DataUploadChart /> 
          </div>
        </div>
      </div>
    </div>
    </section>
  );
};

export default BiodiversityDashboard;