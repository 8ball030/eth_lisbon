/* eslint-disable react/prop-types */
import dynamic from 'next/dynamic';
import AgentTable from '../AgentTable';

const ChartComponent = dynamic(() => import('../PriceProphet'), { ssr: false });

const Component = ({ ftxData }) => (
  <>
    <AgentTable />
    <ChartComponent ftxData={ftxData} />
  </>
);

export default Component;
