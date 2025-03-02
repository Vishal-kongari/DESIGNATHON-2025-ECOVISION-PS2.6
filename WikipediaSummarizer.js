import React, { useState } from "react";
import axios from "axios";

const WikipediaSummarizer = () => {
  const [keywords, setKeywords] = useState("");
  const [summary, setSummary] = useState("");

  const handleFetchSummary = async () => {
    if (!keywords.trim()) return alert("Enter at least one keyword!");

    const formData = new FormData();
    formData.append("keywords", keywords);

    try {
      const response = await axios.post("http://127.0.0.1:8000/wikipedia_summary/", formData);
      setSummary(response.data.summary);
    } catch (error) {
      console.error("Wikipedia Fetch Error:", error);
    }
  };

  return (
    <div>
      <h2>🌍 Wikipedia Summarizer</h2>
      <input type="text" placeholder="Enter keywords..." onChange={(e) => setKeywords(e.target.value)} />
      <button onClick={handleFetchSummary}>Fetch Summary</button>
      {summary && <p><strong>Summary:</strong> {summary}</p>}
    </div>
  );
};

export default WikipediaSummarizer;
