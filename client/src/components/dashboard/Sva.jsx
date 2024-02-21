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
        const title = data.name
        // check if title has spaces and replace with %20
        const titleArr = title.split(' ');
        const titleStr = titleArr.join('%20');
        const url = `https://serpapi.com/search.json?engine=google_trends&q=Colgate%20MaxFresh%20Toothpaste&date=now+7-d&tz=-540&data_type=TIMESERIES&gl=in&api_key=ec2c1ad96bd52a6d5e2e2517b652f836464b651290bfe851687da79c97ce9a3a`;
          await axios.get(url)
          .then((res) => {
            console.log(res.data);
            const currSvaData = res.data.interest_over_time.map((item) => {
              return {
                date: item.date,
                score: item.values.extracted_value
              };
            });
            setSvaData(currSvaData);
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