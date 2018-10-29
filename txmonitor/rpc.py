from bitcoinrpc.authproxy import AuthServiceProxy


class RPC:
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.connection = self.authenticate()

    # Authentication to the Bitcoin node
    def authenticate(self):
        # TODO check connection errors
        return AuthServiceProxy("http://%s:%s@%s:%s" % (self.user, self.password, self.ip, self.port))

    # Get information about node's current mempool
    # result (object) A object containing information about the memory pool
    # size (int) The number of transactions currently in the memory pool
    # bytes (int) The total number of bytes in the transactions in the memory pool
    # usage (int) Total memory usage for the mempool in bytes
    # maxmempool (int) Maximum memory usage for the mempool in bytes
    # mempoolminfee (int) The lowest fee per kilobyte paid by any transaction in the memory pool
    def get_mempool_info(self):
        data = self.connection.getmempoolinfo()
        print("GET_MEMPOOL_INFO: Number of TXID: %s, Number of Bytes: %s" % (data['size'], data['bytes']))
        return data

    # Get all TXIDs in the mempool
    # Parameter
    # verbose (bool):
    # true to get description of each TXIDS in the mempool
    # false to only get the array of TXIDS in the mempool
    def get_raw_mempool(self, verbose):
        data = self.connection.getrawmempool(verbose)
        print("GET_RAW_MEMPOOL: %s" % data)
        return data
