# Price Prophet

## iExec

### Oracle Parameters

1. FTX
    - Link: https://ftx.com/api/markets/BTC/USD
    - Network: 134
    - OracleId: 0x1fcaceeeb261d6089cff9c300730e5511ef8dbf33df41fb407ac0e0b644714ce

2. CoinGecko
    - Link: https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin
    - Network: 134
    - OracleId: 0xff3d7b93e9dd86339cb5c61226ecf48b68e18623742409d48ca5d392f5de24a3

### Implement Oracle into our dApp

see contracts/PriceOracleStorage.sol.

Oracle information with updated price information is retrieved for the caller and saved in the contract.


## Cronos

### Cronos testnet deployment
PricePrediction.sol deployed to
> 0x6D6754DD2DFc1EcA7F2aD982d48bEbAAB44E7F73

### Cronos mainnet deployment

PricePrediction.sol deployed to 
> 0xACF6F2b3dfCC96DcE5BdFFC422cbDd3b179727db

and successfully verified contract PricePrediction on cronoscan.com:
https://cronoscan.com/address/0xACF6F2b3dfCC96DcE5BdFFC422cbDd3b179727db#code


---
## Hardhat 

Try running some of the following tasks:


### install commands
```
npm install
```

### compile contracts

```
npx hardhat compile
```

### deploy
```
 npx hardhat run scripts/deploy.js --network cronos

```

### verify
```
npx hardhat verify --network cronos 0xACF6F2b3dfCC96DcE5BdFFC422cbDd3b179727db

```

### run 
```shell
    npx hardhat help
    npx hardhat test
    REPORT_GAS=true npx hardhat test
    npx hardhat node
    npx hardhat run scripts/deploy.js
```
