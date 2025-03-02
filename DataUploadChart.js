import React, { useState } from "react";
import { Bar } from "react-chartjs-2";
import * as XLSX from "xlsx";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// ✅ Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const DataUploadChart = () => {
  const [chartData, setChartData] = useState(null);
  const [speciesMap, setSpeciesMap] = useState({}); // Store year-wise species names

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.readAsBinaryString(file);
    reader.onload = (e) => {
      const data = e.target.result;
      const workbook = XLSX.read(data, { type: "binary" });
      const sheetName = workbook.SheetNames[0];
      const sheet = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);

      processChartData(sheet);
    };
  };

  const processChartData = (data) => {
    if (!data || data.length === 0) return;

    // ✅ Extract column names dynamically
    const firstRow = data[0];
    const yearKey = Object.keys(firstRow).find((key) => key.toLowerCase().includes("year"));
    const countKey = Object.keys(firstRow).find((key) => key.toLowerCase().includes("count"));
    const speciesKey = Object.keys(firstRow).find((key) => key.toLowerCase().includes("species name"));

    if (!yearKey || !countKey || !speciesKey) {
      alert("Invalid file format! Ensure it has 'Year', 'Species Count', and 'Species Name' columns.");
      return;
    }

    const labels = data.map((row) => row[yearKey]);
    const values = data.map((row) => row[countKey]);
    const speciesData = data.reduce((acc, row) => {
      acc[row[yearKey]] = row[speciesKey];
      return acc;
    }, {});

    setSpeciesMap(speciesData);

    setChartData({
      labels: labels,
      datasets: [
        {
          label: "Species Count",
          data: values,
          backgroundColor: "rgba(75, 192, 192, 0.6)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    });
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Upload Dataset</h2>
      <input type="file" accept=".xlsx, .csv" onChange={handleFileUpload} className="mb-4" />

      {chartData && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">Biodiversity Chart</h3>
          <Bar
            data={chartData}
            options={{
              responsive: true,
              plugins: {
                legend: { display: true },
                title: { display: true, text: "Biodiversity Trends" },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      let year = context.label;
                      let count = context.raw;
                      let species = speciesMap[year] || "Unknown";
                      return `Species Count: ${count} | ${species}`;
                    },
                  },
                },
              },
            }}
          />
        </div>
      )}
    </div>
  );
};

export default DataUploadChart;
