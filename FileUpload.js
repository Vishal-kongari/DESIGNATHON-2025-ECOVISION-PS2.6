import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");

  const handleFileUpload = async () => {
    if (!file) return alert("Please select a file!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/summarize_pdf/", formData);
      setSummary(response.data.summary);
    } catch (error) {
      console.error("File Upload Error:", error);
    }
  };

  return (
    <div>
      <h2>📂 Summarize PDF</h2>
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleFileUpload}>Upload & Summarize</button>
      {summary && <p><strong>Summary:</strong> {summary}</p>}
    </div>
  );
};

export default FileUpload;
