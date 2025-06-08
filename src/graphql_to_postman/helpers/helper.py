import json
import os
import requests
import urllib.parse


def introspect_schema(endpoint_url, include_deprecation=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "..", "templates", "introspection-query.txt")
    with open(template_path, "r") as f:
        query = f.read()
    return send_introspection_query(endpoint_url, query)

def send_introspection_query(url, query):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json={"query": query}, headers=headers)
    if not response.ok:
        raise Exception(f"GraphQL error: {response.status_code}\n{response.text}")
    return response.json()

def get_fields(types, type_name):
    for t in types:
        if t["name"] == type_name and t.get("fields"):
            return t["fields"]
    return []

def get_return_type(field):
    type_info = field["type"]
    while type_info.get("ofType"):
        type_info = type_info["ofType"]
    return type_info

def build_fields_block(types, return_type_name, current_depth, max_depth, visited = None):
    if visited is None:
        visited = set()

    if return_type_name in visited:
        return ""

    visited.add(return_type_name)

    for t in types:
        if t["name"] == return_type_name and t.get("fields"):
            sub_fields = []
            for f in t["fields"]:
                f_type = get_return_type(f)
                if f_type["kind"] in ["SCALAR", "ENUM"]:
                    sub_fields.append(f["name"])
                elif f_type["kind"] == "OBJECT":
                    nested_block = build_fields_block(types, f_type["name"], current_depth + 1, max_depth, visited.copy())
                    if nested_block:
                        if current_depth <= max_depth:
                            sub_fields.append(f"{f['name']} {{\n{nested_block}\n    }}")
            if not sub_fields:
                print(f"Warning: No valid subfields found for type {return_type_name}")
            return "\n".join(f"    {field}" for field in sub_fields)
    return ""

def is_non_null_type(type_obj):
    type_obj = type_obj['type']
    while type_obj:
        if type_obj.get("kind") == "NON_NULL" or type_obj.get("kind") == "INPUT_OBJECT":
            return True
        type_obj = type_obj.get("ofType")
    return False


def build_query_item(types, query_fields, field_name, args, current_depth, parsed_url, graphql_endpoint):
    args_str = ""
    if args:
        arg_values = []
        for arg in args:
            arg_type = get_return_type(arg)
            is_non_null = is_non_null_type(arg)
            if is_non_null:
                if arg_type["name"] in ["ID", "String"]:
                    arg_values.append(f"{arg['name']}: \"default_{arg['name']}\"")
                elif arg_type["name"] == "Int":
                    arg_values.append(f"{arg['name']}: 1")
                elif arg_type["name"] == "Boolean":
                    arg_values.append(f"{arg['name']}: true")
                elif arg_type["name"] == "Float":
                    arg_values.append(f"{arg['name']}: 1.0")
                else:
                    arg_values.append(f"{arg['name']}: \"{arg_type['name']}\"")
        if arg_values:
            args_str = "(" + ", ".join(arg_values) + ")"

    return_type = None
    for field in query_fields:
        if field["name"] == field_name:
            return_type_info = get_return_type(field)
            return_type = return_type_info["name"]
            break

    fields_block = ""
    if return_type:
        fields_block = build_fields_block(types, return_type, current_depth=0, max_depth=current_depth)

    query_text = f"query {field_name}Query {{\n  {field_name}{args_str} {{\n{fields_block}\n  }}\n}}"
    if not fields_block and return_type:
        type_kind = next((t["kind"] for t in types if t["name"] == return_type), "UNKNOWN")
        if type_kind == "OBJECT":
            print(f"Warning: Empty fields block for {field_name} (type: {return_type}). Schema may lack subfields.")

    variables = {}

    suffix = f"_depth_{current_depth}_sample"

    host_parts = parsed_url.hostname.split('.') if parsed_url.hostname else []
    path_parts = parsed_url.path.strip('/').split('/') if parsed_url.path.strip('/') else []

    return {
        "name": f"{field_name}{suffix}",
        "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
                "mode": "graphql",
                "graphql": {
                    "query": query_text,
                    "variables": json.dumps(variables)
                }
            },
            "url": {
                "raw": graphql_endpoint,
                "protocol": parsed_url.scheme or "https",
                "host": host_parts,
                "path": path_parts
            }
        },
        "response": []
    }


def save_collection_to_file(collection, output_file_name):
    with open(output_file_name, "w") as f:
        json.dump(collection, f, indent=2)





