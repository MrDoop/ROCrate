from math import radians, sin
import time
import mykey

from shepard_client.api.timeseries_reference_api import TimeseriesReferenceApi
from shepard_client.models.timeseries_reference import TimeseriesReference
from shepard_client.models.timeseries_container import TimeseriesContainer
from shepard_client.models.timeseries_payload import TimeseriesPayload
from shepard_client.api.timeseries_api import TimeseriesApi
from shepard_client.models.influx_point import InfluxPoint
from shepard_client.models.timeseries import Timeseries
from shepard_client.configuration import Configuration
from shepard_client.api_client import ApiClient


HOST = "http://[::1]:8080/shepard/api"
key = mykey.key
# Set up configuration
conf = Configuration(host=HOST, api_key={"apikey": key})
conf.access_token = None
client = ApiClient(configuration=conf)

COLLECTION_ID = 6
DATAOBJECT_ID = 10

# In order to upload timeseries, you first need to create a container into which you can upload your data
timeseries_api = TimeseriesApi(client)
container_to_create = TimeseriesContainer(name="MyFirstTimeseriesContainer")
created_container = timeseries_api.create_timeseries_container(
    timeseries_container=container_to_create
)

# Now you can upload some data into your newly created container
nanos = int(round(time.time_ns()))  # current nanoseconds
factor = int(1e9)  # Convert nanoseconds to seconds
points = []
for i in range(0, 360):
    value = sin(radians(i))
    timestamp = nanos - (360 - i) * factor
    points.append(InfluxPoint(value=value, timestamp=timestamp))

timeseries = Timeseries(
    measurement="MyMeas",
    location="MyLoc",
    device="MyDev",
    symbolic_name="MySymName",
    field="value",
)
payload = TimeseriesPayload(timeseries=timeseries, points=points)
created_timeseries = timeseries_api.create_timeseries(
    timeseries_container_id=created_container.id, timeseries_payload=payload
)
# You have now received an object that is the unique identifier of your uploaded timeseries
print(created_timeseries)

# See which time series are available in the container
timeseries_available = timeseries_api.get_timeseries_available(created_container.id)
print(timeseries_available)

# Retrieve your data
timeseries_payload = timeseries_api.get_timeseries(
    created_container.id,
    measurement="MyMeas",
    location="MyLoc",
    device="MyDev",
    symbolic_name="MySymName",
    field="value",
    start=points[0].timestamp,
    end=points[-1].timestamp,
)
print(len(timeseries_payload.points))



# With this identifier in combination with your container you can reference your data from anywhere
timeseries_reference_api = TimeseriesReferenceApi(client)
reference_to_create = TimeseriesReference(
    name="MyFirstReference",
    start=nanos - 360 * factor,
    end=nanos,
    timeseries_container_id=created_container.id,
    timeseries=[created_timeseries],
)
created_reference = timeseries_reference_api.create_timeseries_reference(
    collection_id=COLLECTION_ID,
    data_object_id=DATAOBJECT_ID,
    timeseries_reference=reference_to_create,
)
print(created_reference)

# And now you can download your timeseries using this newly created reference
downloaded_timeseries = timeseries_reference_api.get_timeseries_payload(
    collection_id=COLLECTION_ID,
    data_object_id=DATAOBJECT_ID,
    timeseries_reference_id=created_reference.id,
)
print(downloaded_timeseries[0].points)
