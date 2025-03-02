import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { year: 2015, species: 50 },
  { year: 2016, species: 65 },
  { year: 2017, species: 80 },
  { year: 2018, species: 75 },
  { year: 2019, species: 90 },
  { year: 2020, species: 100 },
];

const BiodiversityChart = () => {
  return (
    <div className="chart-container">
      <h5 className="fw-bold mb-3">📈 Biodiversity Over Time</h5>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="species" stroke="#28a745" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BiodiversityChart;

