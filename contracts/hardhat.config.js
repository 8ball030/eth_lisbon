require("@nomicfoundation/hardhat-toolbox");
require("@cronos-labs/hardhat-cronoscan");
require('dotenv').config()

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  networks: {
    "cronos-testnet": {
        url: "https://evm-t3.cronos.org/",
        accounts: [process.env.PRIVATE_KEY]
    },
    "cronos": {
        url: "https://evm.cronos.org/",
        accounts: [process.env.PRIVATE_KEY]
    },
  },

  etherscan: {
    apiKey: {
      cronos: process.env.SCANNER_API_KEY,
    },
  customChains: [
    {
      network: "cronos",
      chainId: 25,
      urls: {
        apiURL: "https://api.cronoscan.com",
        browserURL: "https://cronoscan.com"
      }
    }
]
},
  solidity: "0.8.17",
};
