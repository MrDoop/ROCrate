from shepard_client.api_client import ApiClient
from shepard_client.configuration import Configuration
from shepard_client.api.collection_api import CollectionApi
from shepard_client.models.collection import Collection
from shepard_client.api.data_object_api import DataObjectApi
from shepard_client.models.data_object import DataObject

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


collection_id = int(input("Enter a Collection ID: "))

dataobject_list = []
dataobject_list_immediate = []

#print(dict(coll6))
#print(coll6.__getattribute__("id"))


### Creates a dict for the given Collection ID
def create_collection_dict(id):
    created_dict = {}
    collection = collection_api.get_collection(id)
    for i in dir(collection):
        if (i.startswith("_") and not i.startswith("__")):
            created_dict[i] = collection.__dict__[i]
            print(i)
            print(collection.__dict__[i])
            print()
            # if i == "_data_object_ids":
            #     for j in user_collection.__dict__[i]:
            #         dataobject_list_immediate.append(dataobject_api.get_data_object(collection_id, j))
    return created_dict

### Collects all DO IDs from a given collection



### Creates a dict for a given DO ID
def create_dataobject_dict(id):
    created_dict = {}
    dataobject = dataobject_api.get_data_object(collection_id, id)
    for i in dir(dataobject):
        if (i.startswith("_") and not i.startswith("__")):
            created_dict[i] = dataobject.__dict__[i]
    return created_dict

collection_dict = create_collection_dict(collection_id)

#print(json.dumps(collection_dict, indent=4, sort_keys=True, default=str))

for i in collection_dict["_data_object_ids"]:
    print(create_dataobject_dict(i))

### Recursive function to find the oldest parent DO
def find_ancestor(id):
    do_dict = create_dataobject_dict(id)
    parent = do_dict["_parent_id"]
    if parent == None:
        return id
    else:
        return find_ancestor(parent)

print(find_ancestor(collection_dict["_data_object_ids"][1]))

children = []
successors = []
