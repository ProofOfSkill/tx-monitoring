import sys
import signal
import configparser
from txmonitor.taskmanager import TaskManager
from txmonitor.rpc import RPC
from txmonitor.data import Data


# Monitor the mempool data from the Bitcoin node
def monitor():
    config = configparser.ConfigParser()
    config.read('config.ini')
    node = RPC(config['RPC']['ip'], config['RPC']['port'], config['RPC']['user'], config['RPC']['password'])
    file = Data()

    def fetch_data():
        # TODO get all necessary data
        data = node.get_mempool_info()
        file.write(data)

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


