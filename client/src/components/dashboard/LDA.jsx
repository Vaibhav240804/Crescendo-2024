import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const LDA = () => {
  const [data, setData] = useState([]);
  const [count, setCount] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/related_sentences"); // Adjust the URL as needed
      console.log(response.data);
      const countData = data.map((item) => ({
        name: item.name,
        count: item.sentences.length,
      }));
        setCount(countData);
        setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const item = data.find((item) => item.name === label);
      return (
        <div
          style={{
            backgroundColor: "#fff",
            padding: "5px",
            border: "1px solid #ccc",
          }}
        >
          <p>{`${label} : ${payload[0].value}`}</p>
          <p>Sentences:</p>
          <ul>
            {item.sentences.map((sentence, index) => (
              <li key={index}>{sentence}</li>
            ))}
          </ul>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <BarChart width={600} height={300} data={count}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Bar dataKey="count" fill="#8884d8" />
      </BarChart>
    </div>
  );
};

export default LDA;
