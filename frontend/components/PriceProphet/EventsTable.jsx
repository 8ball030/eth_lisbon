import React, { useContext } from 'react';
import { Table } from 'antd/lib';
import { DataContext } from 'common-util/context';

const columns = [
  {
    title: 'Events',
    dataIndex: 'events',
    key: 'events',
    render: (text) => (
      <a
        href={`https://cronoscan.com/tx/${text}`}
        target="_blank"
        rel="noreferrer"
        style={{ textDecoration: 'underline' }}
      >
        {text}
      </a>
    ),
  },
];

const EventsTable = () => {
  const { eventsData } = useContext(DataContext);
  const data = Object.keys(eventsData)
    .filter((e) => e.match(/^0x([A-Fa-f0-9]{64})$/))
    .map((e) => ({ events: e, key: e }));

  return (
    <Table
      columns={columns}
      dataSource={data}
      bordered
      pagination={false}
      rowKey="events"
    />
  );
};

export default EventsTable;