from shepard_client.api_client import ApiClient
from shepard_client.configuration import Configuration
from shepard_client.api.collection_api import CollectionApi
from shepard_client.models.collection import Collection
from shepard_client.api.data_object_api import DataObjectApi
from shepard_client.models.data_object import DataObject
from shepard_client.api.timeseries_api import TimeseriesApi
from shepard_client.models.timeseries_container import TimeseriesContainer
from shepard_client.models.timeseries_payload import TimeseriesPayload
from shepard_client.models.timeseries import Timeseries
from shepard_client.api.timeseries_reference_api import TimeseriesReferenceApi


import json
import inspect
import mykey


HOST = "http://[::1]:8080/shepard/api"
key = mykey.key

# Set up configuration
conf = Configuration(host=HOST, api_key={"apikey": key})
conf.access_token = None
client = ApiClient(configuration=conf)
collection_api = CollectionApi(client)
dataobject_api = DataObjectApi(client)
timeseries_api = TimeseriesApi(client)
timeseries_reference_api = TimeseriesReferenceApi(client)



collection_id = 6#int(input("Enter a Collection ID: "))

dataobject_list = []

### Creates a dict for a given DO ID
def create_dataobject_dict(id):
    created_dict = {}
    dataobject = dataobject_api.get_data_object(collection_id, id)
    for i in dir(dataobject):
        if (i.startswith("_") and not i.startswith("__")):
            created_dict[i] = dataobject.__dict__[i]
    return created_dict

### Creates a dict for the given Collection ID
def create_collection_dict(id):
    created_dict = {}
    collection = collection_api.get_collection(id)
    for i in dir(collection):
        if (i.startswith("_") and not i.startswith("__")):
            created_dict[i] = collection.__dict__[i]

            # if i == "_data_object_ids":
            #     for j in user_collection.__dict__[i]:
            #         dataobject_list_immediate.append(dataobject_api.get_data_object(collection_id, j))
    return created_dict

def collect_dataObject_IDs(collection_id):
    DO_IDs = []
    for i in dataobject_api.get_all_data_objects(collection_id):
        DO_IDs.append(i.id)
    return DO_IDs[0]


DOs = [collect_dataObject_IDs(collection_id)]

for i in DOs:
    print(create_dataobject_dict(i)["_children_ids"])

print(timeseries_reference_api.get_all_timeseries_references(collection_id=6,data_object_id=10)[0].__getattribute__('id'))
print(type(json.dumps(timeseries_reference_api.get_timeseries_payload(6,10,14)[0].to_dict())))
