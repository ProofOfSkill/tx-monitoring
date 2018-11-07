import sys
import datetime
from bitcoinrpc.authproxy import AuthServiceProxy


class RPC:
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.connection = None

    # Authentication to the Bitcoin node
    def connect(self):
        try:
            self.connection = AuthServiceProxy(
                "http://%s:%s@%s:%s" % (self.user, self.password, self.ip, self.port), timeout=120)
            self.get_blockchain_info()
        except Exception as err:
            sys.exit("AuthServiceProxy error: {0}".format(err))

    # Get information about node's current mempool
    # -result (object): A object containing information about the memory pool
    # -size (int): The number of transactions currently in the memory pool
    # -bytes (int): The total number of bytes in the transactions in the memory pool
    # -usage (int): Total memory usage for the mempool in bytes
    # -maxmempool (int): Maximum memory usage for the mempool in bytes
    # -mempoolminfee (int): The lowest fee per kilobyte paid by any transaction in the memory pool
    def get_mempool_info(self):
        data = self.connection.getmempoolinfo()
        print("GET_MEMPOOL_INFO: %s TXs, %s Mb" % (data['size'], round(data['bytes']/float(1 << 20), 4)))
        return data

    # Get all TXIDs in the mempool
    # Parameter
    #   verbose (bool):
    #   true to get description of each TXIDS in the mempool
    #   false to only get the array of TXIDS in the mempool
    # -result (object): A object containing transactions currently in the memory pool. May be empty
    # -TXID (string): The TXID of a transaction in the memory pool, encoded as hex in RPC byte order
    # --size (int): The size of the serialized transaction in bytes
    # --fee (bitcoins): The transaction fee paid by the transaction in decimal bitcoins
    # --modifiedfee (bitcoins): The transaction fee with fee deltas used for mining priority in decimal bitcoins
    # --time (int): The time the transaction entered the memory pool, Unix epoch time format
    # --height (int): The block height when the transaction entered the memory pool
    def get_raw_mempool(self, verbose):
        data = self.connection.getrawmempool(verbose)
        mempool_data = {'size': 0, 'bytes': 0, 'value': 0, 'fee': 0}
        if verbose is True:
            for txid in data:
                value = self.get_transaction_value(txid)
                mempool_data['value'] += value
                mempool_data['size'] += 1
                mempool_data['bytes'] += data[txid]['size']
                mempool_data['fee'] += data[txid]['fee']
                # print("TXID: %s, Time: %s, Height: %s, Size: %s, Value: %s BTC, Fee: %s BTC" %
                #       (txid,
                #        datetime.datetime.fromtimestamp(data[txid]['time']).strftime('%Y-%m-%d %H:%M:%S'),
                #        data[txid]['height'],
                #        data[txid]['size'],
                #        value,
                #        data[txid]['fee']))
        print("Current Mempool: %s TXs, Total size: %s bytes, Total Value: %s BTC, Total Fee %s BTC" %
              (mempool_data['size'],
               mempool_data['bytes'],
               mempool_data['value'],
               mempool_data['fee']))
        return mempool_data

    def get_transaction_value(self, txid):
        data = self.connection.getrawtransaction(txid, True)
        value = 0
        if data is not None:
            for vout in data['vout']:
                value += vout['value']
        return value

    # Get information about the current state of the block chain.
    # -result (object): Information about the current state of the local block chain
    # -chain (string): The name of the block chain. One of main for mainnet, test for testnet, or regtest for regtest
    # -blocks (int): The number of validated blocks in the local best block chain. For a new node
    #                with just the hardcoded genesis block, this will be 0
    # -headers(int): The number of validated headers in the local best headers chain. For a new node with just the
    #                hardcoded genesis block, this will be zero. This number may be higher than the number of blocks
    # -bestblockhash (string): The hash of the header of the highest validated block in the best block chain,
    #                          encoded as hex in RPC byte order. This is identical to the string returned by
    #                          the getbestblockhash RPC
    # -difficulty (int): The difficulty of the highest-height block in the best block chain
    # -mediantime (int): The median time of the 11 blocks before the most recent block on the blockchain.
    #                    Used for validating transaction locktime under BIP113
    # -verificationprogress (int): Estimate of what percentage of the block chain transactions have been verified
    #                              so far, starting at 0.0 and increasing to 1.0 for fully verified.
    #                              May slightly exceed 1.0 when fully synced to account for transactions
    #                              in the memory pool which have been verified before being included in a block
    # -chainwork (string): The estimated number of block header hashes checked from the genesis block to this block,
    #                      encoded as big-endian hex
    # -pruned (bool): Indicates if the blocks are subject to pruning
    # -pruneheight (int): The lowest-height complete block stored if prunning is activated
    # -softforks (array): An array of objects each describing a current or previous soft fork
    def get_blockchain_info(self):
        data = self.connection.getblockchaininfo()
        print("Bitcoin Core Node: \nChain: %s\nBlocks: %s\nPruned: %s\nPruneheight %s" %
              (data['chain'], data['blocks'], data['pruned'], data['pruneheight']))
        return data

