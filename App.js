import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { Navbar, Nav, Container, Button, Card, Modal, Image, Form, Spinner, ProgressBar } from "react-bootstrap";
import "./App.css";
import BiodiversityDashboard from "./BiodiversityDashboard";
import WikipediaSummarizer from "./WikipediaSummarizer";

function App() {
    // State for Upload Image/Video Section
    const [file, setFile] = useState(null);
    const [filePreview, setFilePreview] = useState(null);
    const [fileName, setFileName] = useState("📂 Choose a file...");
    const [response, setResponse] = useState(null);
    const [showUploadModal, setShowUploadModal] = useState(false); // Separate modal state
    const [latitude, setLatitude] = useState(null);
    const [longitude, setLongitude] = useState(null);
    const [loading, setLoading] = useState(false);

    // State for Document Summarization Section
    const [docFile, setDocFile] = useState(null);
    const [docFileName, setDocFileName] = useState("📂 Choose a document...");
    const [docSummary, setDocSummary] = useState(null);
    const [docLoading, setDocLoading] = useState(false);

    // State for Satellite Image Analysis Section
    const [pastImage, setPastImage] = useState(null);
    const [recentImage, setRecentImage] = useState(null);
    const [report, setReport] = useState("");
    const [processedImage, setProcessedImage] = useState(null);
    const [showForestModal, setShowForestModal] = useState(false); // Separate modal state
    const [forestLoading, setForestLoading] = useState(false);
    const [error, setError] = useState("");

    // Handle file upload for Satellite Image Analysis
    const handleFileChange1 = (e, setImage) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
        }
    };

    // Handle Satellite Image Analysis
    const handleAnalyze = async () => {
        if (!pastImage || !recentImage) {
            setError("Please upload both past and recent images.");
            return;
        }

        setError("");
        setForestLoading(true);

        const formData = new FormData();
        formData.append("past", pastImage);
        formData.append("recent", recentImage);

        try {
            const response = await fetch("http://localhost:8000/analyze", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            console.log("Response Data:", data);

            setReport(data.report);

            if (data.processed_image) {
                if (data.processed_image.startsWith("/")) {
                    setProcessedImage(`http://localhost:8000${data.processed_image}`);
                } else if (data.processed_image.startsWith("data:image")) {
                    setProcessedImage(data.processed_image);
                } else {
                    setError("Invalid image format received.");
                }

                setShowForestModal(true); // Show forest modal
            } else {
                setError("Processed image not received from the server.");
            }
        } catch (err) {
            console.error("Error:", err);
            setError("An error occurred while processing the images.");
        }
        setForestLoading(false);
    };

    // Fetch user location
    const fetchLocation = () => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setLatitude(position.coords.latitude);
                    setLongitude(position.coords.longitude);
                },
                (error) => console.error("Error fetching location:", error)
            );
        } else {
            console.error("Geolocation is not supported by this browser.");
        }
    };

    useEffect(() => {
        fetchLocation();
    }, []);

    // Handle file upload for Image/Video Section
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setFilePreview(URL.createObjectURL(selectedFile));
            setFileName(`📁 ${selectedFile.name}`);
        }
    };

    // Handle Image/Video upload
    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }

        if (!latitude || !longitude) {
            alert("Unable to get location. Please allow location access and try again.");
            return;
        }

        setLoading(true);

        const formData = new FormData();
        formData.append("file", file);
        formData.append("latitude", latitude);
        formData.append("longitude", longitude);

        try {
            const res = await axios.post("http://localhost:8000/upload/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            console.log("API Response:", res.data);

            if (res.data.confidence === undefined) {
                throw new Error("Invalid response format");
            }

            setResponse(res.data);
            setShowUploadModal(true); // Show upload modal
        } catch (error) {
            console.error("Upload failed", error);
            alert("Error uploading file. Please try again.");
        } finally {
            setLoading(false);
            setFile(null);
            setFilePreview(null);
            setFileName("📂 Choose a file...");
            document.getElementById("fileInput").value = ""; // Reset input field
        }
    };

    // Handle document upload for summarization
    const handleDocChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setDocFile(selectedFile);
            setDocFileName(`📁 ${selectedFile.name}`);
        }
    };

    const handleDocUpload = async () => {
        if (!docFile) {
            alert("Please select a document to summarize.");
            return;
        }

        setDocLoading(true);
        const formData = new FormData();
        formData.append("file", docFile);

        try {
            const res = await axios.post("http://localhost:8000/summarize_pdf/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            console.log("API Response:", res.data);

            if (res.data && res.data.summary) {
                setDocSummary(res.data.summary);
            } else {
                alert("Unexpected response format. Check console.");
                console.error("Unexpected response:", res.data);
            }
        } catch (error) {
            console.error("Document summarization failed", error);
            alert("Error summarizing document. Please try again.");
        } finally {
            setDocLoading(false);
        }
    };

    return (
        <>
            {/* Navbar */}
            <Navbar expand="lg" className="gradient-navbar" variant="dark" fixed="top">
                <Container>
                    <Navbar.Brand href="#home">🌿 Bio Guardian</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ms-auto">
                            <Nav.Link href="#home">Home</Nav.Link>
                            <Nav.Link href="#about">About</Nav.Link>
                            <Nav.Link href="#upload">Upload</Nav.Link>
                            <Nav.Link href="#contact">Contact</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>

            {/* Home Section */}
            <section id="home" className="hero-section">
                <Container className="text-center text-white">
                    <h1 className="display-3 fw-bold">Guarding Nature with AI 🌏</h1>
                    <p className="lead">Analyze images & videos to detect endangered species. Let's protect wildlife together! 🦜🌿</p>
                    <a href="#upload"><Button className="custom-button" size="lg">Start Analyzing 🧐</Button></a>
                </Container>
            </section>

            {/* About Section */}
            <section id="about" className="py-abc">
                <Container>
                    <h2 className="text-center text-success">🌍 About Bio Guardian</h2>
                    <p className="text-center">
                        Bio Guardian is an AI-powered system that analyzes images and videos to identify endangered species.
                        It helps conservationists protect wildlife by detecting threats and monitoring biodiversity.
                    </p>
                    <h4 className="text-center text-success">Why it matters?</h4>
                    <p className="text-center">
                        With growing environmental threats, Bio Guardian empowers organizations, wildlife researchers, and governments with real-time insights to take timely action and protect nature.
                        It’s a powerful tool in the fight against biodiversity loss and climate change.
                    </p>
                </Container>
            </section>

            {/* Upload Image/Video Section */}
            <section id="upload" className="py-5">
                <Container className="text-center">
                    <h2 className="text-center text-green">Upload Image/Video 📷</h2>
                    <Card className="p-4 shadow-lg mx-auto upload-card">
                        <Form.Group controlId="fileInput" className="mb-3">
                            <Form.Label className="custom-file-label">{fileName}</Form.Label>
                            <Form.Control type="file" accept="image/*,video/*" onChange={handleFileChange} hidden />
                        </Form.Group>
                        {filePreview && (
                            <div className="mb-3">
                                {file?.type?.startsWith("image/") ? (
                                    <Image src={filePreview} alt="Preview" thumbnail style={{ maxHeight: "200px" }} />
                                ) : (
                                    <video controls width="100%" style={{ maxHeight: "200px" }}>
                                        <source src={filePreview} type={file?.type} />
                                        Your browser does not support the video tag.
                                    </video>
                                )}
                            </div>
                        )}
                        <Button className="custom-button" onClick={handleUpload} disabled={loading}>
                            {loading ? <Spinner animation="border" size="sm" /> : "Analyze 🧐"}
                        </Button>
                    </Card>
                </Container>
            </section>

            {/* Modal for Upload Image/Video Results */}
            <Modal show={showUploadModal} onHide={() => setShowUploadModal(false)} centered>
                <Modal.Header closeButton style={{ backgroundColor: "#e8f5e9" }}>
                    <Modal.Title style={{ color: "#388e3c" }}>🌿 AI Wildlife Analysis</Modal.Title>
                </Modal.Header>
                <Modal.Body className="text-center" style={{ backgroundColor: "#f1f8e9" }}>
                    {response ? (
                        <>
                            <h4 style={{ color: "#2e7d32" }}>🐾 Identified Species: <strong>{response.species}</strong></h4>
                            <h5>📊 Confidence:
                                <ProgressBar
                                    now={response.confidence}
                                    label={`${response.confidence.toFixed(2)}%`}
                                    variant={response.confidence > 80 ? "success" : "warning"}
                                    style={{ backgroundColor: "#a5d6a7" }}
                                />
                            </h5>
                            <h5>📍 Location:
                                <a
                                    href={`https://www.google.com/maps?q=${response.latitude},${response.longitude}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    style={{ color: "#1b5e20" }}
                                >
                                    View on Maps
                                </a>
                            </h5>
                            <h5>⚠️ Status:
                                <strong className={response.endangered ? "text-danger" : "text-success"}>
                                    {response.endangered ? "Endangered - Immediate Action Needed!" : "Not Endangered - Safe"}
                                </strong>
                            </h5>
                            <h5>🔢 Count: <strong>{response.count}</strong></h5>
                        </>
                    ) : (
                        <Spinner animation="border" />
                    )}
                </Modal.Body>
                <Modal.Footer style={{ backgroundColor: "#e8f5e9" }}>
                    <Button
                        variant="success"
                        onClick={() => setShowUploadModal(false)}
                        style={{ backgroundColor: "#388e3c", borderColor: "#388e3c" }}
                    >
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>

            {/* Document Summarization Section */}
            <section className="py-abc">
                <div className="flex items-center justify-center h-screen w-screen bg-green-200">
                    <div className="bg-green-700 p-8 rounded-lg shadow-xl text-black w-full max-w-lg text-center">
                        <WikipediaSummarizer />
                    </div>
                </div>
            </section>

            {/* Summarize Documents Section */}
            <section id="summarize" className="py-5 bg-light">
                <Container className="text-center">
                    <h2 className="text-center text-green">Summarize Documents 📜</h2>
                    <Card className="p-4 shadow-lg mx-auto upload-card">
                        <Form.Group controlId="docFileInput" className="mb-3">
                            <Form.Label className="custom-file-label">{docFileName}</Form.Label>
                            <Form.Control type="file" accept=".txt,.pdf" onChange={handleDocChange} hidden />
                        </Form.Group>

                        <Button className="custom-button" onClick={handleDocUpload} disabled={docLoading}>
                            {docLoading ? <Spinner animation="border" size="sm" /> : "Summarize 📄"}
                        </Button>
                        {docSummary && (
                            <Card className="mt-3 p-3 text-start bg-white">
                                <h5 className="text-success">Summary:</h5>
                                <p>{docSummary}</p>
                            </Card>
                        )}
                    </Card>
                </Container>
            </section>

            {/* Biodiversity Dashboard */}
            <div>
                <BiodiversityDashboard />
            </div>

            {/* Satellite Image Analysis Section */}
            <section id="forest" className="py-5">
                <Container className="text-center">
                    <h2 className="text-center text-green">🌲 Satellite Image Analysis 📷</h2>
                    <Card className="p-4 shadow-lg mx-auto upload-card" style={{ maxWidth: "600px" }}>
                        {/* Past Image Upload */}
                        <Form.Group controlId="pastImageUpload" className="mb-3">
                            <Form.Label className="fw-bold">Upload Past Image</Form.Label>
                            <Form.Control type="file" accept="image/*" onChange={(e) => handleFileChange1(e, setPastImage)} />
                            {pastImage && <Image src={URL.createObjectURL(pastImage)} thumbnail className="mt-2" style={{ maxHeight: "200px" }} />}
                        </Form.Group>

                        {/* Recent Image Upload */}
                        <Form.Group controlId="recentImageUpload" className="mb-3">
                            <Form.Label className="fw-bold">Upload Recent Image</Form.Label>
                            <Form.Control type="file" accept="image/*" onChange={(e) => handleFileChange1(e, setRecentImage)} />
                            {recentImage && <Image src={URL.createObjectURL(recentImage)} thumbnail className="mt-2" style={{ maxHeight: "200px" }} />}
                        </Form.Group>

                        {/* Analyze Button */}
                        <Button className="custom-button w-100" onClick={handleAnalyze} disabled={forestLoading}>
                            {forestLoading ? <Spinner animation="border" size="sm" /> : "Analyze 🧐"}
                        </Button>

                        {/* Error Message */}
                        {error && <p className="mt-2 text-danger">{error}</p>}
                    </Card>
                </Container>
            </section>

            {/* Modal for Satellite Image Analysis Results */}
            <Modal show={showForestModal} onHide={() => setShowForestModal(false)} centered>
                <Modal.Header closeButton style={{ backgroundColor: "#e8f5e9" }}>
                    <Modal.Title style={{ color: "#388e3c" }}>🌿 AI Forest Analysis</Modal.Title>
                </Modal.Header>
                <Modal.Body className="text-center" style={{ backgroundColor: "#f1f8e9" }}>
                    {report && <pre className="p-3 bg-light border rounded text-start">{report}</pre>}
                    {processedImage && <Image src={processedImage} alt="Processed" thumbnail className="mt-3" style={{ maxHeight: "250px" }} />}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowForestModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>

            {/* Footer */}
            <footer className="gradient-footer text-center text-white py-3">
                © 2025 Bio Guardian | AI for Wildlife Protection
            </footer>
        </>
    );
}

export default App;