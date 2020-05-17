from web3 import Web3
import json
import random
infra_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(infra_url))
print(web3.isConnected())
hash_store=[]
web3.eth.defaultAccount = web3.eth.accounts[1]

abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"posid","type":"uint256"}],"name":"GetPos","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"displayAll","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}]')


bytecode = '608060405234801561001057600080fd5b506101ef806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80631003e2d2146100465780634c9beb5314610074578063ca530361146100d3575b600080fd5b6100726004803603602081101561005c57600080fd5b8101908080359060200190929190505050610115565b005b61007c610141565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156100bf5780820151818401526020810190506100a4565b505050509050019250505060405180910390f35b6100ff600480360360208110156100e957600080fd5b8101908080359060200190929190505050610199565b6040518082815260200191505060405180910390f35b600081908060018154018082558091505060019003906000526020600020016000909190919091505550565b6060600080548060200260200160405190810160405280929190818152602001828054801561018f57602002820191906000526020600020905b81548152602001906001019080831161017b575b5050505050905090565b60008082815481106101a757fe5b9060005260206000200154905091905056fea2646970667358221220bf7a10cc899b81dbb50a3c5b7e739c987aff51bf975b12ef16f4464403745b0d64736f6c63430006060033'


greeter = web3.eth.contract(abi=abi,bytecode=bytecode)
#initialize the blockchain with a contruct
tx_hash=greeter.constructor().transact() 
tx_recipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract = web3.eth.contract(address=tx_recipt.contractAddress, abi=abi)

for i in range(0,5):
    id = random.randint(0,1000000000)
    hash_store.append(id)
    tx_hash=contract.functions.add(id).transact() 
    tx_recipt = web3.eth.waitForTransactionReceipt(tx_hash)
    

print(contract.functions.displayAll().call())
