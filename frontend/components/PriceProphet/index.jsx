/* eslint-disable react/prop-types */
import React, { useContext } from 'react';
import dynamic from 'next/dynamic';
import get from 'lodash/get';
import {
  Typography, Card, Statistic, Row, Col,
} from 'antd/lib';
import { COLOR } from 'util/theme';
import { DataContext } from 'common-util/context';
import { ChartContainer } from './styles';
import EventsTable from './EventsTable';

const ChartComponent = dynamic(() => import('./Chart'), { ssr: false });

const { Title: Header } = Typography;

const ValueCard = ({ title, price }) => (
  <Col span={8}>
    <Card>
      <Statistic
        title={title}
        value={price / 10000}
        precision={2}
        valueStyle={{
          color: COLOR.PRIMARY,
        }}
        prefix="$"
      />
    </Card>
  </Col>
);

const LineChart = ({ ftxData }) => {
  const { predictedData, lastPredictedPrice } = useContext(DataContext);

  return (
    <ChartContainer>
      <Header level={2}>BTC - USD Price Prophet</Header>
      <Row gutter={16}>
        <ValueCard
          title="Predicted Price"
          price={get(predictedData, 'price') / 10000 || 0}
        />
        <ValueCard
          title="Last Predicted Price"
          price={get(lastPredictedPrice, 'price') / 10000 || 0}
        />
        <ValueCard
          title="Actual Price"
          price={get(ftxData[ftxData.length - 1], 'close') || 0}
        />
      </Row>
      <ChartComponent ftxData={ftxData} />
      <br />
      <EventsTable />
    </ChartContainer>
  );
};

export default LineChart;
