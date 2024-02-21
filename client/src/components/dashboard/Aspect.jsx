import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { CircularProgress } from "@mui/material";
import axios from "axios";

const Aspect = ({ data }) => {
  const [loading, setLoading] = React.useState(true);
  const [aspects, setAspects] = React.useState([]);

  React.useEffect(() => {
    // if (data.sva) {
    //     const svaData = data.sva;
    //     setSvaData(svaData);
    //     setLoading(false);
    // }
    const fetchData = async () => {
      const title = data.name;
      // check if title has spaces and replace with %20
      await axios
        .get('http://127.0.0.1:5000/absa')
        .then((res) => {
          console.log(res.data);
          setAspects(res.data);
          setLoading(false);
        })
        .catch((err) => {
          console.log(err);
        });
    };
    fetchData();
  }, [data]);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div
          style={{
            backgroundColor: "#fff",
            padding: "5px",
            border: "1px solid #ccc",
          }}
        >
          <p>{`${data.aspect} : ${data.score.toFixed(2)} (${data.label})`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <>
      {loading ? (
        <CircularProgress />
      ) : (
        <BarChart width={700} height={300} data={aspects}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="aspect" />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar dataKey="score" fill="#8884d8" />
        </BarChart>
      )}
    </>
  );
};

export default Aspect;
