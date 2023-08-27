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

from rocrate.rocrate import ROCrate
from rocrate.model.person import Person


import json
import inspect
import mykey
import os
import ro_crate_contributers

### Local shepard backend address, and locally stored API key
HOST = "http://[::1]:8080/shepard/api"
key = mykey.key

### Set up configuration for the shepard client
conf = Configuration(host=HOST, api_key={"apikey": key})
conf.access_token = None
client = ApiClient(configuration=conf)
collection_api = CollectionApi(client)
dataobject_api = DataObjectApi(client)
timeseries_api = TimeseriesApi(client)
timeseries_reference_api = TimeseriesReferenceApi(client)

### User input section
coll_id = int(input("Enter a Collection ID: "))
collection = collection_api.get_collection(coll_id)

### Collect all dataobjects linked to the Collection
def get_all_DO_IDs(coll_id):
    list_of_dataobjects = dataobject_api.get_all_data_objects(coll_id)
    id_list=[]
    for i in list_of_dataobjects:
        id_list.append(i.__getattribute__('id'))
    return id_list

def get_all_TSR_IDs(coll_id, do_id, id_list):
    tsr_list = timeseries_reference_api.get_all_timeseries_references(coll_id, do_id)
    if not tsr_list:
        return None
    else:
        for i in tsr_list:
            id_list.append([do_id, i.__getattribute__('id')])

do_list = dataobject_api.get_all_data_objects(coll_id)
do_id_list = get_all_DO_IDs(coll_id)
tsr_id_list = []
for i in do_id_list:
    get_all_TSR_IDs(coll_id, i, tsr_id_list)

### Create the relationship tree
prev_objects = []
def find_ancestor(id):
    dataobject = dataobject_api.get_data_object(coll_id,id)
    parent = dataobject.__getattribute__('parent_id')
    if parent == None or dataobject.__getattribute__('id') in prev_objects:
        return id
    else:
        prev_objects.append(dataobject.__getattribute__('id'))
        return find_ancestor(parent)

unique_ancestors = []
for i in do_id_list:
    ancestor = find_ancestor(i)
    if ancestor not in unique_ancestors:
        unique_ancestors.append(ancestor)

### Create RO-Crate
crate = ROCrate()

os.mkdir("./collection")
os.mkdir("./dataobject")
os.mkdir("./timeseriesreference")
os.mkdir("./data")

with open("./collection/Collection"+".json", 'w', encoding='utf-8') as f:
    json.dump(collection.to_dict(), f, ensure_ascii=False, indent=4, sort_keys=True, default=str)
f.close()

for i in do_list:
    with open("./dataobject/"+str(i.__getattribute__('id'))+".json", 'w', encoding='utf-8') as f:
        json.dump(i.to_dict(), f, ensure_ascii=False, indent=4, sort_keys=True, default=str)
    f.close()

for i in tsr_id_list:
    tsr = timeseries_reference_api.get_timeseries_reference(coll_id, i[0], i[1])
    with open("./timeseriesreference/"+str(tsr.__getattribute__('id'))+".json", 'w', encoding='utf-8') as f:
        json.dump(tsr.to_dict(), f, ensure_ascii=False, indent=4, sort_keys=True, default=str)
    f.close()

for i in tsr_id_list:
    timeseries = timeseries_reference_api.get_timeseries_payload(coll_id, i[0], i[1])
    timeseries_reference = timeseries_reference_api.get_timeseries_reference(coll_id, i[0], i[1])
    for j in range(len(timeseries)):
        with open("./data/timeseries_"+str(j)+"_from_reference_"+str(timeseries_reference.__getattribute__('id'))+".json", 'w', encoding='utf-8') as f:
            json.dump(timeseries[j].to_dict(), f, ensure_ascii=False, indent=4, sort_keys=True, default=str)
        f.close()


input("Waiting...")

### Add data to the Crate

crate.add_file("./collection/Collection.json", "collection.json", properties={
    "name" : collection.__getattribute__('name'),
    "author" : collection.__getattribute__('created_by'),
    "description" : collection.__getattribute__('description')
})
crate.add_dataset("./dataobject", "dataobject")
crate.add_dataset("./timeseriesreference", "timeseriesreference")
crate.add_dataset("./data", "data")

for i in ro_crate_contributers.people:
    crate.add(Person(crate, i[2], properties={
        "name": i[0],
        "affiliation": i[1]
    }))

crate.write("shepard_crate")

### Remove the temporary dictionaries

for i in os.listdir("./dataobject"):
    os.remove("./dataobject/"+i)
for i in os.listdir("./collection"):
    os.remove("./collection/"+i)
for i in os.listdir("./timeseriesreference"):
    os.remove("./timeseriesreference/"+i)
for i in os.listdir("./data"):
    os.remove("./data/"+i)
os.rmdir("./dataobject")
os.rmdir("./collection")
os.rmdir("./timeseriesreference")
os.rmdir("./data")
