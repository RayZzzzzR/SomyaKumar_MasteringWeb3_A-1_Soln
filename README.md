# BitCoin mining Simulation

`Main Goal`:- Simulate the mining process of a block by validating and including transactions from a given set of JSON files in the `mempool` folder.

So.....Let's understand the implementation behind my simulation :)
`mempool` is a temporary storage that contains all the transactions. New transactions are stored in a node's memory pool while they're waiting to get mined on to the blockchain. We use `mempool` to sort out conflicting transactions.

Pseudo Code of Block constructor :-
IMPORTS
```py
import hashlib  # for hash algorithms
import json     # for json files
import os       # to link to os files
import binascii # to convert to hex and other systems
import datetime 
import calendar # these 3 imports are for setting current time
import time

ut = time.time() # for unix epoch time
```
FUNCTIONS
```py
def SHA256 : #function for sha256
def reverse_byte_order(hexstr) : #change hash to reverse byte order
def HASH_two(firstTxHash, secondTxHash): #Function to hash 2 consecutive txids
def merkleCalculator(transactions): # merkle root calculator via recursion till len(transaction) is 1
def is_valid_transaction(tx): #transaction validator function as per given conditions
```
INPUT FROM MEMPOOL
```py
transactions = []  #list of all validated transactions
for filename in os.listdir(Mempool_folder):                                #iterating files in mempool folder
    if filename.endswith(".json"):                                         #all json files taken
        with open(os.path.join(Mempool_folder, filename), 'r') as f:       #opening files in reading mode
            tx = json.load(f)                                              #load files
            if is_valid_transaction(tx):                                   # check condition for valid transaction
                transactions.append(os.path.splitext(filename)[0])         # Append all selected transactions in above list
```
ASSIGNING BLOCK HEADER VALUES
```py
version = '01000000'                                                                # All transactions have same version
merkle_root = "63385f87b46b3c6abb56e8041c9cb082c7c94bc919c165cafc8f1311f86399e6"    # calculated via merkleCalculator function
previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"  # Given
timestampdec = int(ut)                                                              # Current time
timestamp = str(hex(timestampdec).lstrip("0x"))                                     #time in hex
difficulty_target = '1f00ffff'                                                      #target in 4 bytes
target = '0x0000ffff00000000000000000000000000000000000000000000000000000000'       #target in 32 bytes
```
For loop for nonce calculation
```py
s = version + reverse_byte_order(previous_hash) + reverse_byte_order(merkle_root) + reverse_byte_order(timestamp) + reverse_byte_order(difficulty_target)
# as merkle root and others were in reverse byte order so we again converted then into natural byte order by using reverse_byte_order function
# s is the block header is raw form without nonce
nonce = 0 #initially
while True:
    value = s + str(reverse_byte_order(hex(nonce).lstrip('0x')))     #removing 0x part from hex notation
    hash_value = hashlib.sha256(value.encode('utf-8')).hexdigest()
    if int(hash_value, 16)<int(target, 16):                          #converting hex into int for comparision
        break
    nonce += 1 
```
TO ASSIGN TEXT IN OUTPUT.TXT
```py
#disctonary for coinbase transaction
coinbase_tx = {
    "txid": SHA256("coinbase"),
    "vin": [{
        "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303233204368616e63656c6c6f72206f6e20626974636f696e2062756c6c",
        "sequence": 4294967295
    }],
    "vout": [{
        "value": 5000000000,
        "scriptPubKey": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"
    }]
}

transactions.insert(0, SHA256("coinbase")) # add conibase txid at index 0 !!!!!

#dictonary for block header
block_header = {
    "version": 1,
    "previous_block_hash": previous_hash,
    "merkle_root": merkle_root,
    "timestamp": timestampdec,
    "difficulty_target": "0000"+target.lstrip("0x"), #to remove  0x from hex notation and 0000 is added 
    "nonce": nonce
}

with open(OUTPUT_FILE, 'w') as f:                           # to add all text in output.txt in writng mode
    f.write("Block Header:\n")                              
    f.write(json.dumps(block_header, indent=2) + "\n\n")    
    f.write("Serialized Coinbase Transaction:\n")
    f.write(json.dumps(coinbase_tx, indent=2) + "\n\n")
    f.write("Transaction IDs:\n")                           # All transaction IDs with coinbase transaction ID
    for i in range(len(transactions)):
        f.write(f"{transactions[i]}\n")
```
