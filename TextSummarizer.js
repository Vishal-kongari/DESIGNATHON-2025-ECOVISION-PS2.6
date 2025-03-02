import React, { useState } from "react";
import axios from "axios";

const TextSummarizer = () => {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");

  const handleSummarize = async () => {
    if (!text.trim()) return alert("Please enter some text!");

    const formData = new FormData();
    formData.append("text", text);

    try {
      const response = await axios.post("http://127.0.0.1:8000/summarize_text/", formData);
      setSummary(response.data.summary);
    } catch (error) {
      console.error("Summarization Error:", error);
    }
  };

  return (
    <div>
      <h2>📝 Summarize Text</h2>
      <textarea
        rows="5"
        placeholder="Enter text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handleSummarize}>Summarize</button>
      {summary && <p><strong>Summary:</strong> {summary}</p>}
    </div>
  );
};

export default TextSummarizer;
