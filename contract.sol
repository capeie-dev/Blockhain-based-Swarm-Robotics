pragma solidity >=0.4.22 <0.7.0;

contract StorageArray{
    uint[] ids;
    uint x = 3;
    constructor() public {
        ids.push(x);
    }
    function add(uint id) public{
        ids.push(id);
    }
    
    function GetPos(uint posid) public view returns (uint) {
        return ids[posid];
    }
    
    function displayAll() public view returns(uint[] memory ){
        return ids;
    }
}