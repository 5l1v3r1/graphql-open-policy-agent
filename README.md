# GraphQL Authorization using Open Policy Agent
GraphQL Demo application demonstrating field-level Authorization with Open Policy Agent

# Setup
## Clone repository
`git clone https://github.com/dolevf/graphql-open-policy-agent.git && cd graphql-open-policy-agent`

## Download OPA binary for your CPU architecture
https://www.openpolicyagent.org/docs/latest/#1-download-opa

## Install Python prerequisites
`pip3 install -r requirements.txt`

## Run GraphQL Web Application
This should run on localhost:5013.
`python3 app.py`

## Run OPA Server with the GraphQL Policy
This should run on localhost:8181.
`./opa run --server policy.rego`


# OPA Policy
```
package graphql

default allow = false

privileged_fields := {"price", "discount_code"}

allow {
	input.user == "admin"
	field_allowed
}

field_allowed {
  privileged_fields[input.field]
}
```

# Try it out!
Without authorization, price and discountcode fields are NULL.

```
$ curl -X POST \
  --header 'Content-Type: application/json' \
  --header 'user: admin' \
  --data '{"query": "query { cars { id tier price maker discountcode model } }"}' \
  http://localhost:5013/graphql | jq


{
  "data": {
    "cars": [
      {
        "id": "5",
        "tier": "Premium",
        "price": null,
        "maker": "Mercedes-Benz",
        "discountcode": null,
        "model": "AMG F1"
      },
      {
        "id": "4",
        "tier": "Basic",
        "price": null,
        "maker": "Honda",
        "discountcode": null,
        "model": "Civic"
      },
      {
        "id": "3",
        "tier": "Basic",
        "price": null,
        "maker": "Hyundai",
        "discountcode": null,
        "model": "Accord"
      },
      {
        "id": "2",
        "tier": "Premium",
        "price": null,
        "maker": "Audi",
        "discountcode": null,
        "model": "R8"
      },
      {
        "id": "1",
        "tier": "Premium",
        "price": null,
        "maker": "Tesla",
        "discountcode": null,
        "model": "3"
      }
    ]
  }
}
```

With authorization (user header is specified), price and discountcode fields are returned.
```
{
  "data": {
    "cars": [
      {
        "id": "5",
        "tier": "Premium",
        "price": 40000,
        "maker": "Mercedes-Benz",
        "discountcode": "526df5db-f1ae-42cf-bcb0-d0fb1c16ca79",
        "model": "AMG F1"
      },
      {
        "id": "4",
        "tier": "Basic",
        "price": 15000,
        "maker": "Honda",
        "discountcode": "e05b5d2f-6929-47fc-89fa-d1faff0a4ae9",
        "model": "Civic"
      },
      {
        "id": "3",
        "tier": "Basic",
        "price": 12000,
        "maker": "Hyundai",
        "discountcode": "4b0a189f-dd01-4d8d-80c9-cd8505d03b20",
        "model": "Accord"
      },
      {
        "id": "2",
        "tier": "Premium",
        "price": 350000,
        "maker": "Audi",
        "discountcode": "7efc4a62-2920-4b08-97ce-94676a3e5b85",
        "model": "R8"
      },
      {
        "id": "1",
        "tier": "Premium",
        "price": 30000,
        "maker": "Tesla",
        "discountcode": "2386c295-9a6f-4376-bd94-aa1337545463",
        "model": "3"
      }
    ]
  }
}
```