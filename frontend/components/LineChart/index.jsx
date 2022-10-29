import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { Typography } from 'antd';
import { ChartContainer } from './styles';

const { Title: Header } = Typography;

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Chart.js Line Chart',
    },
  },
  maintainAspectRatio: false,
};

export const data = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'Dataset 1',
      data: [10, 54, 30, 40, 52, 5, 15],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
    },
    // {
    // label: 'Dataset 2',
    // data: labels.map(() => faker.datatype.number({ min: -1000, max: 1000 })),
    // borderColor: 'rgb(53, 162, 235)',
    // backgroundColor: 'rgba(53, 162, 235, 0.5)',
    // },
  ],
};

const LineChart = () => {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  );

  return (
    <ChartContainer>
      <Header level={2}>BTC - USD Price Prophet</Header>

      <div id="line-chart-container">
        <Line options={options} data={data} width={400} height={400} />
      </div>
    </ChartContainer>
  );
};

export default LineChart;
