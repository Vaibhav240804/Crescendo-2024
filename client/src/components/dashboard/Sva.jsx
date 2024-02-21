import React from 'react';
import {  LineChart, Line, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { CircularProgress } from '@mui/material';
import axios from 'axios';

const Sva = ({ data }) => {
  const [loading, setLoading] = React.useState(true);
  const [svaData, setSvaData] = React.useState([]);
  const [currSva, setCurrSva] = React.useState([]);

  React.useEffect(() => {
      // if (data.sva) {
      //     const svaData = data.sva;
      //     setSvaData(svaData);
      //     setLoading(false);
      // }
      const fetchData = async () => {
          await axios.get("http://127.0.0.1:5000/sva")
          .then((res) => {
            console.log(res.data);
          setSvaData(res.data);
          setCurrSva(res.data['now 7-d']);
          setLoading(false);
        })
        .catch((err) => {
          console.log(err);
        });
      };
      fetchData();
  }
  , [data]);

    return (
      <>
      {loading ?
            <CircularProgress /> 
        : (
        <LineChart width={700} height={250} data={svaData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
        )}
      </>
    );
}

export default Sva;