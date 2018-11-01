import sys
import os
import signal
import configparser
from taskmanager import TaskManager
from rpc import RPC
from database import Database


# Monitor the mempool data from the Bitcoin node
def monitor():
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')
    node = RPC(config['RPC']['ip'], config['RPC']['port'], config['RPC']['user'], config['RPC']['password'])
    database = Database(config['DB']['ip'], config['DB']['port'], config['DB']['user'],
                        config['DB']['password'], config['DB']['dbname'])

    def fetch_data():
        # TODO get all necessary data
        data = node.get_mempool_info()
        database.write(data)
        print(data)

    global Task
    Task = TaskManager(2, fetch_data)
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


