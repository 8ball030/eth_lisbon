require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config()

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  networks: {
    "cronos-testnet": {
        url: process.env.CRONOS_TESTNET_RPC_URL,
        accounts: [process.env.PRIVATE_KEY]
    },
  },
  solidity: "0.8.17",
};
