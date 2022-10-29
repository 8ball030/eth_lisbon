import React, { useContext } from 'react';
import { Table } from 'antd';
import { DataContext } from 'common-util/context';

const columns = [
  {
    title: 'Events',
    dataIndex: 'name',
    key: 'name',
    render: (text) => text,
  },
];

const EventsTable = () => {
  const { eventsData } = useContext(DataContext);
  const data = Object.keys(eventsData)
    .filter((e) => e.match(/^0x([A-Fa-f0-9]{64})$/))
    .map((e) => ({ name: e, key: e }));

  return (
    <Table
      columns={columns}
      dataSource={data}
      bordered
      pagination={false}
      rowKey="agent_address"
    />
  );
};

export default EventsTable;
