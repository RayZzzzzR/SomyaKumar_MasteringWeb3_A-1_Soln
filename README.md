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
```
def SHA256 : #function for sha256
def reverse_byte_order(hexstr) : #change hash to reverse byte order
def HASH_two(firstTxHash, secondTxHash): #Function to hash 2 consecutive txids
def merkleCalculator(transactions): # merkle root calculator via recursion till len(transaction) is 1
def is_valid_transaction(tx): #transaction validator function as per given conditions
```
