import sys
import os
import signal
import configparser
from timeit import default_timer as timer
from taskmanager import TaskManager
from rpc import RPC
from database import Database


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
            mempool_data = node.get_raw_mempool(True)
            end = timer()
            print("%f seconds" % (end - start))
            Database.write(mempool_data)
        except (ConnectionError, ConnectionResetError) as err:
            print("ConnectionError: {0}".format(err))
            node.connect()

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


