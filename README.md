# graphql-to-postman

[![PyPI - Python 3.12.5](https://img.shields.io/pypi/pyversions/graphql-to-postman.svg)](https://pypi.org/project/graphql-to-postman)

-----

Generate Postman collections from GraphQL endpoints with ease.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Arguments](#arguments)
- [License](#license)

## Installation

Install this package using the below command

```console
pip install graphql-to-postman
```

## Installation
Run the following command to generate a Postman collection via the command line:

```console
graphql_to_postman <graphql_endpoint> [--depth <depth>] [--output <output_file_name>]
graphql_to_postman https://countries.trevorblades.com --depth 2 --output_file_name "graphql_collections"
```

Use the package programmatically in your Python code:

```console
from graphql_to_postman.generate_collection import create_postman_collection

create_postman_collection(
    graphql_endpoint="https://countries.trevorblades.com",
    depth=2,
    output_file_name="sample_output"
)
```

## Arguments

- graphql_endpoint (required): The GraphQL endpoint URL.
- depth (optional): The depth of the schema to explore (default: 2).
- output_file_name (optional): The name of the output Postman collection file (default: collection.json).

## License

`graphql-to-postman` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.