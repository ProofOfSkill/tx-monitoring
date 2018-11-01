from influxdb import InfluxDBClient
from influxdb import SeriesHelper


class Database:
    def __init__(self, ip, port, user, password, dbname):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.client = self.connect()

    def connect(self):
        # TODO Check errors
        client = InfluxDBClient(self.ip, self.port, self.user, self.password, self.dbname)
        MySeriesHelper.Meta.client = client
        dbs = client.get_list_database()
        if self.dbname not in [d['name'] for d in dbs]:
            print("Create %s Database" % self.dbname)
            client.create_database(self.dbname)
            client.switch_database(self.dbname)
        print(dbs)
        return client

    def write(self, data):
        MySeriesHelper(network='mainnet', size=data['size'], bytes=data['bytes'])


class MySeriesHelper(SeriesHelper):
    """Instantiate SeriesHelper to write points to the backend."""

    class Meta:
        """Meta class stores time series helper configuration."""

        # The client should be an instance of InfluxDBClient.
        client = None

        # The series name must be a string. Add dependent fields/tags
        # in curly brackets.
        series_name = 'monitor.series'

        # Defines all the fields in this time series.
        fields = ['size', 'bytes']

        # Defines all the tags for the series.
        tags = ['network']

        # Defines the number of data points to store prior to writing
        # on the wire.
        bulk_size = 5

        # autocommit must be set to True when using bulk_size
        autocommit = True
