import React from 'react';
import ReactWordcloud from 'react-wordcloud';

const Keyword = ({ data }) => {
    const wordCloudData = data.keywords.map(item => ({ text: item.word, value: item.score }));

    const options = {
        rotations: 0,
        rotationAngles: [0],
        fontFamily: 'Roboto, sans-serif',
        fontSizes: [20, 60],
        fontStyle: 'normal',
        fontWeight: 'normal',
        padding: 1,
        scale: 'sqrt',
        spiral: 'archimedean',
        transitionDuration: 1000
    };
    
    return (
        <div style={{ width: '500px', height: '250px' }}>
            <ReactWordcloud words={wordCloudData} options={options} />
        </div>
    )
}

export default Keyword;