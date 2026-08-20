import hashlib

def performHash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def createBlock(data, previous_hash):
    print(f'data: {type(data)} and hash: {type(previous_hash)} ')
    block = {
        'data': data,
        'previous_hash': previous_hash,
        'hash': performHash(data + previous_hash)
    }
    return block 


def createBlockChain(data_list: list[str]):
    blockchain = []

    previous_hash = '0'  # FirstBlock hash value
    for i in data_list:
        block = createBlock(i, previous_hash=previous_hash)
        blockchain.append(block)
        previous_hash = block.get('hash')
    return blockchain


def main():
    data1 = 'Hello, World!'
    data2 = 'Hello World!'
    
    hash1 = performHash(data1)
    hash2 = performHash(data2)
    
    print(f"Hash of '{data1}': {hash1}")
    print(f"Hash of '{data2}': {hash2}")

    data_list = [data1, data2]
    chain = createBlockChain(data_list=data_list)

    for i in chain:
        print(f"{i}")



if __name__ == "__main__":
    main()