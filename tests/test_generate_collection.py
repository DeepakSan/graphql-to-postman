
from graphql_to_postman.generate_collection import create_postman_collection
import os

def test_create_postman_collection():
    url = "https://countries.trevorblades.com"
    output_file = "test_collection"
    depth = 1

    create_postman_collection(url, depth, output_file)
    file_name = output_file + ".json"
    assert os.path.exists(file_name)
    os.remove(file_name)

