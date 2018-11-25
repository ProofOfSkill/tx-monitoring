from influxdb import InfluxDBClient
from influxdb import SeriesHelper


class Database:
    def __init__(self, ip, port, user, password, dbname):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.client = None

    def connect(self):
        # TODO Check errors
        self.client = InfluxDBClient(self.ip, self.port, self.user, self.password, self.dbname)
        MySeriesHelper.Meta.client = self.client

    @staticmethod
    def write(mempool_data):
        MySeriesHelper(network='mainnet',
                       size=mempool_data['size'],
                       bytes=mempool_data['bytes'],
                       value=float(mempool_data['value']),
                       fee=float(mempool_data['fee'])
                       )


class MySeriesHelper(SeriesHelper):
    """Instantiate SeriesHelper to write points to the backend."""

    class Meta:
        """Meta class stores time series helper configuration."""

        # The client should be an instance of InfluxDBClient.
        client = None

        # The series name must be a string. Add dependent fields/tags
        # in curly brackets.
        series_name = 'mempool.stats'

        # Defines all the fields in this time series.
        fields = ['size', 'bytes', 'value', 'fee']

        # Defines all the tags for the series.
        tags = ['network']

        # Defines the number of data points to store prior to writing
        # on the wire.
        bulk_size = 1

        # autocommit must be set to True when using bulk_size
        autocommit = True
