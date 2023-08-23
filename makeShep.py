from shepard_client.api_client import ApiClient
from shepard_client.configuration import Configuration
from shepard_client.api.collection_api import CollectionApi
from shepard_client.models.collection import Collection
from shepard_client.api.data_object_api import DataObjectApi
from shepard_client.models.data_object import DataObject

import mykey



HOST = "http://[::1]:8080/shepard/api"
key = mykey.key

# Set up configuration
conf = Configuration(host=HOST, api_key={"apikey": key})
conf.access_token = None
client = ApiClient(configuration=conf)
collection_api = CollectionApi(client)
collections = collection_api.get_all_collections()

# Start Program

# CREATING COLLECTION ====================v
collection_attributes = {"attribute1": "firstAttribute",
                         "attribute2": "secondAttribute"}
collection_to_create = Collection(
    name="MyFirstCollection", description="This is my first collection", attributes=collection_attributes
)
created_collection = collection_api.create_collection(collection=collection_to_create)
print(created_collection)


# Create a data object ====================v
dataobject_api = DataObjectApi(client)
dataobject_to_create = DataObject(
    name="MyFirstDataObject", description="This is my first data object"
)
created_dataobject = dataobject_api.create_data_object(
    collection_id=created_collection.id, data_object=dataobject_to_create
)
print(created_dataobject)

# Create another data object as a child to the first one
child_to_create = DataObject(
    name="Child",
    description="This is my second data object",
    parent_id=created_dataobject.id,
)
created_child = dataobject_api.create_data_object(
    collection_id=created_collection.id, data_object=child_to_create
)
print(created_child)

successor_to_create = DataObject(
    name="Successor",
    description="This is my third data object",
    parent_id=created_dataobject.id,
    predecessor_ids=[created_child.id],
)
created_successor = dataobject_api.create_data_object(
    collection_id=created_collection.id, data_object=successor_to_create
)
print(created_successor)
