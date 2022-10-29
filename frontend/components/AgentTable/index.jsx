import React, { useState } from 'react';
import { Table, Tag, Typography } from 'antd';
import { AgentTableContainer } from './styles';

const { Title } = Typography;
const baseURL = 'http://146.190.230.176:5000';

const columns = [
  {
    title: 'Name',
    dataIndex: 'agent_address',
    key: 'agent_address',
    render: (text) => text,
  },
  // {
  //   title: 'Address',
  //   dataIndex: 'address',
  //   key: 'address',
  // },
  {
    title: 'Agent State',
    key: 'agent_state',
    dataIndex: 'agent_state',
    render: (aState) => {
      let color = 'green';
      if (aState === 'PriceEstimationRound') {
        color = 'volcano';
      }
      return (
        <Tag color={color} key={aState}>
          {(aState || '').toUpperCase()}
        </Tag>
      );
    },
  },
];

const AgentTable = () => {
  const [agentData, setAgentData] = useState(null);

  React.useEffect(() => {
    const apiCall = async () => {
      try {
        const response = await fetch(`${baseURL}/peers`);
        const data = await response.json();
        setAgentData(data);
      } catch (error) {
        console.error('Some error occured!', error);
      }
    };
    apiCall();
  }, []);

  return (
    <AgentTableContainer>
      <Title level={2}>Agent Table</Title>
      <Table
        columns={columns}
        dataSource={agentData}
        bordered
        pagination={false}
        rowKey="agent_address"
      />
    </AgentTableContainer>
  );
};

export default AgentTable;
