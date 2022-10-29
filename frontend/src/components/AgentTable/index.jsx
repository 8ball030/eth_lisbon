import React, { useState } from 'react';
import axios from 'axios';
const baseURL = 'http://146.190.230.176:5000/peers/1';

const AgentTable = () => {
  const [post, setPost] = useState(null);

  React.useEffect(() => {
    axios
      .get(baseURL, {
        withCredentials: false,
      })
      .then((response) => {
        setPost(response);
      });
  }, []);

  return (
    <div>
      <header>
        <p>Agent table</p>
        <p>{JSON.stringify(post)}</p>
      </header>
    </div>
  );
};

export default AgentTable;
