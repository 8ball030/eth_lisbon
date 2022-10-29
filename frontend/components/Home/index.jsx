/* eslint-disable react/prop-types */
import AgentTable from '../AgentTable';
import LineChart from '../LineChart';

const Component = ({ ftxData }) => (
  <>
    <AgentTable />
    <LineChart ftxData={ftxData} />
  </>
);

export default Component;
