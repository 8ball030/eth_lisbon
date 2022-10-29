import React, { useState } from 'react';
import { Table, Tag, Typography } from 'antd';
import axios from 'axios';
import { AgentTableContainer } from './styles';

const { Title } = Typography;
const baseURL = 'http://146.190.230.176:5000/peers/1';

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
    title: 'Tags',
    key: 'agent_state',
    dataIndex: 'agent_state',
    render: (aState) => {
      console.log(aState)
      let color = 'green';
      if (aState === 'PriceEstimationRound') {
        color = 'volcano';
      }
      return (
        <Tag color={color} key={aState}>
          {(aState||'').toUpperCase()}
        </Tag>
      );
    },
  },
];

const data = [
  {
    key: '1',
    agent_address: '0xaddress',
    agent_state: 'PriceEstimationRound',
  },
  {
    key: '2',
    agent_address: '0xaddress',
    agent_state: 'PriceEstimationRound',
  },
  {
    key: '3',
    agent_address: '0xaddress',
    agent_state: 'Abc',
  },
];

const AgentTable = () => {
  const [agentData, setAgentData] = useState(null);

  React.useEffect(() => {
    axios
      .get(baseURL, {
        withCredentials: false,
      })
      .then((response) => {
        setAgentData(response);
      })
      .catch((e) => {
        console.error('Some error occured!', e);

        // TODO: remove once cors is fixed
        setAgentData(data);
      });
  }, []);

  console.log(agentData);

  return (
    <AgentTableContainer>
      <Title level={2}>Agent Table</Title>
      <Table columns={columns} dataSource={data} bordered pagination={false} />
    </AgentTableContainer>
  );
};

export default AgentTable;
