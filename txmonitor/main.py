import sys, signal
import csv
import time
import configparser
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from txmonitor.periodic import Periodic


def get_connection(config):
    rpc_user = config['rpc_user']
    rpc_password = config['rpc_password']
    rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password,
                                                              config['rpc_ip'], config['rpc_port']))
    return rpc_connection


def get_mempool_size(connection):
    info = connection.getmempoolinfo()
    return info["size"]


def store_in_file(data):
    with open('../data/mempool.csv', 'a') as csv_file:
        headers = ['Date', 'Size']
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow({'Date': data[0], 'Size': data[1]})


def init_data_csv():
    with open('../data/mempool.csv', 'w') as csv_file:
        headers = ['Date', 'Size']
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    conn = get_connection(config['RPC'])
    init_data_csv()

    def do_job():
        print("get mempool size...")
        size = get_mempool_size(conn)
        store_in_file([time.ctime(), size])

    global P
    P = Periodic(2, do_job)
    P.start()


def handler(signal, frame):
    print("Ctrl-C.... Exiting")
    P.stop()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    main()
    while True:
        signal.pause()  # added


