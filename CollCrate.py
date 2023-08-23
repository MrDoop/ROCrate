import os
from rocrate.rocrate import ROCrate

# Create an empty ROCrate instance
rocrate = ROCrate()
rocrate.add_directory

# Set the main entity as a dataset
dataset = rocrate.add_dataset("exp")
dataset.name = "My Dataset"
dataset.description = "This is a sample dataset."

# Add a directory to the dataset
directory_path = "data"
directory_name = os.path.basename(directory_path)
data_directory = dataset.add_directory(source=directory_path)
data_directory.name = directory_name

# Add the "Collections" subdirectory
subdirectory_path = os.path.join(directory_path, "Collections")
subdirectory_name = os.path.basename(subdirectory_path)
collections_directory = data_directory.add_directory(source=subdirectory_path)
collections_directory.name = subdirectory_name

# Add files to the "Collections" subdirectory
collection_files = [
    "collection1.txt",
    "collection2.txt",
    "collection3.txt"
]

for file_name in collection_files:
    file_path = os.path.join(subdirectory_path, file_name)
    relative_path = os.path.relpath(file_path, directory_path)
    collection_file = collections_directory.add_file(source=file_path)
    collection_file.name = relative_path

# Create a software entity
software = rocrate.add_software(identifier="software_id")
software.name = "My Software"
software.description = "This is a sample software."

# Create an evaluation entity
evaluation = rocrate.add_evaluation(identifier="evaluation_id")
evaluation.name = "My Evaluation"
evaluation.description = "This is a sample evaluation."

# Connect the entities
evaluation.used_software(software)
evaluation.used_entity(dataset)

# Generate the ROCrate metadata file
rocrate.generate_metadata()
rocrate.write_crate("rocrate_example")

print("ROCrate example created successfully.")