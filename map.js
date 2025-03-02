import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

function MapView() {
    return (
        <MapContainer center={[0, 0]} zoom={3} style={{ height: "500px" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <Marker position={[0, 0]}>
                <Popup>Wildlife Threat Detected</Popup>
            </Marker>
        </MapContainer>
    );
}

export default MapView;

