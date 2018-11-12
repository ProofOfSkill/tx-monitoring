class Mempool(object):
    current_txs = {}
    data = {'size': 0, 'bytes': 0, 'value': 0.0, 'fee': 0.0}

    @staticmethod
    def update_tx_id(data):
        Mempool.data['size'] = len(data)
        Mempool.data['bytes'] = 0
        Mempool.data['fee'] = 0

        for txid in data:
            # Add new txid in current mempool tx
            if txid not in Mempool.current_txs:
                Mempool.current_txs[txid] = 0

            # Update bytes and fee for current mempool tx
            Mempool.data['bytes'] += data[txid]['size']
            Mempool.data['fee'] += data[txid]['fee']

        # Delete old txid from current mempool tx
        for key in list(Mempool.current_txs):
            if key not in data:
                del Mempool.current_txs[key]

    @staticmethod
    def update_tx_value(data):
        # Update tx value for current mempool tx
        for tx in data:
            for vout in tx['vout']:
                Mempool.current_txs[tx['txid']] += vout['value']
            if Mempool.current_txs[tx['txid']] >= 1000:
                print("Whale Alert in Mempool: %s BTC transfered!\nDetail: %s" %
                      (Mempool.current_txs[tx['txid']], tx['txid']))
        print("%s Transactions added - Average %s Tx/s in Mempool" % (len(data), len(data) / 20))
        Mempool.data['value'] = sum(Mempool.current_txs.values())

    @staticmethod
    def print_mempool():
        for key, value in Mempool.current_txs.items():
            print("TXID: %s Value: %s" % (key, value))

