export const MAIN_CONTRACT_ADDRESS = '0x72dA4693A52e1e4aE8D1a00fdFb9Df5E39baa544';

export const MAIN_CONTRACT_ABI = [
  { inputs: [], stateMutability: 'nonpayable', type: 'constructor' },
  {
    anonymous: false,
    inputs: [
      {
        indexed: false,
        internalType: 'address',
        name: 'sender',
        type: 'address',
      },
      {
        indexed: false,
        internalType: 'uint256',
        name: 'rateOfChange',
        type: 'uint256',
      },
      {
        indexed: false,
        internalType: 'uint256',
        name: 'price',
        type: 'uint256',
      },
    ],
    name: 'LogPriceDataUpdated',
    type: 'event',
  },
  {
    anonymous: false,
    inputs: [
      {
        indexed: true,
        internalType: 'address',
        name: 'previousOwner',
        type: 'address',
      },
      {
        indexed: true,
        internalType: 'address',
        name: 'newOwner',
        type: 'address',
      },
    ],
    name: 'OwnershipTransferred',
    type: 'event',
  },
  {
    inputs: [],
    name: 'getPriceData',
    outputs: [
      {
        components: [
          {
            internalType: 'uint256',
            name: 'lastRateOfChange',
            type: 'uint256',
          },
          { internalType: 'uint256', name: 'rateOfChange', type: 'uint256' },
          { internalType: 'uint256', name: 'lastPrice', type: 'uint256' },
          { internalType: 'uint256', name: 'price', type: 'uint256' },
        ],
        internalType: 'struct PricePrediction.PriceDataStruct',
        name: 'price',
        type: 'tuple',
      },
    ],
    stateMutability: 'view',
    type: 'function',
  },
  {
    inputs: [],
    name: 'owner',
    outputs: [{ internalType: 'address', name: '', type: 'address' }],
    stateMutability: 'view',
    type: 'function',
  },
  {
    inputs: [],
    name: 'priceData',
    outputs: [
      { internalType: 'uint256', name: 'lastRateOfChange', type: 'uint256' },
      { internalType: 'uint256', name: 'rateOfChange', type: 'uint256' },
      { internalType: 'uint256', name: 'lastPrice', type: 'uint256' },
      { internalType: 'uint256', name: 'price', type: 'uint256' },
    ],
    stateMutability: 'view',
    type: 'function',
  },
  {
    inputs: [],
    name: 'renounceOwnership',
    outputs: [],
    stateMutability: 'nonpayable',
    type: 'function',
  },
  {
    inputs: [{ internalType: 'address', name: 'newOwner', type: 'address' }],
    name: 'transferOwnership',
    outputs: [],
    stateMutability: 'nonpayable',
    type: 'function',
  },
  {
    inputs: [
      { internalType: 'uint256', name: '_rateOfChange', type: 'uint256' },
      { internalType: 'uint256', name: '_price', type: 'uint256' },
    ],
    name: 'updatePriceData',
    outputs: [{ internalType: 'bool', name: 'success', type: 'bool' }],
    stateMutability: 'nonpayable',
    type: 'function',
  },
];
