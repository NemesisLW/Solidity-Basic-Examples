import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as contract:
    simple_storage_file = contract.read()

print("Installing Compiler...")
install_solc("0.8.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

'''
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x7238004D00BFDff5Bce77a7Ba4ed1Ce66D4d9072"
private_key = "97677ef131afbe6c64249d1eb91b5b75cda20223a3505ece7427e973ad4aa2ce"
'''

# Connecting to the Blockchain
web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/56c8f480a6704051b8d7059ef1ae16c1"))
chain_id = 3
address = "0xd0A83eB1f67Cf27C9ec00918a6F9233c641ceD9d"
private_key = os.getenv("API_KEY")

# Contract
simpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)
nonce = web3.eth.getTransactionCount(address)
transaction = simpleStorage.constructor().buildTransaction({
    "chainId": chain_id,
    "gasPrice": web3.eth.gas_price,
    "from": address,
    "nonce": nonce
})

# Sign Transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract")
# Sending txn to be mined
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
# waiting to be mined
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract Deployed to {tx_receipt.contractAdderess}")

# Working with deployed Contracts
simple_storage = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
test_txn = simple_storage.functions.store(4).buildTransaction({
    "chainId": chain_id,
    "gasPrice": web3.eth.gas_price,
    "from": address,
    "nonce": nonce + 1
})

signed_test_txn = web3.eth.account.sign_transaction(test_txn, private_key=private_key)
tx_test_hash = web3.eth.send_raw_transaction(signed_test_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_test_hash)

print(simple_storage.functions.retrieve().call())