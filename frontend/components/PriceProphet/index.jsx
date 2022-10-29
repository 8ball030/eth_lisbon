/* eslint-disable react/prop-types */
import React, { useContext } from 'react';
import dynamic from 'next/dynamic';
import get from 'lodash/get';
import {
  Typography, Card, Statistic, Row, Col,
} from 'antd';
import { COLOR } from 'util/theme';
import { DataContext } from 'common-util/context';
import { ChartContainer } from './styles';
import EventsTable from './EventsTable';

const ChartComponent = dynamic(() => import('./Chart'), { ssr: false });

const { Title: Header } = Typography;

const LineChart = ({ ftxData }) => {
  const { predictedData } = useContext(DataContext);

  return (
    <ChartContainer>
      <Header level={2}>BTC - USD Price Prophet</Header>
      <Row gutter={16}>
        <Col span={8}>
          <Card>
            <Statistic
              title="Predicted Data"
              value={get(predictedData, 'price') || 0}
              precision={2}
              valueStyle={{
                color: COLOR.PRIMARY,
              }}
              prefix="$"
            />
          </Card>
        </Col>
      </Row>
      <ChartComponent ftxData={ftxData} />
      <br />
      <EventsTable />
    </ChartContainer>
  );
};

export default LineChart;
