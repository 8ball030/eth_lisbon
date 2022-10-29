/* eslint-disable react/prop-types */
import React, { useState } from 'react';
import dynamic from 'next/dynamic';

import { Typography, Radio } from 'antd';
import { ChartContainer } from './styles';

const ChartComponent = dynamic(() => import('./Chart'), { ssr: false });

const { Title: Header } = Typography;

const LineChart = ({ ftxData }) => {
  const [size, setSize] = useState('1');

  return (
    <ChartContainer>
      <Header level={2}>BTC - USD Price Prophet</Header>

      <Radio.Group value={size} onChange={(e) => setSize(e.target.value)}>
        <Radio.Button value="1">Prediction</Radio.Button>
        <Radio.Button value="2">ROC</Radio.Button>
      </Radio.Group>

      <ChartComponent ftxData={ftxData} />
    </ChartContainer>
  );
};

export default LineChart;
