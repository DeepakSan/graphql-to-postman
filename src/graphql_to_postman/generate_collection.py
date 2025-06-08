from urllib.parse import urlparse
import uuid

from graphql_to_postman.helpers.helper import save_collection_to_file, introspect_schema, get_fields, build_query_item

def create_postman_collection(graphql_endpoint, depth, output_file_name):

    introspection = introspect_schema(graphql_endpoint)
    types = introspection["data"]["__schema"]["types"]
    query_type = introspection["data"]["__schema"]["queryType"]["name"]
    query_fields = get_fields(types, query_type)
    parsed_url = urlparse(graphql_endpoint)

    collection = {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": "GraphQL_Collection",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for current_depth in range(0, depth):
        for field in query_fields:
            collection["item"].append(
                build_query_item(types, query_fields, field["name"], field.get("args", []), current_depth, parsed_url, graphql_endpoint)
            )

    output_file_name = "graphql_postman_collection"
    save_collection_to_file(collection, output_file_name + ".json")


    print(f"Postman collection generated: {output_file_name}")