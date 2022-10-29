// SPDX-License-Identifier: Unlicense

//ETHLisbon 2022 Hackathon
//Last update: 29.10.2022

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";


/// @title Price Prediction
/// @author Price Prophet Team
/// @notice This price prediction contract holds the latest predicted prices 
contract PricePrediction is Ownable {

    //Variables
    struct PriceDataStruct{
        uint lastRateOfChange;
        uint rateOfChange;
        uint lastPrice;
        uint price;
    }
    PriceDataStruct private priceData;

    //Events
    event LogPriceDataUpdated(address sender, uint rateOfChange, uint price);

    constructor(){}


    function updatePriceData(uint _rateOfChange, uint _price) public onlyOwner returns(bool success){
        
        PriceDataStruct storage d = priceData;

        //copy old values
        d.lastRateOfChange = d.rateOfChange;
        d.lastPrice = d.price;

        //updates actual values
        d.rateOfChange = _rateOfChange;
        d.price = _price;

        emit LogPriceDataUpdated(msg.sender, _rateOfChange, _price);
        return true;
    }

    function getPriceData() public view returns(PriceDataStruct memory price){
        return priceData;
    }
}