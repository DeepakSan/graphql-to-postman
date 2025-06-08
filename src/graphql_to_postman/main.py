import argparse

from graphql_to_postman.generate_collection import create_postman_collection

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("graphql_url", help="The url of the graphql schema")
    parser.add_argument("--output_file_name", help="The name of the output file", default="postman_collection.json")
    parser.add_argument("--depth", help="The depth of the graphql schema", default=2, type=int)
    parser.add_argument("--include_deprecation", help="Include deprecated fields", action="store_true")
    args = parser.parse_args()

    create_postman_collection(args.graphql_url, args.depth,  args.output_file_name)

if __name__ == "__main__":
    main()