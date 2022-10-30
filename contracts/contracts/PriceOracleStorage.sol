// SPDX-License-Identifier: Unlicense

//ETHLisbon 2022 Hackathon
//Last update: 30.10.2022

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";


interface IOracle {
    function getInt(bytes32) external view returns (int256, uint256);
}


contract PricePredictOracleStorage is Ownable{

    //Variables
    struct OracleStruct{
        bytes32 oracleId;
        address oracleAddress;
        int256 storedValue;
        uint256 storedDate;
    }
    OracleStruct[] public oracles;

    mapping (bytes32 => bool) public oracleIdIncluded;

    //Events
    event LogOracleAdded(address indexed sender, bytes32 oracleId, address oracleAddress);
    event LogValueChanged(uint indexed oracleIndex, int256 newValue, uint256 newDate);

    constructor(bytes32 _oracleId, address _oracleAddress){
        addOracle(_oracleId, _oracleAddress);
    }

    modifier idExists(uint _oracleIndex){
         require(_oracleIndex < oracles.length, "Oracle at index does not exist.");
         _;
    }


    function addOracle(bytes32 _oracleId, address _oracleAddress) public onlyOwner returns(bool success){
        require(_oracleId > 0, "addOracle: Id must be provided");
        require(_oracleAddress != address(0x0), "addOracle: Address must be provided");
        require(!oracleIdIncluded[_oracleId], "addOracle: Id was already added");
        
        oracles.push(
            OracleStruct({
                oracleId: _oracleId,
                oracleAddress: _oracleAddress,
                storedValue: 0,
                storedDate: 0
            })
        );
        oracleIdIncluded[_oracleId] = true;

        emit LogOracleAdded(msg.sender, _oracleId, _oracleAddress);
        return true;
    }


    function updateSingleOracleData(uint _oracleIndex) public idExists(_oracleIndex) returns(OracleStruct memory singleOracle){

        OracleStruct storage oracle = oracles[_oracleIndex];

        IOracle oracleContract = IOracle(oracle.oracleAddress);

        (int256 value, uint256 date) = oracleContract.getInt(oracle.oracleId);

        oracle.storedValue = value;
        oracle.storedDate = date;

        emit LogValueChanged(_oracleIndex, value, date);
        return oracle;
    }


    function updateMultipleOracleData() public returns(OracleStruct[] memory multipleOracles){

        for(uint i=0; i<oracles.length; i++) {
            updateSingleOracleData(i);
        }

        return oracles;
    }


    function getSingleOracleData(uint _oracleIndex) public idExists(_oracleIndex) view returns(int256, uint256){
            
        OracleStruct storage oracle = oracles[_oracleIndex];

        return (oracle.storedValue, oracle.storedDate);
    }


    function deleteOracle(uint _oracleIndex) public onlyOwner idExists(_oracleIndex) returns(bool success){

        bytes32 tmpOracleIndex = oracles[_oracleIndex].oracleId;
        oracleIdIncluded[tmpOracleIndex] = false;

        oracles[_oracleIndex] = oracles[oracles.length-1];
        oracles.pop();
        
        return true;
    }


    function getOracleStructSize() public view returns(uint){
        return oracles.length;
    }
}