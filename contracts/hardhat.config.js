require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config()

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  networks: {
    "cronos-testnet": {
        url: "https://evm-t3.cronos.org/",
        accounts: [process.env.PRIVATE_KEY]
    },
    "cronos-main": {
        url: "https://evm.cronos.org/",
        accounts: [process.env.PRIVATE_KEY]
    },
  },
  solidity: "0.8.17",
};
