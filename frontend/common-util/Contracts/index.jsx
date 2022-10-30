import Web3 from 'web3';
import {
  MAIN_CONTRACT_ADDRESS,
  MAIN_CONTRACT_ABI,
  CONTRACT_ADDRESS_GOERLI,
  CONTRACT_ABI_GOERLI,
} from 'common-util/AbiAndAddresses';

export const getContract = (p, chainId) => {
  const web3 = new Web3(p);

  // Goerli has separate contract
  const contract = new web3.eth.Contract(
    chainId === 25 ? CONTRACT_ABI_GOERLI : MAIN_CONTRACT_ABI,
    chainId === 25 ? CONTRACT_ADDRESS_GOERLI : MAIN_CONTRACT_ADDRESS,
  );
  return contract;
};
