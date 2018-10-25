import sys, signal
import csv
import time
import threading
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from txmonitor.periodic import Periodic


def do_job():
    print("lol")
    time.sleep(2)


P = Periodic(1, do_job)


def get_connection():
    rpc_user = "bitcoinrpc"
    rpc_password = "4d76a1178634ae3ee5c0c26af4f3e764"
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (rpc_user, rpc_password))
    return rpc_connection


def get_mempool_size(connection):
    info = connection.getmempoolinfo()
    return info["size"]


def recursive_timer(rpc_connection):
    size = get_mempool_size(rpc_connection)
    print(get_mempool_size(rpc_connection))
    threading.Timer(1, recursive_timer, [rpc_connection]).start()
    store_in_file([time.ctime(), size])


def store_in_file(dataArray):
    with open('mempool.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(dataArray)


def main():
    conn = get_connection()
    # recursive_timer(conn)

    # p = Periodic(1, do_job)
    P.start()
    # time.sleep(3)
    # p.stop()


def handler(signal, frame):
    # global THREADS
    # for t in THREADS:
    #     t.alive = False
    print("Ctrl-C.... Exiting")
    P.stop()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    main()
    while True:
        signal.pause()  # added