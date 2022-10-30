/* eslint-disable react/prop-types */
import React, { useState, createContext } from 'react';

export const DataContext = createContext({});

export const DataProvider = ({ children }) => {
  const [provider, setProvider] = useState(null);
  const [web3Provider, setWeb3Provider] = useState(null);
  const [predictedData, setPredictedData] = useState(null);
  const [lastPredictedPrice, setLastPredictedPrice] = useState(null);
  const [eventsData, setEventsData] = useState({});

  return (
    <div>
      <DataContext.Provider
        value={{
          provider,
          setProvider,
          web3Provider,
          setWeb3Provider,
          predictedData,
          setPredictedData,
          eventsData,
          setEventsData,
          lastPredictedPrice,
          setLastPredictedPrice,
        }}
      >
        {children}
      </DataContext.Provider>
    </div>
  );
};
