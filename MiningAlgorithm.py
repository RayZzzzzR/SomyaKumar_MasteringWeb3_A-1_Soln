import hashlib 
import json
import os
import binascii
import datetime
import calendar
import time

ut = time.time() #in unix epoch timeline
def SHA256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
OUTPUT_FILE = 'output.txt'
Mempool_folder ='mempool' #names based on my folder that I created in my local PC

def reverse_byte_order(hexstr):                                                 # Function to convert into reverse_byte_order
    REV = ''.join(reversed([hexstr[i:i+2] for i in range(0, len(hexstr), 2)]))
    return REV

def HASH_two(firstTxHash, secondTxHash):                                        #Function to hash 2 consecutive txids 
    unhex_reverse_first = binascii.unhexlify(firstTxHash)[::-1]    # binascii.unhexlify() converts the hexadecimal string (txid) into bytes.
    unhex_reverse_second = binascii.unhexlify(secondTxHash)[::-1]  # [:: -1] reverses the byte order to little-endian format (natural byte order)
    concat_inputs = unhex_reverse_first+unhex_reverse_second
    final_hash_inputs = hashlib.sha256(hashlib.sha256(concat_inputs).digest()).digest() # APPLY HASH256 
    return binascii.hexlify(final_hash_inputs[::-1]) # Again reversed
 
def merkleCalculator(transactions):                                              #To calculate merkle root
    if len(transactions) == 1:
        return transactions[0]
    newHashList = []
    for i in range(0, len(transactions)-1, 2):
        newHashList.append(HASH_two(transactions[i], transactions[i+1]))
    if len(transactions) % 2 == 1: # odd, hash last item twice
        newHashList.append(HASH_two(transactions[-1], transactions[-1]))
    return merkleCalculator(newHashList)
    
def is_valid_transaction(tx):                                                     #Transaction Validator function
    if 'vin' not in tx or 'vout' not in tx:
        return False

    for input_tx in tx['vin']:
        if 'txid' not in input_tx or 'prevout' not in input_tx or 'value' not in input_tx['prevout']:
            return False

    total_input_value = sum(input_tx['prevout']['value'] for input_tx in tx['vin'])
    total_output_value = sum(output_tx['value'] for output_tx in tx['vout'])
    return total_input_value > total_output_value
    
# TAKE INPUT FROM MEMPOOL
transactions = []
for filename in os.listdir(Mempool_folder):
    if filename.endswith(".json"):
        with open(os.path.join(Mempool_folder, filename), 'r') as f:
            tx = json.load(f)
            if is_valid_transaction(tx):
                transactions.append(os.path.splitext(filename)[0])
                
print(transactions)                    #to print all txids
print(len(transactions))               #number of validated txids
print(merkleCalculator(transactions))  #will print merkle root!!
#the output will appear as b'63385f87b46b3c6abb56e8041c9cb082c7c94bc919c165cafc8f1311f86399e6'
# where b' denotes byte string in python.......we just have to take the string between the commas '_________'

version = '01000000' # All transactions have same version
merkle_root = "63385f87b46b3c6abb56e8041c9cb082c7c94bc919c165cafc8f1311f86399e6" # calculated via merkleCalculator function
previous_hash = "0000000000000000000000000000000000000000000000000000000000000000" # Given
timestampdec = int(ut) # Any time taken
timestamp = str(hex(timestampdec).lstrip("0x")) #time  in hex
difficulty_target = '1f00ffff'# in 4 bytes
target = '0x0000ffff00000000000000000000000000000000000000000000000000000000' #in 32 bytes

#for n_o_n_c_e
s = version + reverse_byte_order(previous_hash) + reverse_byte_order(merkle_root) + reverse_byte_order(timestamp) + reverse_byte_order(difficulty_target)
# as merkle root and others were in reverse byte order so we again converted then into natural byte order by using reverse_byte_order function
nonce = 0 #initially
while True:
    value = s + str(reverse_byte_order(hex(nonce).lstrip('0x')))
    hash_value = hashlib.sha256(value.encode('utf-8')).hexdigest()
    if int(hash_value, 16)<int(target, 16):      #converting hex into int for comparision
        break
    nonce += 1
    
    
#THIS PART IS FOR OUTPUT.TXT FILE :-   
    
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

block_header = {
    "version": 1,
    "previous_block_hash": previous_hash,
    "merkle_root": merkle_root,
    "timestamp": timestampdec,
    "difficulty_target": "0000"+target.lstrip("0x"), #to remove  0x from hex notation and 0000 is added 
    "nonce": nonce
}

with open(OUTPUT_FILE, 'w') as f: # to add all text in output.txt in writng mode
    f.write("Block Header:\n")
    f.write(json.dumps(block_header, indent=2) + "\n\n")
    f.write("Serialized Coinbase Transaction:\n")
    f.write(json.dumps(coinbase_tx, indent=2) + "\n\n")
    f.write("Transaction IDs:\n")
    for i in range(len(transactions)):
        f.write(f"{transactions[i]}\n")
           
print(nonce) # will print nonce in decimal form
blockHeader = s+str(reverse_byte_order(hex(nonce).lstrip("0x"))) # concatenating nonce as reverse byte order
print(blockHeader+((160-len(blockHeader))*'0'))
#code to print Block Header
