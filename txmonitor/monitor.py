import sys
import os
import signal
import configparser
from bitcoinrpc.authproxy import JSONRPCException
from timeit import default_timer as timer
from taskmanager import TaskManager
from rpc import RPC
from database import Database
from mempool import Mempool


# Monitor the mempool data from the Bitcoin node
def monitor():
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')

    node = RPC(config['RPC']['ip'],
               config['RPC']['port'],
               config['RPC']['user'],
               config['RPC']['password'])
    node.connect()

    database = Database(config['DB']['ip'],
                        config['DB']['port'],
                        config['DB']['user'],
                        config['DB']['password'],
                        config['DB']['dbname'])
    database.connect()

    def fetch_data():
        try:
            start = timer()
            node.get_raw_mempool()
            print("Current Mempool: %s TXs, Total size: %s bytes, Total Value: %s BTC, Total Fee %s BTC" %
                  (Mempool.data['size'], Mempool.data['bytes'], Mempool.data['value'], Mempool.data['fee']))
            end = timer()
            print("%f seconds" % (end - start))

            if Mempool.current_txs:
                Database.write(Mempool.data)
        except (ConnectionError, ConnectionResetError) as err:
            print("ConnectionError: {0}".format(err))
            node.connect()
        except JSONRPCException as err:
            print("JSONError: {0}".format(err))

    global Task
    Task = TaskManager(20, fetch_data)
    Task.start()


# Clean resources and quit the program
def close(signal, frame):
    # TODO free all resources ...
    print("Exiting Mempool Monitoring ...")
    Task.stop()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, close)
    monitor()


