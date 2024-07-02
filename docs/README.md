# Fast AnonCreds
[Gotta Go Fast!](https://www.youtube.com/watch?v=Z9G1Mf6TZRs)

## Creating AnonCreds Objects
```bash
curl -X 'POST' \
  'https://fast.anoncreds.vc' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}' | jq .

```

## Setup parameters
```json
{
    "name": "example", # schema name
    "attributes": [], # schema attributes
    "size": 10, # revocation registry size
    "revocation": false, # create revocation registry object
    "publish": false, # publish verification document
}
```