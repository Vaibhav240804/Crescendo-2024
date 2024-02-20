import React from 'react';
import { LineChart, Line, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Sentiment = ({ data }) => {
    const sentimentData = [
        { name: 'Negative', value: parseFloat(data.sentiment.negative.toFixed(4)) },
        { name: 'Neutral', value: parseFloat(data.sentiment.neutral.toFixed(4)) },
        { name: 'Positive', value: parseFloat(data.sentiment.positive.toFixed(4)) }
    ];

    const colors = ['#FF5733', '#3498DB', '#58D68D'];

    return (
        <PieChart width={500} height={250}>
            <Pie
                data={sentimentData}
                cx={250}
                cy={100}
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
                label={({ name, value }) => `${name}: ${(value * 100).toFixed(2)}%`}
            >
                {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
            </Pie>
            <Tooltip />
            <Legend />
        </PieChart>
    )

}

export default Sentiment;