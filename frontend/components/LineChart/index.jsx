/* eslint-disable react/prop-types */
import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { Typography, Radio } from 'antd';
import { ChartContainer } from './styles';

const { Title: Header } = Typography;

const LineChart = ({ ftxData }) => {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
  );
  console.log(ftxData);

  const [size, setSize] = useState('1');

  React.useEffect(() => {
    const apiCall = async () => {
      try {
        // const response = await fetch('https://ftx.com/api/markets/BTC/USD/candles?resolution=60', {
        //   mode: 'no-cors',
        // });
        // console.log(response);
        // const values = await response.json();
        // console.log(values);
        // setFtxData(get(values, 'result') || []);
      } catch (error) {
        console.error('Some error occured!', error);
      }
    };
    apiCall();
  }, []);

  console.log(ftxData);

  const data = {
    labels: (ftxData || []).map((e) => new Date(e.startTime).toLocaleDateString()),
    datasets: [
      {
        label: 'Dataset 1',
        data: (ftxData || []).map((e) => e.close),
        // borderColor: 'rgb(255, 99, 132)',
        // backgroundColor: 'rgba(255, 99, 132, 0.5)',
        fill: {
          target: {
            value: 0,
          },
          below: 'rgb(255, 99, 132)',
          above: 'rgb(53, 162, 235)',
        },
        // // yAxisID: 'y-axis-0',
        // fill: false,
        // borderWidth: 0,
      },
    ],
  };

  return (
    <ChartContainer>
      <Header level={2}>BTC - USD Price Prophet</Header>

      <Radio.Group value={size} onChange={(e) => setSize(e.target.value)}>
        <Radio.Button value="1">Prediction</Radio.Button>
        <Radio.Button value="2">ROC</Radio.Button>
      </Radio.Group>

      <div id="line-chart-container">
        <Line
          options={{
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'BTC - USD Prediction',
              },
            },
            maintainAspectRatio: false,
            tension: 0.4,

          }}
          data={data}
          width={400}
          height={400}
        />
      </div>
    </ChartContainer>
  );
};

export default LineChart;
